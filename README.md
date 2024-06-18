# CREATIVE --- AWS Rekognition Image & Video Processing

Welcome! This repo contains scripts for performing image and video recognition on political ads through the Amazon Rekognition service (AWS SDK for Python).

This repo is a part of the [Cross-platform Election Advertising Transparency Initiative (CREATIVE)](https://www.creativewmp.com/). CREATIVE has the goal of providing the public with analysis tools for more transparency of political ads across online platforms. In particular, CREATIVE provides cross-platform integration and standardization of political ads collected from Google and Facebook. CREATIVE is a joint project of the [Wesleyan Media Project (WMP)](https://mediaproject.wesleyan.edu/) and the [privacy-tech-lab](https://privacytechlab.org/) at [Wesleyan University](https://www.wesleyan.edu).

To analyze the different dimensions of political ad transparency we have developed an analysis pipeline. The scripts in this repo are part of the Data Processing step in our pipeline.

![A picture of the repo pipeline](CREATIVE_step2_032524.png)

## Table of Contents

- [1. Overview](#1-overview)
- [2. Setup](#2-setup)
- [3. Results Storage](#3-results-storage)
- [4. Thank you!](#4-thank-you)

## 1. Overview

![rekognition-pipeline](rekognition-pipeline.png)

This repo contains scripts for performing image and video recognition on political ads through the Amazon Rekognition service (AWS SDK for Python). The core functionality that the scripts in this repo provide are:

- A video processing module calling the Amazon Rekognition video API to perform text detection, label detection, face detection and face search (searching for faces that match an existing face collection) on video data. The module also provides functions to create SNS Topic and SQS queue necessary for Rekognition video analysis.
- An image processing module calling the Amazon Rekognition image API to perform text detection, face detection, and face search on image data.
- Functions in video and image modules that allow one-step parsing of WMP variables from Rekognition image and video analysis results.
- Code for creating a face collection with Rekognition, which is necessary to run face search for both image and video processing.
- Tutorial notebooks to use the above modules and functions.

## 2. Setup

Before running any of the code in this repo, make sure you have Python installed on your system. You can download Python from the [official Python website](https://www.python.org/downloads/). In addition, install Jupyter Notebook by writing the following command in your terminal:

```bash
pip install jupyter
```

From here, you should be able to run Jupyter Notebook with:

```bash
jupyter notebook
```

Also, install the following dependency:

```bash
pip install boto3
```

You will need to [register for an AWS account](https://aws.amazon.com/). Once you registered your account, proceed as follows:

1. Create an Amazon S3 bucket to store the video and image data for processing via your AWS account.

2. Create your [IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html).

3. Configure your [AWS credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html). Otherwise, pass your credentials whenever calling the Rekognition API.

4. After the above setup procedures, please follow the instructions in the `/code/getting-started` folder, which contains code samples, to upload data to the S3 bucket and create face collections.

   ```bash
   # Upload your face collection data, image data, video data from their local paths to respective Amazon S3 bucket destinations
   aws s3 cp <source> <target> --recursive
   ```

5. After you have your data stored in an S3 bucket, follow the tutorials in the `/code/image` and `/code/video` folders to process the data based on your demands. Make sure to replace the placeholders in the code with your own AWS credentials and file paths.

## 3. Results Storage

Image and video processing modules return the response data from the Amazon Rekognition API in a dictionary. They can be saved into JSON files. You may choose to either store the raw response data in Amazon S3 bucket or in your local machine. To store them in an S3 bucket, see the `tutorial.ipynb` in the `/code/image` and `/code/video` folders.

We also provide helper functions that parse WMP variables from the response data.

These WMP variables parsed from Rekognition response data are saved as columns `aws_ocr_img_text` (image ads), `aws_face_img` (image ads), `aws_face_vid` (video ads), `aws_ocr_video_text` (video ads) into our final output tables. Description and access information of final output tables can be found in [data-post-production](https://github.com/Wesleyan-Media-Project/data-post-production/tree/main).

## 4. Thank You

<p align="center"><strong>We would like to thank our supporters!</strong></p><br>

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
