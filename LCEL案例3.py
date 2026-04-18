
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

from dotenv import load_dotenv
from os import getenv

from langchain_core.runnables import RunnableLambda, RouterRunnable, RunnableSequence
from langchain_openai import ChatOpenAI



load_dotenv()


llm = ChatOpenAI(
    temperature=0,
    model=getenv("MODEL"),
    api_key=getenv("API_KEY"),
    base_url=getenv("API_BASE"),
)

physics_template = ChatPromptTemplate.from_template(
    "你是一位物理教授，擅长用简洁易懂的方式回答物理问题。以下是问题内容：{input}"
)

math_template = ChatPromptTemplate.from_template(
    "你是一位数学家，擅长分解步骤解决数学问题，并提供详细的解决问题。一喜爱是问题的内容：{input}"
)

history_template = ChatPromptTemplate.from_template(
    "你是一位历史学家，对历史事件和背景有一定研究。以下是问题内容{input}"
)

computerscience_template = ChatPromptTemplate.from_template(
    "你是一维计算机科学专家，擅长算法，数据结构和编程问题。以下是问题内容{input}"
)

default_template = ChatPromptTemplate.from_template(
    "输入内容无法归类，请直接回答：{input}"
)

default_chain = default_template | llm
physics_chain = physics_template | llm
math_chain = math_template | llm
history_chain = history_template | llm
computerscience_chain = computerscience_template | llm


def route(input):
    if '物理' in input['type']:
        print('1号')
        return {"key":'physics',"input":input["input"]}
    elif '数学' in input['type']:
        print('2号')
        return {"key":'math',"input":input["input"]}
    elif '历史' in input['type']:
        print('3号')
        return {"key":'history',"input":input["input"]}
    elif '计算机' in input['type']:
        print('4号')
        return {"key":'computer_science',"input":input["input"]}
    else:
        print('5号')
        return {"key":'default',"input":input["input"]}


route_runnable = RunnableLambda(route)

router = RouterRunnable(runnables={
    'physics':physics_chain,
    'math':math_chain,
    'history':history_chain,
    'computer_science':computerscience_chain,
    'default':default_chain,
})

first_prompt =ChatPromptTemplate.from_template(
    "不要回答下面用户的问题，只要根据用户的输入来判断分类，一共[物理，历史，计算机，数学，其他]五种类别。\n\n \n 用户的输入：{input}\n\n"
    "最后的输出包含分类的类别和用户输入的内容，输出格式为json，其中，类别的key为type，用户输入内容的key为input"

)

def print_llm_output(llm_result):
    print("=" * 50)
    print("原始输出内容】")
    print(llm_result)  # 打印 LLM 返回的完整消息
    print("=" * 50)
    return llm_result  # 必须返回，否则 chain 会断


#用于检查断点的输出
r1 = RunnableLambda(print_llm_output)

chain1 = first_prompt | r1 | llm | r1 | JsonOutputParser()

# chain2 = RunnableSequence(chain1,route_runnable,router,StrOutputParser())

chain2 = chain1 | route_runnable | router | StrOutputParser()
inputs = [
    {"input":"什么事黑体辐射"},
    {"input":"计算2加2的结果"},
    {"input":"介绍一次世界大战背景"},
    {"input":"如何实现快速排序算法"},

]

for inp in inputs:
    result = chain2.invoke(inp)
    print(f'问题{inp}\n{result}\n')
