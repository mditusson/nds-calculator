import streamlit as st
import pandas as pd
from num2words import num2words

# Настройка страницы
st.set_page_config(page_title="Калькулятор НДС", layout="wide")

# Улучшенные стили для печати и копирования в Word
st.markdown("""
    <style>
    /* Стили для таблицы */
    .word-table {
        font-family: "Times New Roman", Times, serif !important;
        font-size: 11pt !important;
        border-collapse: collapse !important;
        width: 170mm !important; /* Стандартная ширина текста на А4 */
        table-layout: fixed !important; /* Фиксирует ширину колонок */
        color: black !important;
        background-color: white !important;
    }
    .word-table th, .word-table td {
        border: 1px solid black !important;
        padding: 5px !important;
        text-align: left !important;
        word-wrap: break-word !important; /* Перенос длинных слов */
        vertical-align: top !important;
    }
    /* Стили для текста под таблицей */
    .word-text {
        font-family: "Times New Roman", Times, serif !important;
        font-size: 11pt !important;
        color: black !important;
        background-color: transparent !important;
        margin-top: 20px !important;
        width: 170mm !important;
        line-height: 1.5 !important;
    }
    /* Скрываем элементы Streamlit при копировании (опционально) */
    .stAlert { background-color: white !important; color: black !important; border: 1px solid #ccc !important; }
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

    # Данные для таблицы
    columns = ["№ п.п", "Наименование", "Кол-во", "Цена ед. без НДС", "Стоим. без НДС", "НДС %", "Сумма НДС", "Всего с НДС"]
    values = [
        "1", name, str(quantity), f"{price_no_nds:.2f}", 
        f"{total_no_nds:.2f}", f"{nds_rate}%", f"{nds_sum:.2f}", f"{total_with_nds:.2f}"
    ]

    # Генерация HTML таблицы с фиксированными ширинами колонок (примерно)
    widths = ["5%", "30%", "10%", "12%", "13%", "8%", "10%", "12%"]
    
    html_table = '<table class="word-table">'
    html_table += '<thead><tr>'
    for col, width in zip(columns, widths):
        html_table += f'<th style="width: {width};">{col}</th>'
    html_table += '</tr></thead><tbody><tr>'
    for val in values:
        html_table += f'<td>{val}</td>'
    html_table += '</tr></tbody></table>'
    
    st.markdown(html_table, unsafe_allow_html=True)

    # Функция суммы прописью
    def to_words(amount):
        rub = int(amount)
        kop = int(round((amount - rub) * 100))
        words = num2words(rub, lang='ru')
        return f"{amount:.2f} ({words}) белорусских рублей {kop:02d} копеек"

    total_words = to_words(total_with_nds)
    nds_words = to_words(nds_sum)

    # Итоговый текст
    result_html = f"""
    <div class="word-text">
    Общая стоимость оборудования составляет <b>{total_words}</b>, <br>
    включая НДС (20%) в сумме <b>{nds_words}</b>.
    </div>
    """
    st.markdown(result_html, unsafe_allow_html=True)
    st.info("Выделите таблицу и текст мышкой, затем нажмите Ctrl+C для вставки в Word.")
