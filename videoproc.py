import boto3
import json
import sys
import time

'''
Modified based on Amazon rekognition developer guide - code examples: https://github.com/awsdocs/amazon-rekognition-developer-guide/tree/master (For license details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE)
'''

class Messenger:
    
    '''
    A class that creates and deletes an SNS topic and an SQS queue for video analysis
    '''
        
    roleArn = ''
    sqsQueueUrl = ''
    snsTopicArn = ''

    def __init__(self, sns, sqs, role):
        self.sns = sns
        self.sqs = sqs
        self.roleArn = role
        
    def CreateTopicandQueue(self, TopicName, QueueName):
        '''
        Args: 
        TopicName: (str) AWS SNS topic name
        QueueName: (str) AWS SQS queue name
        '''

        # Create SNS topic

        topicResponse = self.sns.create_topic(Name=TopicName)
        
        self.snsTopicArn = topicResponse['TopicArn']

        # Create SQS queue
        
        self.sqs.create_queue(QueueName=QueueName)
        
        self.sqsQueueUrl = self.sqs.get_queue_url(QueueName=QueueName)['QueueUrl']

        attribs = self.sqs.get_queue_attributes(QueueUrl=self.sqsQueueUrl,
                                                AttributeNames=['QueueArn'])['Attributes']

        sqsQueueArn = attribs['QueueArn']

        # Subscribe SQS queue to SNS topic
        self.sns.subscribe(
            TopicArn=self.snsTopicArn,
            Protocol='sqs',
            Endpoint=sqsQueueArn)

        # Authorize SNS to write SQS queue 
        # Edit accordingly for permissions, see policy generator: https://awspolicygen.s3.amazonaws.com/policygen.html)
        policy = """{{
      "Version":"2012-10-17",
      "Statement":[
        {{
          "Sid":"MyPolicy",
          "Effect":"Allow",
          "Principal" : {{"AWS" : "*"}},
          "Action":"SQS:SendMessage",
          "Resource": "{}",
          "Condition":{{
            "ArnEquals":{{
              "aws:SourceArn": "{}"
            }}
          }}
        }}
      ]
    }}""".format(sqsQueueArn, self.snsTopicArn)

        response = self.sqs.set_queue_attributes(
            QueueUrl=self.sqsQueueUrl,
            Attributes={
                'Policy': policy
            })

    def DeleteTopicandQueue(self):
        self.sqs.delete_queue(QueueUrl=self.sqsQueueUrl)
        self.sns.delete_topic(TopicArn=self.snsTopicArn)

        

