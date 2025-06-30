import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from geopy.geocoders import Nominatim
import time

@st.cache_data(ttl=3600)  # Cache for 1 hour
def geocode_address(address):
    """
    Geocode an address and return location data.
    Cached to avoid repeated API calls for the same address.
    """
    try:
        geolocator = Nominatim(
            user_agent="house_planner_v1.0",
            timeout=10
        )
        location = geolocator.geocode(address)
        
        if location:
            return {
                "latitude": location.latitude,
                "longitude": location.longitude,
                "address": location.address,
                "found": True
            }
        else:
            return {"found": False}
            
    except Exception as e:
        return {"found": False, "error": str(e)}

# Seitenkonfiguration
st.set_page_config(
    page_title="Hausplaner - Grundstück & Präferenzen",
    page_icon="🏠",
    layout="wide"
)

# Session State für Bestätigung und Zusammenfassung initialisieren
if 'eingaben_bestaetigt' not in st.session_state:
    st.session_state.eingaben_bestaetigt = False
if 'zusammenfassung_angezeigt' not in st.session_state:
    st.session_state.zusammenfassung_angezeigt = False

# Logo anzeigen (zentriert)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <svg width="211" height="43" viewBox="0 0 211 43" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M64.5024 11.9037C66.5348 11.9037 68.2316 12.1461 69.5928 12.6309C70.954 13.1157 72.0355 13.7777 72.8373 14.6168C73.6577 15.4372 74.2358 16.3882 74.5714 17.4697C74.9257 18.5511 75.1028 19.6886 75.1028 20.8819C75.1028 22.0753 74.907 23.2221 74.5155 24.3222C74.1425 25.4223 73.5365 26.4013 72.6974 27.259C71.877 28.0981 70.7862 28.7693 69.425 29.2728C68.0825 29.7576 66.4416 30 64.5024 30H54.1537V11.9037H64.5024ZM57.8736 26.8115H64.4185C65.761 26.8115 66.8705 26.653 67.7468 26.336C68.6419 26.0004 69.3504 25.5528 69.8725 24.9935C70.3946 24.4341 70.7675 23.8001 70.9913 23.0915C71.215 22.383 71.3269 21.6464 71.3269 20.8819C71.3269 20.1174 71.215 19.3902 70.9913 18.7003C70.7675 18.0104 70.3946 17.3951 69.8725 16.8543C69.3504 16.3136 68.6419 15.8847 67.7468 15.5677C66.8705 15.2507 65.761 15.0923 64.4185 15.0923H57.8736V26.8115ZM78.2607 16.0992H81.8968V30H78.2607V16.0992ZM87.239 19.0919C86.1948 19.0919 85.2904 19.297 84.5259 19.7072C83.7614 20.0988 83.1461 20.5836 82.6799 21.1616C82.2138 21.7397 81.8875 22.2991 81.701 22.8398L81.673 21.3015C81.6917 21.0777 81.7663 20.7514 81.8968 20.3226C82.0273 19.875 82.2231 19.3996 82.4841 18.8961C82.7452 18.374 83.0901 17.8799 83.519 17.4137C83.9479 16.9289 84.47 16.5373 85.0853 16.239C85.7006 15.9407 86.4185 15.7915 87.239 15.7915V19.0919ZM96.2554 30.3077C94.8756 30.3077 93.6169 30.0093 92.4795 29.4126C91.3607 28.7973 90.4657 27.9489 89.7944 26.8674C89.1418 25.7673 88.8155 24.4993 88.8155 23.0636C88.8155 21.5905 89.1511 20.3132 89.8224 19.2317C90.4937 18.1503 91.398 17.3112 92.5355 16.7145C93.6915 16.0992 94.9968 15.7915 96.4512 15.7915C98.0548 15.7915 99.3414 16.1178 100.311 16.7704C101.299 17.4044 102.017 18.2715 102.465 19.3716C102.912 20.4717 103.136 21.7024 103.136 23.0636C103.136 23.884 103.005 24.7231 102.744 25.5808C102.483 26.4199 102.082 27.203 101.542 27.9303C101.001 28.6388 100.292 29.2169 99.416 29.6644C98.5396 30.0932 97.4861 30.3077 96.2554 30.3077ZM97.4301 27.5107C98.5303 27.5107 99.4812 27.3243 100.283 26.9513C101.085 26.5784 101.7 26.0563 102.129 25.385C102.558 24.7138 102.772 23.9399 102.772 23.0636C102.772 22.1126 102.549 21.3108 102.101 20.6582C101.672 19.9869 101.057 19.4835 100.255 19.1478C99.4719 18.7936 98.5303 18.6164 97.4301 18.6164C95.8825 18.6164 94.6798 19.0266 93.8221 19.8471C92.9643 20.6489 92.5355 21.721 92.5355 23.0636C92.5355 23.9586 92.7406 24.7417 93.1508 25.413C93.561 26.0656 94.1297 26.5784 94.8569 26.9513C95.6028 27.3243 96.4605 27.5107 97.4301 27.5107ZM102.772 16.0992H106.408V30H103.024C103.024 30 102.996 29.8229 102.94 29.4686C102.903 29.0957 102.866 28.6295 102.828 28.0701C102.791 27.5107 102.772 26.9606 102.772 26.4199V16.0992ZM108.72 16.3509H119.908V19.1199H108.72V16.3509ZM117.223 10.5053H120.104V13.4421H118.09C117.549 13.4234 117.083 13.4793 116.691 13.6099C116.3 13.7404 116.002 13.9828 115.796 14.3371C115.591 14.6727 115.489 15.1575 115.489 15.7915V30H111.853V15.344C111.853 14.2252 112.058 13.3115 112.468 12.603C112.878 11.8758 113.484 11.3443 114.286 11.0087C115.088 10.6731 116.067 10.5053 117.223 10.5053ZM121.203 16.0992H131.999V18.9241H121.203V16.0992ZM124.783 12.2953H128.419V30H124.783V12.2953ZM133.582 23.9026H137.358C137.432 24.5366 137.721 25.1147 138.225 25.6368C138.747 26.1402 139.427 26.5411 140.267 26.8394C141.106 27.1191 142.047 27.259 143.091 27.259C144.042 27.259 144.826 27.1564 145.441 26.9513C146.056 26.7462 146.513 26.4572 146.811 26.0843C147.11 25.7113 147.259 25.2638 147.259 24.7417C147.259 24.2383 147.072 23.856 146.699 23.595C146.327 23.3153 145.739 23.0915 144.937 22.9237C144.136 22.7373 143.082 22.5508 141.777 22.3643C140.751 22.2152 139.782 22.01 138.868 21.749C137.954 21.4693 137.143 21.115 136.435 20.6862C135.745 20.2573 135.195 19.7352 134.784 19.1199C134.393 18.4859 134.197 17.74 134.197 16.8823C134.197 15.8195 134.495 14.8871 135.092 14.0854C135.707 13.2836 136.612 12.6589 137.805 12.2114C138.999 11.7639 140.462 11.5401 142.196 11.5401C144.807 11.5401 146.811 12.0995 148.21 13.2183C149.627 14.3184 150.317 15.8381 150.28 17.7773H146.644C146.569 16.6772 146.103 15.8847 145.245 15.3999C144.406 14.9151 143.343 14.6727 142.057 14.6727C140.863 14.6727 139.875 14.8499 139.092 15.2041C138.327 15.5584 137.945 16.1644 137.945 17.0221C137.945 17.3578 138.038 17.6561 138.225 17.9172C138.411 18.1596 138.728 18.374 139.176 18.5605C139.623 18.7469 140.229 18.9241 140.994 19.0919C141.758 19.2597 142.709 19.4275 143.847 19.5953C144.909 19.7445 145.87 19.9496 146.727 20.2107C147.604 20.4531 148.35 20.7794 148.965 21.1896C149.599 21.5812 150.084 22.0846 150.419 22.7C150.755 23.3153 150.923 24.0705 150.923 24.9655C150.923 26.0656 150.634 27.0259 150.056 27.8463C149.496 28.6481 148.62 29.2728 147.427 29.7203C146.252 30.1678 144.723 30.3916 142.84 30.3916C141.497 30.3916 140.313 30.2517 139.288 29.972C138.262 29.6737 137.376 29.2821 136.63 28.7973C135.885 28.3125 135.279 27.7811 134.812 27.203C134.346 26.625 134.011 26.047 133.806 25.4689C133.619 24.8909 133.545 24.3688 133.582 23.9026ZM163.854 30.3356C162.624 30.3356 161.57 30.1212 160.694 29.6923C159.836 29.2448 159.137 28.6668 158.596 27.9582C158.055 27.231 157.654 26.4385 157.393 25.5808C157.132 24.7231 157.002 23.884 157.002 23.0636C157.002 22.038 157.123 21.0871 157.365 20.2107C157.626 19.3343 158.027 18.5698 158.568 17.9172C159.109 17.2459 159.808 16.7238 160.666 16.3509C161.542 15.978 162.605 15.7915 163.854 15.7915C165.253 15.7915 166.511 16.0992 167.63 16.7145C168.749 17.3298 169.635 18.1875 170.287 19.2877C170.958 20.3692 171.294 21.6278 171.294 23.0636C171.294 24.5366 170.958 25.8232 170.287 26.9234C169.616 28.0048 168.721 28.8439 167.602 29.4406C166.483 30.0373 165.234 30.3356 163.854 30.3356ZM162.679 27.5107C163.668 27.5107 164.525 27.3243 165.253 26.9513C165.999 26.5784 166.567 26.0656 166.959 25.413C167.369 24.7417 167.574 23.9586 167.574 23.0636C167.574 21.721 167.145 20.6395 166.288 19.8191C165.448 18.9987 164.246 18.5884 162.679 18.5884C161.691 18.5884 160.787 18.7656 159.966 19.1199C159.165 19.4741 158.531 19.9869 158.065 20.6582C157.598 21.3108 157.365 22.1126 157.365 23.0636C157.365 23.9586 157.58 24.7417 158.009 25.413C158.437 26.0656 159.053 26.5784 159.855 26.9513C160.656 27.3243 161.598 27.5107 162.679 27.5107ZM153.729 16.0992H157.197L157.365 19.7911V35.5939H153.729V16.0992ZM182.164 30.3356C180.411 30.3356 178.864 30.0559 177.521 29.4965C176.197 28.9372 175.162 28.126 174.416 27.0632C173.671 25.9817 173.298 24.6578 173.298 23.0915C173.298 21.5252 173.671 20.2013 174.416 19.1199C175.162 18.0197 176.197 17.19 177.521 16.6306C178.864 16.0712 180.411 15.7915 182.164 15.7915C183.917 15.7915 185.446 16.0712 186.751 16.6306C188.075 17.19 189.11 18.0197 189.856 19.1199C190.601 20.2013 190.974 21.5252 190.974 23.0915C190.974 24.6578 190.601 25.9817 189.856 27.0632C189.11 28.126 188.075 28.9372 186.751 29.4965C185.446 30.0559 183.917 30.3356 182.164 30.3356ZM182.164 27.5387C183.134 27.5387 184.001 27.3709 184.765 27.0352C185.548 26.681 186.164 26.1775 186.611 25.5249C187.059 24.8536 187.282 24.0425 187.282 23.0915C187.282 22.1406 187.059 21.3295 186.611 20.6582C186.164 19.9683 185.558 19.4462 184.793 19.0919C184.029 18.7376 183.152 18.5605 182.164 18.5605C181.194 18.5605 180.318 18.7376 179.535 19.0919C178.752 19.4462 178.127 19.9589 177.661 20.6302C177.213 21.3015 176.99 22.1219 176.99 23.0915C176.99 24.0425 177.213 24.8536 177.661 25.5249C178.108 26.1775 178.724 26.681 179.507 27.0352C180.29 27.3709 181.176 27.5387 182.164 27.5387ZM192.492 16.0992H203.288V18.9241H192.492V16.0992ZM196.072 12.2953H199.708V30H196.072V12.2953Z" fill="white"/>
            <path d="M22.8358 28.7303C22.8358 23.9231 26.769 20.0773 31.5762 20.0773H34.8102C37.5197 20.0773 39.7048 17.8922 39.7048 15.1827H31.5762C30.877 15.1827 30.1777 15.2701 29.5659 15.3575C28.08 15.5323 27.643 13.4346 29.0415 12.9976C29.8281 12.7354 30.7022 12.648 31.5762 12.648H34.8102C37.5197 12.648 39.7048 10.4629 39.7048 7.75334H31.5762C30.7022 7.75334 29.9155 7.84074 29.1289 8.01555C27.7304 8.27777 27.1186 6.26746 28.5171 5.74304C29.4785 5.39342 30.5274 5.13121 31.6636 5.13121H34.8102C37.5197 5.13121 39.7048 2.9461 39.7048 0.236572H31.6636C24.1469 0.236572 17.8538 6.26747 17.9412 13.6968C18.0286 18.5915 14.0954 22.5246 9.20074 22.5246H6.14159C3.43206 22.5246 1.24695 24.7098 1.24695 27.4193H9.11333C9.98737 27.4193 10.774 27.3319 11.5606 27.1571C12.9591 26.8949 13.5709 28.9052 12.1725 29.4296C11.211 29.7792 10.1622 30.0414 9.02593 30.0414H5.96678C3.25725 30.0414 1.07214 32.2265 1.07214 34.936H8.93852C9.63776 34.936 10.337 34.8486 10.9488 34.7612C12.4347 34.5864 12.8717 36.6841 11.4732 37.1211C10.6866 37.3834 9.81256 37.4708 8.93852 37.4708H5.87937C3.16985 37.4708 0.984741 39.6559 0.984741 42.3654H8.85112C16.7175 42.3654 22.8358 36.2471 22.8358 28.7303Z" fill="white"/>
        </svg>
    </div>
    """, unsafe_allow_html=True)

# Titel der Anwendung (zentriert)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🏠 Hausplaner - Grundstück & Ihre Präferenzen")
st.markdown("---")

# Sektion 1: Grundstücksinformationen (zentriert)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.header("📍 Grundstücksinformationen")

col1, col2 = st.columns(2)

with col1:
    # Eingabefeld für Grundstücksgröße
    grundstuecks_groesse = st.number_input(
        "Größe des Baugrundstücks (in m²)",
        min_value=0,
        value=0,
        step=1,
        help="Geben Sie die Größe Ihres Grundstücks in Quadratmetern ein"
    )

with col2:
    # Eingabefeld für Adresse
    adresse = st.text_input(
        "Adresse des Grundstücks",
        placeholder="z.B. Musterstraße 1, 12345 Musterstadt",
        help="Geben Sie die vollständige Adresse Ihres Grundstücks ein"
    )

# Karte anzeigen, wenn Adresse eingegeben wurde
if adresse:
    # Zentrierte Überschrift für Karte
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("🗺️ Lage des Grundstücks")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col2:
        # Use cached geocoding function
        with st.spinner("🔍 Suche Adresse..."):
            location_data = geocode_address(adresse)
        
        if location_data["found"]:
            # Karte erstellen
            m = folium.Map(
                location=[location_data["latitude"], location_data["longitude"]],
                zoom_start=15,
                width=700,
                height=400
            )
            
            # Marker für das Grundstück hinzufügen
            folium.Marker(
                [location_data["latitude"], location_data["longitude"]],
                popup=f"Grundstück: {adresse}",
                tooltip="Ihr Grundstück",
                icon=folium.Icon(color='red', icon='home')
            ).add_to(m)
            
            # Karte anzeigen
            st_folium(m, width=700, height=400)
            
            # Zusätzliche Informationen
            st.info(f"📍 Koordinaten: {location_data['latitude']:.6f}, {location_data['longitude']:.6f}")
            
        elif "error" in location_data:
            st.error(f"❌ Fehler beim Laden der Karte: {location_data['error']}")
        else:
            st.warning("⚠️ Adresse konnte nicht gefunden werden. Bitte überprüfen Sie die Eingabe.")

st.markdown("---")

# Sektion 2: Bewertungsfragen für Hausdesign (zentriert)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.header("🏡 Präferenzen für Ihr Traumhaus")
    st.markdown("Bewerten Sie bitte die folgenden Aspekte nach ihrer Wichtigkeit für Sie (1 = unwichtig, 5 = sehr wichtig)")

# Liste der Fragen
fragen = [
    "Wie wichtig ist es Ihnen, mit Sonnenschein im Fenster frühstücken zu können?",
    "Wie wichtig ist Ihnen ein großer, offener Wohnbereich?",
    "Wie wichtig ist Ihnen ein separates Arbeitszimmer/Home Office?",
    "Wie wichtig ist Ihnen ein direkter Zugang zur Terrasse/Garten vom Wohnbereich?",
    "Wie wichtig ist Ihnen eine moderne, offene Küche?",
    "Wie wichtig ist Ihnen viel natürliches Licht in den Räumen?",
    "Wie wichtig ist Ihnen die Privatsphäre gegenüber Nachbarn?",
    "Wie wichtig ist Ihnen ein Gästezimmer?",
    "Wie wichtig ist Ihnen eine energieeffiziente Bauweise?",
    "Wie wichtig ist Ihnen ausreichend Stauraum/Abstellmöglichkeiten?"
]

# Dictionary zur Speicherung der Antworten
antworten = {}

# Bewertungsskala
bewertung_optionen = {
    1: "1 - Unwichtig",
    2: "2 - Wenig wichtig", 
    3: "3 - Neutral",
    4: "4 - Wichtig",
    5: "5 - Sehr wichtig"
}

# Fragen mit Bewertung anzeigen (zentriert)
for i, frage in enumerate(fragen, 1):
    # Zentrierte Spalten für Fragen
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader(f"Frage {i}")
        st.write(frage)
        
        # Radio buttons für die Bewertung
        bewertung = st.radio(
            "Bewertung:",
            options=list(bewertung_optionen.keys()),
            format_func=lambda x: bewertung_optionen[x],
            key=f"frage_{i}",
            horizontal=True
        )
        
        antworten[f"frage_{i}"] = {
            "frage": frage,
            "bewertung": bewertung
        }
        
        st.markdown("---")

# Zusammenfassung der Eingaben (zentriert)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("📋 Zusammenfassung anzeigen", type="primary"):
        st.session_state.zusammenfassung_angezeigt = True

# Zusammenfassung anzeigen, wenn sie angefordert wurde
if st.session_state.zusammenfassung_angezeigt:
    # Zentrierte Spalten für die Zusammenfassung
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.header("📋 Zusammenfassung Ihrer Eingaben")
        
        # Grundstücksinformationen
        st.subheader("Grundstücksdaten")
        st.write(f"**Größe:** {grundstuecks_groesse} m²")
        st.write(f"**Adresse:** {adresse if adresse else 'Nicht angegeben'}")
        
        # Bewertungen
        st.subheader("Ihre Präferenzen")
        
        # Sortiere Antworten nach Bewertung (höchste zuerst)
        sortierte_antworten = sorted(antworten.items(), 
                                   key=lambda x: x[1]['bewertung'], 
                                   reverse=True)
        
        for key, data in sortierte_antworten:
            frage = data['frage']
            bewertung = data['bewertung']
            bewertung_text = bewertung_optionen[bewertung]
            
            # Farbe basierend auf Bewertung
            if bewertung >= 4:
                st.success(f"**{bewertung_text}:** {frage}")
            elif bewertung == 3:
                st.info(f"**{bewertung_text}:** {frage}")
            else:
                st.warning(f"**{bewertung_text}:** {frage}")
        
        st.markdown("---")
    
    # Bestätigungsbutton - jetzt außerhalb des ursprünglichen Button-Blocks
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Eingaben bestätigen und 3D-Modell anzeigen", type="primary", key="bestaetigung"):
            st.session_state.eingaben_bestaetigt = True
            st.success("🎉 Eingaben bestätigt! Das 3D-Modell wird geladen...")
            st.rerun()

# 3D-Modell anzeigen, wenn Eingaben bestätigt wurden
if st.session_state.eingaben_bestaetigt:
    st.markdown("---")
    # Zentrierte Überschrift für 3D-Modell
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.header("🏠 Ihr 3D-Hausmodell")
        st.markdown("Hier sehen Sie ein interaktives 3D-Modell basierend auf Ihren Präferenzen:")
    
    # Sketchfab 3D-Modell einbetten
    sketchfab_html = '''
    <div class="sketchfab-embed-wrapper"> 
        <iframe title="VIANNEY HOUSE 2" 
                frameborder="0" 
                allowfullscreen 
                mozallowfullscreen="true" 
                webkitallowfullscreen="true" 
                allow="autoplay; fullscreen; xr-spatial-tracking" 
                xr-spatial-tracking 
                execution-while-out-viewport 
                execution-while-not-rendered 
                web-share 
                src="https://sketchfab.com/models/b45403bf4f7849aebb61f7623c00b714/embed?autospin=1&camera=0"
                style="width: 100%; height: 600px;">
        </iframe> 
        <p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;"> 
            <a href="https://sketchfab.com/3d-models/vianney-house-2-b45403bf4f7849aebb61f7623c00b714?utm_medium=embed&utm_campaign=share-popup&utm_content=b45403bf4f7849aebb61f7623c00b714" 
               target="_blank" 
               rel="nofollow" 
               style="font-weight: bold; color: #1CAAD9;"> 
               VIANNEY HOUSE 2 
            </a> 
            by 
            <a href="https://sketchfab.com/fantecboisseau?utm_medium=embed&utm_campaign=share-popup&utm_content=b45403bf4f7849aebb61f7623c00b714" 
               target="_blank" 
               rel="nofollow" 
               style="font-weight: bold; color: #1CAAD9;"> 
               Fantec Boisseau 
            </a> 
            on 
            <a href="https://sketchfab.com?utm_medium=embed&utm_campaign=share-popup&utm_content=b45403bf4f7849aebb61f7623c00b714" 
               target="_blank" 
               rel="nofollow" 
               style="font-weight: bold; color: #1CAAD9;">
               Sketchfab
            </a>
        </p>
    </div>
    '''
    
    # 3D-Modell anzeigen
    st.components.v1.html(sketchfab_html, height=650)
    
    # Zusätzliche Informationen zum Modell
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("""
        🎯 **Bedienung des 3D-Modells:**
        - **Drehen**: Linke Maustaste gedrückt halten und bewegen
        - **Zoomen**: Mausrad oder Pinch-Geste auf Touchscreens
        - **Verschieben**: Rechte Maustaste gedrückt halten und bewegen
        - **Automatische Rotation**: Das Modell dreht sich automatisch
        - **Vollbild**: Klicken Sie auf das Vollbild-Symbol im 3D-Viewer    """)
    
    # Buttons für Aktionen
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col2:
        if st.button("💰 Bauplan und statische Berechnung kaufen", key="kaufen", type="secondary"):
            st.success("🛒 Vielen Dank für Ihr Interesse! Sie werden zur Kaufabwicklung weitergeleitet...")
            st.info("""
            📋 **Unser Angebot umfasst:**
            - 📐 Detaillierte Baupläne basierend auf Ihren Präferenzen
            - 🔧 Statische Berechnung durch unseren DraftSpot Agent
            - 📄 Eine detaillierte Auflistung aller für benötigten Materialien
            
            💡 Ein schneller und unkomplizierter Weg zu ihrem Eigenheim
            """)
    
    with col2:
        if st.button("🔄 Neue Eingaben machen", key="reset"):
            st.session_state.eingaben_bestaetigt = False
            st.session_state.zusammenfassung_angezeigt = False
            st.rerun()

# Sidebar mit zusätzlichen Informationen
st.sidebar.header("ℹ️ Informationen")
st.sidebar.markdown("""
**Über diese Anwendung:**

Diese App hilft Ihnen dabei, Ihre Präferenzen für Ihr Traumhaus zu erfassen und zu organisieren.

**Funktionen:**
- 📍 Grundstücksdaten erfassen
- 🗺️ Lage auf der Karte anzeigen
- 📝 Präferenzen bewerten
- 📋 Zusammenfassung erstellen
- 🏠 3D-Hausmodell generieren

**3D-Modell:**
- Wird nach Bestätigung der Eingaben generiert
- Interaktive Steuerung mit Maus/Touch
- Automatische Rotation aktiviert
- Vollbild-Modus verfügbar

**Hinweise:**
- Für die Kartenfunktion wird eine Internetverbindung benötigt
- Alle Eingaben werden nur lokal gespeichert
- Das 3D-Modell lädt automatisch nach Bestätigung
""")

# Footer
st.markdown("---")
st.markdown("*Entwickelt für die Hausplanung - Alle Daten werden lokal verarbeitet*")
