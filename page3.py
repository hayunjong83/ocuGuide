import streamlit as st
from helper import autoplay_audio, stop_audio, stream_partial_data
from page2 import supabase
import time

def set_form_step(action,step=None):
    if action == 'Next':
        st.session_state['current_step'] = st.session_state['current_step'] + 1
    if action == 'Back':
        st.session_state['current_step'] = st.session_state['current_step'] - 1
    if action == 'Jump':
        st.session_state['current_step'] = step

def page_info():
    # 페이지 제목
    st.markdown(
    """
        ## 백내장 수술 정보
    """
    )

    if 'current_step' not in st.session_state:
        st.session_state['current_step'] = 0
    if 'progress' not in st.session_state:
        st.session_state['progress'] = 0

    # # 단계 제목
    # step0 = "정보 안내"
    # step1 = "단계 1 🔒" if "step_1" not in st.session_state else "단계 1"
    # step2 = "단계 2 🔒" if "step_2" not in st.session_state else "단계 2"
    # step3 = "단계 3 🔒" if "step_3" not in st.session_state else "단계 3"
    # step4 = "단계 4 🔒" if "step_4" not in st.session_state else "단계 4"
    # step5 = "단계 5 🔒" if "step_5" not in st.session_state else "단계 5"
    # step6 = ":red[환자별 정보] 🔒" if "step_6" not in st.session_state else ":red[환자별 정보]"
    # # tab_lst = [step0, step1, step2, step3, step4, step5]
    # info_lst = [step0, step1, step2, step3, step4, step5]

    step0_type = 'primary' if st.session_state['current_step'] == 0 else 'secondary'
    step1_type = 'primary' if st.session_state['current_step'] == 1 else 'secondary'
    step2_type = 'primary' if st.session_state['current_step'] == 2 else 'secondary'
    step3_type = 'primary' if st.session_state['current_step'] == 3 else 'secondary'
    step4_type = 'primary' if st.session_state['current_step'] == 4 else 'secondary'
    step5_type = 'primary' if st.session_state['current_step'] == 5 else 'secondary'
    step6_type = 'primary' if st.session_state['current_step'] == 6 else 'secondary'


    step_cols= st.columns([1, 1, 1, 1, 1, 1, 2])
    step_cols_below_1 = st.columns([1, 1, 1])
    step_cols_below_2 = st.columns([1, 1, 1])
    
    step_cols[0].button('개요', on_click=set_form_step, args=['Jump', 0], type=step0_type, use_container_width=True)
    able_step_1 = True if st.session_state['progress'] < 1 else False
    # step_cols[1].button('정보 1', on_click=set_form_step, args=['Jump', 1], type=step1_type, disabled=able_step_1)
    step_cols_below_1[0].button('**정보 1**', on_click=set_form_step, args=['Jump', 1], type=step1_type, disabled=able_step_1, use_container_width=True)
    step_cols_below_1[0].markdown(
        """
        <p style='text-align: center; margin-top: -10px;'>
            백내장 및 백내장 수술
        </p>
        """, unsafe_allow_html=True)
    able_step_2 = True if st.session_state['progress'] < 2 else False
    # step_cols[2].button('정보 2', on_click=set_form_step, args=['Jump', 2], type=step2_type, disabled=able_step_2)
    step_cols_below_1[1].button('**정보 2**', on_click=set_form_step, args=['Jump', 2], type=step2_type, disabled=able_step_2, use_container_width=True)
    step_cols_below_1[1].markdown(
        """
        <p style='text-align: center; margin-top: -10px;'>
            백내장 수술에서 렌즈 종류
        </p>
        """, unsafe_allow_html=True)
    able_step_3 = True if st.session_state['progress'] < 3 else False
    # step_cols[3].button('정보 3', on_click=set_form_step, args=['Jump', 3], type=step3_type, disabled=able_step_3)
    step_cols_below_1[2].button('**정보 3**', on_click=set_form_step, args=['Jump', 3], type=step3_type, disabled=able_step_3, use_container_width=True)
    step_cols_below_1[2].markdown(
        """
        <p style='text-align: center; margin-top: -10px;'>
            백내장 수술 후 시력, 일상생활
        </p>
        """, unsafe_allow_html=True)
    able_step_4 = True if st.session_state['progress'] < 4 else False
    # step_cols[4].button('정보 4', on_click=set_form_step, args=['Jump', 4], type=step4_type, disabled=able_step_4)
    step_cols_below_2[0].button('**정보 4**', on_click=set_form_step, args=['Jump', 4], type=step4_type, disabled=able_step_4, use_container_width=True)
    step_cols_below_2[0].markdown(
        """
        <p style='text-align: center; margin-top: -10px;'>
            백내장 수술의 합병증
        </p>
        """, unsafe_allow_html=True)
    able_step_5 = True if st.session_state['progress'] < 5 else False
    # step_cols[5].button('정보 5', on_click=set_form_step, args=['Jump', 5], type=step5_type, disabled=able_step_5)
    step_cols_below_2[1].button('**정보 5**', on_click=set_form_step, args=['Jump', 5], type=step5_type, disabled=able_step_5, use_container_width=True)
    step_cols_below_2[1].markdown(
        """
        <p style='text-align: center; margin-top: -10px;'>
            빈번한 질문 리스트
        </p>
        """, unsafe_allow_html=True)
    able_step_6 = True if st.session_state['progress'] < 6 else False      
    # step_cols[6].button('환자별 정보', on_click=set_form_step, args=['Jump', 6], type=step6_type, disabled=able_step_6)      
    step_cols_below_2[2].button('**정보6**', on_click=set_form_step, args=['Jump', 6], type=step6_type, disabled=able_step_6, use_container_width=True)
    step_cols_below_2[2].markdown(
        """
        <p style='text-align: center; margin-top: -10px;'>
            수술후주의사항 및 환자별정보
        </p>
        """, unsafe_allow_html=True)

    st.markdown('---')
    personalized = False
    if 'patient_info' in st.session_state:
        if st.session_state['patient_info'] != None:
            personalized = True

    # 단계 0) 정보 안내
    if st.session_state['current_step'] == 0:
        with st.container():
            st.subheader("정보 개요")
            st.markdown(
            """
            **백내장 수술정보**에서는 백내장 수술에 관하여 환자분들께서 가장 궁금해하고, 꼭 알아야 할 정보를 :blue[**단계별로**] 제공합니다.
            수술 과정부터 회복, 주의사항까지 핵심적인 내용을 담아 환자분들께서 수술 전 안심하고 준비할 수 있도록 돕겠습니다. 

            - 앞으로의 동의 과정을 위해서, 관련 정보를 단계별로 확인해주세요.
            - 하나의 정보를 확인 후, :red[**다음 단계로**]버튼을 누르시면 다음 단계를 확인할 수 있습니다.

            환자분들께서 확인하실 수 있는 단계별 정보는 다음과 같습니다.
            - 정보 1) **백내장 및 백내장 수술**
            - 정보 2) **백내장 수술에서 렌즈 종류**
            - 정보 3) **백내장 수술 후 시력, 일상생활**
            - 정보 4) **백내장 수술의 합병증**
            - 정보 5) **빈번한 질문 리스트**
            - 정보 6) **수술 후 주의사항 및 환자별 맞춤정보**

            백내장 수술은 환자 분들의 눈 건강을 위한 안전하고 효율적인 치료법입니다. 
            세브란스 안과병원의 모든 의료진은 이를 위해 최선의 노력을 다하고 있습니다.
            이 페이지를 통해 백내장에 관한 궁금증을 해결하시고, 안심하고 수술을 준비하십시오.

            - 추가적인 질문이 있으신 경우에는 :red[ :question: Q&A 챗봇]을 통하여 간단하게 알아보세요.
            - 언제든 주치의 선생님을 통하여, 더 상세하고 친절한 설명을 받으실 수 있습니다.
            """)
            disable_step_0_again = True if st.session_state['progress'] > 0 else False
            unlock_step_1 = st.button("확인하였습니다.", key="to_step_1", disabled=disable_step_0_again)
            if unlock_step_1:
                if 'patient_info' not in st.session_state:
                    st.warning("환자 정보를 먼저 등록해주세요.")
                elif st.session_state['patient_info'] == None:
                    st.warning("환자 정보를 먼저 등록해주세요.")
                else:
                    st.session_state['current_step'] = 1
                    st.session_state['progress'] += 1
                    st.rerun()

    # 단계 1) 백내장 및 백내장 수술
    elif st.session_state['current_step'] == 1:
    # elif active_tab == step1:   
        sppech_example()
        with st.container():

            st.subheader("정보 1) 백내장 및 백내장 수술")

            # 내용 1-1
            st.markdown(
        """
        #### Q. 백내장이란 무엇인가요?

        - 백내장이란 노화에 의해 **‘카메라의 렌즈에 해당하는 수정체’에 혼탁이 생기는 것**입니다.
        - 현재로서는 백내장을 치료할 수 있는 약제는 없으며, 따라서 백내장은 반드시 수술적 치료를 해야하는 질환입니다.
        """)

            # 내용 1-2
            st.markdown(
        """
        #### Q. 백내장 수술은 어떻게 진행되나요?

        백내장 수술은 다음과 같은 2가지 과정으로 이루어집니다. 
        1) **혼탁해진 백내장을 제거**하고 (Phacoemulsification)
        2) 수정체 역할을 대신할 **인공수정체(=렌즈)를 넣는 것** (IOL implantation)
        """)
            
            # 내용 1-3
            st.markdown(
        """
        #### Q. 백내장 수술시간은 어느정도 되나요?

        - 평균적으로 :red[**약 20~30분**] 정도 소요되나, **난이도에 따라 더 오래 소요될 수 있습니다.**
        """)
            
            # 내용 1-4
            st.markdown(
        """
        #### Q. 백내장 수술 시 마취는 어떠한 방식으로 하나요?

        - 일반적으로 점안 마취 및 국소마취로 진행됩니다.
        - **예외적으로 협조가 어려운 환자의 경우에는 전신마취로 진행**하게 됩니다.
        - :red[**폐쇄공포증**]이 있거나, 30분 정도 가만히 누워 계시기나 어렵거나, 눈을 가만히 있기가 어려운 분들은 사전에 주치의에게 꼭 말씀해주시길 바랍니다.
        """)
            
            # 내용 1-5
            st.markdown(
        """
        #### Q. 백내장 수술 입원은 며칠 동안 하나요?

        - 백내장 수술은 일일입원(당일 입원, 당일 퇴원)으로 진행됩니다.
        - 당일 내원시간은 전날에 전화 및 문자메세지로 안내해드리니 전화를 잘 받아주시기 바랍니다.
        - 일반적으로 **수술 1-2시간 전에 도착**하여 산동제를 점안하기 시작하며, 산동이 충분히 된 후에 수술을 진행하게 됩니다. 
        """)

            # 추가 영상
            with st.expander("백내장 수술영상"):
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
            
            disable_step_1_again = True if st.session_state['progress'] > 1 else False
            unlock_step_2 = st.button("확인하였습니다.", key="to_step_2", disabled=disable_step_1_again)
            if unlock_step_2:
                # st.session_state["step_2"] = True
                # st.session_state["active_tab"] = "단계 2"
                st.session_state['current_step'] = 2
                st.session_state['progress'] += 1
                st.rerun()

    # 단계 2) 백내장 수술에서 렌즈의 종류 및 도수
    elif st.session_state['current_step'] == 2:
        with st.container():
        
            st.subheader("단계 2) 백내장 수술에서 렌즈의 종류 및 도수")

            # 내용 2-1
            st.markdown(
        """
        #### Q. 백내장 수술시 눈의 도수는 어떻게 되나요?

        - 사람의 눈은 원래 수정체의 두께를 조절하여 먼거리와 근거리를 모두 잘 볼 수 있으며, 이러한 기능이 떨어져 일반적으로 가까운 거리를 잘 못보게 되는 것을 ‘노안’이라고 합니다.
        - **백내장 수술 후에는 이러한 조절력이 사라지기에 눈이 단초점 상태가 되어, 먼거리와 근거리 중 하나만 잘 볼 수 있게 됩니다.**
        - (예외적으로 다초점렌즈를 넣게 되면 먼거리와 근거리를 모두 잘 볼 수 있게 됩니다.)
        """)
            
            # 내용 2-2
            st.markdown(
        """
        #### Q. 백내장 수술시 넣을 수 있는 인공수정체 (=렌즈)의 종류에는 어떤 것이 있나요?

        1) **일반 렌즈**

        2) **다초점렌즈 (Multifocal)**
            - 먼거리와 가까운거리(30cm)를 둘 다 잘 보이게 하는 장점이 있어 노안교정을 원하시는 분들에게 추천드릴 수 있지만, 부작용으로 빛번짐, 시야흐림 등이 나타날 수 있습니다.
        
        3) **아이헨스렌즈 (Eyhance)**
            - 다초점렌즈의 부작용은 없으면서 먼거리와 중간거리(50cm)을 잘 보이게 하는 렌즈입니다.

        4) **난시교정렌즈 (Toric)**
            - 난시가 심한 경우 난시교정렌즈를 고려할 수 있습니다.

        - :red[**한번 수술을 하게 되면 렌즈의 교체는 어렵기에**] 수술 전 주치의와 충분히 상의하여 개개인의 연령 및 눈상태에 따라 알맞은 렌즈를 잘 결정하는 것이 중요합니다.
        - 수술 후 도수는 일반적으로 먼거리가 잘보이는 정시 도수로 진행하지만, 고도근시, 근거리 작업을 많이 하시는 분들의 경우에는 예외적으로 근거리가 잘보이는 근시 도수로 진행하기도 합니다.
        - :red[**렌즈 및 도수의 결정은 주치의선생님의 설명을 충분히 들은후에 결정하시길 바랍니다.**]
        """)
            
            disable_step_2_again = True if st.session_state['progress'] > 2 else False
            unlock_step_3 = st.button("확인하였습니다.", key="to_step_3", disabled=disable_step_2_again)
            if unlock_step_3:
                # st.session_state["step_3"] = True
                # st.session_state["active_tab"] = "단계 3"
                st.session_state['current_step'] = 3
                st.session_state['progress'] += 1
                st.rerun()

    # 단계 3) 백내장 수술 후 시력, 일상생활
    elif st.session_state['current_step'] == 3:
        with st.container():
            st.subheader("단계 3) 백내장 수술 후 시력, 일상생활")
            
            # 내용 3-1 : *****환자별 정보 입력 후에는 수정할 수 있도록 함
            st.markdown(
        """
        #### Q. 백내장 수술 후에는 바로 잘 보이게 되나요?

        - 백내장 수술 후 **1~2달 정도 뒤에 정확한 도수 및 시력**이 나오게 됩니다.
        - 일반적으로 이 때, 안경검사를 진행하고 필요하면 돋보기를 처방하게 됩니다.
        - 수술 직후에는 각막 부종 등으로 오히려 시력이 떨어질 수 있습니다.

        - 망막질환, 녹내장 등 기저 안질환이 동반되어 있는 경우에는 시력 회복이 제한될 가능성이 있습니다.
        """)
            
            # 내용 3-2
            st.markdown(
        """
        #### Q. 백내장 수술 이후 일상생활은 언제부터 가능한가요?

        - 백내장 수술 당일부터 일상 생활은 가능합니다. (식사에도 제약은 없습니다.)
        - 다만, **세수와 샤워는 일주일 뒤부터 가능합니다.**
        """)
            
            # 내용 3-3
            st.markdown(
        """
        #### Q. 백내장 수술 후에는 안약을 얼마나 사용하나요?

        - 일반적으로 수술 후에는 항생제, 항염증제 등 **안약을 약 한달 간 사용**하게 됩니다.
        - 다만, 필요에 따라서 안약을 추가하거나 더 오래 사용하게 될 수 있습니다.
        """)
            
            # 내용 3-4
            st.markdown(
        """
        #### Q. 백내장 수술 후에는 병원에 얼마나 자주 와야하나요?

        - 수술일 기준 **다음날, 1주일, 1개월, 3-6개월 주기로 내원**하게 됩니다.
        - 다만 필요에 따라서 조금 이른 주기로 경과관찰하게 될 수 있습니다.
        """)
            
            disable_step_3_again = True if st.session_state['progress'] > 3 else False
            unlock_step_4 = st.button("확인하였습니다.", key="to_step_4", disabled=disable_step_3_again)
            if unlock_step_4:
                # st.session_state["step_4"] = True
                # st.session_state["active_tab"] = "단계 4"
                st.session_state['current_step'] = 4
                st.session_state['progress'] += 1
                st.rerun()

    # 단계 4) 백내장 수술의 부작용 및 합병증
    elif st.session_state['current_step'] == 4:
        with st.container():
            st.subheader("단계 4) 백내장 수술의 부작용 및 합병증")

            # 내용 4-1 : *****환자별 정보 입력 후에는 수정할 수 있도록 함
            st.markdown(
        """
        #### Q. 백내장 수술의 부작용에는 어떤 것들이 있나요?

        - 백내장 수술의 부작용은 크게 '수술 중 합병증'과 '수술 후 부작용/합병증' 으로 나눌 수 있습니다.

        1) 수술 중 합병증
        - 백내장 수술 도중 발생할 수 있는 합병증은 여러가지가 있으나 가장 중요한 합병증은 **후낭파열 (Posterior capsular rupture)** 과 **유리체손실 (Vitreous prolapse)**입니다. 
        - 이는 백내장 수술과정의 약 5%에서 나타날 수 있는 수술 중 합병증이며, 특히 난이도가 높은 백내장 수술에서 확률이 증가합니다.
        - 이러한 경우에는 예정된 렌즈가 아닌 다른 종류의 일반렌즈를 넣고 나오게 될 가능성이 있으며, **유리체절제술까지 수술이 확대될 가능성** 또한 있습니다.

        2) 수술 후 경미한 부작용
        - 경미한 수술 부작용으로는 ':red[**건조증**], **이물감, 비특이적인 눈주변 불편감, 충혈, 결막하출혈'** 등이 있습니다.
        - 수술시 눈을 기구로 강제로 벌린 후에 눈깜빡임 없이 20-30분 정도 진행하기 때문에, 수술 후 건조증은 필연적으로 악화되게 됩니다. 
        - 건조증, 이물감은 상당기간 오래 지속될 수 있으며 이로 인한 불편감이 나타날 수 있습니다.
        - 수술 후 충혈 및 결막하출혈은 자연스럽게 나타나며 2-4주 안에 자연소멸됩니다.
        - :red[**비문증(날파리증)**] 또한 흔한 부작용 중 하나이며, 수술 이후 이로 인한 불편감이 나타날 수 있습니다.

        3) 수술 후 심한 합병증
        - 가장 심각한 부작용으로는 :red[**수술 후 감염**]이 있습니다.
        - 이를 예방하기 위해 충분한 소독을 하고 무균적으로 수술을 진행하며,
        - 수술 후에도 항생제 안약을 점안하고, 눈을 비비지 않고, 일주일간 눈에 물이 들어가지 않도록 교육하지만, 그럼에도 **1/1000 확률로 발생 가능**한 중요한 부작용입니다. 

        - 수술 후 **갑작스런 시력저하, 통증, 심한충혈 발생시,** 감염의 초기 증상일 수 있으므로 즉시 내원하셔야 합니다.
        - 수술 후 감염 발생시에는 반복적인 안구내주사 혹은 재수술 (유리체절제술)이 필요할 수 있습니다.

        - 이외에도 백내장 수술 이후 안검하수, 복시, 망막박리 등의 합병증이 발생할 수 있습니다.

        4) 수술 후 장기적인 합병증
        - (1) **렌즈의 탈구/아탈구**
            + 백내장 수술 이후에도 자연스럽게 발생할 수 있는 장기적인 합병증으로, 백내장을 지지해주던 소대가 약한 경우에서 발생할 가능성 높습니다.
            + 렌즈가 탈구/아탈구된 경우에는 재수술 (유리체절제술 및 이차적 인공수정체 삽입술)이 필요하게 됩니다.
        - (2) **각막부종**
            + 이는 수술 직후에도 발생할 수 있는 부작용으로 수술 전 각막내피세포가 좋지 않거나, 심한 백내장으로 수술 시 많은 열에너지를 사용해야 하는 경우 발생할 확률이 증가합니다.
            + 각막부종으로 인해 시력회복이 더딜 수 있으며, 장기간 지속되는 경우 :red[**각막이식술이 필요할 수 있습니다.**]
        - (3) **후낭혼탁 (=후발백내장)**
            + 이는 수술 이후에 자연스럽게 생길 수 있는 합병증으로 재수술이 아닌 간단한 ‘YAG 레이져 시술’을 통해 제거할 수 있습니다.

        """)
            
            disable_step_4_again = True if st.session_state['progress'] > 4 else False
            unlock_step_5 = st.button("확인하였습니다.", key="to_step_5", disabled=disable_step_4_again)
            if unlock_step_5:
                # st.session_state["step_5"] = True
                # st.session_state["active_tab"] = "단계 5"
                st.session_state['current_step'] = 5
                st.session_state['progress'] += 1
                st.rerun()
        
    ## 단계 5와 단계 6은 동시 활성화하고 순서 바꾸기
    # 단계 5) 자주 묻는 질문
    elif st.session_state['current_step'] == 5:
        with st.container():
            st.subheader("단계 5) 빈번한 질문 리스트")

            # 내용 5-1
            st.markdown(
        """
        #### Q. 양쪽 눈을 동시에 수술이 가능한가요?

        - 일반적으로 한 눈씩 진행하지만, 원하면 한 번에 양안 수술이 가능하기도 합니다.
        - 그러나 **대부분은 한쪽 눈 수술 경과를 보며 반대쪽 눈 수술을 결정**하게 됩니다.
        - 다만, 전신마취로 하는 경우에는 양안을 동시에 수술하게 됩니다.
        """)
            
            # 내용 5-2
            st.markdown(
        """
        #### Q. 수술 당일에는 어떻게 준비해야 하나요?

        - 보통 수술 전날 오전에 내원시간 및 장소에 대한 안내가 유선으로 진행되기에, 전화를 잘 받아주시기 바랍니다. 안내 문자도 함께 보내드립니다.
        - 수술안이 충분히 산동되어야 잘 진행될 수 있기에, 보통 수술 1~2시간 전에 도착하여 산동제를 점안하게 됩니다.
        - 수술 이후에는 간호사의 설명을 들은 후에, 퇴원약이 준비되는 대로 바로 퇴원 가능합니다.
        """)
            
            # 내용 5-3
            st.markdown(
        """
        #### Q. 백내장 수술 전에 복용하지 말아야 할 약제가 있을까요?

        - 일반적으로 피가 많이나는 수술은 아니기에 항혈소판제, 항응고제는 유지하며 수술합니다.
        - 대대분의 약제는 **수술 당일 아침까지 복용하셔도 됩니다.**
        - 전립선 약제를 복용하는 경우 동공확대를 저하시켜, 수술 난이도가 높아질 수 있습니다.
        - 다만 모든 약제는 수술 전 주치의와 상의 후 복용하셔야 합니다.
        """)
            
            disable_step_5_again = True if st.session_state['progress'] > 5 else False
            unlock_step_6 = st.button("확인하였습니다.", key="to_step_6", disabled=disable_step_5_again)
            if unlock_step_6:
                # st.session_state["step_6"] = True
                # st.session_state["active_tab"] = ":red[환자별 정보]"
                st.session_state['current_step'] = 6
                st.session_state['progress'] += 1
                st.rerun()
            
    elif st.session_state['current_step'] == 6:
        if not personalized:
            st.error("회원정보를 먼저 등록해주십시오.")
            # st.session_state["active_tab"] = step0

        else:
            st.markdown(
            """
            #### Q. 수술 후 주의해야 할 것에는 무엇이 있나요?
            - 수술 이후에는 다음과 같은 사항을 꼭 지켜주셔야 합니다.

            1) **눈 비비지 말 것**
            2) **일주일 간 세수, 샤워하지 말 것**
            3) **안약 잘 넣을 것**
            4) **외상 조심할 것**
            5) **감염징후(통증, 시력저하, 심한 충혈)가 나타나면 바로 내원할 것**
            """)

            with st.container():
                diag = st.session_state['patient_info']['diagnosis']
                patient_name = st.session_state['patient_info']['patient_name']
                # st.write(st.session_state['patient_info']['diagnosis'])
                st.subheader("종합 소견")
                contents = personalized_diagnosis(diag, patient_name)
                st.write(contents)

                with st.container(border=True):
                    explain = st.session_state["patient_info"]["explain"]
                    explain = explain.replace("#","")
                    st.write("**환자 상태에 관한 인공지능 소견**")
                    st.write(explain)

                # st.write("---")
                # st.write("#### 세부 내용")

                # for cat, details in diag.items():
                #     if len(details) == 0:
                #         continue
                #     with st.container(border=True):
                #         st.write(f"**{cat} 이상**")
                #         for detail in details:    
                #             res = supabase.table("diagnosis").select("explain").eq("diag", detail).execute()
                #             raw = res.data[0]['explain'].replace("{patient}", patient_name)
                #             st.write(raw)
                #             st.write("---")
    
    st.markdown('---')
    disable_back_button = True if st.session_state['current_step'] == 0 else False
    if st.session_state['current_step'] == 6 or st.session_state['current_step'] >= st.session_state['progress']:
        disable_next_button = True
    else:
        disable_next_button = False
    # disable_next_button = True if st.session_state['current_step'] == 6 else False

    form_footer_cols = st.columns([1,5,1])

    form_footer_cols[0].button('이전',on_click=set_form_step, args=['Back'], disabled=disable_back_button)
    form_footer_cols[2].button('다음',on_click=set_form_step, args=['Next'], disabled=disable_next_button)

