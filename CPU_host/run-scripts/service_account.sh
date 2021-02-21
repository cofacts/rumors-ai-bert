

# refer to: https://cloud.google.com/sdk/gcloud/reference/auth/activate-service-account
# obtain the key file

gcloud iam service-accounts keys create


# refer to: https://cloud.google.com/sdk/gcloud/reference/auth/activate-service-account
# authorize access to Google Cloud Platform with a service account

gcloud auth activate-service-account [ACCOUNT] --key-file=KEY_FILE


# refer to: https://cloud.google.com/sdk/gcloud/reference/compute/instances/set-service-account#--scopes
# set service account and scopes for a Compute Engine instance

gcloud compute instances set-service-account INSTANCE_NAME [--zone=ZONE] --scopes=compute-rw [--service-account=SERVICE_ACCOUNT]