class VideoProc:
    
    '''
    This class allows you to analyze videos stored in an Amazon S3 bucket. Available methods: 
    text detection
    label detection
    face detection
    face search
    
    Each method returns a single response object in a dictionary which includes 
    JobStatus, VideoMetadata, and a list of detected objects of interest (e.g. text, labels, faces) 
    '''

    jobId = ''
    startJobId = ''

    def __init__(self, role, bucket, video, rek, sqs, sns, QueueUrl, TopicArn): # removed client
        self.roleArn = role
        self.bucket = bucket
        self.video = video
        self.rek = rek
        self.sqs = sqs
        self.sns = sns
        self.sqsQueueUrl = QueueUrl
        self.snsTopicArn = TopicArn

    def GetSQSMessageSuccess(self):

        jobFound = False
        succeeded = False

        dotLine = 0
        while jobFound == False:
            sqsResponse = self.sqs.receive_message(QueueUrl=self.sqsQueueUrl, MessageAttributeNames=['ALL'],
                                                   MaxNumberOfMessages=10)

            if sqsResponse:

                if 'Messages' not in sqsResponse:
                    if dotLine < 40:
                        print('.', end='')
                        dotLine = dotLine + 1
                    else:
                        print()
                        dotLine = 0
                    sys.stdout.flush()
                    time.sleep(5)
                    continue

                for message in sqsResponse['Messages']:
                    notification = json.loads(message['Body'])
                    rekMessage = json.loads(notification['Message'])
                    print(rekMessage['Status'])
                    if rekMessage['JobId'] == self.startJobId:
                        print('Matching Job Found:' + rekMessage['JobId'])
                        jobFound = True
                        if (rekMessage['Status'] == 'SUCCEEDED'):
                            succeeded = True

                        self.sqs.delete_message(QueueUrl=self.sqsQueueUrl,
                                                ReceiptHandle=message['ReceiptHandle'])
                    else:
                        print("Job didn't match:" +
                              str(rekMessage['JobId']) + ' : ' + self.startJobId)
                    
                    # Delete the unknown message. Consider sending to dead letter queue
                    self.sqs.delete_message(QueueUrl=self.sqsQueueUrl,
                                            ReceiptHandle=message['ReceiptHandle'])

        return succeeded

    # ============== Text detection ================
    def StartTextDetection(self):
        response = self.rek.start_text_detection(Video={'S3Object': {'Bucket': self.bucket, 'Name': self.video}},
                                                  NotificationChannel={'RoleArn': self.roleArn,
                                                                       'SNSTopicArn': self.snsTopicArn})
        
        self.startJobId = response['JobId']
        print('Start Job Id: ' + self.startJobId)
        
    def GetTextDetectionResults(self):
        paginationToken = ''
        finished = False
        results = {}
        
        while finished == False:
            response = self.rek.get_text_detection(JobId=self.startJobId,
                                                    NextToken=paginationToken)
            
            
            results['TextDetections'] = results.get('TextDetections', []) + response['TextDetections']
                        
            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                results['JobStatus'] = response['JobStatus']
                results['VideoMetadata'] = response['VideoMetadata']
                finished = True
                
        return results
    
    # ============== Label detection ===============
    
    def StartLabelDetection(self):
        response = self.rek.start_label_detection(Video={'S3Object': {'Bucket': self.bucket, 'Name': self.video}},
                                                  NotificationChannel={'RoleArn': self.roleArn,
                                                                       'SNSTopicArn': self.snsTopicArn},
                                                  MinConfidence=90,
                                                   )

        self.startJobId = response['JobId']
        print('Start Job Id: ' + self.startJobId)
        


    def GetLabelDetectionResults(self):
        paginationToken = ''
        finished = False
        results = {}
        
        while finished == False:
            response = self.rek.get_label_detection(JobId=self.startJobId,
                                                    NextToken=paginationToken,
                                                    SortBy='TIMESTAMP',
                                                    AggregateBy="TIMESTAMPS")
            
            
            results['Labels'] = results.get('Labels', []) + response['Labels']
                        
            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                results['JobStatus'] = response['JobStatus']
                results['VideoMetadata'] = response['VideoMetadata']
                finished = True
                
        return results
                    
    # ============== Face detection===============
    
    def StartFaceDetection(self):
        response=self.rek.start_face_detection(Video={'S3Object': {'Bucket': self.bucket, 'Name': self.video}},
            NotificationChannel={'RoleArn': self.roleArn, 'SNSTopicArn': self.snsTopicArn}, FaceAttributes='ALL')

        self.startJobId=response['JobId']
        print('Start Job Id: ' + self.startJobId)

    def GetFaceDetectionResults(self):
        paginationToken = ''
        finished = False
        results = {}

        while finished == False:
            response = self.rek.get_face_detection(JobId=self.startJobId,
                                            NextToken=paginationToken,
                                            MaxResults=123,)

            results['Faces'] = results.get('Faces', []) + response['Faces']
            
            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                results['JobStatus'] = response['JobStatus']
                results['VideoMetadata'] = response['VideoMetadata']
                finished = True
        
        return results


    # ============== Face Search ===============
    
    def StartFaceSearchCollection(self, collection, MatchThreshold=0.7):
        
        token = 'tok-' + str(int(round(time.time() * 1000)))
        
        response = self.rek.start_face_search(Video={'S3Object':{'Bucket':self.bucket,'Name':self.video}},
            ClientRequestToken = token, CollectionId=collection, FaceMatchThreshold = MatchThreshold,
            NotificationChannel={'RoleArn':self.roleArn, 'SNSTopicArn':self.snsTopicArn})
        
        self.startJobId=response['JobId']
        
        print('Start Job Id: ' + self.startJobId)


    def GetFaceSearchCollectionResults(self):
        paginationToken = ''
        finished = False
        results = {}

        while finished == False:
            response = self.rek.get_face_search(JobId=self.startJobId,
                                        NextToken=paginationToken) #SortBy='INDEX'
            
            results['Persons'] = results.get('Persons', []) + response['Persons']
            
            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                results['JobStatus'] = response['JobStatus']
                results['VideoMetadata'] = response['VideoMetadata']
                finished = True
        
        return results




