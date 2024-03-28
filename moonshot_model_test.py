from langchain_community.langchain_moonshot.moonshot import ChatMoonshot
import os


llm = ChatMoonshot(
    moonshot_api_key="sk-yrU5C6KyXyqXuII5vHy5tVrYPjUUCNg0iFOQWOASldwm8hoX",
    moonshot_model_name="moonshot-v1-32k",
    temperature=0.0,
    moonshot_api_base="https://api.moonshot.cn/v1",
)

def ask_question(question, text):
    # 将问题和上下文合并为一个字符串
    input_str = f"{question} {text}"
    res = llm.invoke(input=input_str)  # 使用字符串作为输入
    return res.content  

# res = ask_question("请总结文本的关键信息", "我去公司上班了，今天是2022年5月12日。")
# print(res)
