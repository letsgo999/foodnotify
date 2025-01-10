import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

# 데이터베이스 초기화
conn = sqlite3.connect('supplements.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS supplements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        start_date DATE,
        daily_intake INTEGER,
        current_stock INTEGER
    )
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS intake_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        supplement_id INTEGER,
        date DATE,
        intake INTEGER,
        FOREIGN KEY(supplement_id) REFERENCES supplements(id)
    )
''')
conn.commit()

# 사용자 입력 섹션
st.title('건강식품 섭취 관리 앱')

name = st.text_input('건강식품 이름')
start_date = st.date_input('시작 날짜')
daily_intake = st.number_input('일일 섭취량', min_value=1)
current_stock = st.number_input('현재 재고량', min_value=1)

if st.button('건강식품 추가'):
    c.execute('INSERT INTO supplements (name, start_date, daily_intake, current_stock) VALUES (?, ?, ?, ?)',
              (name, start_date, daily_intake, current_stock))
    conn.commit()
    st.success('건강식품이 추가되었습니다!')

# 섭취 기록 섹션
st.header('섭취 기록')
supplement_id = st.number_input('건강식품 ID', min_value=1)
intake_date = st.date_input('섭취 날짜')
intake_amount = st.number_input('섭취량', min_value=1)

if st.button('섭취 기록 추가'):
    c.execute('INSERT INTO intake_records (supplement_id, date, intake) VALUES (?, ?, ?)',
              (supplement_id, intake_date, intake_amount))
    c.execute('UPDATE supplements SET current_stock = current_stock - ? WHERE id = ?',
              (intake_amount, supplement_id))
    conn.commit()
    st.success('섭취 기록이 추가되었습니다!')

# 재고 확인 및 알림
st.header('재고 확인')
supplement_id_check = st.number_input('확인할 건강식품 ID', min_value=1)

if st.button('재고 확인'):
    c.execute('SELECT name, current_stock FROM supplements WHERE id = ?', (supplement_id_check,))
    result = c.fetchone()
    if result:
        name, current_stock = result
        st.write(f'{name}의 현재 재고량: {current_stock}개')
        if current_stock <= 7:
            st.warning('재고가 1주일 이하로 남았습니다. 다시 주문하세요!')
    else:
        st.error('해당 ID의 건강식품이 존재하지 않습니다.')

# 섭취 기록 조회
st.header('섭취 기록 조회')
if st.button('섭취 기록 조회'):
    c.execute('SELECT * FROM intake_records')
    records = c.fetchall()
    df = pd.DataFrame(records, columns=['ID', 'Supplement ID', 'Date', 'Intake'])
    st.write(df)

conn.close()
