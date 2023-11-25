# Wesleyan Media Project - Aws-Rekognition-Image-Video-Processing

Welcome! This repo is part of the Cross-platform Election Advertising Transparency initiatIVE (CREATIVE) project. CREATIVE is a joint infrastructure project of WMP and privacy-tech-lab at Wesleyan University. CREATIVE provides cross-platform integration and standardization of political ads collected from Google and Facebook.

This repo is a part of the data storage and processing step.

## Table of Contents

- [Introduction](#introduction)

- [Objective](#objective)

- [Data](#data)

- [Setup](#setup)

## Introduction

This repo contains codes that replicate the workflow used by the Wesleyan Media Project to perform image and video recogonition process on political ads through Amazon Web Services. The core functionality this repo provides includes:

- Text Detection from Videos: We call the AWS Rekogonition `GetTextDetection`API to extract text from videos.
- Face Detection from Videos: We call the AWS Rekogonition `GetFaceSearch` API to detect faces from videos. In addition, we also retrieve persons who matched WMP candidate list through variable "aws_face_vid"
- Text Detection from Images: We call the AWS Rekognition `DetectText` API for images and return the detected text in a dictionary
- Face Detection and Searching from Images: We call the AWS `DetectFaces` API to detect faces and facial attributes from imagesand; and `SearchFacesByImage`API to search for faces that matches an existing face collection

## Objective

Each of our repos belongs to one or more of the following categories:

- Data Collection
- Data Storage & Processing
- Preliminary Data Classification
- Final Data Classification

This repo is part of the data storage and processing section.

## Data

The data created by the scripts in this repo is in JSON format.

In this repo, you can choose to either store the output data in Amazon S3 bucket or in your local machine.
If you want to store the output in S3 bucket, you can create an S3 resource session and save a response in S3 bucket. If you want to store locally, you can convert response to file-like object and then create an S3 object to hold results. For more information, please check the code `tutorial.ipynb` under `/image` folder.

## Setup

- To begin, you will need to register for AWS Services if you have not already done so. You can find more information about AWS Services [here](https://aws.amazon.com/).
+ Create your IAM role on AWS: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html 
- After you have your AWS Services ready, please follow the folder `/getting-started` to create face collections and upload data to S3 bucket. 


````bash
# Upload your face collection data, image data, video data from their local paths to respective Amazon S3 bucket destinations
aws s3 cp <source> <target> --recursive```
````

- After you have your data ready, you can follow the image and video pipelines to process the recognition tasks. Please make sure to replace the placeholder in the code with your own AWS credentials and file paths.
- Below are some dependencies you may need to install before running the code:

```bash
pip install boto3
pip install pandas
```
