import json
import time

from API.ollama import generate_completion_stream_ollama
from model.function import write_excel, read_word, match_json
from API.siliconflow import generate_completion_stream_flow
from model.expert_prompt import prompt_list, sys_prompt6, sys_prompt7
from json_repair import repair_json
import model.function


def no_multi_thread_function(test_require):
    combined_test_cases = ""
    for i, sys_prompt in enumerate(prompt_list):
        combined_test_cases += model.function.clear_think(
            generate_completion_stream_ollama(sys_prompt + test_require, index=i))

    # 去重处理
    print("\nteacher 开始处理 students 结果\n")
    # final_test_cases = str(
    #     generate_completion_stream_ollama(sys_prompt6 + str(combined_test_cases),
    #                                       model="deepseek-r1:32b",
    #                                       base_url="http://192.168.13.191:11434/api", show=True, temperature=0.5,
    #                                       num_ctx=8192, num_predict=-1))
    final_test_cases = str(generate_completion_stream_flow(sys_prompt7 + str(combined_test_cases)))
    return final_test_cases


file_path = r"./test_data/1. ERP管理平台需求说明书商品分类模块.docx"
output_path = r'./test_report/测试用例.xlsx'
section_title = "Web端系统需求说明"

print("\n程序启动")
start_time = time.time()
require = read_word(file_path, section_title)[section_title]
res = ""
json_list = []
for r in require:
    for key, value in r.items():
        for val in value:
            res += no_multi_thread_function(str(val))

matches = match_json(res)
for match in matches:
    try:
        json_data = json.loads(repair_json(match))
        for data in json_data:
            json_list.append(data)
    except Exception as e:
        print(f"\n方法:'get_json_list'发生错误\n错误原因:{e}\n")

write_excel(json_list, output_path)
end_time = time.time()
print(f"\n程序结束，共花费{end_time - start_time:.2f}秒!")
