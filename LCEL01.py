import time

from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough
from langchain_core.tracers import Run


def test1(x:int):
    return x +10

def test2(prompt:str):
    for item in prompt.split(' '):
        yield item

# r1 = RunnableLambda(test2)
# res = r1.stream('This is a dog.')
#
# # print(res)
#
# for chunk in res:
#     print(chunk)
#


# r1 = RunnableLambda(test1)
# r2 = RunnableLambda(lambda x: x + 10)
# #并行操作
# chain = RunnableParallel(r1=r1, r2=r2)
# chain.get_graph().print_ascii()  # 画图
# print(chain.invoke(2,config={'max_concurrency':1}))




#合并输入 ，处理中间数据


# r1 = RunnableLambda(lambda x:{'key1':x})
# r2 = RunnableLambda(lambda x:x['key1']+10)
#
# chain = r1 | RunnableParallel(foo=RunnablePassthrough(),new_key=RunnablePassthrough.assign(key2 = r2))
#
# print(chain.invoke(2))
#
#
#
#
# chain1 = r1.with_fallbacks([r2])



def test4(n:int):
    time.sleep(n)
    return n*2


r1=RunnableLambda(test4)

def on_start(run_obj:Run):
    print('r1启动的时间',run_obj.start_time)


def on_stop(run_obj:Run):
    print('r1结束的时间：',run_obj.end_time)



chain = r1.with_listeners(on_start=on_start,on_end=on_stop)
print(chain.invoke(2))


