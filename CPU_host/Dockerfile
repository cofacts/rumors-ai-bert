FROM tiangolo/meinheld-gunicorn-flask:python3.7

# Create app directory
RUN mkdir /app/tasks

RUN mkdir /root/run-scripts
RUN mkdir /root/run-scripts/tasks
WORKDIR /root/run-scripts

# Copy gcloud auth keyfile
COPY ./cofacts-dev-cd6d8e1c4016.json /root/cofacts-dev-key.json

# Copy ssh files
COPY .ssh /root/.ssh

# Copy scripts
COPY ./run-scripts /root/run-scripts


# Copy pipfile and install required packages
COPY ./Pipfile /root/run-scripts/
COPY ./Pipfile.lock /root/run-scripts/
RUN  pip install pipenv && pipenv install --deploy --dev --system

# Install gcloud command
RUN apt-get update && apt-get -y install sudo

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN sudo apt-get install apt-transport-https ca-certificates gnupg -y
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
#RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
RUN sudo apt-get update && sudo apt-get install google-cloud-sdk -y

# Set all environment variables
## for CPU host performing register/start action
ENV CFA_URL="https://ai-api-stag.cofacts.org"
ENV CFA_ACTION=""
ENV CFA_API_KEY=""
ENV MODEL_NAME="test_modelll"

## for gcloud auth
ENV SERVICE_ACCOUNT="69418316315-compute@developer.gserviceaccount.com"
ENV KEY_FILE="/root/cofacts-dev-key.json"

## for local machine connecting to GCP VMs
ENV PROJECT="cofacts-dev"
ENV VM="rumors-ai-test"

## for start action
ENV TASK_HOST="https://ai-api-stag.cofacts.org"
ENV MODEL_ID="5f03292b8cc16e0b1d1e5f16"
#ENV MODEL_ID=""

ENV GPU_INSTANCE_NAME="gpu-instance-2"
ENV GPU_INSTANCE_ZONE="asia-east1-a"
ENV USER="gary96302000_eecs96"

# Execute main program
#CMD python /root/run-scripts/task_handler.py --debug_mode True --category_num 17

CMD python main.py --url=$CFA_URL --action=$CFA_ACTION --model_name=$MODEL_NAME --model_ID=$MODEL_ID --api_key=$CFA_API_KEY --debug_mode=True
