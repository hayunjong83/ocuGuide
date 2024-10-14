import streamlit as st
from openai import OpenAI
from helper import client, text_to_speech, speech_to_text
from langsmith import traceable
from audio_recorder_streamlit import audio_recorder
import random
import os

@traceable
def page_w_chatgpt():
    st.title("❔ Q&A 챗봇 [챗GPT]")

    with st.container(border=True):
        c1, c2 = st.columns([7, 1])
        with c1:
            st.write("""
                    - :blue[**OcuGUIDE**]에서 궁금했던 내용을 무엇이든 물어보세요.
                    - ℹ️ 백내장수술정보에서 어려웠던 내용을 챗봇이 성심껏 답변드립니다.
                    - 오른쪽의 마이크를 누르면, 음성으로 질문할 수 있습니다.
                    - 질문이 끝나신 후, 이제 곧 만나실 주치의에게 추가 설명을 들을 수 있습니다.
                    """)
        with c2:
            audio_bytes = audio_recorder(text="음성모드", neutral_color="#6aa36f", icon_size="3x")
        # st.write("- :blue[**OcuGUIDE**]에서 궁금했던 내용을 무엇이든 물어보세요.  \n")
        # st.write("- 이해가 어려웠거나, 다시 듣고 싶으신 내용을 챗GPT 에이전트가 성심껏 답변드립니다.  \n")
        # st.write("- 질문이 끝나신 후, 이제 곧 만나실 주치의에게 추가 질문과 설명을 들을 수 있습니다.")
    
    # with st.container(border=True):
    #     speak, listen = st.columns([1, 1])
    #     with speak:
    #         st.write("### 음성 도움 안내 ###")
    #     audio_bytes = audio_recorder()

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
            "content": "안녕하세요. 백내장의 모든것 OcuGUIDE 입니다."
        })
        st.session_state.messages = initial_messages
    
    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # st.markdown("""
    # <style>
    # .fixed-container {
    #     position: fixed;
    #     bottom: -100px;  /* chat_input 바로 위에 고정될 위치 설정 */
    #     left: 0;
    #     width: 100%;
    #     background-color: white;
    #     padding: 10px;
    #     z-index: 9999;
    #     text-align: center;
    # }   
    # </style>
    # """, unsafe_allow_html=True)
    
    # st.markdown('<div class="fixed-container">', unsafe_allow_html=True)
    # with st.container(border=True):
    #     explain, speak, listen = st.columns([4,1,1])
    #     with explain:
    #         st.write("음성 도움 안내입니다.")
    #         st.write("마이크를 눌러서 질문 후, 다시 눌러서 질문을 종료합니다.")
    #     with speak:
    #         audio_bytes = audio_recorder("말하기", key="before")
    #     with listen:
    #         on_before = st.toggle("듣기", key="toggle_before")
    # st.markdown('</div>', unsafe_allow_html=True)
    
    if audio_bytes:
        with st.spinner("Transcribing..."):
            rand_idx = random.randint(10000, 99999)
            webm_file_path = f"temp_{str(rand_idx)}.mp3"
            with open(webm_file_path, "wb") as f:
                f.write(audio_bytes)
            
            transcript = speech_to_text(webm_file_path)
            st.session_state.messages.append({"role": "user", "content": transcript})

            if transcript:
                with st.chat_message("user"):
                    st.markdown(transcript)
                os.remove(webm_file_path)

            
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
        # #     # 고정된 위치에 container
        # # st.markdown('<div class="fixed-container">', unsafe_allow_html=True)
        # # with st.container(border=True):
        # #     st.write("This is a container fixed above the chat input.")
        # #     st.write("This is a container fixed above the chat input.")
        # # st.markdown('</div>', unsafe_allow_html=True)    
        # st.markdown('<div class="fixed-container">', unsafe_allow_html=True)
        # with st.container(border=True):
        #     explain, speak, listen = st.columns([4,1,1])
        #     with explain:
        #         st.write("음성 도움 안내입니다.")
        #         st.write("마이크를 눌러서 질문 후, 다시 눌러서 질문을 종료합니다.")
        #     with speak:
        #         audio_bytes = audio_recorder("말하기", key="after")
        #     with listen:
        #         on_after = st.toggle("듣기", key="toggle_after")
        # st.markdown('</div>', unsafe_allow_html=True)

        
