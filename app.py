import streamlit as st
import streamlit_authenticator as stauth
from datetime import datetime, timedelta
from supabase import create_client, Client
import pandas as pd
import base64

st.set_page_config(
    page_title="OcuGuide",
    page_icon=":clap:"
    )

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
    return supabase

supabase = init_connection()

@st.cache_resource(ttl=600)
def run_related_query():
    doctor = supabase.table("doctor").select("*").execute()
    category = supabase.table("diagnosis_1st").select("*").execute()
    diagnosis = supabase.table("diagnosis_2nd").select("*").execute()
    return doctor, category, diagnosis

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

def init_session():
    # declare Login-authenticator
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
    # Login and logout methods
    name, authentication_status, username = auth.login('main')

    if st.session_state["authentication_status"]:
        
        st.sidebar.markdown("## :male-doctor:백내장의 모든 것:female-doctor: OcuGUIDE ##")
        st.sidebar.image("ref/side_logo.png")
        page = st.sidebar.selectbox(
            "원하시는 과정을 선택하세요", ["HOME", "👨‍⚕️ 환자정보 입력", "ℹ️ 백내장수술정보", "❔ Q&A 챗봇"])

        # Page content rendering based on selection
        if page == "HOME":
            page_home()
        elif page == "👨‍⚕️ 환자정보 입력":
            page_input()
        elif page == "ℹ️ 백내장수술정보":
            page_info()
        elif page == "❔ Q&A 챗봇":
            page_chatbot()

        # Add logout button
        auth.logout('Logout', 'sidebar')
    elif st.session_state["authentication_status"] == False:
        st.error("Username/password is incorrect")
    elif st.session_state["authentication_status"] == None:
        st.warning("Please enter your username and password")

def page_home():
    
    st.write("# 세브란스 OcuGUIDE :eye-in-speech-bubble:")

    st.sidebar.success("필요한 단계를 위에서 선택하세요.")

    st.markdown(
        """
        세브란스 안과병원의 **OcuGuide**에서는 백내장에 관한 정보와 수술을 환자분들께 안내합니다.
        현재 페이지는 *OcuGuide*를 위한 테스트 페이지로서,
        **환자 정보 입력**, **백내장 수술 정보 안내**, **Q&A 챗봇** 등의 기능을 수행합니다.
        **👈 좌측 메뉴에서 원하는 기능을 선택하여** 진행하십시오.
        
        ### 현재 제공 기능 설명
        - 👨‍⚕️ **환자정보 등록** : 환자의 백내장 수슬 전 검사 결과를 등록합니다.
        - ℹ️ **백내장수술 정보** : 수술 전 환자에게 안내할 백내장 관련 정보
        - ❔ **Q&A 챗봇** : 수술 전 동의를 받기 전에, 환자의 질문에 응대하는 LLM 챗봇

        ### 구현 예정 기능
        - ✔️ **환자의 질문-응답 요약** : 주치의가 확인할 수 있느 환자의 질문 요약 및 검토
        - ❕ **Q&A 통계** : 환자가 자주 물어본 질문과 정보에 대한 통계 제공
    """
    )

def page_input():    
    st.write("# :male-doctor: 환자 정보 등록")
    st.sidebar.success("환자별 맞춤 안내를 제공합니다.")

    if 'patient_info' not in st.session_state:
        st.session_state['patient_info'] = None

    if st.session_state['patient_info']:

        patient_data = {
            "항목": ["환자 번호", "이름", "성별", "생년월일", "주치의", "수술 부위", "수술 날짜", "수술 시간", "1차 소견", "2차소견"],
            "정보": [
                st.session_state['patient_info']['patient_number'],
                st.session_state['patient_info']['patient_name'],
                st.session_state['patient_info']['gender'],
                st.session_state['patient_info']['birth_date'],
                st.session_state['patient_info']['primary_doctor'],
                st.session_state['patient_info']['surgery_eye'],
                st.session_state['patient_info']['surgery_date'],
                st.session_state['patient_info']['surgery_time'],
                st.session_state['patient_info']['category'],
                st.session_state['patient_info']['diagnosis']
            ]
        }
        df_patient_info = pd.DataFrame(patient_data)
        st.markdown(df_patient_info.style.hide(axis="index").to_html(), unsafe_allow_html=True)
        # st.table(patient_data)
        res = supabase.table("diagnosis_2nd").select("explain").eq("name", st.session_state['patient_info']['diagnosis']).execute()
        explain = res.data[0]['explain']
        st.text_area("**환자 상태에 관한 상세 소견**",
                     explain, height=200)

        # 리셋 버튼
        if st.button("환자 정보 재등록"):
            reset_info()

    else:
        input_patient_info()
    
    
