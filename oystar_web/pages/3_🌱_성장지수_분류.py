import streamlit as st
import pandas as pd
import xgboost as xgb
from lightgbm import LGBMClassifier
import openpyxl
import numpy as np
import time
from annotated_text import annotated_text
from collections import Counter
import joblib
import pickle
import matplotlib.pyplot as plt
# 한글폰트 적용
# 폰트 적용
import os
import matplotlib.font_manager as fm  # 폰트 관련 용도 as fm


def unique(list):
    x = np.array(list)
    return np.unique(x)


@st.cache_data
def fontRegistered():
    font_dirs = [os.getcwd() + '/customFonts']
    font_files = fm.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    fm._load_fontmanager(try_read_cache=False)



st.set_page_config(page_title='성장지수 분류', page_icon='🌱', layout='wide')
st.title('🌱 성장지수 분류')

# XGBoost 모델 로드
# model = LGBMClassifier()
model = joblib.load('growth_lgb.pkl')

# 입력 폼 구성
st.write('**성장지수를 분류하기 위해 필요한 데이터를 입력해주세요.**')
tanks, days = st.columns(2)
container = tanks.container()
tank_no = container.multiselect("**분류에 사용할 수조를 고르세요**", range(1, 15))  # 14번

days = days.selectbox('**유생일차(일)**', range(1, 21))  # 2일차

# 엑셀 파일 업로드
uploaded_file = st.file_uploader('**행동패턴 파일 업로드** (저속카메라 수집 데이터 파일)', type='xlsx')

st.write('**수조 환경 정보**')

c1, c2 = st.columns(2)


def update_slider1():
    st.session_state.slider1 = st.session_state.numeric1
def update_numin1():
    st.session_state.numeric1 = st.session_state.slider1
def update_slider2():
    st.session_state.slider2 = st.session_state.numeric2
def update_numin2():
    st.session_state.numeric2 = st.session_state.slider2
def update_slider3():
    st.session_state.slider3 = st.session_state.numeric3
def update_numin3():
    st.session_state.numeric3 = st.session_state.slider3
def update_slider4():
    st.session_state.slider4 = st.session_state.numeric4
def update_numin4():
    st.session_state.numeric4 = st.session_state.slider4


temp_val = c1.number_input('온도(°C)', min_value=0.0, max_value=50.0, value=0.0, key='numeric1', on_change=update_slider1) #25
temp_slider_value = c1.slider('온도', min_value=0.0,
                             value=temp_val,
                             max_value=50.0,
                             key='slider1', on_change=update_numin1)
DO_val = c2.number_input('용존산소도(mg/L)', min_value=0.0, max_value=50.0, value=0.0, key='numeric2', #7.6
                         on_change=update_slider2)
DO_slider_value = c2.slider('DO', min_value=0.0,
                            value=DO_val,
                            max_value=50.0,
                            key='slider2', on_change=update_numin2)  #8.15
pH_val = c1.number_input('pH', min_value=0.0, max_value=50.0, value=0.0, key='numeric3', on_change=update_slider3)
pH_slider_value = c1.slider('pH', min_value=0.0,
                            value=pH_val,
                            max_value=50.0,
                            key='slider3', on_change=update_numin3)
sal_val = c2.number_input('염도(ppt)', min_value=0.0, max_value=50.0, value=0.0, key='numeric4', on_change=update_slider4) #33.27
sal_slider_value = c2.slider('염도', min_value=0.0,
                             value=sal_val,
                             max_value=50.0,
                             key='slider4', on_change=update_numin4)


if st.button('분류 시작'):
    if uploaded_file is not None:
        # 업로드된 파일 읽어오기
        df = pd.read_excel(uploaded_file)
        # 슬라이더에서 얻은 값으로 칼럼 값 대체
        df['grow_day'] = days
        df['Temperatue'] = temp_slider_value
        df['DO'] = DO_slider_value
        df['pH'] = pH_slider_value
        df['salinity'] = sal_slider_value

    input_data = df.iloc[:, 1:15]
    # XGBoost 모델로 예측 수행
    xgb_pred = model.predict(input_data)

    # 예측 결과 출력
    st.markdown("---")
    xgb_result = pd.DataFrame(xgb_pred, columns=['predict'], index=df['ID'])
    xgb_result['predict_category'] = xgb_result['predict'].map({0: '저성장', 1: '표준성장', 2: '과성장'})
    # st.markdown('### 성장지수 분류 결과')
    c1, c2, c3 = st.columns(3)
    # c1.write(xgb_result)

    with st.spinner('Wait for it...'):
        time.sleep(2)
    st.success('Done!')

    # 예측 결과 카테고리 개수 계산
    result_counts = Counter(xgb_pred)
    total_samples = len(xgb_pred)

    # 예측 결과 비율 계산
    result_ratios = {category: count / total_samples for category, count in result_counts.items()}


    # 결과 비율 출력
    st.markdown('### 결과 비율')
    max_ratio_category = None
    max_ratio = 0.0
    for category in range(3):
        if category in result_ratios:
            ratio = result_ratios[category]
        else:
            ratio = 0.0

        if category == 0:
            category_label = '저성장'
        elif category == 1:
            category_label = '표준성장'
        else:
            category_label = '과성장'
        st.write(f"{category_label}: {ratio:.2%}")
        if ratio > max_ratio:
            max_ratio = ratio
            max_ratio_category = category_label

    # 어노테이션 텍스트 출력
    if max_ratio > 0.7:
        screening_needed = "무"
    else:
        screening_needed = "유"

    annotated_text(
        "➡ ",
        (f"{tank_no}번","","#ffeb99"),
        " 수조는 대부분 ",
        (f"{max_ratio_category}", "", "#ffb3b3"),
        " 단계 입니다. 선별 작업의 필요 유무는 ",
        (f"{screening_needed}", "", '#cce6ff'),
        " 입니다."
    )
