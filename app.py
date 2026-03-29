import streamlit as st
import pandas as pd
from num2words import num2words

# Настройка страницы
st.set_page_config(page_title="Калькулятор НДС", layout="wide")

# Стили для имитации "белого листа" и четких границ
st.markdown("""
    <style>
    .paper-container {
        background-color: white !important;
        padding: 20px;
        color: black !important;
        width: 175mm;
    }
    
    .word-table {
        font-family: "Times New Roman", Times, serif !important;
        font-size: 11pt !important;
        border-collapse: collapse !important;
        width: 100% !important;
        table-layout: fixed !important;
        color: black !important;
        background-color: white !important;
    }
    
    .word-table th, .word-table td {
        border: 1pt solid black !important;
        padding: 5px !important;
        text-align: left !important;
        word-wrap: break-word !important;
        color: black !important;
    }

    .word-text {
        font-family: "Times New Roman", Times, serif !important;
        font-size: 11pt !important;
        color: black !important;
        background-color: white !important;
        margin-top: 15px !important;
        line-height: 1.4 !important;
        text-align: justify !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Калькулятор НДС (BYN)")

with st.form("calc_form"):
    col1, col2, col3 = st.columns(3)
    name = col1.text_input("Наименование", "Оборудование")
    quantity = col2.number_input("Кол-во", min_value=1, value=1)
    price_no_nds = col3.number_input("Цена за ед. без НДС, руб", min_value=0.0, value=0.0, step=0.01)
    submitted = st.form_submit_button("Поехали")

if submitted:
    nds_rate = 20
    total_no_nds = quantity * price_no_nds
    nds_sum = total_no_nds * (nds_rate / 100)
    total_with_nds = total_no_nds + nds_sum

    def to_words(amount):
        rub = int(amount)
        kop = int(round((amount - rub) * 100))
        words = num2words(rub, lang='ru')
        return f"{amount:.2f} ({words}) белорусских рублей {kop:02d} копеек"

    total_words = to_words(total_with_nds)
    nds_words = to_words(nds_sum)

    # Формируем HTML
    columns = ["№ п.п", "Наименование оборудования", "Кол-во", "Цена ед. без НДС, руб", "Стоим. без НДС, руб", "НДС %", "Сумма НДС, руб", "Всего с НДС, руб"]
    values = ["1", name, str(quantity), f"{price_no_nds:.2f}", f"{total_no_nds:.2f}", f"{nds_rate}%", f"{nds_sum:.2f}", f"{total_with_nds:.2f}"]
    widths = ["7%", "28%", "10%", "12%", "13%", "8%", "10%", "12%"]

    full_html = '<div class="paper-container">'
    
    # Таблица
    full_html += '<table class="word-table"><thead><tr>'
    for col, width in zip(columns, widths):
        full_html += f'<th style="width: {width}; border: 1pt solid black;">{col}</th>'
    full_html += '</tr></thead><tbody><tr>'
    for val in values:
        full_html += f'<td style="border: 1pt solid black;">{val}</td>'
    full_html += '</tr></tbody></table>'
    
    # Текст без жирного выделения (убраны теги <b>)
    full_html += f"""
    <div class="word-text">
    Общая стоимость оборудования составляет {total_words}, 
    включая НДС (20%) в сумме {nds_words}.
    </div>
    """
    
    full_html += '</div>'

    st.markdown(full_html, unsafe_allow_html=True)
    st.info("Результат готов. Выделите область выше и вставьте в Word.")
