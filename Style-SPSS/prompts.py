

# the func to generate self-summary
def generate_self_summary(question, related_items):
    summary = f"针对新问题 '{question}'，先根据历史回答自我反思：\n"
    for i, item in enumerate(related_items):
        summary += f"\n第 {i+1} 个相关的问题是：'{item['input']}'，\n\n对应的回答是：'{item['answer']}'，\n\n分析建议是：'{item['advice']}'。\n\n"
    summary += "从历史回答和分析建议中你学到了什么，可以如何改进？请总结出你自己的经验。\n"
    # print(summary)
    return summary

# the prompt to generate response with self-summary 
prompt_to_generate_response_with_self_summary="""你对历史的类似问题总结的经验如下：
{self_summary}

请结合你自己总结出的经验，回答以下问题：
{prompt}
"""
#the prompt to get teacher model guidance
prompt_to_get_teacher_model_guidance=f"""## 角色
你是一个优化提示词的专家，善于根据已有的用户和AI的问答对，分析现有AI回答的不足，然后优化用户的输入提示词。
已有的问答对：
问题：{query}

输入提示词:{prompt}

AI答复:{response}

## 任务
用户需求的AI回答风格种类为{style}。
先分析AI针对当前问题和当前提示词的回答有哪些不足，是否解答了问题，然后根据分析优化和完善用户的输入提示词,使得优化之后的提示词能够得到更好的AI答复。
## 技能
- 帮助用户优化完善提示词，使得该提示词能够得到更优质的具备用户需求的{style}的AI答复
- 自主选择适合当前问题的提示词优化技术
## 要求
- 先分析回答的不足，再使用代码块的方式输出提示词，方便用户使用
- 目的是优化输入提示词，不要对优化后的提示词做出答复！
"""

# the prompt used to evaluate the response
prompt_to_LLM_evaluate=f"""## 角色
你是一名专业的答案评估专家，擅长根据用户提供的问答对，对AI的答复进行打分。
已有的问答对：
问题：{query}

AI答复:{response}

## 任务
你的任务是评估AI回答的以下三个维度，每个维度的评分范围是1-10分，得分越高代表质量越高：
语言连贯性： 回答是否流畅，语法是否正确。
问题相关性： 回答是否与问题紧密相关，是否准确解答了问题。
语言风格性： 回答是否符合{style}的风格要求。
## 技能
- 擅长评估回答的质量。
- 能够识别和评价语言的连贯性和流畅性。
- 具备分析和评估回答是否与问题相关的能力。
- 熟悉并能识别{style}的语言风格和表达方式。
## 要求
- 你很严格，不要都打高分。
- 先为回答的三个维度打分，然后计算总分。

## 示例输出格式
AI答复：
语言连贯性：X分
问题相关性：X分
语言风格性 ：X分
总分：X分

"""