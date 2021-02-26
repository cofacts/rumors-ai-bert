import os


TASK_HOST = os.environ.get('TASK_HOST', 'https://ai-api-stag.cofacts.org')
MODEL_ID = os.environ.get('MODEL_ID', '5f03292b8cc16e0b1d1e5f16')

SERVICE_ACCOUNT = os.environ.get('SERVICE_ACCOUNT', '')
GPU_INSTANCE_NAME = os.environ.get('GPU_INSTANCE_NAME', '')
GPU_INSTANCE_ZONE = os.environ.get('GPU_INSTANCE_ZONE', '')
