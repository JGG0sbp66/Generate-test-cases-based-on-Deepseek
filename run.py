from model.function import write_excel
from model.function import get_json_list
import time

file_path = r"./test_data/1. ERP管理平台需求说明书四个模块.docx"
output_path = r'./test_report/测试用例.xlsx'
section_title = "Web端系统需求说明"

print("\n程序启动")
start_time = time.time()
json_list = get_json_list(file_path, section_title)
write_excel(json_list, output_path)
end_time = time.time()
print(f"\n程序结束，共花费{end_time - start_time:.2f}秒!")
