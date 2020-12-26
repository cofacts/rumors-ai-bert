#!bin/bash

rm ./tasks/cached*

/opt/conda/bin/python ./model_bert/run_multi_label_classification.py \
	--task_name cofacts \
	--model_name_or_path models_bert \
	--do_eval \
	--data_dir ./tasks/ \
	--predict_file test.csv \
	--output_dir ./prediction/ \
	--per_gpu_eval_batch_size=16 \
