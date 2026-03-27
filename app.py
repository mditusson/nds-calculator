import streamlit as st
import pandas as pd
from num2words import num2words

st.set_page_config(page_title="Калькулятор НДС", layout="wide")
st.title("Калькулятор НДС (BYN)")

# 1. Поля ввода
with st.form("calc_form"):
    col1, col2, col3 = st.columns(3)
    name = col1.text_input("Наименование", "Оборудование")
    quantity = col2.number_input("Кол-во", min_value=1, value=1)
    # Значение по умолчанию теперь 0.0
    price_no_nds = col3.number_input("Цена за ед. без НДС, руб", min_value=0.0, value=0.0, step=0.01)
    
    # Кнопка с новым названием
    submitted = st.form_submit_button("Поехали")

if submitted:
    # 2. Логика расчета
    nds_rate = 20
    total_no_nds = quantity * price_no_nds
    nds_sum = total_no_nds * (nds_rate / 100)
    total_with_nds = total_no_nds + nds_sum

    # 3. Формируем данные для таблицы
    data = {
        "№ п.п": [1],  # Номер позиции
        "Наименование": [name],
        "Кол-во": [quantity],
        "Цена за ед., без НДС, руб": [f"{price_no_nds:.2f}"],
        "Стоимость, без НДС, Руб": [f"{total_no_nds:.2f}"],
        "Ставка НДС, %": [f"{nds_rate}%"],
        "Сумма НДС, руб": [f"{nds_sum:.2f}"],
        "Стоимость с НДС, руб": [f"{total_with_nds:.2f}"]
    }
    
    df = pd.DataFrame(data)
    
    # Отображаем таблицу (убираем индекс pandas для красоты)
    st.table(df.set_index("№ п.п"))

    # 4. Функция для суммы прописью
    def to_words(amount):
        rub = int(amount)
        kop = int(round((amount - rub) * 100))
        # num2words выдает текст, добавляем логику валюты
        words = num2words(rub, lang='ru')
        return f"{amount:.2f} ({words}) белорусских рублей {kop:02d} копеек"

    total_words = to_words(total_with_nds)
    nds_words = to_words(nds_sum)

    # 5. Итоговый текст по твоему формату
    st.success(f"""
    Общая стоимость оборудования составляет **{total_words}**, 
    включая НДС (20%) в сумме **{nds_words}**.
    """)
