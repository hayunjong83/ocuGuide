import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from supabase import create_client, Client
from helper import diagnosis_draft, diagnosis_draft2

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
    return doctor

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

def pick_patient_info2(patient_info):
    name = patient_info["patient_name"]
    gender = patient_info["gender"]
    birthday = patient_info["birth_date"]
    age = datetime.now().year - birthday.year - ((datetime.now().month, datetime.now().day) < (birthday.month, birthday.day))
    eye = patient_info["surgery_eye"]
    diagnosis = patient_info["diagnosis"]

    msg = f"""환자의 정보는 다음과 같습니다.
    이름 : {name}, 성별 : {gender}, 나이 : {age}, 수술부위 : {eye}, 검사 결과 : {diagnosis}"""
    return msg

# 환자 정보 등록
def page_input():    
    st.write("# :male-doctor: 환자 정보 등록")
    st.sidebar.success("환자별 맞춤 안내를 제공합니다.")

    # 세션에 환자 정보 저장 키 여부 확인
    if 'patient_info' not in st.session_state:
        st.session_state['patient_info'] = None

    # 환자 등록이 완료된 경우, 등록된 정보를 보여준다.
    if st.session_state['patient_info']:
        # patient_data = {
        #     "항목": ["환자 번호", "이름", "성별", "생년월일", "주치의", "수술 부위", "수술 날짜", "수술 시간"],
        #     "정보": [
        #         st.session_state['patient_info']['patient_number'],
        #         st.session_state['patient_info']['patient_name'],
        #         st.session_state['patient_info']['gender'],
        #         st.session_state['patient_info']['birth_date'],
        #         st.session_state['patient_info']['primary_doctor'],
        #         st.session_state['patient_info']['surgery_eye'],
        #         st.session_state['patient_info']['surgery_date'],
        #         st.session_state['patient_info']['surgery_time'],
        #         # st.session_state['patient_info']['diagnosis']
        #     ]
        # }
        # df_patient_info = pd.DataFrame(patient_data)
        # st.markdown(df_patient_info.style.hide(axis="index").to_html(), unsafe_allow_html=True)

        info = st.session_state['patient_info']
        patient_data = {
            "환자번호 / 이름": [f"{info['patient_number']} / {info['patient_name']}"],
            "성별 / 생년월일": [f"{info['gender']} / {info['birth_date']}"],
            "주치의 / 수술부위": [f"{info['primary_doctor']} / {info['surgery_eye']}"],
            "수술날짜 / 수술 시간": [f"{info['surgery_date']} / {info['surgery_time']}"]
        }
        df_patient_info = pd.DataFrame(patient_data)
        st.markdown("### 등록된 환자정보")
        st.markdown(df_patient_info.style.hide(axis="index").to_html(), unsafe_allow_html=True)

        with st.container(border=True):
            st.write("#### 등록된 1차 소견")
            for k, v in info["diagnosis"].items():
                if len(v) != 0:
                    st.markdown(f"- {k}: {v}")

        with st.container(border=True):
            st.write("#### 검사 결과를 바탕으로 한 종합 소견")
            if 'explain' not in st.session_state["patient_info"]:
                st.session_state['patient_info']["explain"] = None
                picked_info = pick_patient_info2(info)
                msg = {"role": "user", "content": picked_info}
                with st.spinner('검사 결과를 바탕으로 진단을 내리는 중입니다...'):
                    explain = diagnosis_draft2(msg)
                st.session_state["patient_info"]["explain"] = explain
            else:
                explain = st.session_state["patient_info"]["explain"]
            
            explain = explain.replace("#","")
            st.write("**환자 상태에 관한 종합 소견**")
            st.write(explain)

        
            
        # 야래쪽에는 등록된 정보에 기반하여, 상세 소견을 DB에서 검색하여 보여준다.
        # res = supabase.table("diagnosis_2nd").select("explain").eq("name", st.session_state['patient_info']['diagnosis']).execute()
        # explain = res.data[0]['explain']
        
        # if explain == 'undefined':
        #     if 'explain' not in st.session_state['patient_info']:
        #         info = pick_patient_info(st.session_state['patient_info'])
        #         msg = {"role": "user", "content": info}
        #         explain = diagnosis_draft(msg)
        #         st.session_state['patient_info']['explain'] = explain
        #     else:
        #         explain = st.session_state['patient_info']['explain']

        # with colp_1:
        #     st.markdown("**환자 상태에 관한 상세 소견**")
        #     st.markdown(explain)
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
        # Chatbot history reset
        st.session_state['messages'] = None
        st.rerun()

