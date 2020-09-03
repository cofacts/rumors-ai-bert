#!/bin/bash

gcloud compute instances create $GPU_INSTANCE_NAME \
    --machine-type n1-standard-2 --zone $GPU_INSTANCE_ZONE \
    --accelerator type=nvidia-tesla-t4,count=1 \
    --image-family pytorch-latest-gpu --image-project deeplearning-platform-release \
    --maintenance-policy TERMINATE --restart-on-failure \
