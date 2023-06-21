import pandas as pd
import streamlit as st
import xgboost as xgb
from xgboost.sklearn import XGBRegressor
import pickle

st.set_page_config(page_title='먹이생물 밀도예측', page_icon='🐟', layout='wide')
st.title('🐟 먹이생물 밀도예측')

# XGBoost 모델 로드
xgb_model_loaded = pickle.load(open('feed_xgb.pkl', "rb"))

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

# 입력 폼 구성
st.write('**먹이생물 밀도를 예측하기 위해 필요한 데이터를 입력해주세요.**')
c1, c2 = st.columns(2)
c1.write('**수조 환경 변수**')
DO_val = c1.number_input('용존산소도(mg/L)', min_value=0.0, max_value=50.0, value=0.0, key='numeric1', on_change=update_slider1) #25
DO_slider_value = c1.slider('DO', min_value=0.0,
                             value=DO_val,
                             max_value=50.0,
                             key='slider1', on_change=update_numin1, label_visibility='collapsed')
sal_val = c1.number_input('염도(ppt)', min_value=0.0, max_value=50.0, value=0.0, key='numeric2', #7.6
                         on_change=update_slider2)
sal_slider_value = c1.slider('염도', min_value=0.0,
                            value=sal_val,
                            max_value=50.0,
                            key='slider2', on_change=update_numin2, label_visibility='collapsed')  #8.15
ntu_val = c1.number_input('탁도(NTU)', min_value=0.0, max_value=50.0, value=0.0, key='numeric3', on_change=update_slider3)
ntu_slider_value = c1.slider('탁도', min_value=0.0,
                            value=ntu_val,
                            max_value=50.0,
                            key='slider3', on_change=update_numin3, label_visibility='collapsed')
c2.write("**먹이생물 종**")
feedtype = c2.selectbox(' ', ['isochrysis galbana', 'pavlova viridis', 'tetraselmis',
                              'nannochloropsis', 'chaetoceros muelleri', 'phaeodactylum tricornutum'])
c2.write('**먹이생물 수조 용량(L)**')
volume = c2.number_input('용량', min_value=0, max_value=300, value=0, label_visibility='collapsed')

c2.write('**목표 먹이 수(마리)**')
target_feed = c2.number_input('목표먹이수', min_value=0, max_value=9999999999, value=0, label_visibility='collapsed')

if feedtype == 'isochrysis galbana': feedtype_n = 0
elif feedtype == 'pavlova viridis': feedtype_n = 1
elif feedtype == 'tetraselmis': feedtype_n = 2
elif feedtype == 'nannochloropsis': feedtype_n = 3
elif feedtype == 'chaetoceros muelleri': feedtype_n = 4
else: feedtype_n = 5


if st.button('밀도 예측 시작'):
    data = [[DO_val, sal_val, ntu_val, feedtype_n]]
    df = pd.DataFrame(data, columns=['DO', 'salinity', 'NTU', 'feedtype'])

    input_data = df
    # st.dataframe(input_data)

    prediction = int(xgb_model_loaded.predict(input_data)[0])

    # 예측 결과 출력
    st.markdown('---')

    st.success(f'현재 먹이생물 밀도: {prediction} 마리/cc', icon="✅")
    st.success(f'해당 수조의 총 먹이생물 수: {prediction*volume*1000} 마리', icon="✅")

    if prediction*volume*1000 >= target_feed:
        st.success(f'목표 먹이 수에 도달했습니다.(급여 가능)', icon="✅")
    elif prediction*volume*1000 < target_feed:
        st.error('목표 먹이 수에 도달하지 못했습니다.(급여 불가능)', icon="⚠")