def personalized_diagnosis(diag, patient_name):
    pass
    # a) 아무것도 체크되지 않은 경우
    # b) 전안부만 체크된 경우
    # c) 망막 또는 시신경 체크가 된경우
    # d) 각막 체크가 된 경우
    # e) 전방 또는 수정체 체크가 된 경우
    # 중요도 : e > d > c > b > a
    cat = ""
    severe = False
    sentence = ""
    detail = []

    # 최상위(e와 d) : 일반적인 경우와 비교하여 위험요인을 추가로 가지고 있는 상태 + [마지막 문장]
    if len(diag["전방"]) != 0 or len(diag["수정체"]) != 0 or len(diag["각막"]):
        severe = True
        # e만
        if len(diag["각막"]) == 0:

            if len(diag["전방"]) == 0 :
                cat = "수정체"
            elif len(diag["수정체"]) == 0:
                cat = "전방"
            else:
                cat = "전방 및 수정체"
            
            detail.append("e")
            if "심한 백내장(백색, 갈색, 후낭하혼탁 포함)" in diag["수정체"]:
                detail.append("e_add")

        else:
            detail.append("e")
            if "심한 백내장(백색, 갈색, 후낭하혼탁 포함)" in diag["수정체"]:
                detail.append("e_add")
            if len(diag["전방"]) != 0 and len(diag["수정체"]) !=0:
                cat = "전방 및 수정체 그리고 각막"
            elif len(diag["수정체"]) == 0:
                cat = "전방 그리고 각막"
            elif len(diag["전방"]) == 0:
                cat = "수정체 그리고 각막"
            else:
                cat = "각막"
                detail.remove("e")
            detail.append("d")
            if "내피세포 이상 1200개 미만" in diag["각막"] or  "내피세포 이상 1200~1500개" in diag["각막"]:
                detail.append("d_add")
            
    # 위험도에 따른 첫문장 선택 : (e,d / c,b,a)
    if severe:
        sentence = f"{patient_name}님은 일반적인 경우와 비교하여 {cat} 관련 위험요인(들)을 추가로 가지고 있는 상태입니다.\n"
    else:
        sentence = f"{patient_name}님은 백내장 수술의 위험성이 낮고, 합병증 발생 가능성이 높지 않은 상태입니다.\n"

    minor_cat = ""
    if len(diag["망막"]) !=0 or len(diag["시신경"]):
        detail.append("c")
        if len(diag["시신경"]) == 0:
            minor_cat = "망막"
        elif len(diag["망막"]) == 0:
            minor_cat = "녹내장"
        else:
            minor_cat = "망막 또는 녹내장"

    if len(diag["전안부"]) != 0:
        detail.append("b")

    info = {
        "e": "백내장 수술의 난이도가 높고, 수술의 범위가 커질 가능성이 있습니다.\n",
        "e_add": "심한 백내장을 제거하는 과정에서 나타나는 각막부종으로 시력 호전에 제한이 있을 수 있습니다.\n",
        "d": "백내장 수술 후에도 각막질환으로 인해 시력회복에 제한이 있을 수 있습니다.\n",
        "d_add": "각막내피세포의 저하로 수술 이후 각막 부종이 나타날 수 있으며, 이로 인한 시력저하가 지속될 시 각막이식술을 고려할 수 있습니다.\n",
        "c": f"백내장 수술 후에도 {minor_cat} 질환으로 인해 시력 호전에 제한이 있을 수 있습니다.\n",
        "b": "수술 후 건성안 증상이 악화될 수 있어 이에 대한 지속적인 관리가 필요합니다.\n"
    }
    sentence += '\n'
    sentence += "\n또한 ".join([info[idx] for idx in detail])

    if severe:
        sentence += '\n'
        sentence += "저희 세브란스 안과 병원 의료진은 이러한 위험요인(들)을 충분히 숙지하고 준비하겠습니다."

    return sentence

