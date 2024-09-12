import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from supabase import create_client, Client
from helper import diagnosis_draft

# Supabase 연결 설정
@st.cache_resource
def init_connection():
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
    return supabase

# Supabase 연결 설정
supabase = init_connection()

@st.cache_resource(ttl=600)
def run_related_query():
    doctor = supabase.table("doctor").select("*").execute()
    category = supabase.table("diagnosis_1st").select("*").execute()
    return doctor, category

def pick_patient_info(patient_info):
    name = patient_info["patient_name"]
    gender = patient_info["gender"]
    birthday = patient_info["birth_date"]
    age = datetime.now().year - birthday.year - ((datetime.now().month, datetime.now().day) < (birthday.month, birthday.day))
    eye = patient_info["surgery_eye"]
    cats = patient_info["category"]
    detail = patient_info["diagnosis"]

    msg = f"""환자의 정보는 다음과 같습니다.
    이름 : {name}, 성별 : {gender}, 나이 : {age}, 수술부위 : {eye}, 검사 결과 : {cats} / {detail}"""
    return msg


# 환자 정보 등록
def page_input():    
    st.write("# :male-doctor: 환자 정보 등록")
    st.sidebar.success("환자별 맞춤 안내를 제공합니다.")

    if 'patient_info' not in st.session_state:
        st.session_state['patient_info'] = None

    # 환자 등록이 완료된 경우, 등록된 정보를 보여준다.
    if st.session_state['patient_info']:
        colp_1, colp_2 = st.columns(2)
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
        with colp_2:
            st.markdown(df_patient_info.style.hide(axis="index").to_html(), unsafe_allow_html=True)
        
        # 야래쪽에는 등록된 정보에 기반하여, 상세 소견을 DB에서 검색하여 보여준다.
        res = supabase.table("diagnosis_2nd").select("explain").eq("name", st.session_state['patient_info']['diagnosis']).execute()
        explain = res.data[0]['explain']
        
        if explain == 'undefined':
            if 'explain' not in st.session_state['patient_info']:
                info = pick_patient_info(st.session_state['patient_info'])
                msg = {"role": "user", "content": info}
                explain = diagnosis_draft(msg)
                st.session_state['patient_info']['explain'] = explain
            else:
                explain = st.session_state['patient_info']['explain']

        with colp_1:
            st.markdown("**환자 상태에 관한 상세 소견**")
            st.markdown(explain)
        # st.text_area("**환자 상태에 관한 상세 소견**",
        #              explain, height=200)

        # 또다른 환자 정보를 등록할 때, 기존 정보를 리셋한다.
        if st.button("환자 정보 재등록"):
            reset_info()

    # 새로운 환자 정보를 등록한다.
    else:
        input_patient_info()

# 새로운 환자 정보 입력을 위한 리셋    
def reset_info():
        st.session_state['patient_info'] = None
        st.rerun()

# 환자 정보 등록 과정
def input_patient_info():
    
    doctors, categories = run_related_query()
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
