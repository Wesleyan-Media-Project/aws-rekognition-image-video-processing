import os
import json
import pandas as pd

#================== Raw data storage ======================

def write_to_bucket(data, s3_resource, bucket, filename):
    '''
    write rekognition results to an Amazon S3 bucket
    Params: 
        data: data to upload, as bytes or seekable file-like object (e.g. a json object)
        s3_resource: a boto3 S3 resource session
        bucket: S3 bucket name
        filename: S3 object key (the file path to upload data)

    '''
    obj = s3_resource.Object(bucket, filename)
    
    results = obj.put(Body=data)
    


#================== Parsing WMP variables ======================

#==================== lines detected from OCR: aws_ocr_video_text ===============================

def extract_text_from_TextDetection(response):
    '''
    Take a response object from Amazon rekognition GetTextDetection (with TextDetections in its keys) and parse detected text lines along with timestamp information. 
    
    Return a list of lists in the format of [timestamp, detected line]
    '''
    
    timestamped_text = []
        
    for i, frame in enumerate(response['TextDetections']):
        if frame['TextDetection']['Type'] == 'LINE': # Type "WORD" was omitted
            timestamp = frame['Timestamp']
            detected_text = frame['TextDetection']['DetectedText']
            timestamped_text.append([timestamp, detected_text])
            
    return timestamped_text


def aggregate_text_by_timestamp(response, sep='\n'):
    
    '''
    Take a response object from Amazon rekognition GetTextDetection and return a timestamp-level dataframe of detected text lines
    
    Args:
        response: results from GetTextDetection stored in a dictionary, with 'TextDetections' among its keys
        sep: the delimiter that separates lines detected at the same timestamp. 
    
    return: 
        a pandas dataframe with timestamp and the lines detected at the timestamp 
    
    '''
    df = pd.DataFrame(extract_text_from_TextDetection(response), columns=['timestamp', 'detected_text'])
    agg = df.groupby(['timestamp'], as_index=False).agg({'detected_text': lambda x: sep.join(x)})
    
    return agg


def concat_unique_lines(response, sep='\n', sep_ts=';'):
    '''
    Take a response object from Amazon rekognition GetTextDetection and return a string of detected lines separated by given separators (Video-level OCR lines if the response object holds information extracted from a complete video). 
    
    Use this function by itself if only video-level text is needed.
    
    Args: 
        response: results from GetTextDetection stored in a dictionary, with 'TextDetections' among its keys
        sep: the delimiter that separates lines detected at the same timestamp. 
        sep_ts: the delimiter that separates lines detected from different timestamps. 
    
    Return: 
        a string that stores unique lines collected by the reponse. 
    
    '''
    agg = aggregate_text_by_timestamp(response, sep=sep)
    deduped_text = agg['detected_text'].drop_duplicates().tolist()
    return sep_ts.join(deduped_text)

#==================== WMP candidate matches: aws_face_vid ===============================

def get_candidate_matches(response):
    
    '''
    Take a response object from Amazon rekognition GetFaceSearch and return a list of WMP candidate IDs who were featured in video. 
    
    Use this function if only video-level candidate IDs are needed. 
    '''
    
    candidates = set()
    
    for personMatch in response['Persons']:
        if ('FaceMatches' in personMatch):
            for faceMatch in personMatch['FaceMatches']:
                CandidateID = faceMatch['Face']['ExternalImageId']
                if CandidateID not in candidates:
                    candidates.add(CandidateID)
    
    return list(candidates)


def get_candidate_appearances(response):
    
    '''
    Take a response object from Amazon rekognition GetFaceSearch and return a dictionary of identified WMP candidates (Candidate IDs as keys, a list of timestamps when they appeared as values)
    
    Use this function if timestamps of candidate appearances are needed. 
    '''
    
    matches = {}
        
    for personMatch in response['Persons']:
        
        if ('FaceMatches' in personMatch):
            for faceMatch in personMatch['FaceMatches']:
                
                Timestamp = personMatch['Timestamp']
                CandidateID = faceMatch['Face']['ExternalImageId']
                
                if CandidateID in matches:
                    matches[CandidateID].append(Timestamp)
                else:
                    matches[CandidateID] = [Timestamp]              
        
    return matches


