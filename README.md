# LangChain Expression Language (LCEL) 语法测试项目

本项目是学习 LangChain Expression Language (LCEL) 的实践代码集合，通过多个案例演示了 LCEL 的核心概念和用法。

## 什么是 LCEL

LCEL (LangChain Expression Language) 是 LangChain 提供的一种声明式语法，用于组合不同的组件（如提示词模板、LLM、输出解析器等）构建复杂的 AI 处理链。它使用管道操作符 `|` 将各个组件串联起来，使代码更加简洁易读。

## 项目结构

```
.
├── LCEL01.py           # LCEL 基础语法演示
├── LCEL案例.py          # 链式调用基础案例
├── LCEL案例2.py         # 多步骤餐厅推荐链
├── LCEL案例3.py         # 智能路由分类系统
├── .env                # 环境变量配置文件（已忽略）
└── .gitignore          # Git 忽略文件配置
```

## 环境配置

1. 安装依赖：
```bash
pip install langchain langchain-openai python-dotenv
```

2. 配置环境变量：
创建 `.env` 文件并添加以下配置：
```
MODEL=your-model-name
API_KEY=your-api-key
API_BASE=your-api-base-url
```

## 案例详解

### 1. LCEL01.py - 基础语法演示

展示了 LCEL 的核心组件和用法：

- **RunnableLambda**: 将普通函数包装为可运行的组件
- **RunnableParallel**: 并行执行多个任务
- **RunnablePassthrough**: 透传数据，用于合并输入和处理中间数据
- **with_listeners**: 添加生命周期监听器（启动/结束回调）
- **流式输出**: 使用 `stream()` 方法实现逐字输出

### 2. LCEL案例.py - 链式调用基础

演示了如何将多个步骤串联成一个完整的处理链：

**场景**: 根据关键词生成短文，然后对短文进行评分

**流程**:
```
提示词1 → LLM → 文本输出 → 提示词2 → LLM → 评分结果
```

**关键技术点**:
- 使用 `StrOutputParser()` 解析 LLM 输出为字符串
- 通过字典传递中间结果到下一个提示词
- 使用 `RunnableLambda` 插入自定义处理逻辑

### 3. LCEL案例2.py - 多步骤餐厅推荐

展示了更复杂的多步骤链式处理：

**场景**: 根据用户偏好推荐餐厅

**流程**:
```
收集偏好 → 总结需求 → 推荐餐厅 → 总结推荐理由
```

**特点**:
- 多个提示词模板串联
- 每一步的输出作为下一步的输入
- 最终输出简洁的推荐总结

### 4. LCEL案例3.py - 智能路由分类系统

实现了一个根据问题类型自动路由到不同专家链的系统：

**场景**: 自动识别问题类型并分配给对应的专家回答

**支持的分类**:
- 物理 → 物理教授链
- 数学 → 数学家链
- 历史 → 历史学家链
- 计算机 → 计算机科学专家链
- 其他 → 默认链

**关键技术点**:
- 使用 `RouterRunnable` 实现动态路由
- 结合 `JsonOutputParser` 解析分类结果
- 使用 `RunnableLambda` 自定义路由逻辑
- 通过 `RunnableSequence` 组合多个链

## LCEL 核心概念

### 管道操作符 `|`

LCEL 使用管道操作符将组件串联：
```python
chain = prompt | llm | output_parser
```

### 常用组件

| 组件 | 说明 |
|------|------|
| `RunnableLambda` | 包装普通函数为可运行组件 |
| `RunnableParallel` | 并行执行多个组件 |
| `RunnablePassthrough` | 透传或合并数据 |
| `RouterRunnable` | 根据条件路由到不同组件 |
| `StrOutputParser` | 将输出解析为字符串 |
| `JsonOutputParser` | 将输出解析为 JSON |

### 链的执行方式

```python
# 同步调用
result = chain.invoke(input_data)

# 流式输出
for chunk in chain.stream(input_data):
    print(chunk)

# 批量处理
results = chain.batch([input1, input2, input3])
```

## 学习建议

1. 从 `LCEL01.py` 开始，理解基础组件的用法
2. 逐步阅读案例，理解链的组合方式
3. 尝试修改提示词和参数，观察输出变化
4. 参考 [LangChain 官方文档](https://python.langchain.com/docs/expression_language/) 深入学习

## 注意事项

- 确保 `.env` 文件中的 API 密钥正确配置
- `.env` 文件已添加到 `.gitignore`，不会提交到版本控制
- 运行前请确认已安装所有依赖包
-------
