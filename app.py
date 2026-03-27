import streamlit as st
import pandas as pd
from num2words import num2words

st.set_page_config(page_title="Калькулятор НДС", layout="wide")

# Инициализация хранилища данных (сессии), если его еще нет
if 'items' not in st.session_state:
    st.session_state.items = []

# Стили (белая подложка, Times New Roman, границы)
st.markdown("""
    <style>
    .paper-container { background-color: white !important; padding: 20px; color: black !important; width: 175mm; }
    .word-table { font-family: "Times New Roman", Times, serif !important; font-size: 11pt !important; 
                  border-collapse: collapse !important; width: 100% !important; table-layout: fixed !important; 
                  color: black !important; background-color: white !important; }
    .word-table th, .word-table td { border: 1pt solid black !important; padding: 5px !important; 
                                     text-align: left !important; word-wrap: break-word !important; color: black !important; }
    .word-text { font-family: "Times New Roman", Times, serif !important; font-size: 11pt !important; 
                 color: black !important; background-color: white !important; margin-top: 15px !important; 
                 line-height: 1.4 !important; text-align: justify !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("Многопозиционный калькулятор НДС (BYN)")

# 1. Форма ввода данных
with st.form("add_form", clear_on_submit=True):
    col1, col2, col3 = st.columns([3, 1, 1])
    name = col1.text_input("Наименование товара/услуги")
    qty = col2.number_input("Кол-во", min_value=1, value=1)
    price = col3.number_input("Цена за ед. без НДС", min_value=0.0, value=0.0, step=0.01)
    
    add_button = st.form_submit_button("Добавить в список")

if add_button and name:
    # Сохраняем товар в память
    item_data = {
        "name": name,
        "qty": qty,
        "price": price
    }
    st.session_state.items.append(item_data)
    st.success(f"Добавлено: {name}")

# Кнопка очистки списка
if st.button("Очистить всё"):
    st.session_state.items = []
    st.rerun()

# 2. Расчет и отображение результатов (если в списке есть товары)
if st.session_state.items:
    total_sum_no_nds = 0
    total_nds_sum = 0
    total_sum_with_nds = 0
    
    # Заголовки таблицы
    columns = ["№ п.п", "Наименование", "Кол-во", "Цена ед. без НДС", "Стоим. без НДС", "НДС %", "Сумма НДС", "Всего с НДС"]
    widths = ["7%", "28%", "8%", "12%", "13%", "8%", "11%", "13%"]
    
    full_html = '<div class="paper-container"><table class="word-table"><thead><tr>'
    for col, width in zip(columns, widths):
        full_html += f'<th style="width: {width}; border: 1pt solid black;">{col}</th>'
    full_html += '</tr></thead><tbody>'
    
    # Проход по всем товарам в списке
    for i, item in enumerate(st.session_state.items, 1):
        nds_rate = 20
        sum_no_nds = item['qty'] * item['price']
        nds_val = sum_no_nds * (nds_rate / 100)
        sum_with_nds = sum_no_nds + nds_val
        
        # Накопление итогов
        total_sum_no_nds += sum_no_nds
        total_nds_sum += nds_val
        total_sum_with_nds += sum_with_nds
        
        # Добавляем строку в HTML
        row_vals = [i, item['name'], item['qty'], f"{item['price']:.2f}", f"{sum_no_nds:.2f}", f"{nds_rate}%", f"{nds_val:.2f}", f"{sum_with_nds:.2f}"]
        full_html += '<tr>'
        for val in row_vals:
            full_html += f'<td style="border: 1pt solid black;">{val}</td>'
        full_html += '</tr>'
    
    # Добавляем строку ИТОГО
    full_html += f"""
        <tr>
            <td colspan="4" style="border: 1pt solid black; text-align: right;"><b>ИТОГО:</b></td>
            <td style="border: 1pt solid black;"><b>{total_sum_no_nds:.2f}</b></td>
            <td style="border: 1pt solid black;">-</td>
            <td style="border: 1pt solid black;"><b>{total_nds_sum:.2f}</b></td>
            <td style="border: 1pt solid black;"><b>{total_sum_with_nds:.2f}</b></td>
        </tr>
    """
    
    full_html += '</tbody></table>'
    
    # 3. Сумма прописью для общего итога
    def to_words(amount):
        rub = int(amount)
        kop = int(round((amount - rub) * 100))
        words = num2words(rub, lang='ru')
        return f"{amount:.2f} ({words}) белорусских рублей {kop:02d} копеек"

    total_words = to_words(total_sum_with_nds)
    nds_words = to_words(total_nds_sum)

    full_html += f"""
    <div class="word-text">
    Общая стоимость оборудования составляет {total_words}, 
    включая НДС (20%) в сумме {nds_words}.
    </div>
    </div>
    """
    
    st.markdown(full_html, unsafe_allow_html=True)
    st.info("Добавляйте товары выше, затем скопируйте всю итоговую таблицу в Word.")
else:
    st.write("Список пуст. Добавьте первый товар выше.")