def sppech_example():
    script = [
        {"text": " - 백내장이란 노화에 의해 ‘카메라의 렌즈에 해당하는 수정체’에 혼탁이 생기는 것입니다.", "time": 0.5},
        {"text": " - 40~50대 이상부터는 필연적으로 백내장이 생기게 되지만 모든 사람들이 수술을 바로 해야하는 것은 아니고, 백내장으로 인한 시력저하 등 불편감이 생길 때 수술을 고려하게 됩니다.", "time": 7.8},
        {"text": " - 예외적으로 굉장히 심한 백내장을 제외하고는 백내장의 정해진 수술시기는 없습니다.", "time": 20},
        {"text": " - 즉 환자가 원하는 시기에 진행하면 됩니다.", "time": 27},
        {"text": " - 백내장 수술은 다음과 같은 상황에서 고려하게 됩니다. 1) 객관적으로 백내장 진행정도가 심하거나 2) 주관적으로 환자의 불편감이 심할 때", "time": 31},
        {"text": "                                           ", "time": 43},
    ]
    full_text_container = st.empty()
    stream_text_container = st.empty()

    if st.session_state["speech_mode"] == True:
        stop_audio()
        autoplay_audio('./ref/contents/info_1_1.mp3')
        stream_example(script, stream_text_container, full_text_container)
        
        # if st.button("다시듣기", use_container_width=True):
        #     stop_audio()
        #     stream_text_container.empty()  # 스트리밍된 텍스트 영역 비우기
        #     full_text_container.empty()
        #     st.session_state["speech_mode"] == False
        #     st.session_state["speech_mode"] == True
        #     # stream_example(script, stream_text_container, full_text_container)
        time.sleep(1)
        full_text_container.empty()
        stream_text_container.empty()
        
def stream_example(script, stream_text_container, full_text_container):
    start_time = time.time()
    # autoplay_audio('./ref/contents/info_1_1.mp3')
    full_text = ""

    for sent in script:
        # 대사가 나오는 시간까지 대기
        while time.time() - start_time < sent["time"]:
            time.sleep(0.1)

        # 스트리밍 텍스트 출력
        for partial_text in stream_partial_data(sent["text"]):
            stream_text_container.markdown(partial_text, unsafe_allow_html=True)  # 새로운 박스에 출력

        # 대사가 끝나면 전체 텍스트 영역에 덮어쓰기
        full_text += sent["text"] + "\n\n"
        full_text_container.markdown(full_text, unsafe_allow_html=True)