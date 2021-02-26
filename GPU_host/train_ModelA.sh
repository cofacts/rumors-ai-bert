#!bin/bash

python ~/rumors-ai-bert/GPU_host/model_bert/run_multi_label_classification.py \
	--task_name cofacts \
	--model_name_or_path bert-base-chinese \
	--do_train \
	--do_eval \
	--data_dir ~/rumors-ai-bert/GPU_host/data/processed_data/ \
	--category_num 17 \
	--learning_rate 1e-4 \
	--num_train_epochs 3 \
	--max_seq_length 128 \
	--output_dir model_bert/ \
	--per_gpu_eval_batch_size=16 \
	--per_gpu_train_batch_size=16 \
	--gradient_accumulation_steps 2 \
	--overwrite_output
