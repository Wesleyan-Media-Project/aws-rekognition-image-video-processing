# Wesleyan Media Project - Aws-Rekognition-Image-Video-Processing

Welcome! This repository contains code that replicates the workflow used by the Wesleyan Media Project to perform image and video recogonition on political ads through the Amazon Rekognition service (AWS SDK for Python).

This repo is a part of the [Cross-platform Election Advertising Transparency Initiative (CREATIVE)](https://www.creativewmp.com/). CREATIVE has the goal of providing the public with analysis tools for more transparency of political ads across online platforms. In particular, CREATIVE provides cross-platform integration and standardization of political ads collected from Google and Facebook. CREATIVE is a joint project of the [Wesleyan Media Project (WMP)](https://mediaproject.wesleyan.edu/) and the [privacy-tech-lab](https://privacytechlab.org/) at [Wesleyan University](https://www.wesleyan.edu).

To analyze the different dimensions of political ad transparency we have developed an analysis pipeline. The scripts in this repo are part of the Data Processing Step in our pipeline.

![A picture of the repo pipeline](CREATIVE_step2_032524.png)

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Results Storage](#results-storage)
- [Thank you!](#thank-you)

## Overview

![rekognition-pipeline](rekognition-pipeline.png)

This repository contains code that works to perform image and video recogonition on political ads through the Amazon Rekognition service (AWS SDK for Python). The core functionality this repository includes:

- A video processing module calls Amazon Rekognition video API to perform text detection, labels detection, face detection and face search (searching for faces that match an existing face collection) on video data. It also provides functions to create SNS Topic and SQS queue necessary for Rekognition video analysis.
- An image processing module calls Amazon Rekognition image API to perform text detection, face detection and face search on image data.
- Functions in video and image modules that allow one-step parsing of WMP variables from Rekognition image and video analysis results
- Code for creating a face collection with Rekognition which is necessary to run face search for both image and video processing.
- Tutorial notebooks to use the above modules and functions.

## Setup

Before running any of the code in this repo, make sure you have Python installed on your system. You can do so on the [official Python website](https://www.python.org/downloads/). In addition, install Jupyter Notebook by writing the following command in your terminal 'pip install jupyter'. From here, you should be able to run Jupyter Notebook by entering this command in your terminal 'jupyter notebook'

Below is an additional dependency you may need to install before running the code:

```bash
pip3 install boto3
```

Step One: To begin, you will need to register for AWS Services if you have not already done so. You can find more information about AWS Services [here](https://aws.amazon.com/).

Step Two: Create an Amazon S3 bucket to store the video and image data for processing via your AWS account.

Step Three: Create your [IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html).

Step Four: Configure your [AWS credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html). Otherwise, pass your credentials whenever calling Rekognition API.

Step Five: After the above setup procedures, please follow the folder `/code/getting-started` to upload data to S3 bucket and create face collections.

```bash
# Upload your face collection data, image data, video data from their local paths to respective Amazon S3 bucket destinations
aws s3 cp <source> <target> --recursive
```

Step Six: After you have your data stored in an S3 bucket, follow the tutorials in the image and video folders to process the data based on your demands. Please make sure to replace the placeholders in the code with your own AWS credentials and file paths.

## Results Storage

Image and video processing modules return the response data from Amazon Rekognition API in a dictionary. They can be saved into JSON files. You may choose to either store the raw response data in Amazon S3 bucket or in your local machine. To store them in an S3 bucket, see the `tutorial.ipynb` in the `/code/image` and `/code/video` folder.

We also provided helper functions that parse WMP variables from the response data.

These WMP variables parsed from Rekognition response data are saved as columns `aws_ocr_img_text` (image ads), `aws_face_img` (image ads), `aws_face_vid` (video ads), `aws_ocr_video_text` (video ads) into our final output tables. Description and access information of final output tables can be found in [data-post-production](https://github.com/Wesleyan-Media-Project/data-post-production/tree/main). 

## Thank You

<p align="center"><strong>We would like to thank our financial supporters!</strong></p><br>

<p align="center">This material is based upon work supported by the National Science Foundation under Grant Numbers 2235006, 2235007, and 2235008.</p>

<p align="center" style="display: flex; justify-content: center; align-items: center;">
  <a href="https://www.nsf.gov/awardsearch/showAward?AWD_ID=2235006">
    <img class="img-fluid" src="nsf.png" height="150px" alt="National Science Foundation Logo">
  </a>
</p>

<p align="center">The Cross-Platform Election Advertising Transparency Initiative (CREATIVE) is a joint infrastructure project of the Wesleyan Media Project and privacy-tech-lab at Wesleyan University in Connecticut.

<p align="center" style="display: flex; justify-content: center; align-items: center;">
  <a href="https://www.creativewmp.com/">
    <img class="img-fluid" src="CREATIVE_logo.png"  width="220px" alt="CREATIVE Logo">
  </a>
</p>

<p align="center" style="display: flex; justify-content: center; align-items: center;">
  <a href="https://mediaproject.wesleyan.edu/">
    <img src="wmp-logo.png" width="218px" height="100px" alt="Wesleyan Media Project logo">
  </a>
</p>
