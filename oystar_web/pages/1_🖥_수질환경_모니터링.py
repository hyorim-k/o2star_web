import random
import time
import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def generate_environment_data(aquarium_type):
    if aquarium_type == "먹이생물 수조":
        # 먹이생물 수조 환경 데이터 생성
        temp = round(random.uniform(19.7, 27.3), 1)  # 온도 범위: 19.0 ~ 30.0
        DO = round(random.uniform(3.6, 11.8), 1)  # DO 범위: 3.0 ~ 12.0
        pH = round(random.uniform(5.3, 11.5), 1)  # pH 범위: 5.0 ~ 12.0
        sal = round(random.uniform(17.4, 37.5), 1)  # 염도 범위: 17.0 ~ 38.0
    elif aquarium_type == "유생기 수조":
        # 유생기 수조 환경 데이터 생성
        temp = round(random.uniform(24.2, 29.6), 1)
        DO = round(random.uniform(4.84, 8.24), 1)
        pH = round(random.uniform(7.0, 8.96), 1)
        sal = round(random.uniform(32.14, 34.15), 1)
    else:
        # 부착기 수조 환경 데이터  (유생기와 동일한 조건임)
        temp = round(random.uniform(24.2, 29.6), 1)
        DO = round(random.uniform(4.84, 8.24), 1)
        pH = round(random.uniform(7.0, 8.96), 1)
        sal = round(random.uniform(32.14, 34.15), 1)
    return temp, DO, pH, sal


def display_graphs(time_data, temp_data, DO_data, pH_data, sal_data, anomaly_time=None, anomaly_temp=None, anomaly_DO=None,
                   anomaly_pH=None, anomaly_sal=None):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time_data, y=temp_data, name="온도(°C)", mode="lines"))
    fig.add_trace(go.Scatter(x=time_data, y=DO_data, name="용존산소도(mg/L)", mode="lines"))
    fig.add_trace(go.Scatter(x=time_data, y=pH_data, name="pH", mode="lines"))
    fig.add_trace(go.Scatter(x=time_data, y=sal_data, name="염도(ppt)", mode="lines"))

    if anomaly_time:
        fig.add_trace(go.Scatter(x=[anomaly_time], y=[anomaly_temp], mode="markers", marker=dict(color="red"),
                                 name="이상치(온도)"))
        fig.add_trace(go.Scatter(x=[anomaly_time], y=[anomaly_DO], mode="markers", marker=dict(color="red"),
                                 name="이상치(용존산소도)"))
        fig.add_trace(go.Scatter(x=[anomaly_time], y=[anomaly_pH], mode="markers", marker=dict(color="red"),
                                 name="이상치(pH)"))
        fig.add_trace(go.Scatter(x=[anomaly_time], y=[anomaly_sal], mode="markers", marker=dict(color="red"),
                                 name="이상치(염도)"))

    fig.update_layout(title="환경 데이터 추이", xaxis_title="Time(s)", yaxis_title="Value")
    st.plotly_chart(fig, use_container_width=True)


def monitor_aquarium(aquarium_types):
    temp_data = []
    DO_data = []
    pH_data = []
    sal_data = []
    time_data = []
    max_data_length = 200

    placeholder = st.empty()
    monitoring = True
    anomaly_detected = False
    while monitoring:
        for aquarium_type in aquarium_types:
            now = time
            temp, DO, pH, sal = generate_environment_data(aquarium_type)

            time_data.append(now.strftime('%Y-%m-%d %H:%M:%S'))
            temp_data.append(temp)
            DO_data.append(DO)
            pH_data.append(pH)
            sal_data.append(sal)

            if len(temp_data) > max_data_length:
                temp_data.pop(0)
            if len(DO_data) > max_data_length:
                DO_data.pop(0)
            if len(pH_data) > max_data_length:
                pH_data.pop(0)
            if len(sal_data) > max_data_length:
                sal_data.pop(0)

            with placeholder.container():
                if anomaly_detected:
                    display_graphs(time_data, temp_data, DO_data, pH_data, sal_data, time_data[-1], temp, DO, pH, sal)
                else:
                    display_graphs(time_data,temp_data, DO_data, pH_data, sal_data)

                # 조건 확인 및 경고 메시지 출력
                if aquarium_type == "먹이생물 수조":
                    cond_tmp = 19 <= temp <= 27.2
                    cond_DO = 3.7 <= DO <= 11.7
                    cond_pH = 5.3 <= pH <= 11.4
                    cond_sal = 17.5 <= sal <= 37.4
                elif aquarium_type == "유생기 수조":
                    cond_tmp = 24.1 <= temp <= 29.7
                    cond_DO = 4.83 <= DO <= 8.25
                    cond_pH = 6.9 <= pH <= 8.97
                    cond_sal = 32.13 <= sal <= 34.16
                else:
                    cond_tmp = 24.1 <= temp <= 29.7
                    cond_DO = 4.83 <= DO <= 8.25
                    cond_pH = 7.0 <= pH <= 8.97
                    cond_sal = 32.11 <= sal <= 34.16

            if not (cond_tmp and cond_DO and cond_pH and cond_sal):
                df = pd.DataFrame((zip(temp_data, DO_data, pH_data, sal_data)), index=time_data,
                                  columns=['온도(°C)', 'DO(mg/L)', 'pH', '염도(ppt)'])
                st.error(f"{aquarium_type} 환경 조건이 정상 범위에서 벗어났습니다. 확인해주세요")

                # 이상치가 발생한 환경 변수를 빨간 글자로 표시
                st.markdown('### 이상치 발생 결과')
                st.write(f"**이상치 발생 시간**: {now.strftime('%Y-%m-%d %H:%M:%S')}")
                if not cond_tmp:
                    st.error(f"온도: {temp} °C")
                if not cond_DO:
                    st.error(f"용존산소: {DO} mg/L")
                if not cond_pH:
                    st.error(f"pH: {pH}")
                if not cond_sal:
                    st.error(f"염도: {sal} ppt")

                st.markdown('### Detailed Data View')
                st.dataframe(df)



                anomaly_detected = True
                monitoring = False
                break

            if not monitoring:
                break

        time.sleep(1)


# streamlit 앱 실행
if __name__ == "__main__":
    # Config
    st.set_page_config(page_title='수질환경 모니터링', page_icon='🖥️', layout='wide')

    st.title("🖥️ 수질 환경 모니터링")

    aquarium_types = st.multiselect("수조 종류 선택", ["먹이생물 수조", "유생기 수조", "부착기 수조"])

    monitoring = st.button("모니터링 시작")

    if len(aquarium_types) == 0:
        st.warning("최소 하나 이상의 수조 종류를 선택해야 합니다.")
    elif monitoring:
        monitor_aquarium(aquarium_types)
