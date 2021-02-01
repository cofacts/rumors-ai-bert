# coding:utf-8

import os
import config
import requests
import json
import subprocess
import argparse

from shutil import copyfile



from transform_json_to_csv import Transform_JSON_to_CSV

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # parameters
    parser.add_argument(
        "--debug_mode",
        default=False,
        type=bool,
        required=False,
        help="Enable debug mode",
    )
    parser.add_argument(
        "--category_num",
        default=17,
        type=int,
        required=False,
        help="Category numbers",
    )

    args = parser.parse_args()

    debug_mode = args.debug_mode
    category_num = args.category_num


    TASK_QUEUE = True

    # start GPU machine
    if not debug_mode:
        subprocess.call(['bash', './start_GPU.sh'])

    while TASK_QUEUE:

        if debug_mode:
            get_task_site = config.TASK_HOST + '/v1/tasks?modelId=' + config.MODEL_ID + '&test=1'
        else:
            get_task_site = config.TASK_HOST + '/v1/tasks?modelId=' + config.MODEL_ID

        post_task_site = config.TASK_HOST + '/v1/tasks'

        response = requests.get(get_task_site)

        if response.status_code == 200:
            print('Task retrieving is successful!')

            task_dict = {}

            with open('task.json', 'w') as jsonfile:
                task_dict = response.json()
                json.dump(task_dict, jsonfile, ensure_ascii=False, indent=4)


            # check the task needs to continue or not (status code or folder contains indicator file)
            if len(task_dict) > 0:
                print('OKKK, continue')
                Transform_JSON_to_CSV('task.json', 'task.csv')
                subprocess.call(['mv', './task.csv', './tasks/task.csv'])

                subprocess.call(['bash', './send_task.sh'])
                subprocess.call(['mv', './tasks/task.csv', './tasks/task_sended.csv'])
                TASK_QUEUE = True
            else:
                print('Empty task!')
                TASK_QUEUE = False
                break
        else:
            print(response.text)
            print('Task retrieveing is failed, please check task host or model ID settings!')
            TASK_QUEUE = False
            break


        # Read prediction result file: result_task.txt
        result_file = './tasks/result_task.txt'

        try:
            with open(result_file, 'r') as file:
                results = file.readlines()


            result_task_payload = []
            for task, result in zip(task_dict, results[3:]):
                #print(task, result)
                result_task_dict = {}
                # prediction = {'confidence': {'c1': 0, 'c2': 0, 'c3': 0, 'c4': 0,
                #                 'c5': 0, 'c6': 0, 'c7': 0, 'c8': 0, 'c9': 0,
                #                 'c10': 0, 'c11': 0, 'c12': 0, 'c13': 0, 'c14': 0,
                #                 'c15': 0, 'c16': 0, 'c17': 0,
                #             }}
                prediction = { 'confidence': { f'c{i+1}': 0 for i in range(len(category_num))}}
                predict_class = str(int(result.replace('\n', '').split(' ')[-1])+1)

                prediction['confidence']['c'+predict_class] = 1

                result_task_dict['id'] = task['id']
                result_task_dict['result'] = {'prediction': prediction, 'time': 5566}

                result_task_payload.append(result_task_dict)


            headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
            post_response = requests.post(post_task_site, json=result_task_payload, headers=headers)

            # post_response = requests.post(post_task_site, data=result_task_payload)

            with open('debug.json', 'w') as jsonfile:
                json.dump(result_task_payload, jsonfile, ensure_ascii=False, indent=4)


            if post_response.status_code == 200:
                print('Task submission is successful!')
                subprocess.call(['mv', './tasks/result_task.txt', './tasks/result_task_submitted.txt'])

                if debug_mode:
                    print(post_response.text)
                    TASK_QUEUE = False
                else:
                    TASK_QUEUE = True

            else:
                print(post_response.text)
                print('Task submission is failed! Please check task host is alive or correct!')
                TASK_QUEUE = False


        except OSError:
            print(OSError.message)
            # print('The result task file:{} does not exist'.format(result_file))
            TASK_QUEUE = False

    if not debug_mode:
        subprocess.call(['bash', './stop_GPU.sh'])
