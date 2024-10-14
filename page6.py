import streamlit as st
import pandas as pd
from page2 import style_dataframe

def statistics():
    st.title("✨ OcuGUIDE 사용내역")

    st.subheader("현재 OcuGUIDE 접속 환자 정보")

    if 'patient_info' not in st.session_state:
        st.warning("👨‍⚕️ 환자정보 입력에서 환자 정보를 먼저 등록해주세요.")
    elif st.session_state['patient_info'] == None:
        st.warning("👨‍⚕️ 환자정보 입력에서 환자 정보를 먼저 등록해주세요.")
    else:
        info = st.session_state['patient_info']
        patient_personal_data = {
            "환자번호": [f"{info['patient_number']}"],
            "이름": [f"{info['patient_name']}"],
            
            "성별": [f"{info['gender']}"],
            "생년월일": [f"{info['birth_date']}"],
            "나이": [f"{info['age']}"]
        }
        patient_operation_data = {
            "주치의": [f"{info['primary_doctor']}"],
            "수술부위": [f"{info['surgery_eye']}"],
            
            "수술날짜": [f"{info['surgery_date']}"],
            "수술 시간": [f"{info['surgery_time']}"]
        }
        df_patient_personal = style_dataframe(pd.DataFrame(patient_personal_data), '#F5F5DC')
        df_patient_operation = style_dataframe(pd.DataFrame(patient_operation_data), '#FAEBD7')
        
        st.markdown("### 등록된 환자정보")
        st.markdown(df_patient_personal.to_html(), unsafe_allow_html=True)
        st.markdown(df_patient_operation.to_html(), unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("ℹ️ 백내장수술정보 진행 단계")
    if 'patient_info' not in st.session_state:
        st.warning("👨‍⚕️ 환자정보 입력에서 환자 정보를 먼저 등록해주세요.")
    elif st.session_state['patient_info'] == None:
        st.warning("👨‍⚕️ 환자정보 입력에서 환자 정보를 먼저 등록해주세요.")
    else:
        if 'progress' not in st.session_state:
            st.warning("ℹ️ 백내장수술정보에서 필요한 정보 확인을 시작하세요.")
        else:
            progress = st.session_state["progress"]
            if progress < 6:
                st.info(f"현재 {progress}까지 정보를 확인하였습니다.")
            else:
                st.success("모든 백내장수술정보를 확인하였습니다.")

            st.write(st.session_state['stay'])