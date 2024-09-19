import streamlit as st
from helper import autoplay_audio
from page2 import supabase

def page_info():
    st.markdown(
    """
        ## 백내장 수술 정보
    """
    )

    tab_lst = ["**개요**", "정보1", "정보2", "정보3", "정보4", "정보5"]
    personalized = False
    if 'patient_info' in st.session_state:
        if st.session_state['patient_info'] != None:
            tab_lst.append(":red[환자별 맞춤 진단]")
            personalized = True
    
    tabs = st.tabs(tab_lst)

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
        st.markdown("### 백내장 수술 영상")
        st.markdown(
        """
        <div style="display: flex; justify-content: center;">
            <iframe src="https://drive.google.com/file/d/1DTmGn-RaQs9R7T3k1VfbPf1TiOQ0xki0/preview" 
                    style="width: 90%; height: auto; aspect-ratio: 16/9;" 
                    frameborder="0" allowfullscreen></iframe>
        </div>
        """,
        unsafe_allow_html=True)

    with tabs[1]:
        # st.subheader("백내장이란?")
        st.markdown(
    """
    ### Q. 백내장이란 무엇인가요?

    - 백내장이란 노화에 의해 ‘카메라의 렌즈에 해당하는 수정체’에 혼탁이 생기는 것입니다.
    - 40~50대 이상부터는 필연적으로 백내장이 생기게 되지만 모든 사람들이 수술을 바로 해야하는 것은 아니고, 백내장으로 인한 시력저하 등 불편감이 생길 때 수술을 고려하게 됩니다.
    - 예외적으로 굉장히 심한 백내장을 제외하고는 백내장의 정해진 수술시기는 없습니다. 
        + 즉 환자가 원하는 시기에 진행하면 됩니다. 
    - 백내장 수술은 다음과 같은 상황에서 고려하게 됩니다. 
    1) 객관적으로 백내장 진행정도가 심하거나
    2) 주관적으로 환자의 불편감이 심할때
    """)
        if st.button(f"▶️ 음성으로 듣기", key='info_1_1'):
            autoplay_audio('./ref/contents/info_1_1.mp3')

        st.markdown(
    """
    ### Q. 백내장은 어떻게 치료하나요?
    - 현재로서는 백내장을 치료할 수 있는 약제는 없습니다. 
    - 따라서 백내장은 반드시 수술적 치료를 해야하는 질환입니다. 
    - 백내장의 정도를 완화시켜주는 약제는 현재로서는 없지만, 
    진행속도를 조금 늦출 수 있는 것으로 알려진 약제 (안약) 은 존재합니다.
    """)
        if st.button(f"▶️ 음성으로 듣기", key='info_1_2'):
            autoplay_audio('./ref/contents/info_1_2.mp3')

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
    최근에는 수술장비의 발전으로 좁은 절개창을 통해 기구를 집어넣고 
    초음파를 통해 백내장을 부수어 잘게 쪼개고,
    작은 조각들을 흡입하여 제거하는 과정(=수정체유화술)으로 변화되었습니다.
    """)
        if st.button(f"▶️ 음성으로 듣기", key='info_2_1'):
            autoplay_audio('./ref/contents/info_2_1.mp3')
            
        st.markdown(
    """
    ### Q. 백내장 수술 소요시간은 어느 정도 되나요?
    - 평균적으로 약 20~30분 정도 소요되나, 난이도에 따라 더 오래 소요될 수 있습니다.
    """)
        if st.button(f"▶️ 음성으로 듣기", key='info_2_2'):
            autoplay_audio('./ref/contents/info_2_2.mp3')

        st.markdown(
    """
    ### Q. 백내장 수술 시 마취는 어떠한 방식으로 하나요?
    - 일반적으로 점안 마취 또는 국소마취로 진행됩니다.
    - 예외적으로 협조가 어려운 환자의 경우에는 전신마취로 진행하게 됩니다.
    """)
        if st.button(f"▶️ 음성으로 듣기", key='info_2_3'):
            autoplay_audio('./ref/contents/info_2_3.mp3')
        
    with tabs[3]:
        # st.subheader("수술 전 준비")
        st.markdown(
    """
    ### Q. 백내장 수술 입원은 며칠 동안 하나요?
    - 백내장 수술은 일일입원(당일 입원, 당일 퇴원)으로 진행됩니다.
    """)
        if st.button(f"▶️ 음성으로 듣기", key='info_3_1'):
            autoplay_audio('./ref/contents/info_3_1.mp3')
        
        st.markdown(
    """
    ### Q. 수술 당일에는 어떻게 준비해야 하나요?
    - 보통 수술 전날 오전에 내원시간 및 장소에 대한 안내가 유선으로 진행되기에, 전화를 잘 받아주시기 바랍니다. 안내 문자도 함께 보내드립니다.
    - 수술안이 충분히 산동되어야 잘 진행될 수 있기에, 보통 수술 1~2시간 전에 도착하여 산동제를 점안하게 됩니다.
    - 수술 이후에는 간호사의 설명을 들은 후에, 퇴원약이 준비되는 대로 바로 퇴원 가능합니다.
    """)
        if st.button(f"▶️ 음성으로 듣기", key='info_3_2'):
            autoplay_audio('./ref/contents/info_3_2.mp3')

        st.markdown(
    """
    ### Q. 백내장 수술 전에 복용하지 말아야 할 약제가 있을까요?
    - 일반적으로 피가 많이나는 수술은 아니기에 항혈소판제, 항응고제는 유지하며 수술합니다.
    - 수술 당일 아침까지 복용하셔도 됩니다.  
    - 전립선 약제를 복용하는 경우 동공확대를 저하시켜, 수술 난이도가 높아질 수 있습니다.
    - 다만 모든 약제는 수술전 주치의와 상의후 복용하셔야 합니다. 
    """)
        if st.button(f"▶️ 음성으로 듣기", key='info_3_3'):
            autoplay_audio('./ref/contents/info_3_3.mp3')


    with tabs[4]:
        # st.subheader("수술 후 회복")
        st.markdown(
    """
    ### Q. 백내장 수술 후에는 바로 잘 보이게 되나요?
    - 백내장 수술 후 1~2달 정도 뒤에 정확한 도수 및 시력이 나오게 됩니다.
    - 일반적으로 이 때, 안경검사를 진행하고 필요하면 돋보기를 처방하게 됩니다.
    - 수술 직후에는 각막 부종 등으로 오히려 시력이 떨어질 수 있습니다.
    - 망막질환, 녹내장 등 기저 안질환이 동반되어 있는 경우에는 시력 회복이 제한될 가능성이 있습니다.
    """)
        if st.button(f"▶️ 음성으로 듣기", key='info_4_1'):
            autoplay_audio('./ref/contents/info_4_1.mp3')

        st.markdown(
    """
    ### Q. 수술 후 주의해야 할 것에는 무엇이 있나요?
    - 수술 이후에는 다음과 같은 사항을 꼭 지켜주셔야 합니다.
        1) 눈 비비지 말 것
        2) 일주일 간 세수, 샤워하지 말 것
        3) 안약 잘 넣을 것
        4) 외상 조심할 것
        5) 감염징후(통증, 시력 저하, 심한 충혈)가 나타나면 바로 내원할 것
    """)
        if st.button(f"▶️ 음성으로 듣기", key='info_4_2'):
            autoplay_audio('./ref/contents/info_4_2.mp3')

        st.markdown(
    """

    ### Q. 백내장 수술 후에는 안약을 얼마나 사용하나요?
    - 일반적으로 수술 후에는 항생제, 항염증제 등 안약을 약 한달 간 사용하게 됩니다.
    - 다만, 필요에 따라서 안약을 추가하거나 더 오래 사용하게 될 수 있습니다.
    """)
        if st.button(f"▶️ 음성으로 듣기", key='info_4_3'):
            autoplay_audio('./ref/contents/info_4_3.mp3')
        
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
                "q": "2. **양쪽 눈을 동시에 수술이 가능한가요?**", 
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
    
    if personalized:
        with tabs[-1]:
            diag = st.session_state['patient_info']['diagnosis']
            patient_name = st.session_state['patient_info']['patient_name']
            # st.write(st.session_state['patient_info']['diagnosis'])
            st.subheader("종합 소견")
            if len(diag['전안부']) != 0:
                st.write(f"{patient_name}님은 백내장 수술의 위험성이 낮고, 합병증 발생 가능성이 높지 않은 상태입니다. 하지만 수술 후 건성안 증상이 악화될 수 있어 이에 대한 지속적인 관리가 필요합니다. 수술 시에는 불가항력적인 상황이 발생할 수 있으므로, 저희 세브란스 안과 병원 의료진은 {patient_name}님이 최고의 결과를 얻을 수 있도록 최선의 노력을 다하겠습니다."
                )
            elif len(diag["각막"]) or len(diag["전방"]) or len(diag["수정체"]) or len(diag["망막"]) or len(diag["시신경"]):
                st.write(f"{patient_name}님은 일반적인 경우와 비교하여 위험요인들을 추가로 가지고 있는 상태입니다. 저희 세브란스 안과 병원 의료진은 이러한 위험요인들을 충분히 숙지하고 준비하여, {patient_name}님이 최고의 결과를 얻을 수 있도록 최선의 노력을 다하겠습니다."
                )
            else:
                st.write(f"{patient_name}님은 백내장 수술의 위험성이 낮고, 합병증 발생 가능성이 높지 않은 상태입니다. 하지만 수술 시에는 불가항력적인 상황이 발생할 수 있으므로, 저희 세브란스 안과 병원 의료진은 {patient_name}님이 최고의 결과를 얻을 수 있도록 최선의 노력을 다하겠습니다.")

            st.write("---")
            st.write("#### 세부 내용")

            for cat, details in diag.items():
                if len(details) == 0:
                    continue
                with st.container(border=True):
                    st.write(f"**{cat} 이상**")
                    for detail in details:    
                        res = supabase.table("diagnosis").select("explain").eq("diag", detail).execute()
                        raw = res.data[0]['explain'].replace("{patient}", patient_name)
                        st.write(raw)
                        st.write("---")