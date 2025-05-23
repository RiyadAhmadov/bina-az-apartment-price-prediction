import streamlit as st
import pandas as pd
import joblib
import pickle
import re
import folium
from streamlit_folium import st_folium
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; MyApp/1.0; +http://yourdomain.com)',
    'Accept-Language': 'az'
}

st.set_page_config(page_title="Model Prediction", layout="centered")

st.markdown("<h1 style='color: #FFFFFF; font-weight: bold;'>🏠 Qiymət Proqnozlaşdırılması</h1>", unsafe_allow_html=True)

st.sidebar.markdown(
    f"""
    <div style="display: flex; justify-content: center;">
        <img src="https://cdn3d.iconscout.com/3d/premium/thumb/ai-home-3d-icon-download-in-png-blend-fbx-gltf-file-formats--wifi-logo-house-smart-artificial-intelligence-pack-science-technology-icons-8877577.png?f=webp" width="190">
    </div>
    """,
    unsafe_allow_html=True
)

data = pd.read_excel('combined_model.xlsx')
model = joblib.load('random_forest_price_model.pkl')  

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(email_to, app_password, subject, body):
    try:
        msg = MIMEMultipart()
        msg['To'] = email_to
        msg['From'] = 'riyadehmedov03@gmail.com'
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login('riyadehmedov03@gmail.com', app_password)
            server.sendmail('riyadehmedov03@gmail.com', email_to, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

def get_address_in_az(lat, lon):
    headers = {"User-Agent": "StreamlitApp/1.0"}
    url = "https://api.opencagedata.com/geocode/v1/json"
    params = {
        "key": API_KEY,
        "q": f"{lat},{lon}",
        "language": "az",
        "pretty": 1,
        "no_annotations": 1
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]['formatted']
        else:
            return "Address not found"
    return f"Error: {response.status_code}"

with st.form("name_surname"):
    global name, surname
    name = st.text_input("Adınızı daxil edin: ")
    surname = st.text_input("Soyadınızı daxil edin: ")
    submit_button1 = st.form_submit_button("Məlumat Düzgündür")

if submit_button1:
    if name and surname:
        pass
    elif name:
        st.warning('⚠ Zəhmət olmasa soyadınızı daxil edin.')
    elif surname:
        st.warning('⚠ Zəhmət olmasa adınızı daxil edin.')
    else:
        st.warning('⚠ Zəhmət olmasa ad və soyadınızı daxil edin.')
    

if name and surname:
    st.subheader(f"{surname} {name}, zəhmət olmasa mənzili almaq istəyiniz ərazini seçin:")
else: 
    st.subheader(f"Hörmətli müştəri, zəhmət olmasa mənzili almaq istəyiniz ərazini seçin:")
m = folium.Map(location=[40.4093, 49.8671], zoom_start=12, tiles=None)
folium.TileLayer(tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", attr="Google", name="Google Satellite Hybrid", overlay=True, control=True).add_to(m)
folium.TileLayer(tiles="OpenStreetMap", name="OpenStreetMap", overlay=False, control=True).add_to(m)
folium.LayerControl().add_to(m)
folium.LatLngPopup().add_to(m)
map_data = st_folium(m, width=725)  

if map_data.get("last_clicked"):
    global lat, lon
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    address = get_address_in_az(lat, lon)

    st.markdown(
        f"""
        <div style="background-color: #2e2e2e; padding: 15px; padding-top: 7px; padding-bottom: 7px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);">
            <h3 style="color: rgb(17, 194, 41); font-weight: 600; font-size: 27px;">Seçilmiş Kordinatlar</h3>
            <p style="font-size: 16px; color: #f1f1f1; line-height: 0.9;">Latitude: <strong>{lat}</strong></p>
            <p style="font-size: 16px; color: #f1f1f1; line-height: 0.7;">Longitude: <strong>{lon}</strong></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div style="background-color: #2e2e2e; padding: 15px; padding-top: 7px; padding-bottom: 7px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); margin-top: 10px; margin-bottom: 10px;">
            <h3 style="color: rgb(17, 194, 41); font-weight: 600; font-size: 27px;">Ünvan</h3>
            <p style="font-size: 16px; color: #f1f1f1; line-height: 0.9; padding-bottom: 5px;">{address}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.session_state.selected_lat = lat
    st.session_state.selected_lon = lon
    st.session_state.lat = lat
    st.session_state.long = lon
    submit_button2 = st.button("✅ Ərazi doğrudur.")
    if submit_button2:
        text = address
        global rayon
        rayon_pattern = r"(\w+)\s+rayonu"
        rayon = re.search(rayon_pattern, text)
        rayon = rayon.group(1) if rayon else None
        rayon = rayon + ' r.'
        st.session_state.rayon = rayon
        # seher_pattern = r"(\w+)\s+şəhəri"
        # metro_pattern = r"(\d{1,2}\s?\w+|\w+)\s+mst"
        # seher = re.search(seher_pattern, text)
        # metro = re.search(metro_pattern, text)
        # seher = seher.group(1) if seher else None
        # metro = metro.group(1) if metro else None
        st.success(f"Ərazi təsdiqləndi: {address}")
else:
    st.write("Zəhmət olmasa ərazini seçin.")

if name and surname:
    st.markdown(f"<h3>{surname} {name}, zəhmət olmasa məlumatları daxil edin.</h3>", unsafe_allow_html=True)
else: 
    st.markdown("<h3>Hörmətli müştəri zəhmət olmasa məlumatları daxil edin.</h3>", unsafe_allow_html=True)
with st.form("prediction_form"):
    otaqlar = st.number_input("Otaqların Sayı", min_value=1, max_value=10, step=1)
    kvadrat = st.number_input("Sahə (m²)", min_value=float(data['sahə'].min()), max_value=float(data['sahə'].max()), step=1.0)
    mərtəbə_bina = st.number_input("Binanın Ümumi Mərtəbəsi", min_value=data['mərtəbə_bina'].min(), max_value=data['mərtəbə_bina'].max(), step=1)
    mərtəbə_fakt = st.number_input("Evin Mərtəbəsi", min_value=data['mərtəbə_faktiki'].min(), max_value=data['mərtəbə_faktiki'].max(), step=1)
    yeni_tikili = st.selectbox("Yeni Tikili", ["Bəli", "Xeyr"])
    təmirli = st.selectbox("Təmirli", ["Bəli", "Xeyr"])
    kupçalı = st.selectbox("Çıxarışlı", ["Bəli", "Xeyr"])
    ipoteka = st.selectbox("İpotekalı", ["Bəli", "Xeyr"])
    mail = st.text_input("Ətraflı məlumat əldə etmək istəyirsinizsə mailinizi qeyd edin: ")
    submit_button = st.form_submit_button("Mənzilin Qiymətini Proqnoz Edin")

if st.session_state.get('rayon'):
    if submit_button:
        if mail:
            email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if re.match(email_pattern, mail):
                if mərtəbə_bina < mərtəbə_fakt:
                    st.warning('⚠ Xəta: Hörmətli müştəri binanın ümumi mərtəbəsi evin mərtəbəsindən kiçik ola bilməz.')
                else:
                    yeni_tikili_value = 1 if yeni_tikili == "Bəli" else 0
                    təmirli_value = 1 if təmirli == "Bəli" else 0
                    kupçalı_value = 1 if kupçalı == "Bəli" else 0
                    ipoteka_value = 1 if ipoteka == "Bəli" else 0

                    input_data = pd.DataFrame({
                        'yer': [st.session_state.rayon],
                        'otaq_sayı': [otaqlar],
                        'sahə': [kvadrat],
                        'mərtəbə_faktiki': [mərtəbə_fakt],
                        'mərtəbə_bina': [mərtəbə_bina],
                        'yeni_tikili': [yeni_tikili_value],
                        'təmirli': [təmirli_value],
                        'kupçalı': [kupçalı_value],
                        'ipoteka': [ipoteka_value],
                        'lat': [st.session_state.lat],
                        'long': [st.session_state.long],
                        'mail': [mail]
                    })

                    mail_table = input_data.copy()

                    del input_data['mail'] 
                    input_data['mərtəbə_faktiki'] = input_data['mərtəbə_faktiki'].astype('int')
                    input_data['mərtəbə_bina'] = input_data['mərtəbə_bina'].astype('int')
                    input_data['mərtəbə_faizi'] = input_data['mərtəbə_faktiki']/input_data['mərtəbə_bina']
                    input_data['1_otaq_sahəsi'] = input_data['sahə']/input_data['otaq_sayı']
                            
                    with open('scaling_params.pkl', 'rb') as f:
                        scaling_params = pickle.load(f)

                    columns_to_normalize = ['1_otaq_sahəsi', 'sahə', 'otaq_sayı', 'mərtəbə_faktiki', 'mərtəbə_bina','lat','long']
                    for column in columns_to_normalize:
                        min, max = scaling_params[column]['min'], scaling_params[column]['max']
                        input_data[column] = (input_data[column] - min) / max

                    columns = ['Nəsimi r.', 'Nizami r.', 'Abşeron r.', 'Xətai r.', 'Suraxanı r.',
       'Sabunçu r.', 'Yasamal r.', 'Səbail r.', 'Binəqədi r.', 'Xəzər r.',
       'Nərimanov r.', 'Qaradağ r.']
                    for i in ['yer__Abşeron r.', 'yer__Binəqədi r.', 'yer__Nizami r.',
                        'yer__Nərimanov r.', 'yer__Nəsimi r.', 'yer__Qaradağ r.',
                        'yer__Sabunçu r.', 'yer__Suraxanı r.', 'yer__Səbail r.',
                        'yer__Xətai r.', 'yer__Xəzər r.', 'yer__Yasamal r.', 'yer_others']:
                        input_data[i] = 0

                    yer = input_data['yer'].iloc[0]
                    if yer not in columns:
                        input_data['yer_others'] = 1
                    else: 
                        input_data[f'yer__{yer}'] = 1

                    rf_reg = joblib.load('random_forest_price_model.pkl')

                    input_data = input_data[['yeni_tikili', 'sahə', 'otaq_sayı', 'kupçalı', 'təmirli',
                        'lat', 'long', 'ipoteka', 'mərtəbə_faktiki', 'mərtəbə_bina',
                        'mərtəbə_faizi', '1_otaq_sahəsi', 'yer__Abşeron r.', 'yer__Binəqədi r.',
                        'yer__Nizami r.', 'yer__Nərimanov r.', 'yer__Nəsimi r.',
                        'yer__Qaradağ r.', 'yer__Sabunçu r.', 'yer__Suraxanı r.',
                        'yer__Səbail r.', 'yer__Xətai r.', 'yer__Xəzər r.', 'yer__Yasamal r.',
                        'yer_others']]

                    predictions = rf_reg.predict(input_data)

                    min, max = scaling_params['qiymət']['min'], scaling_params['qiymət']['max']
                    predictions = (predictions[0] * max) + min

                    email_to = mail_table['mail'].iloc[0]  
                    app_password = 'ogfp zzmi uhxh vdkd'  
                    subject = f"{name} {surname} | Evin Məbləği"

                    mail_table_html = mail_table.to_html(index=False)  

                    body = f"""
                    <html>
                        <body>
                            <p>Hər vaxtınız xeyir {name} {surname},</p>
                            <p>Mənzilin proqnozlaşdırılmış qiyməti: <strong>{predictions:.2f} AZN</strong>.</p>
                            <p>Daxil etdiyiniz məlumatlar:</p>
                            {mail_table_html}  <!-- Insert the HTML table here -->
                            <p>Təşəkkür edirik!</p>
                        </body>
                    </html>
                    """
                    if send_email(email_to, app_password, subject, body):
                        st.success(f"🎉 Təşəkkür edirik, {name} {surname}! Mənzilin proqnozlaşdırılmış qiyməti: {predictions:.2f} AZN. Əlavə olaraq mail ünvanınıza ətraflı məlumat göndərildi.")
                    else:
                        st.error("Email göndərilmədi. Xahiş edirik yenidən cəhd edin.")
            else:
                st.warning("⚠ Xəta: Zəhmət olmasa düzgün mail ünvanı qeyd edin.")
        else:
            if mərtəbə_bina < mərtəbə_fakt:
                st.warning('⚠ Xəta: Hörmətli müştəri binanın ümumi mərtəbəsi evin mərtəbəsindən kiçik ola bilməz.')
            else:
                yeni_tikili_value = 1 if yeni_tikili == "Bəli" else 0
                təmirli_value = 1 if təmirli == "Bəli" else 0
                kupçalı_value = 1 if kupçalı == "Bəli" else 0
                ipoteka_value = 1 if ipoteka == "Bəli" else 0

                input_data = pd.DataFrame({
                    'yer': [st.session_state.rayon],
                    'otaq_sayı': [otaqlar],
                    'sahə': [kvadrat],
                    'mərtəbə_faktiki': [mərtəbə_fakt],
                    'mərtəbə_bina': [mərtəbə_bina],
                    'yeni_tikili': [yeni_tikili_value],
                    'təmirli': [təmirli_value],
                    'kupçalı': [kupçalı_value],
                    'ipoteka': [ipoteka_value],
                    'lat': [st.session_state.lat],
                    'long': [st.session_state.long],
                })

                input_data['mərtəbə_faktiki'] = input_data['mərtəbə_faktiki'].astype('int')
                input_data['mərtəbə_bina'] = input_data['mərtəbə_bina'].astype('int')
                input_data['mərtəbə_faizi'] = input_data['mərtəbə_faktiki']/input_data['mərtəbə_bina']
                input_data['1_otaq_sahəsi'] = input_data['sahə']/input_data['otaq_sayı']
                        
                with open('scaling_params.pkl', 'rb') as f:
                    scaling_params = pickle.load(f)

                columns_to_normalize = ['1_otaq_sahəsi', 'sahə', 'otaq_sayı', 'mərtəbə_faktiki', 'mərtəbə_bina','lat','long']
                for column in columns_to_normalize:
                    min, max = scaling_params[column]['min'], scaling_params[column]['max']
                    input_data[column] = (input_data[column] - min) / max
                
                
                columns = ['Nəsimi r.', 'Nizami r.', 'Abşeron r.', 'Xətai r.', 'Suraxanı r.',
       'Sabunçu r.', 'Yasamal r.', 'Səbail r.', 'Binəqədi r.', 'Xəzər r.',
       'Nərimanov r.', 'Qaradağ r.']
                for i in ['yer__Abşeron r.', 'yer__Binəqədi r.', 'yer__Nizami r.',
                    'yer__Nərimanov r.', 'yer__Nəsimi r.', 'yer__Qaradağ r.',
                    'yer__Sabunçu r.', 'yer__Suraxanı r.', 'yer__Səbail r.',
                    'yer__Xətai r.', 'yer__Xəzər r.', 'yer__Yasamal r.', 'yer_others']:
                    input_data[i] = 0

                yer = input_data['yer'].iloc[0]
                if yer not in columns:
                    input_data['yer_others'] = 1
                else: 
                    input_data[f'yer__{yer}'] = 1

                rf_reg = joblib.load('random_forest_price_model.pkl')

                input_data = input_data[['yeni_tikili', 'sahə', 'otaq_sayı', 'kupçalı', 'təmirli',
       'lat', 'long', 'ipoteka', 'mərtəbə_faktiki', 'mərtəbə_bina',
       'mərtəbə_faizi', '1_otaq_sahəsi', 'yer__Abşeron r.', 'yer__Binəqədi r.',
       'yer__Nizami r.', 'yer__Nərimanov r.', 'yer__Nəsimi r.',
       'yer__Qaradağ r.', 'yer__Sabunçu r.', 'yer__Suraxanı r.',
       'yer__Səbail r.', 'yer__Xətai r.', 'yer__Xəzər r.', 'yer__Yasamal r.',
       'yer_others']]

                predictions = rf_reg.predict(input_data)

                min, max = scaling_params['qiymət']['min'], scaling_params['qiymət']['max']
                predictions = (predictions[0] * max) + min
                min, max = scaling_params['qiymət']['min'], scaling_params['qiymət']['max']
                predictions = (predictions[0] * max) + min

                st.success(f"🎉 Təşəkkür edirik, {name} {surname}! Mənzilin proqnozlaşdırılmış qiyməti: {predictions:.2f} AZN.")
else:
    st.warning('⚠ Ərazini seçməmisiniz.')
