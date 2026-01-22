import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="공유형 상담 일지", layout="wide")
st.title("🌐 공유형 고객 상담 관리 시스템")

DB_FILE = "consultation_log.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["날짜", "고객명", "상담유형", "상담내용"])

# 1. 입력 화면
st.sidebar.header("📝 새 상담 기록")
with st.sidebar.form("consultation_form", clear_on_submit=True):
    client_name = st.text_input("고객명")
    consult_type = st.selectbox("상담 유형", ["제품 문의", "결제/환불", "기술 지원", "기타"])
    consult_date = st.date_input("상담 날짜", datetime.now())
    details = st.text_area("상담 상세 내용")
    submit_button = st.form_submit_button("저장하기")

if submit_button and client_name and details:
    df = load_data()
    new_row = pd.DataFrame([{"날짜": consult_date.strftime("%Y-%m-%d"), "고객명": client_name, "상담유형": consult_type, "상담내용": details}])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DB_FILE, index=False)
    st.sidebar.success("저장 완료!")

# 2. 조회 화면
df = load_data()
st.subheader("🔍 전체 상담 기록")
st.dataframe(df, use_container_width=True)

# 3. 엑셀 다운로드 기능 추가
if not df.empty:
    csv = df.to_csv(index=False).encode('utf-8-sig') # 한글 깨짐 방지용 utf-8-sig
    st.download_button(label="📥 상담 기록 엑셀(CSV) 다운로드", data=csv, file_name=f"consultation_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")