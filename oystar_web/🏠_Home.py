# Libraries
import streamlit as st
from PIL import Image

# Confit
st.set_page_config(page_title='DSBA O2STAR', page_icon='🦪', layout='wide')

# Title
st.title('🦪 DSBA O2STAR 지능형 굴 양식 시스템')



c1, c2 = st.columns(2)
c1.image(Image.open('images/양식장1.jpg'))
c2.image(Image.open('images/구현목표.png'))
st.markdown("---")


# 팀 멤버 정보
team_members = [
    {
        'name': '👑 김효림',
        'role': '기술수집/적용, 코드작성(코드 전체), 최종 발표',
        'photo': 'images/김효림.png',
    },
    {
        'name': '김예림',
        'role': '기술수집/적용, 코드작성(통계 데이터 위주), 중간 발표',
        'photo': 'images/김예림.png',
    },
    {
        'name': '정재훈',
        'role': '기술수집/적용, 코드작성(이미지 데이터 위주), 주제 발표',
        'photo': 'images/정재훈.png',
    },
]



# 페이지 제목
st.subheader('👥 O2Star Team')

# 팀 멤버 소개
columns = st.columns(len(team_members))

for i, member in enumerate(team_members):
    # 멤버 정보 컬럼
    with columns[i]:
        photo = Image.open(member['photo'])
        st.image(photo, width=150)
        st.markdown(f"**{member['name']}**")
        st.write(member['role'])
        st.markdown("---")