def reset_info():
        st.session_state['patient_info'] = None
        st.rerun()

def input_patient_info():
    
    # 임시로 필요한 전처리 수행
    doctors, categories, _ = run_related_query()
    df_docs = pd.DataFrame(doctors.data)
    docs_lst = df_docs['name'].tolist()
    docs_lst.insert(0, '<선택>')

    df_cats = pd.DataFrame(categories.data)
    cats_lst = df_cats['name'].tolist()
    cats_lst.insert(0, '<카테고리 선택>')

    def update_details():
        if 'category' in st.session_state:
            category = st.session_state['category']
            cat_idx = cats_lst.index(category)-1
            if cat_idx == -1:
                st.session_state['diagnosis'] = []
            else:
                response = supabase.table("diagnosis_2nd").select("id", "name").eq("category", (cat_idx)).execute()
                st.session_state['diagnosis'] = [item['name'] for item in response.data]
        else:
            st.session_state['category'] = "<카테고리 선택>"

    _ = st.selectbox("1차 소견", cats_lst, key='category', on_change=update_details)

    with st.form("환자 정보 입력"):
        # 1. 환자번호 입력 (7자리 숫자)
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            patient_number = st.text_input("환자번호(7자리)", max_chars=7)

        # 2. 환자 이름 입력
        with col1_2:
            patient_name = st.text_input("환자 이름")

        col2_1, col2_2 = st.columns(2)
        # 3. 성별 선택 (라디오버튼)
        with col2_1:
            gender = st.radio("성별", ("남성", "여성", "기타"), horizontal=True)
        
        with col2_2:
            # 4. 생일 선택
            birth_date = st.date_input("생년월일",
                                    value=datetime(2000, 1, 1),
                                        min_value=datetime(1924, 1, 1),
                                        max_value=datetime.today())

        # 5. 주치의 선택
        primary_doctor = st.selectbox("주치의", docs_lst)

        # 6. 수술 눈 부위 선택 (좌안, 우안, 양안)
        surgery_eye = st.radio("수술 부위", ["좌안", "우안", "양안"])

        # 7. 예정 수술 일자와 시간 선택
        col3_1, col3_2 = st.columns(2)
        with col3_1:
            surgery_date = st.date_input("수술 날짜")
        with col3_2:
            surgery_time = st.time_input("수술 시간", datetime.now().time())

        if 'diagnosis' in st.session_state and st.session_state['diagnosis']:
            diagnosis = st.selectbox("2차 소견", st.session_state['diagnosis'])

        # 폼 제출 버튼
        submitted = st.form_submit_button("환자 정보 등록")
                # 유효성 검사
        if submitted:
            error_messages = []

            # 환자번호가 7자리 숫자인지 확인
            if not patient_number.isdigit() or len(patient_number) != 7:
                error_messages.append("환자번호는 숫자만 포함되어야 합니다.")

            # 빈 필드가 있는지 확인
            if not patient_name:
                error_messages.append("환자 이름을 입력해주세요.")
            if not gender:
                error_messages.append("성별을 입력해주세요.")
            if not birth_date:
                error_messages.append("생일을 입력해주세요.")
            if not primary_doctor or primary_doctor == "<선택>":
                error_messages.append("주치의를 입력해주세요.")
            if not surgery_eye:
                error_messages.append("수술 부위를 선택해주세요.")
            if not surgery_date:
                error_messages.append("수술 날짜를 선택해주세요.")
            if not surgery_time:
                error_messages.append("수술 시간을 선택해주세요.")

            # 오류 메시지가 있으면 표시
            if error_messages:
                for error in error_messages:
                    st.error(error)
            else:
                # 유효성 검사를 통과한 경우 세션에 정보 저장
                st.session_state['patient_info'] = {
                    'patient_number': patient_number,
                    'patient_name': patient_name,
                    'gender': gender,
                    'birth_date': birth_date,
                    'primary_doctor': primary_doctor,
                    'surgery_eye': surgery_eye,
                    'surgery_date': surgery_date,
                    'surgery_time': surgery_time,
                    'category': st.session_state['category'],
                    'diagnosis' : diagnosis
                }
                st.success("환자 정보가 성공적으로 등록되었습니다.")
                st.rerun()

