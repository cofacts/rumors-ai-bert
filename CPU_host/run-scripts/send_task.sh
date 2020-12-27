
cat /root/.ssh/google_compute_engine
cat /root/.ssh/google_compute_engine.pub

gcloud compute scp ./tasks/task.csv $USER@$GPU_INSTANCE_NAME:~/rumors-ai-bert/GPU_host/tasks/test.csv --zone=$GPU_INSTANCE_ZONE --ssh-key-file=/root/.ssh/google_compute_engine

gcloud compute ssh $USER@$GPU_INSTANCE_NAME --zone $GPU_INSTANCE_ZONE --command="bash ~/rumors-ai-bert/GPU_host/predict_ModelA.sh"

gcloud compute scp $USER@$GPU_INSTANCE_NAME:~/rumors-ai-bert/GPU_host/prediction/Predict_results.txt ./tasks/result_task.txt  --zone $GPU_INSTANCE_ZONE --ssh-key-file=/root/.ssh/google_compute_engine