# 환자 정보 등록 과정
def input_patient_info():

    # DB에 저장된 주치의 명을 가져온다.    
    doctors = run_related_query()
    df_docs = pd.DataFrame(doctors.data)
    docs_lst = df_docs['name'].tolist()
    docs_lst.insert(0, '<선택>')

    # 소견 분류 상세 내용
    categories = {1: '전안부', 2:'각막', 3:'전방', 4:'수정체', 5:'망막', 6:'시신경'}
    category_details = {
        '전안부': ["안검염(마이봄샘 기능장애 포함)", "건성안"], 
        '각막': ["내피세포 이상 1200개 미만", "내피세포 이상 1200~1500개", "각막혼탁","기타각막질환"], 
        '전방': ["얕은 전방", "산동 저하", "소대 이상", "급성폐쇄각녹내장", "거짓비늘증후군", "외상"],
        '수정체': ["심한 백내장(백색, 갈색, 후낭하혼탁 포함)", "안저검사 불가"],
        '망막': ["망막질환 (황반변성, 당뇨망막병증 등)"],
        '시신경': ["녹내장", "뇌병변으로 인한 시야장애"]}

    # 환자의 소견 정보 저장
    diagnosis = {}

    with st.container(border=True):
        st.subheader("환자의 소견 정보")
        # 분류 1 : '전안부': ["안검염(마이봄샘 기능장애 포함)", "건성안"]
        with st.container(border=True):
            cat1_title, cat1_cotent = st.columns([1, 5])
            with cat1_title:
                st.write("#### 전안부")
            selelcted_cats = []
            with cat1_cotent:
                cat1_1, cat1_2 = st.columns([2, 1])
                with cat1_1:
                    if st.checkbox("안검염(마이봄샘 기능장애 포함)", key=1_1):
                        selelcted_cats.append("안검염(마이봄샘 기능장애 포함)")
                with cat1_2:
                    if st.checkbox("건성안", key=1_2):
                        selelcted_cats.append("건성안")
            diagnosis["전안부"] = selelcted_cats

        # 분류 2 : '각막': ["내피세포 이상 1200개 미만", "1200~1500개", "각막혼탁","기타각막질환"],
        with st.container(border=True):
            cat2_title, cat2_cotent = st.columns([1, 5])
            with cat2_title:
                st.write("#### 각막")
            selelcted_cats = []
            with cat2_cotent:
                cat2_1, cat2_2 = st.columns([1, 1])
                with cat2_1:
                    if st.checkbox("내피세포 이상 1200개 미만", key=2_1):
                        selelcted_cats.append("내피세포 이상 1200개 미만")
                with cat2_2:
                    if st.checkbox("내피세포 이상 1200~1500개", key=2_2):
                        selelcted_cats.append("내피세포 이상 1200~1500개")
                cat2_1_u, cat2_2_u = st.columns([1, 1])
                with cat2_1_u:
                    if st.checkbox("각막혼탁", key=2_3):
                        selelcted_cats.append("각막혼탁")
                with cat2_2_u:
                    if st.checkbox("기타각막질환", key=2_4):
                        selelcted_cats.append("기타각막질환")
            diagnosis["각막"] = selelcted_cats
        # 분류 3 : '전방': ["얕은 전방", "산동 저하", "소대 이상", "급성폐쇄각녹내장", "거짓비늘증후군", "외상"]
        with st.container(border=True):
            cat3_title, cat3_cotent = st.columns([1, 5])
            with cat3_title:
                st.write("#### 전방")
            selelcted_cats = []
            with cat3_cotent:
                cat3_1, cat3_2, cat3_3 = st.columns([1, 1, 1])
                with cat3_1:
                    if st.checkbox("얕은 전방", key=3_1):
                        selelcted_cats.append("얕은 전방")
                with cat3_2:
                    if st.checkbox("산동 저하", key=3_2):
                        selelcted_cats.append("산동 저하")
                with cat3_3:
                    if st.checkbox("소대 이상", key=3_3):
                        selelcted_cats.append("소대 이상")
                cat3_1_u, cat3_2_u, cat3_3_u = st.columns([1, 1, 1])
                with cat3_1_u:
                    if st.checkbox("급성폐쇄각녹내장", key=3_4):
                        selelcted_cats.append("급성폐쇄각녹내장")
                with cat3_2_u:
                    if st.checkbox("거짓비늘증후군", key=3_5):
                        selelcted_cats.append("거짓비늘증후군")
                with cat3_3_u:
                    if st.checkbox("외상", key=3_6):
                        selelcted_cats.append("외상")
            diagnosis["전방"] = selelcted_cats
        # 분류 4 : '수정체': ["심한 백내장(백색, 갈색, 후낭하혼탁 포함)", "안저검사 불가"]
        with st.container(border=True):
            cat4_title, cat4_cotent = st.columns([1, 5])
            selelcted_cats = []
            with cat4_title:
                st.write("#### 수정체")
            with cat4_cotent:
                cat4_1, cat4_2 = st.columns([2, 1])
                with cat4_1:
                    if st.checkbox("심한 백내장(백색, 갈색, 후낭하혼탁 포함)", key=4_1):
                        selelcted_cats.append("심한 백내장(백색, 갈색, 후낭하혼탁 포함)")
                with cat4_2:
                    if st.checkbox("안저검사 불가", key=4_2):
                        selelcted_cats.append("안저검사 불가")
            diagnosis["수정체"] = selelcted_cats
        # 분류 5 : '망막': ["망막질환 (황반변성, 당뇨망막병증 등)"]
        with st.container(border=True):
            cat5_title, cat5_cotent = st.columns([1, 5])
            with cat5_title:
                st.write("#### 망막")
            selelcted_cats = []
            with cat5_cotent:
                if st.checkbox("망막질환(황반변성, 당뇨망막병증 등)", key=5_1):
                    selelcted_cats.append("망막질환(황반변성, 당뇨망막병증 등)")
            diagnosis["망막"] = selelcted_cats
        # 분류 6 :'시신경': ["녹내장", "뇌병변으로 인한 시야장애"]
        with st.container(border=True):
            cat6_title, cat6_cotent = st.columns([1, 5])
            with cat6_title:
                st.write("#### 시신경")
            selelcted_cats = []
            with cat6_cotent:
                cat6_1, cat6_2 = st.columns([1, 2])
                with cat6_1:
                    if st.checkbox("녹내장", key=6_1):
                        selelcted_cats.append("녹내장")
                with cat6_2:
                    if st.checkbox("뇌병변으로 인한 시야장애", key=6_2):
                        selelcted_cats.append("뇌병변으로 인한 시야장애")
            diagnosis["시신경"] = selelcted_cats

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
        col3_1, col3_2 = st.columns(2)
        with col3_1:
            primary_doctor = st.selectbox("주치의", docs_lst)

        # 6. 수술 눈 부위 선택 (좌안, 우안, 양안)
        with col3_2:
            surgery_eye = st.radio("수술 부위", ["좌안", "우안", "양안"], horizontal=True)

        # 7. 예정 수술 일자와 시간 선택
        col4_1, col4_2 = st.columns(2)
        with col4_1:
            surgery_date = st.date_input("수술 날짜")
        with col4_2:
            surgery_time = st.time_input("수술 시간", datetime.now().time())

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
                    'diagnosis' : diagnosis
                }
                st.success("환자 정보가 성공적으로 등록되었습니다.")
                st.rerun()

def reset_category_select():
    pass