import streamlit as st
import sqlite3
from datetime import datetime, timedelta

# 데이터베이스 초기화
conn = sqlite3.connect('simplified_supplements.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS supplements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        start_date DATE,
        current_stock INTEGER,
        daily_intake INTEGER
    )
''')
conn.commit()

# 앱 제목
st.title('건강기능식품 관리 앱')

# 사용자 입력 섹션
st.header('건강기능식품 추가')
name = st.text_input('건강기능식품 이름')
current_stock = st.number_input('현재 재고량', min_value=1)
daily_intake = st.number_input('일일 섭취량', min_value=1)
start_date = st.date_input('복용 시작 날짜')

if st.button('건강기능식품 추가'):
    c.execute('INSERT INTO supplements (name, start_date, current_stock, daily_intake) VALUES (?, ?, ?, ?)',
              (name, start_date, current_stock, daily_intake))
    conn.commit()
    st.success(f'{name}이(가) 추가되었습니다!')

# 예상 소진 날짜 계산 섹션
st.header('소진 예상 날짜 확인')
query_name = st.text_input('조회할 건강기능식품 이름')

if st.button('소진 날짜 계산'):
    c.execute('SELECT name, start_date, current_stock, daily_intake FROM supplements WHERE name = ?', (query_name,))
    result = c.fetchone()
    if result:
        name, start_date, current_stock, daily_intake = result
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        days_remaining = current_stock // daily_intake  # 정수로 일수 계산
        expected_end_date = start_date + timedelta(days=int(days_remaining))
        st.write(f'{name}의 예상 소진 날짜는 {expected_end_date.date()}입니다.')
    else:
        st.error('해당 이름의 건강기능식품이 존재하지 않습니다.')

conn.close()
