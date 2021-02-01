# GPU host guide

GPU host usage guide.

## Train a fine-tuned BERT model

Follow the instructions in [model_bert](https://github.com/cofacts/rumors-ai-bert/tree/master/GPU_host/model_bert).

After successfully trained a model (or put your trained model), you will see the repo structure similar to following:

![](./img/repo_structure.png)


## Model with New main Categories

Category definition may differ at different time point.

For instance, currently we have trained a model with 17 main categories.

If you want to train a model with 20 main categories, you have to do following steps:
 - Prepare train/dev/test datasets with 20 categories
 - Run model training/testing with given category number with [run_multi_label_classification.py](https://github.com/cofacts/rumors-ai-bert/blob/master/GPU_host/model_bert/run_multi_label_classification.py)


## Model with New Sub-Categories

If one main category contains many important sub-categories and has enough articles for training.

You may prefer to create sub-categories classification model.

You can do it for sure! Merely treat these sub-categories as independent datasets.

In other words, you have to train a new fine-tuned BERT model with different sub-categories in the same main category. Following are the steps to build a sub-categories model:
 - Prepare train/dev/test datasets with given sub-categories
 - Run model training/testing with given category number with [run_multi_label_classification.py](https://github.com/cofacts/rumors-ai-bert/blob/master/GPU_host/model_bert/run_multi_label_classification.py)
 - Remember to save the model in the different path than main category model
