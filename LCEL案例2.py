from ipaddress import summarize_address_range

from dotenv import load_dotenv
from os import getenv

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 提示词---> llm ---> 文本 --->  提示词2 ----->llm ---评分
load_dotenv()

llm = ChatOpenAI(
    temperature=0,
    model=getenv("MODEL"),
    api_key=getenv("API_KEY"),
    base_url=getenv("API_BASE"),
)

gather_preferences_prompt = ChatPromptTemplate.from_template(
    "用户输入了一些餐厅偏好：\n{input1}\n"
    "请将用户的偏好总结为清洗的需求："
)

recommend_restaurants_prompt = ChatPromptTemplate.from_template(
    "基于用户需求：\n{input2}\n"
    "请推荐3家适合的餐厅，并说明推荐理由"
)

summarize_recommendations_prompt = ChatPromptTemplate.from_template(
    "以下是餐厅推荐和理由：\n{input3}\n"
    "请总结成2-3句话，供用户快速参考"
)



chain = gather_preferences_prompt |  llm | recommend_restaurants_prompt | summarize_recommendations_prompt | llm | StrOutputParser()

print(chain.invoke({'input1':'我喜欢安静的地方，有素食的餐厅更好，而且价格也不贵。'}))