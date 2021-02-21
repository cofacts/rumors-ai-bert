# coding:utf-8
import os
import config
import requests
import json
import subprocess
import argparse

from shutil import copyfile
from transform_json_to_csv import Transform_JSON_to_CSV

DEFAULT_CATEGORY_MAPPING = {
  0: 'kj287XEBrIRcahlYvQoS', # 中國影響力
  1: 'kz3c7XEBrIRcahlYxAp6', # 性少數與愛滋病
  2: 'lD3h7XEBrIRcahlYeQqS', # 女權與性別刻板印象
  3: 'lT3h7XEBrIRcahlYugqq', # 保健秘訣、食品安全
  4: 'lj2m7nEBrIRcahlY6Ao_', # 基本人權問題
  5: 'lz2n7nEBrIRcahlYDgri', # 農林漁牧政策
  6: 'mD2n7nEBrIRcahlYLAr7', # 能源轉型
  7: 'mT2n7nEBrIRcahlYTArI', # 環境生態保護
  8: 'mj2n7nEBrIRcahlYdArf', # 優惠措施、新法規、政策宣導
  9: 'mz2n7nEBrIRcahlYnQpz', # 科技、資安、隱私
  10: 'nD2n7nEBrIRcahlYwQoW', # 免費訊息詐騙
  11: 'nT2n7nEBrIRcahlY6QqF', # 有意義但不包含在以上標籤
  12: 'nj2n7nEBrIRcahlY-gpc', # 無意義
  13: 'nz2o7nEBrIRcahlYBgqQ', # 廣告
  14: 'oD2o7nEBrIRcahlYFgpm', # 只有網址其他資訊不足
  15: 'oT2o7nEBrIRcahlYKQoM', # 政治、政黨
  16: 'oj2o7nEBrIRcahlYRAox' # 轉發協尋、捐款捐贈
}

def register_model(cofacts_url, model_name, categoryMapping):
    """
    Register AI model in Cofacts host

    :param cofacts_url: Cofacts host url
    :param model_name: model name to be registered
    :param categoryMapping: category mapping dictionary

    :return: model ID and api key
    """
    register_url = cofacts_url + '/v1/models'
    model_ID = ''
    api_key = ''

    model_register_dict = {}
    headers = {'Content-Type': 'application/json', 'Accept':'application/json'}

    model_register_dict["name"] = model_name
    model_register_dict["realTime"] = False
    model_register_dict["categoryMapping"] = categoryMapping

    post_response = requests.post(register_url, json=model_register_dict, headers=headers)

    print('='*20)
    print(post_response.text)
    print('='*20)

    if post_response.status_code == 200:
        print(f'Model registration is successful!')
        post_response_data = post_response.json()

        model_ID = post_response_data["id"]
        api_key = post_response_data["apiKey"]

    else:
        print(f'Model registration is failed! Error code = {post_response.status_code}')

    return model_ID, api_key


def get_task(cofacts_url, model_ID, debug_mode=False):

    if debug_mode:
        get_task_url = cofacts_url + '/v1/tasks?modelId=' + model_ID + '&test=1'
    else:
        get_task_url = cofacts_url + '/v1/tasks?modelId=' + model_ID

    return requests.get(get_task_url)



if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # parameters
    parser.add_argument(
        "--url",
        default="https://ai-api-stag.cofacts.org",
        type=str,
        required=True,
        help="Cofacts AI master server",
    )
    parser.add_argument(
        "--action",
        default="start",
        type=str,
        required=True,
        help="Performing action: register or start(default)",
    )
    ## model register parameters
    parser.add_argument(
        "--model_name",
        default="",
        type=str,
        required=False,
        help="Model name to be registered",
    )
    ## task start parameters
    parser.add_argument(
        "--model_ID",
        default="",
        type=str,
        required=False,
        help="Model ID",
    )
    parser.add_argument(
        "--api_key",
        default="",
        type=str,
        required=False,
        help="API key to access Cofacts API",
    )
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

    cofacts_url = args.url
    action = args.action
    model_name = args.model_name
    model_ID = args.model_ID
    api_key = args.api_key
    debug_mode = args.debug_mode
    category_num = args.category_num

    if action == 'register':
        if model_name == "":
            print("MODEL_NAME is not given! Automatically set MODEL_NAME=test_model to continue registering process.")
            model_name = 'test_model'


        categoryMapping = DEFAULT_CATEGORY_MAPPING

        model_ID, api_key = register_model(cofacts_url, model_name, categoryMapping)

    elif action == 'start':

        TASK_QUEUE = True

        # gcloud auth
        subprocess.call(['bash', './service_account.sh'])

        # start GPU machine
        if not debug_mode:
            subprocess.call(['bash', './start_GPU.sh'])

        while TASK_QUEUE:

            # get task and send to GPU host to do article classification
            response = get_task(cofacts_url, model_ID, debug_mode)

            if response.status_code == 200:
                print('Task retrieving is successful!')

                task_dict = {}

                with open('task.json', 'w') as jsonfile:
                    task_dict = response.json()
                    json.dump(task_dict, jsonfile, ensure_ascii=False, indent=4)


                # check the task needs to continue or not (status code or folder contains indicator file)
                if len(task_dict) > 0:
                    print('Task is not empty, sending to GPU host...')
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
                print('Task retrieveing is failed, please check Cofacts host or model ID settings!')
                TASK_QUEUE = False
                break


            # parse prediction results from GPU host and send to Cofacts host
            try:
                # Read prediction result file: result_task.txt
                result_file = './tasks/result_task.txt'

                with open(result_file, 'r') as file:
                    results = file.readlines()


                result_task_payload = []
                for task, result in zip(task_dict, results[3:]):

                    result_task_dict = {}
                    prediction = { 'confidence': { f'c{i+1}': 0 for i in range(category_num)}}
                    predict_class = str(int(result.replace('\n', '').split(' ')[-1])+1)

                    prediction['confidence']['c'+predict_class] = 1

                    result_task_dict['id'] = task['id']
                    result_task_dict['result'] = {'prediction': prediction, 'time': 5566}

                    result_task_payload.append(result_task_dict)

                post_task_site = cofacts_url + '/v1/tasks'

                headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
                post_response = requests.post(post_task_site, json=result_task_payload, headers=headers)

                print('='*20)
                print(post_response.text)
                print('='*20)

                if post_response.status_code == 200:
                    print('Task submission is successful!')
                    subprocess.call(['mv', './tasks/result_task.txt', './tasks/result_task_submitted.txt'])

                else:
                    print(f'Task submission is failed! Please check task host is alive or correct! Error code = {post_response.status_code}')
                    TASK_QUEUE = False


                if debug_mode:
                    with open('debug.json', 'w') as jsonfile:
                        json.dump(result_task_payload, jsonfile, ensure_ascii=False, indent=4)

            except OSError:
                print(OSError.message)
                # print('The result task file:{} does not exist'.format(result_file))
                TASK_QUEUE = False

        # stop GPU machine
        if not debug_mode:
            subprocess.call(['bash', './stop_GPU.sh'])

    else:
        print('No such action! We only support register or start action.')
