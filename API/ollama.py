import json

import requests

# 基础初始化设置
# base_url = "http://localhost:11434/api"
# base_url = "http://192.168.13.191:11434/api"
# base_url = "http://556515i74q.oicp.vip:11434/api"
headers = {"Content-Type": "application/json"}


"""
该接口为ollama API，比赛时用的本地化部署就是这个接口

详情可以查看ollamaAPI文档 https://ollama.cadn.net.cn/api.html
"""
def generate_completion_stream_ollama(prompt: str, index=-1, model="deepseek-r1:7b",
                                      base_url="http://localhost:11434/api", show=False, temperature=0.7, num_ctx=None,
                                      num_predict=None) -> str:
    """

    :param prompt: 传入给ai的提示词，在本项目中即为需求说明
    :param index: 用于表示第几个ai进行作答
    :param model: 用于选择ai模型
    :param base_url: ollama的地址
    :param show: 是否展示回答内容
    :param temperature: 模型温度，温度越高模型回答越有想象力
    :param num_ctx: 表示prompt长度，例如8192则表示最大能够理解8192个提示词，超出部分则会忘记
    :param num_predict: 表示输出长度，-1表示无限制
    :return: 返回结果，类型为str
    """
    if index != -1:
        print(f"\nstudent{index} 开始作答")
    url = f"{base_url}/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": temperature,
            "num_ctx": num_ctx,
            "num_predict": num_predict
        }
    }
    response = requests.post(url, headers=headers, json=data, stream=True)
    result = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode('utf-8'))  # 修改为utf-8
            response_value = data.get("response")  # 获取response
            result += response_value
            if show:
                print(response_value, end="")  # 输出

    if index != -1:
        print(f"\nstudent{index} 回答完毕")
    return result
