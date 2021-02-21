

# refer to: https://cloud.google.com/sdk/gcloud/reference/auth/activate-service-account
# authorize access to Google Cloud Platform with a service account

gcloud auth activate-service-account $SERVICE_ACCOUNT --key-file=$KEY_FILE


# set project values in gcloud config

gcloud config set project $PROJECT
gcloud config set compute/zone $GPU_INSTANCE_ZONE

# refer to: https://cloud.google.com/sdk/gcloud/reference/compute/instances/set-service-account#--scopes
# set service account and scopes for a Compute Engine instance

#gcloud compute instances set-service-account INSTANCE_NAME [--zone=ZONE] --scopes=compute-rw [--service-account=SERVICE_ACCOUNT]
