import streamlit as st
import pandas as pd

def consolidate_excels(excel_files):
    all_data = pd.DataFrame()
    for excel_file in excel_files:
        data = pd.read_excel(excel_file)
        all_data = pd.concat([all_data, data], ignore_index=True)
    return all_data

st.title('Excel Dosyalarını Birleştir')

uploaded_files = st.file_uploader("Excel dosyalarını seçin", accept_multiple_files=True, type=['xlsx'])
if uploaded_files:
    consolidated_data = consolidate_excels(uploaded_files)
    st.write(consolidated_data)
    output = consolidated_data.to_excel("consolidated.xlsx", index=False)
    st.download_button(
        label="Birleştirilmiş Excel'i İndir",
        data="consolidated.xlsx",
        file_name="consolidated.xlsx",
        mime="application/vnd.ms-excel"
    )
