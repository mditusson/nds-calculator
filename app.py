import streamlit as st
import pandas as pd
from num2words import num2words

# Настройка страницы
st.set_page_config(page_title="Калькулятор НДС", layout="wide")

# Внедрение CSS для Times New Roman 11pt
st.markdown("""
    <style>
    .custom-table {
        font-family: "Times New Roman", Times, serif !important;
        font-size: 11pt !important;
        border-collapse: collapse;
        width: 100%;
    }
    .custom-table th, .custom-table td {
        border: 1px solid black !important;
        padding: 8px;
        text-align: left;
    }
    .custom-text {
        font-family: "Times New Roman", Times, serif !important;
        font-size: 11pt !important;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Калькулятор НДС (BYN)")

# 1. Поля ввода
with st.form("calc_form"):
    col1, col2, col3 = st.columns(3)
    name = col1.text_input("Наименование", "Оборудование")
    quantity = col2.number_input("Кол-во", min_value=1, value=1)
    price_no_nds = col3.number_input("Цена за ед. без НДС, руб", min_value=0.0, value=0.0, step=0.01)
    
    submitted = st.form_submit_button("Поехали")

if submitted:
    # 2. Логика расчета
    nds_rate = 20
    total_no_nds = quantity * price_no_nds
    nds_sum = total_no_nds * (nds_rate / 100)
    total_with_nds = total_no_nds + nds_sum

    # 3. Данные
    row = {
        "№ п.п": 1,
        "Наименование": name,
        "Кол-во": quantity,
        "Цена за ед., без НДС, руб": f"{price_no_nds:.2f}",
        "Стоимость, без НДС, Руб": f"{total_no_nds:.2f}",
        "Ставка НДС, %": f"{nds_rate}%",
        "Сумма НДС, руб": f"{nds_sum:.2f}",
        "Стоимость с НДС, руб": f"{total_with_nds:.2f}"
    }

    # 4. Создание HTML таблицы для легкого копирования и стилизации
    html_table = f"""
    <table class="custom-table">
        <thead>
            <tr>
                {"".join([f"<th>{k}</th>" for k in row.keys()])}
            </tr>
        </thead>
        <tbody>
            <tr>
                {"".join([f"<td>{v}</td>" for v in row.values()])}
            </tr>
        </tbody>
    </table>
    """
    
    st.markdown(html_table, unsafe_allow_html=True)

    # 5. Сумма прописью
    def to_words(amount):
        rub = int(amount)
        kop = int(round((amount - rub) * 100))
        words = num2words(rub, lang='ru')
        return f"{amount:.2f} ({words}) белорусских рублей {kop:02d} копеек"

    total_words = to_words(total_with_nds)
    nds_words = to_words(nds_sum)

    # 6. Итоговый текст (тоже в Times New Roman 11)
    result_text = f"""
    <div class="custom-text">
    Общая стоимость оборудования составляет <b>{total_words}</b>, <br>
    включая НДС (20%) в сумме <b>{nds_words}</b>.
    </div>
    """
    st.markdown(result_text, unsafe_allow_html=True)

    st.success("Таблицу выше можно выделить мышкой и скопировать в Word/Excel.")
