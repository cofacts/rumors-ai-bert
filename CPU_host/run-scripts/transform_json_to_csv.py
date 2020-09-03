# coding=utf-8


import os
import json

import pandas as pd


def Transform_JSON_to_CSV(input_file_name, output_file_name):

    define_columns = ['id', 'text', 'label']

    data_list = []

    with open(input_file_name, 'r') as f:
        tasks = list(json.load(f))

        for task in tasks:

            data_list.append([task['id'], task['content'], '0'])


    df_data = pd.DataFrame(data_list, columns=define_columns)

    df_data.to_csv(output_file_name)
