from openai import OpenAI

client = OpenAI(api_key="sk-etivkrjoaidjvggnkxpxyfmfvawycdcznmwjooespajdixjd", base_url="https://api.siliconflow.cn/v1")

"""
该接口为硅基流动API接口，属于第三方接口，需要支付额外费用并且需要连接网络，使用前需要填写api_key，上面是我的api_key，钱包余额还有11块

硅基流动官网：https://account.siliconflow.cn/zh/login

硅基流动API使用说明：https://docs.siliconflow.cn/cn/api-reference/chat-completions/chat-completions

"""


def generate_completion_stream_flow(prompt):
    """

    :param prompt: 输入提示词
    :return: 输出内容，类型为str
    """
    result = "<think>"
    print(result)
    flag = True
    response = client.chat.completions.create(
        model='deepseek-ai/DeepSeek-R1-Distill-Llama-70B',
        messages=[
            {'role': 'user',
             'content': prompt,
             }
        ],
        max_tokens=16384,
        stream=True
    )

    for chunk in response:
        obj = chunk.choices[0].delta
        if obj.reasoning_content is not None:
            print(obj.reasoning_content, end="")
            result += obj.reasoning_content
        else:
            if flag:
                flag = False
                result += "</think>"
                print("</think>")
            print(obj.content, end="")
            result += obj.content

    print("\nround finished")
    return result
