# rumors-ai-bert
Containerized BERT model for article categorizer

## Pipelines of rumors-ai-bert

1. Get articles needs to be classify in rumors-ai database.
2. Preprocess JSON response into CSV file for BERT model inputs
3. Send CSV file and prediction commands to GPU host
4. Read article classification results
5. Send classification results to cofacts rumors-ai host

![](./img/pipeline_of_rumors-ai-bert.png)

## CPU host

The CPU host repo is mainly for user to build a service to:
  - Send tasks to GPU host
  - Control GPU host turn on/off (cost saving purpose)
  - Retrieve article classification results
  - Send results to cofacts rumors-ai host

### Build docker image

```bash
cd CPU_host
docker build ./ -t IMAGE_NAME:IMAGE_VERSION
```

### Image on Dockerhub

https://hub.docker.com/r/gary9630/rumors-ai-bert/tags


### Run model registration

```bash
docker run --rm --env CFA_ACTION=register [--env MODEL_NAME=YOUR_NAME] -t IMAGE_NAME:IMAGE_VERSION
```

After successfully registering, you will receive your MODEL_ID and CFA_API_KEY.

Please store these information carefully. You will need these information to send prediction results.

### Run articles classification

```bash
docker run --rm --env CFA_ACTION=start --env CFA_API_KEY=YOUR_API_KEY \
--env MODEL_ID=YOUR_MODEL_ID --env SERVICE_ACCOUNT=YOUR_SERVICE_ACCOUNT --env KEY_FILE=KEY_FILE_PATH \
--env GPU_INSTANCE_NAME=YOUR_GPU_INSTANCE_NAME --env GPU_INSTANCE_ZONE=YOUR_GPU_INSTANCE_ZONE --env USER=YOUR_GPU_USER_ACCOUNT \
 -v $(pwd)/YOUR_SERVICE_ACCOUNT_KEY.json:$KEY_FILE -t IMAGE_NAME:IMAGE_VERSION
```

These environment variables can also be set in Dockerfile before building image.

This command will start retrieving tasks from Cofacts AI master host, send to GPU host making predictions, and finally send results back to Cofacts AI master host.


## GPU host

The GPU host repo is mainly for user to build a service to:
 - Train BERT models for pre-defined article classes/sub-classes
 - Classify articles sended from CPU host
