import streamlit as st
import base64
from openai import OpenAI
from langsmith.wrappers import wrap_openai
from langsmith import traceable
import os
# from langchain_chroma import Chroma
# from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

os.environ["LANGCHAIN_TRACING_V2"] = st.secrets["LANGCHAIN_TRACING_V2"]
os.environ["LANGCHAIN_ENDPOINT"] = st.secrets["LANGCHAIN_ENDPOINT"]
os.environ["LANGCHAIN_PROJECT"] = st.secrets["LANGCHAIN_PROJECT"]
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]

# OpenAI 클라이언트
client = wrap_openai(OpenAI(api_key=st.secrets["OPENAI_API_KEY"]))
langchain_client = ChatOpenAI(model = "gpt-4o-mini", api_key=st.secrets["OPENAI_API_KEY"])

# 임베딩 모델 선언
openai_embedding_model = "text-embedding-3-small"
openai_embedding = OpenAIEmbeddings(model=openai_embedding_model, api_key=st.secrets["OPENAI_API_KEY"])

collection_name = "ocuguide_chromadb"
ocuguide_path = "./db/ocuguide_chromadb/"

# persist_db = Chroma(
#     persist_directory = ocuguide_path,
#     embedding_function=OpenAIEmbeddings(),
#     collection_name=collection_name
# )
# retriever = persist_db.as_retriever()

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
@traceable
def diagnosis_draft(msg):
    messages = [
        {"role": "system", 
         "content": 
         """당신은 백내장 수술 경험이 많은 안과 전문의 입니다.
         지금부터 환자의 최초 검진결과로부터 환자의 상태를 진단하고, 이에 대한 종합소견을 밝힙니다.
         최초 검진은 다음 여섯개의 항목으로 분류됩니다.
         #1.전안부 이상, #2.각막 이상, #3.전방 이상, #4. 수정체 이상, #5.망막 이상, #6.시신경 이상

         아래의 기준에 따라서 소견을 밝힐 수 있습니다.
         1) 어떤 항목도 검진되지 않았을 경우
         ### {환자이름}님께서는 백내장 수술의 위험성이 낮고, 합병증 발생 가능성이 높지 않은 상태입니다.

         2) "전안부 이상" 항목만 검진되었을 경우
         ### {환자이름}님께서는 백내장 수술의 위험성이 낮고, 합병증 발생 가능성이 높지 않은 상태입니다. 하지만 수술 후 건성안 증상이 악화될 수 있어 이에 대한 지속적인 관리가 필요합니다.

         3) 기타 항목이 검진되었을 경우
         ### {환자이름}님께서는 일반적인 경우와 비교하여 OOO의 위험요인(들)을 추가로 가지고 있는 상태입니다. 저희 세브란스 안과 병원 의료진은 이러한 위험요인(들)을 충분히 숙지하고 준비하겠습니다.

         지금부터 아래의 지시사항에 따라서, 답변을 생성합니다.
         #지시사항(instructions)
        1. 환자가 불안하지 않도록 친절하게 답변합니다.
        2. 위의 기준이 중복되었을 경우에는, 가장 위험도가 높은 상태를 기준으로 답변을 만듭니다.
        3. 답변의 맨 뒤에는 다음과 같은 문장을 덧붙입니다.
           ### 수술 시에는 불가항력적인 상황이 발생할 수 있지만, 저희 세브란스 안과 병원 의료진은 {환자이름}님께서 최고의 결과를 얻을 수 있도록 최선의 노력을 다하겠습니다. ###
        4. {환자이름}에는 함께 입력된 환자 이름을 사용합니다.
        5. 위의 기준 이외에 함께 제공된 나이와 수술 부위에 대한 당신의 생각을 덧붙여주세요.
        """}]

    messages.append(msg)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message.content
