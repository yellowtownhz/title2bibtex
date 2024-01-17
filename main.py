#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author             : ZhenHuang (muzhao.hz@alibaba-inc.com)
Date               : 2024-01-17 11:25
Last Modified By   : ZhenHuang (muzhao.hz@alibaba-inc.com)
Last Modified Date : 2024-01-17 12:18
Description        : 
-------- 
Copyright (c) 2024 Alibaba Inc. 
'''

import requests
import gradio as gr


def get_bibtext_from_title(title):
    # URL编码查询参数
    encoded_query = requests.utils.quote(title)
    print(f'query: {encoded_query}')
    # 假设API的endpoint为'https://api.example.com/search'
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={encoded_query}&offset=0&limit=3&fields=title,citationStyles"
    
    # 发送GET请求
    response = requests.get(url)
    
    # 检查请求是否成功
    if response.status_code == 200:
        # 如果请求成功，返回JSON格式的数据
        data = response.json()['data']
        bibtex = data[0]['citationStyles']['bibtex']
        return bibtex
    else:
        # 如果请求失败，打印错误信息
        print("Failed to retrieve data:", response.status_code)
        return None


def process_text(input_text):
    titles = input_text.split('\n')
    # 在这个例子中，我们仅仅将输入的文本原样返回。
    # 你可以在这个函数中加入任何你想要的文本处理逻辑。
    output = []
    for title in titles:
        if not title:
            continue
        bibtex = get_bibtext_from_title(title)
        if bibtex is not None:
            output.append(bibtex)
    return '\n'.join(output)

    return output

# 创建Gradio界面
iface = gr.Interface(
    fn=process_text,                 # 要调用的处理函数
    inputs=gr.Textbox(lines=10, placeholder="请在此输入论文标题..."),  # 输入组件：文本框，设置多行输入
    outputs=gr.Textbox(lines=20, placeholder="输出BibTex信息将会在此显示..."), # 输出组件：文本框，设置多行输出
)

# 启动界面
iface.launch()
