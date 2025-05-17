import concurrent.futures

from API.ollama import generate_completion_stream_ollama
from API.siliconflow import generate_completion_stream_flow
from model.expert_prompt import prompt_list, sys_prompt6, sys_prompt7, sys_prompt8
import model.function

from concurrent.futures import ThreadPoolExecutor


def multi_thread_function(test_require: str) -> str:
    with ThreadPoolExecutor() as executor:
        # 将任务提交至线程池
        futures = []
        for i, sys_prompt in enumerate(prompt_list):
            # futures.append(executor.submit(generate_completion_stream_ollama, sys_prompt + test_require, index=i, show=False))
            futures.append(executor.submit(generate_completion_stream_flow, sys_prompt + test_require))
        # 开始处理
        combined_test_cases = []
        for future in concurrent.futures.as_completed(futures):
            try:
                result = model.function.clear_think(future.result())
                combined_test_cases.append(result)
            except Exception as e:
                print(f"方法:'multi_thread_function'发生错误\n错误原因:{e}\n")

    # 去重处理
    print("\nteacher 开始处理 students 结果\n")
    final_test_cases = str(
        # generate_completion_stream_ollama(sys_prompt8 + test_require + "\n"  + str(combined_test_cases),
        #                                   model="deepseek-r1:32b",
        #                                   base_url="http://192.168.46.1:11434/api", show=True, temperature=0.5,
        #                                   num_ctx=8192, num_predict=-1))
        generate_completion_stream_flow(sys_prompt8 + test_require + "\n" + str(combined_test_cases)))
    # final_test_cases = str(generate_completion_stream_flow(sys_prompt7 + str(combined_test_cases)))
    return final_test_cases
