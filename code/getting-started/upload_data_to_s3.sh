#!/bin/sh

# Upload your face collection data, image data, video data from their local paths to respective Amazon S3 bucket destinations
aws s3 cp <source> <target> --recursive