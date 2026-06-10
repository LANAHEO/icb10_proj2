import requests
import streamlit as st

def get_headers():
    if "client_id" not in st.session_state or "client_secret" not in st.session_state:
        raise ValueError("API 키가 설정되지 않았습니다. 사이드바에서 키를 입력해주세요.")
    return {
        "X-Naver-Client-Id": st.session_state["client_id"],
        "X-Naver-Client-Secret": st.session_state["client_secret"],
    }

def fetch_datalab_search(start_date, end_date, time_unit, keyword_groups):
    url = "https://openapi.naver.com/v1/datalab/search"
    headers = get_headers()
    headers["Content-Type"] = "application/json"
    
    payload = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": time_unit,
        "keywordGroups": keyword_groups
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def fetch_datalab_shopping(start_date, end_date, time_unit, category_id, keywords):
    url = "https://openapi.naver.com/v1/datalab/shopping/category/keywords"
    headers = get_headers()
    headers["Content-Type"] = "application/json"
    
    keyword_groups = [
        {"name": k, "param": [k]} for k in keywords
    ]
    
    payload = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": time_unit,
        "category": category_id,
        "keyword": keyword_groups
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def fetch_search_api(api_type, query, display=10, start=1, sort="sim"):
    base_urls = {
        "blog": "https://openapi.naver.com/v1/search/blog.json",
        "news": "https://openapi.naver.com/v1/search/news.json",
        "cafearticle": "https://openapi.naver.com/v1/search/cafearticle.json",
        "shop": "https://openapi.naver.com/v1/search/shop.json"
    }
    
    if api_type not in base_urls:
        raise ValueError(f"지원하지 않는 검색 타입입니다: {api_type}")
        
    url = base_urls[api_type]
    headers = get_headers()
    params = {
        "query": query,
        "display": display,
        "start": start,
        "sort": sort
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()
