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

### 👈 API 키 설정 안내
로컬 환경에서는 `.env` 파일, 배포 환경에서는 **Streamlit Secrets**를 통해 **Client ID**와 **Client Secret**을 설정해주세요.

---

### 페이지 안내
- **통합 검색어 트렌드**: 네이버 데이터랩 검색어 트렌드를 선 그래프로 확인합니다.
- **쇼핑/블로그/카페글/뉴스**: 각 서비스의 검색 결과를 조회합니다.
""")

with st.sidebar:
    st.header("🔑 API 키 설정")
    
    # Streamlit Secrets (배포 환경)에서 먼저 찾고, 없으면 로컬 환경 변수(.env)에서 가져옴
    if "NAVER_CLIENT_ID" in st.secrets and "NAVER_CLIENT_SECRET" in st.secrets:
        client_id = st.secrets["NAVER_CLIENT_ID"]
        client_secret = st.secrets["NAVER_CLIENT_SECRET"]
        success_msg = "Streamlit Secrets에서 API 키를 성공적으로 불러왔습니다."
    else:
        client_id = os.environ.get("NAVER_CLIENT_ID")
        client_secret = os.environ.get("NAVER_CLIENT_SECRET")
        success_msg = "로컬 `.env` 파일에서 API 키를 성공적으로 불러왔습니다."
    
    if client_id and client_secret:
        st.session_state["client_id"] = client_id
        st.session_state["client_secret"] = client_secret
        st.success(success_msg)
    else:
        st.error("API 키가 설정되지 않았습니다. 로컬의 `.env` 파일이나 배포 환경의 Streamlit Secrets에 NAVER_CLIENT_ID와 NAVER_CLIENT_SECRET을 설정해주세요.")
