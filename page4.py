import streamlit as st
from openai import OpenAI
from helper import client

def page_chatbot():
    st.title("Q&A 챗봇")

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"

    if "messages" not in st.session_state or st.session_state["messages"] == None:
        initial_messages = [
        {"role": "system", 
         "content": 
         """당신은 백내장 수술 경험이 많은 안과 전문의 입니다.
         지금부터 당신은 백내장 수술에 관한 환자의 질문에 대답합니다.
         이 때, 반드시 아래의 지시사항에 따라서 답변을 생성합니다.
         #지시사항(instructions)
         1. 답변은 반드시 의학적 사실에 기반을 두어야하고, 근거가 없는 사실을 만들어내서는 안됩니다.
         2. 답변은 정확하고 핵심이 분명하면서도, 환자들이 불안하지 않도록 친절하게 답변합니다.
         3. 우선, 당신만의 답변을 만들 후에, 일반인이 이해할 수 있는 수준으로 대답을 정리합니다. 이 때, 어려운 용어는 설명을 짧게 덧붙입니다.
         4. 백내장 수술이나 안과와 관련이 없는 질문에는 대답할 수 없다고 말합니다.
        """}]
        initial_messages.append({
            "role": "assistant",
            "content": "설명을 다시 듣고 싶은 내용이 있으시거나, 질문이 있으시면 말씀해주세요."
        })
        st.session_state.messages = initial_messages
    
    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("궁금한 사항을 물어봐주세요."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

