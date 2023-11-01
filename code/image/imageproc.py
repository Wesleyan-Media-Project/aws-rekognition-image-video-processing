import os
import json
import boto3
from botocore.exceptions import ClientError
import logging


'''
Reference: 
https://github.com/awsdocs/amazon-rekognition-developer-guide/tree/master
https://docs.aws.amazon.com/rekognition/latest/dg/service_code_examples.html 
'''

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class ImageProc:
    
    def __init__(self, image, rekognition_client, image_name=None):
        '''
        Params:
            image: Blob of image bytes or a dictionary of an S3 object composed of bucket and key (format: {'S3Object':{'Bucket':bucket, 'Name':key})
            rekognition_client: a boto3 rekognition client
            image_name (optional): (str) image identifier for printing warning messages
        '''
        self.image = image
        self.client = rekognition_client
        self.image_name = image_name
    
    def detect_text(self):
        '''
        call Rekognition DetectText API for images and return the detected text in a dictionary
        '''
        try:
            response = self.client.detect_text(Image=self.image)
            
        except ClientError:
            if self.image_name:
                logger.warning("Couldn't detect text in %s", self.image_name)
            
            return None
            
        else:
            return {'TextDetections': response['TextDetections']}
    
    def detect_faces(self, attr='ALL'):
        '''
        call Rekognition DetectFaces API for images and return the detected face details in a dictionary
        '''
        try:
            response = self.client.detect_faces(
                                    Image=self.image, 
                                    Attributes=[attr])
        
        except ClientError:
            if self.image_name:
                logger.warning("Couldn't detect faces in %s", self.image_name)
        
        else:
            if not response['FaceDetails']:
                return None
            
            return {'FaceDetails': response['FaceDetails']}
    
    def search_faces(self, collection_id, maxFaces=123, faceMatchThreshold=0.7):
        '''
        call Rekognition SearchFaces API for images and return the recognized face IDs based on the existing face collection
        '''
        try: 
            response = self.client.search_faces_by_image(
                CollectionId=collection_id,
                Image=self.image,
                MaxFaces=maxFaces,
                FaceMatchThreshold=faceMatchThreshold)
        
        except self.client.exceptions.InvalidParameterException as e:
            if self.image_name:
                logger.warning("No faces in %s", self.image_name)
            
        except ClientError:
            if self.image_name:
                logger.warning("Couldn't find matching faces in %s", self.image_name) 
        
        else:
            return {'FaceMatches': response['FaceMatches'],
                   'SearchedFaceBoundingBox': response['SearchedFaceBoundingBox'],
                   'SearchedFaceConfidence': response['SearchedFaceConfidence']}



def parse_text_detection(response, sep=';'):
    '''
    Take a response from Rekoginition detect_text and return detected text from images
    '''
    if response:
        
        detected_text = []

        for text in response['TextDetections']:
            if text['Type'] == 'LINE':
                detected_text.append(text['DetectedText'])
    
        return sep.join(detected_text)
    

def parse_matched_persons(response, sep=';'):
    
    if response:
        
        persons = []
        
        for person in response['FaceMatches']:
            person_id = person['Face']['ExternalImageId']
            persons.append(person_id)
        
        return sep.join(persons)
    
    
