import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.api import fetch_datalab_search

st.title("📈 통합 검색어 트렌드")

st.markdown("""
네이버 데이터랩 통합 검색어 트렌드 API를 사용하여 검색어들의 검색량 추이를 비교합니다.
""")

if "client_id" not in st.session_state or "client_secret" not in st.session_state:
    st.warning("👈 사이드바에서 API 키를 먼저 설정해주세요.")
    st.stop()

# Inputs
keywords_input = st.text_input("검색어", value="", placeholder="여러 개일 경우 콤마(,)로 구분 (예: 파이썬, 자바, C++)")
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("시작일", datetime.today() - timedelta(days=30))
with col2:
    end_date = st.date_input("종료일", datetime.today() - timedelta(days=1))
    
time_unit = st.selectbox("구간 단위", options=["date", "week", "month"], format_func=lambda x: {"date": "일간", "week": "주간", "month": "월간"}[x])

if st.button("트렌드 조회"):
    keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
    
    if not keywords:
        st.error("검색어를 입력해주세요.")
    elif len(keywords) > 5:
        st.error("검색어는 최대 5개까지 비교 가능합니다.")
    else:
        try:
            keyword_groups = [
                {"groupName": k, "keywords": [k]} for k in keywords
            ]
            
            with st.spinner("데이터를 가져오는 중..."):
                res = fetch_datalab_search(
                    start_date=start_date.strftime("%Y-%m-%d"),
                    end_date=end_date.strftime("%Y-%m-%d"),
                    time_unit=time_unit,
                    keyword_groups=keyword_groups
                )
            
            results = res.get("results", [])
            if not results:
                st.info("검색 결과가 없습니다.")
            else:
                # 데이터를 DataFrame으로 변환
                df_list = []
                for result in results:
                    group_name = result["title"]
                    for data in result["data"]:
                        df_list.append({
                            "날짜": data["period"],
                            "검색량": data["ratio"],
                            "검색어": group_name
                        })
                
                if df_list:
                    df = pd.DataFrame(df_list)
                    fig = px.line(df, x="날짜", y="검색량", color="검색어", markers=True, title="검색어 트렌드 추이")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("추출된 데이터가 없습니다.")
                    
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