def page_info():
    st.markdown(
    """
        ## 백내장 수술 정보
    """
    )

    tabs = st.tabs([":blue[**개요**]",
                    "정보1", "정보2", "정보3", "정보4", "정보5"])

    with tabs[0]:
        # st.subheader("정보 개요")
        st.markdown(
    """
    여기에서는 백내장 수술에 관하여 환자분들께서 가장 궁금해하고, 꼭 알아야 할 정보를 제공합니다.
    수술 과정부터 회복, 주의사항까지 핵심적인 내용을 담아 환자분들께서 수술 전 안심하고 준비할 수 있도록 돕겠습니다. 

    이 곳에서 확인하실 수 있는 내용은 차례로 다음과 같습니다.
    - 정보1) **백내장이란?** : 백내장의 증상,원인과 치료 방법 설명
    - 정보2) **백내장 수술과정** : 백내장 수술의 진행 과정과 안정성
    - 정보3) **수술 전 준비** : 백내장 수술 전 알아야 할 사항과 준비 방법
    - 정보4) **수술 후 회복** : 백내장 수술 회복 과정과 주의해야 할 사항
    - 정보5) **자주 묻는 질문** : 환자분들께서 자주 알아야할 질문과 그에 대한 답변

    백내장은 환자 분들의 눈 건강을 위한 안전하고 효율적인 치료법입니다. 
    세브란스 안과병원의 모든 의료진은 이를 위해 최선의 노력을 다하고 있습니다.
    이 페이지를 통해 백내장에 관한 궁금증을 해결하시고, 안심하고 수술을 준비하십시오.

    - 추가적인 질문이 있으신 경우에는 :red[ :question: Q&A 챗봇]을 통하여 간단하게 알아보세요.
    - 언제든 주치의 선생님을 통하여, 더 상세하고 친절한 설명을 받으실 수 있습니다.

    """)

    with tabs[1]:
        # st.subheader("백내장이란?")
        st.markdown(
    """
    ### Q. 백내장이란 무엇인가요?

    - 백내장이란 노화에 의해 ‘카메라의 렌즈에 해당하는 수정체’에 혼탁이 생기는 것입니다.
    - 40~50대 이상부터는 필연적으로 백내장이 생기게 되지만 모든 사람들이 수술을 바로 해야하는 것은 아니고, 백내장으로 인한 시력저하 등 불편감이 생길 때 수술을 고려하게 됩니다.
    - 예외적으로 드문 굉장히 심한 백내장을 제외하고는 백내장의 정해진 수술시기는 없습니다. 
        + 즉 환자가 원하는 시기에 진행하면 됩니다. 
    - 백내장 수술은 다음과 같은 상황에서 고려하게 됩니다. 
    1) 객관적으로 백내장 진행정도가 심하거나
    2) 주관적으로 환자의 불편감이 심할때  

    ### Q. 백내장은 어떻게 치료하나요?
    - 현재로서는 백내장을 치료할 수 있는 약제는 없습니다. 
    - 따라서 백내장은 반드시 수술적 치료를 해야하는 질환입니다. 
    - 백내장의 정도를 완화시켜주는 약제는 현재로서는 없지만, 
    진행속도를 조금 늦출 수 있는 것으로 알려진 약제 (안약) 은 존재합니다.
    """)

    with tabs[2]:
        # st.subheader("백내장 수술 과정")
        st.markdown(
    """
    ### Q. 백내장 수술은 어떻게 진행되나요?
    - 백내장 수술은 다음과 같은 2가지 과정으로 이루어집니다. 
        1) 혼탁해진 백내장을 제거하고 (Phacoemulsification)
        2) 수정체 역할을 대신할 인공수정체(=렌즈)를 넣는 것 (IOL implantation)

    - 일반인들은 백내장 수술이 렌즈를 넣는 수술이라는 사실을 잘 모르지만, 
    반드시 렌즈를 넣는 과정까지가 백내장 수술이라고 이해하시면 되겠습니다.

    - 과거에는 넓은 절개창을 통해 수정체 자체를 통으로 밖으로 꺼냈다면,
    최근에는 수술장비의 발전으로 좁은 절개창을 통해 기구를 집어넣어 
    초음파를 통해 백내장을 부수어 잘게 쪼개고,
    작은 조각들을 흡입하여 제거하는 과정(=수정체유화술)으로 변화되었습니다.

    ### Q. 백내장 수술 소요시간은 어느 정도 되나요?
    - 평균적으로 약 20~30분 정도 소요되나, 난이도에 따라 더 오래 소요될 수 있습니다.

    ### Q. 백내장 수술 시 마취는 어떠한 방식으로 하나요?
    - 일반적으로 점안 마취 또는 국소마취로 진행됩니다.
    - 예외적으로 협조가 어려운 환자의 경우에는 전신마취로 진행하게 됩니다.
    """)
        
    with tabs[3]:
        # st.subheader("수술 전 준비")
        st.markdown(
    """
    ### Q. 백내장 수술 입원은 며칠 동안 하나요?
    - 백내장 수술은 일일입원(당일 입원, 당일 퇴원)으로 진행됩니다.

    ### Q. 수술 당일에는 어떻게 준비해야 하나요?
    - 보통 수술 전날 오전에 내원시간 및 장소에 대한 안내가 유선으로 진행되기에, 전화를 잘 받아주시기 바랍니다. 안내 문자도 함께 보내드립니다.
    - 수술안이 충분히 산동되어야 잘 진행될 수 있기에, 보통 수술 1~2시간 전에 도착하여 산동제를 점안하게 됩니다.
    - 수술 이후에는 간호사의 설명을 들은 후에, 퇴원약이 준비되는 대로 바로 퇴원 가능합니다.

    ### Q. 백내장 수술 전에 복용하지 말아야 할 약제가 있을까요?
    - 일반적으로 피가 많이나는 수술은 아니기에 항혈소판제, 항응고제는 유지하며 수술합니다.
    - 수술 당일 아침까지 복용하셔도 됩니다.  
    - 전립선 약제를 복용하는 경우 동공확대를 저하시켜, 수술 난이도가 높아질 수 있습니다.
    - 다만 모든 약제는 수술전 주치의와 상의후 복용하셔야 합니다. 
    """)

    with tabs[4]:
        # st.subheader("수술 후 회복")
        st.markdown(
    """
    ### Q. 백내장 수술 후에는 바로 잘 보이게 되나요?
    - 백내장 수술 후 1~2달 정도 뒤에 정확한 도수 및 시력이 나오게 됩니다.
    - 일반적으로 이 때, 안경검사를 진행하고 필요하면 돋보기를 처방하게 됩니다.
    - 수술 직후에는 각막 부종 등으로 오히려 시력이 떨어질 수 있습니다.
    - 망막질환, 녹내장 등 기저 안질환이 동반되어 있는 경우에는 시력 회복이 제한될 가능성이 있습니다.

    ### Q. 수술 후 주의해야 할 것에는 무엇이 있나요?
    - 수술 이후에는 다음과 같은 사항을 꼭 지켜주셔야 합니다.
        1) 눈 비비지 말 것
        2) 일주일 간 세수, 샤워하지 말 것
        3) 안약 잘 넣을 것
        4) 외상 조심할 것
        5) 감염징후(통증, 시력 저하, 심한 충혈)가 나타나면 바로 내원할 것

    ### Q. 백내장 수술 후에는 안약을 얼마나 사용하나요?
    - 일반적으로 수술 후에는 항생제, 항염증제 등 안약을 약 한달 간 사용하게 됩니다.
    - 다만, 필요에 따라서 안약을 추가하거나 더 오래 사용하게 될 수 있습니다.
    """)
        
    with tabs[5]:
        # st.subheader("자주 묻는 질문들")
        faqs = [
            {
                "q": "1. **백내장 수술 이후 일상생활은 언제부터 가능한가요?**", 
                "a": """ 
                - 백내장 수술 당일부터 일상 생활은 가능합니다.
                - 다만, 세수와 샤워는 일주일 뒤부터 가능합니다.
                - 식사에도 제약은 없습니다.""",
                "p": "./ref/contents/info_5_1.mp3"},
            {
                "q": "2. 양쪽 눈을 동시에 수술이 가능한가요?", 
                "a": """ 
                - 일반적으로 한 눈씩 진행하지만, 원하면 한 번에 양안 수술이 가능하기도 합니다.
                - 그러나 대부분은 한쪽 눈 수술 경과를 보며 반대쪽 눈 수술을 결정하게 됩니다.
                - 다만, 전신마취로 하는 경우에는 양안을 동시에 수술하게 됩니다.""",
                "p": "./ref/contents/info_5_2.mp3"}
            ]
        
        for faq in faqs:
            with st.expander(faq["q"]):
                st.write(faq["a"])
                if st.button(f"▶️ 음성으로 듣기", key=faq["q"]):
                    autoplay_audio(faq['p'])

def page_chatbot():
    st.title("Q&A 챗봇")

if __name__ == '__main__':
    app()
