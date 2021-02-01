#!bin/bash

rm ~/rumors-ai-bert/GPU_host/tasks/cached*

/opt/conda/bin/python ~/rumors-ai-bert/GPU_host/model_bert/run_multi_label_classification.py \
	--task_name cofacts \
	--model_name_or_path models_bert \
	--do_eval \
	--data_dir ~/rumors-ai-bert/GPU_host/tasks/ \
	--category_num 17 \
	--predict_file test.csv \
	--output_dir ~/rumors-ai-bert/GPU_host/prediction/ \
	--per_gpu_eval_batch_size=16 \
