import json
import re

import pandas as pd
from docx import Document

from model.mul_thread_function import multi_thread_function

from json_repair import repair_json


def read_word(file_path, section_title="Web端系统需求说明") -> dict[str, list[str]]:
    """
    读取需求文档，分割为各个模块，格式化输出

    :param file_path: 文档路径
    :param section_title: 需要提取的内容
    :return: 返回提取内容
    """

    doc = Document(file_path)
    capture = False
    heading1 = section_title
    heading2 = ''
    heading3 = ''
    heading4 = ''
    context = {heading1: []}

    for para in doc.paragraphs:
        # 检测到目标后开始捕获
        if section_title in para.text:
            capture = True
            continue

        if capture:
            # 检测到下一个一级标题则退出
            if para.style.name == 'Heading 1':
                break
            elif para.style.name == 'Heading 2':
                heading2 = para.text.strip()
                context[heading1].append({heading2: []})
            elif para.style.name == 'Heading 3':
                heading3 = para.text.strip()
                context[heading1][-1][heading2].append({heading3: []})
            elif para.style.name == 'Heading 4':
                heading4 = para.text.strip()
                context[heading1][-1][heading2][-1][heading3].append({heading4: []})
            else:
                try:
                    context[heading1][-1][heading2][-1][heading3][-1][heading4].append(para.text.strip())
                except:
                    print('文件格式有误，已忽略')

    return context

def write_excel(json_list, output_file):
    """
    :function:将json列表输入进excel中
    :param json_list: json列表
    :param output_file: 输出文件路径
    :return:
    """
    df = pd.DataFrame(json_list)
    df.to_excel(output_file, sheet_name='Sheet1', index=False)

def clear_think(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)


def match_json(text, pattern=r"(?:<JSON>|```json)(.*?)(?:</JSON>|```)"):
    """
    :function: 匹配str中的json内容
    :param text: 匹配文本
    :param pattern: 匹配规则
    :return:
    """
    text = clear_think(text)
    matches = re.findall(pattern, text, re.DOTALL)
    return matches


def get_json_list(file_path, section_title) -> list:
    """
    :function:将得到的文字转化为json列表
    :param file_path: 文档路径
    :param section_title: 需要提取的内容
    :return: 返回提取内容
    """
    require = read_word(file_path, section_title)[section_title]
    res = ""
    json_list = []

    for r in require:
        for key, value in r.items():
            for val in value:
                res += multi_thread_function(str(val))

    matches = match_json(res)
    for match in matches:
        try:
            json_data = json.loads(repair_json(match))
            for data in json_data:
                json_list.append(data)
        except Exception as e:
            print(f"\n方法:'get_json_list'发生错误\n错误原因:{e}\n")
            print(f"正在重新生成\n")
            get_json_list(file_path, section_title)

    return json_list