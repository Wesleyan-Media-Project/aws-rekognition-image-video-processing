# Wesleyan Media Project - Aws-Rekognition-Image-Video-Processing

Welcome! This repository is part of the Cross-platform Election Advertising Transparency initiatIVE (CREATIVE) project. CREATIVE is a joint infrastructure project of WMP and privacy-tech-lab at Wesleyan University. CREATIVE provides cross-platform integration and standardization of political ads collected from Google and Facebook.

This repository is a part of the Data Processing step.

## Table of Contents

- [Introduction](#introduction)

- [Objective](#objective)

- [Data](#data)

- [Setup](#setup)

## Introduction

![rekognition-pipeline](rekognition-pipeline.png)

This repository contains code that replicates the workflow used by the Wesleyan Media Project to perform image and video recogonition on political ads through the Amazon Rekognition service (AWS SDK for Python). The core functionality this repository includes:

- A video processing module calls Amazon Rekognition video API to perform text detection, labels detection, face detection and face search (searching for faces that match an existing face collection) on video data. It also provides functions to create SNS Topic and SQS queue necessary for Rekognition video analysis.
- An image processing module calls Amazon Rekognition image API to perform text detection, face detection and face search on image data.
- Functions in video and image modules that allow one-step parsing of WMP variables from Rekognition image and video analysis results
- Code for creating a face collection with Rekognition which is necessary to run face search for both image and video processing.
- Tutorial notebooks to use the above modules and functions.

## Objective

Each of our repositories belongs to one or more of the following categories:
- Data Collection
- Data Processing
- Data Classification
- Compiled Final Data

This repository is part of the Data Processing section.

## Data

Image and video processing modules return the response data from Amazon Rekognition API in a dictionary. They can be saved into JSON files. You may choose to either store the response data in Amazon S3 bucket or in your local machine. To store them in an S3 bucket, see the `tutorial.ipynb` in the `/code/image` and `/code/video` folder.

We also provided helper functions that parse WMP variables from the response data.

## Setup

- To begin, you will need to register for AWS Services if you have not already done so. You can find more information about AWS Services [here](https://aws.amazon.com/).

* Create an Amazon S3 bucket to store the video and image data for processing via your AWS account.

- Create your [IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html).

* Configure your [AWS credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html). Otherwise, pass your credentials whenever calling Rekognition API.

- After the above setup procedures, please follow the folder `/getting-started` to upload data to S3 bucket and create face collections.

```bash
# Upload your face collection data, image data, video data from their local paths to respective Amazon S3 bucket destinations
aws s3 cp <source> <target> --recursive
```

- After you have your data stored in an S3 bucket, follow the tutorials in the image and video folders to process the data based on your demands. Please make sure to replace the placeholders in the code with your own AWS credentials and file paths.
- Below are some dependencies you may need to install before running the code:

```bash
pip install boto3
```
