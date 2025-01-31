import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import base64
import io

st.sidebar.image(r"C:\Users\HP\OneDrive\İş masası\Streamlit\LOGO WHITE.png", use_container_width = True, width = 5)
data = pd.read_excel(r'C:\Users\HP\OneDrive\İş masası\Streamlit\combined_output.xlsx')

st.title("🏠 Mənzillərin Qiymət Proqnozlaşdırılması Layihəsi")
st.subheader("📋 Layihə Haqqında")
st.markdown("""
Bu layihə, mənzillərin qiymətlərinin proqnozlaşdırılması üçün hazırlanmışdır. 
Layihənin əsas məqsədi, müxtəlif xüsusiyyətlərə əsaslanaraq mənzilin dəyərini təxmin edə biləcək dəqiq bir maşın öyrənməsi modeli yaratmaqdır.
""")

st.subheader("📊 Verilənlər Haqqında (Dataset)")
st.markdown("""
Layihədə istifadə olunan məlumat aşağıdakı sütunları əhatə edir:
- **Qiymət**: Mənzilin satış qiyməti (hədəf dəyişən).
- **Ərazi**: Mənzilin yerləşdiyi ərazi.
- **Otaq Sayı**: Mənzildəki otaq sayı.
- **Sahə**: Mənzilin ümumi sahəsi (m²).
- **Mərtəbə**: Mənzilin yerləşdiyi mərtəbə.
- **Yeni Tikili**: Mənzilin yeni tikili olub-olmaması (Bəli/Xeyr).
- **Təmir**: Mənzildə təmirin olub-olmaması (Bəli/Xeyr).
- **Çıxarış**: Satış sənədinin olub-olmaması (Bəli/Xeyr).
- **İpoteka**: İpoteka imkanının olub-olmaması (Bəli/Xeyr).
- **Latitude**: Mənzilin yerləşdiyi ərazinin enliyi.	
- **Longitude** Mənzilin yerləşdiyi ərazinin uzunluğu.
- **Elanın Tarixi**: Elanın paylaşıldığı gün.
- **Elanın Saatı**: Elanın paylaşıldığı saat.
""")

st.write("🔍 **Verilənlərə Baxış:**")
st.dataframe(data.head())

st.subheader("🎯 Layihənin Məqsədi")
st.markdown("""
- **Problemin Təsviri**: Mənzil bazarında qiymətlərin dəyişkənliyi və müxtəlif xüsusiyyətlərin mənzil dəyərinə təsirini anlamaq.
- **Hədəf**: Yuxarıdakı xüsusiyyətlərdən istifadə edərək mənzilin satış qiymətini proqnozlaşdırmaq üçün model qurmaq.
""")

st.subheader("🌟 Layihənin Faydaları")
st.markdown("""
- **Alıcılar üçün üstünlüklər**: Mənzil alarkən müxtəlif xüsusiyyətlər əsasında qiymətləri müqayisə etməyə kömək edir.
- **Satıcılar üçün üstünlüklər**: Mənzilin bazar dəyərini daha yaxşı anlamağa dəstək olur.
- **Sektor üçün üstünlüklər**: Daşınmaz əmlak bazarında daha məlumatlı qərarlar qəbul edilməsini təmin edir.
""")

st.markdown("---")
st.write("📥 **Məlumatı Yükləyin:**")

excel_data = io.BytesIO()
data.to_excel(excel_data, index=False)
excel_data.seek(0) 

st.download_button(
    label="Excel Faylını Yüklə",
    data=excel_data,
    file_name='BakuApartmentDataset.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)

st.markdown("---")
st.write("💡 Daha ətraflı məlumat üçün layihə sənədlərinə baxın və ya əlaqə saxlayın.")

# ✅Done