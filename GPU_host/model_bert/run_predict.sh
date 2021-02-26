#!/bin/bash

### User define parameters
model_name_or_path=model_bert
data_dir=./data/
category_num=17
predict_file=dev.csv
output_dir=./prediction/

per_gpu_eval_batch_size=16

### run training program
python ./run_multi_label_classification.py \
--task_name cofacts \
--model_name_or_path $model_name_or_path \
--do_eval \
--data_dir $data_dir \
--category_num $category_num \
--predict_file $predict_file \
--per_gpu_eval_batch_size=$per_gpu_eval_batch_size \
--output_dir $output_dir
