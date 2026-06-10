import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.api import fetch_datalab_shopping

st.title("🛍️ 쇼핑 카테고리 검색어 트렌드")

st.markdown("""
네이버 데이터랩 쇼핑인사이트 API를 사용하여 특정 카테고리 내의 검색어 추이를 비교합니다.
""")

if "client_id" not in st.session_state or "client_secret" not in st.session_state:
    st.warning("👈 사이드바에서 API 키를 먼저 설정해주세요.")
    st.stop()

# 카테고리 매핑
SHOPPING_CATEGORIES = {
    "패션의류": "50000000",
    "패션잡화": "50000001",
    "화장품/미용": "50000002",
    "디지털/가전": "50000003",
    "가구/인테리어": "50000004",
    "출산/육아": "50000005",
    "식품": "50000006",
    "스포츠/레저": "50000007",
    "생활/건강": "50000008",
    "여가/생활편의": "50000009",
    "면세점": "50000010",
    "도서": "50005542"
}

category_name = st.selectbox("쇼핑 카테고리", list(SHOPPING_CATEGORIES.keys()))
keywords_input = st.text_input("검색어", value="", placeholder="여러 개일 경우 콤마(,)로 구분 (예: 노트북, 스마트폰)")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("시작일", datetime.today() - timedelta(days=30))
with col2:
    end_date = st.date_input("종료일", datetime.today() - timedelta(days=1))

time_unit = st.selectbox("구간 단위", options=["date", "week", "month"], format_func=lambda x: {"date": "일간", "week": "주간", "month": "월간"}[x])

if st.button("쇼핑 트렌드 조회"):
    keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
    
    if not keywords:
        st.error("검색어를 입력해주세요.")
    elif len(keywords) > 5:
        st.error("검색어는 최대 5개까지 비교 가능합니다.")
    else:
        try:
            category_id = SHOPPING_CATEGORIES[category_name]
            
            with st.spinner("데이터를 가져오는 중..."):
                res = fetch_datalab_shopping(
                    start_date=start_date.strftime("%Y-%m-%d"),
                    end_date=end_date.strftime("%Y-%m-%d"),
                    time_unit=time_unit,
                    category_id=category_id,
                    keywords=keywords
                )
            
            results = res.get("results", [])
            if not results:
                st.info("검색 결과가 없습니다.")
            else:
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
                    fig = px.line(df, x="날짜", y="검색량", color="검색어", markers=True, title=f"[{category_name}] 카테고리 검색어 트렌드 추이")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("추출된 데이터가 없습니다.")
                    
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
