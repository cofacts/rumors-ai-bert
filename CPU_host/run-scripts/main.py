# coding:utf-8

import os
import requests
import json
import argparse

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

def register_model(register_url, model_name, categoryMapping):
    """
    Register AI model in Cofacts host

    :param register_url: Cofacts model registration url
    :param model_name: model name to be registered
    :param categoryMapping: category mapping dictionary

    :return: model ID and api key
    """

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
    parser.add_argument(
        "--model_name",
        default="",
        type=str,
        required=False,
        help="Model name to be registered",
    )
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


    args = parser.parse_args()

    cofacts_url = args.url
    action = args.action
    model_name = args.model_name
    model_ID = args.model_ID
    api_key = args.api_key

    if action == 'register':
        if model_name == "":
            print("MODEL_NAME is not given! Automatically set MODEL_NAME=test_model to continue registering process.")
            model_name = 'test_model'

        register_url = cofacts_url + '/v1/models'
        categoryMapping = DEFAULT_CATEGORY_MAPPING

        model_ID, api_key = register_model(register_url, model_name, categoryMapping)

    elif action == 'start':
        pass
    else:
        print('No such action! We only support register or start action.')
