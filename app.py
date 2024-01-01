import os
from apikey import apikey

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory

os.environ['OPENAI_API_KEY'] = apikey

st.title ('AutoGPT from YouTube Tutorials')

prompt = st.text_input ('Type your prompt here')

title_template = PromptTemplate(
    input_variables = ['topic'],
    template = 'Write me a youtube video title about {topic}'
)

script_template = PromptTemplate(
    input_variables = ['title'],
    template = 'Write me a youtube video script based on this title: {title}'
)

title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
script_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')


llm = OpenAI(temperature=0.2)
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title', memory=title_memory)
script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True, output_key='script', memory=script_memory)
# sequential_chain = SequentialChain(chains=[title_chain, script_chain], input_variables=['topic'], output_variables=['title', 'script'], verbose=True)



if prompt:
    title = title_chain.run(prompt)
    script = script_chain.run(title)

    st.write(title)
    st.write(script)

    with st.expander('Title History'):
        st.info(title_memory.buffer)

    with st.expander('Script History'):
        st.info(script_memory.buffer)