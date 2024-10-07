import streamlit as st
import streamlit_authenticator as stauth

# 페이지 설정
st.set_page_config(
    page_title="OcuGuide",
    page_icon=":clap:"
    )

from page1 import page_home
from page2 import page_input
from page3 import page_info
from page4 import page_w_chatgpt
from page5 import page_w_rag

# 로그인 페이지와 로그인 정보를 위한 인증 객체
def init_session():
    authenticator = stauth.Authenticate(
        st.secrets['credentials'].to_dict(),
        st.secrets['cookie']['name'],
        st.secrets['cookie']['key'],
        st.secrets['cookie']['expiry_days'],
        st.secrets['preauthorized']
    )

    return authenticator

def app():

    auth= init_session()
    name, authentication_status, username = auth.login('main')

    if st.session_state["authentication_status"]:
        
        st.sidebar.markdown("## :male-doctor:백내장의 모든 것:female-doctor: OcuGUIDE ##")
        st.sidebar.image("ref/side_logo.png")
        page = st.sidebar.selectbox(
            "원하시는 과정을 선택하세요", ["HOME", "👨‍⚕️ 환자정보 입력", "ℹ️ 백내장수술정보","❔ Q&A [챗GPT]", "❓ Q&A [OcuGuide]"])

        # Page content rendering based on selection
        if page == "HOME":
            page_home()
        elif page == "👨‍⚕️ 환자정보 입력":
            page_input()
        elif page == "ℹ️ 백내장수술정보":
            page_info()
        elif page == "❔ Q&A [챗GPT]":
            page_w_chatgpt()
        elif page == "❓ Q&A [OcuGuide]":
            page_w_rag()
        
        if 'speech_mode' not in st.session_state:
            st.session_state['speech_mode'] = True
        toggle_button = st.sidebar.toggle("음성모드", value=st.session_state['speech_mode'])
        st.session_state['speech_mode'] = toggle_button

        auth.logout('Logout', 'sidebar')

    elif st.session_state["authentication_status"] == False:
        st.error("Username/password is incorrect")
    elif st.session_state["authentication_status"] == None:
        st.warning("Please enter your username and password")

if __name__ == '__main__':
    app()
