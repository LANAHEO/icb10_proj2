import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Naver API Dashboard",
    page_icon="🟢",
    layout="wide"
)

st.title("🟢 네이버 OpenAPI 대시보드")
st.markdown("""
이 대시보드는 네이버 OpenAPI를 활용하여 검색어 트렌드, 쇼핑, 블로그, 카페글, 뉴스 검색 결과를 조회하고 분석합니다.

### 👈 `.env` 파일에 API 키를 설정해주세요.
네이버 개발자 센터에서 발급받은 **Client ID**와 **Client Secret**이 필요합니다.

---

### 페이지 안내
- **통합 검색어 트렌드**: 네이버 데이터랩 검색어 트렌드를 선 그래프로 확인합니다.
- **쇼핑/블로그/카페글/뉴스**: 각 서비스의 검색 결과를 조회합니다.
""")

with st.sidebar:
    st.header("🔑 API 키 설정")
    
    client_id = os.environ.get("NAVER_CLIENT_ID")
    client_secret = os.environ.get("NAVER_CLIENT_SECRET")
    
    if client_id and client_secret:
        st.session_state["client_id"] = client_id
        st.session_state["client_secret"] = client_secret
        st.success("`.env` 파일에서 API 키를 성공적으로 불러왔습니다.")
    else:
        st.error("`.env` 파일에 NAVER_CLIENT_ID와 NAVER_CLIENT_SECRET을 설정해주세요.")
