import streamlit as st
import pandas as pd
from io import BytesIO

def consolidate_excels(excel_files):
    all_data = pd.DataFrame()
    for excel_file in excel_files:
        if excel_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            try:
                bytes_data = BytesIO(excel_file.getvalue())
                data = pd.read_excel(bytes_data)
                all_data = pd.concat([all_data, data], ignore_index=True)
            except Exception as e:
                st.error(f"Dosya işlenirken bir hata oluştu: {excel_file.name}. Hata: {str(e)}")
                return pd.DataFrame()  # Hata ile karşılaşıldığında boş bir DataFrame döndür
    return all_data

st.title('Excel Dosyalarını Birleştir')

uploaded_files = st.file_uploader("Excel dosyalarını seçin", accept_multiple_files=True, type=['xlsx'])
if uploaded_files:
    consolidated_data = consolidate_excels(uploaded_files)
    if not consolidated_data.empty:
        st.write(consolidated_data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            consolidated_data.to_excel(writer, index=False)
        st.download_button(
            label="Birleştirilmiş Excel'i İndir",
            data=output.getvalue(),
            file_name="consolidated.xlsx",
            mime="application/vnd.ms-excel"
        )
