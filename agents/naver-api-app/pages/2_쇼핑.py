import streamlit as st
import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.api import fetch_search_api

st.title("🛍️ 쇼핑 검색")

if "client_id" not in st.session_state or "client_secret" not in st.session_state:
    st.warning("👈 사이드바에서 API 키를 먼저 설정해주세요.")
    st.stop()

query_input = st.text_input("검색어", value="", placeholder="여러 개일 경우 콤마(,)로 구분 (예: 노트북, 스마트폰)")
display = st.slider("표시 건수", 10, 100, 10, step=10)
sort_option = st.selectbox("정렬 기준", ["sim", "date", "asc", "dsc"], format_func=lambda x: {"sim": "유사도순", "date": "날짜순", "asc": "가격오름차순", "dsc": "가격내림차순"}[x])

if st.button("쇼핑 검색"):
    queries = [q.strip() for q in query_input.split(",") if q.strip()]
    if not queries:
        st.error("검색어를 입력해주세요.")
    else:
        tabs = st.tabs(queries)
        for i, query in enumerate(queries):
            with tabs[i]:
                try:
                    with st.spinner(f"'{query}' 검색 중..."):
                        res = fetch_search_api("shop", query, display=display, sort=sort_option)
                        items = res.get("items", [])
                        if not items:
                            st.info("검색 결과가 없습니다.")
                        else:
                            df = pd.DataFrame(items)
                            # HTML 태그 제거
                            df["title"] = df["title"].str.replace(r'<[^<>]*>', '', regex=True)
                            st.dataframe(
                                df[["title", "lprice", "mallName", "link"]],
                                column_config={
                                    "title": "상품명",
                                    "lprice": st.column_config.NumberColumn("최저가", format="%d"),
                                    "mallName": "쇼핑몰",
                                    "link": st.column_config.LinkColumn("링크")
                                },
                                hide_index=True,
                                use_container_width=True
                            )
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
