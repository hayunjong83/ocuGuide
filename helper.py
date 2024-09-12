import streamlit as st
import base64
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 음성 파일의 자동 재생
def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

# 환자 정보에 맞는 진단
def diagnosis_draft(msg):
    messages = [
        {"role": "system", 
         "content": 
         """당신은 백내장 수술 경험이 많은 안과 전문의 입니다.
         지금부터 당신은 환자의 등록정보를 기반으로,
         환자의 상태를 설명하고, 백내장 수술에서 주의해야 할 사항을 설명합니다.
        
        아래의 지시사항에 따라서, 답변을 생성합니다.
        #지시사항(instructions)
        1. 답변은 반드시 의학적 사실에 기반을 두어야하고, 근거가 없는 사실을 만들어내서는 안됩니다.
        2. 환자의 상태를 요약해서 설명하고, 수술 전에 주의해야 할 점을 함께 생성합니다.
        3. 답변은 정확하고 핵심이 분명하면서도, 환자들이 불안하지 않도록 친절하게 답변합니다.
        4. 우선, 당신만의 답변을 만들 후에, 일반인이 이해할 수 있는 수준으로 대답을 정리합니다. 이 때, 어려운 용어는 설명을 짧게 덧붙입니다.
        """}]

    messages.append(msg)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message.content