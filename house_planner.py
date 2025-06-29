import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from geopy.geocoders import Nominatim
import time

# Seitenkonfiguration
st.set_page_config(
    page_title="Hausplaner - Grundstück & Präferenzen",
    page_icon="🏠",
    layout="wide"
)

# Titel der Anwendung
st.title("🏠 Hausplaner - Grundstück & Ihre Präferenzen")
st.markdown("---")

# Sektion 1: Grundstücksinformationen
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
    st.subheader("🗺️ Lage des Grundstücks")
    
    try:
        # Geocoding der Adresse
        geolocator = Nominatim(user_agent="house_planner")
        location = geolocator.geocode(adresse)
        
        if location:
            # Karte erstellen
            m = folium.Map(
                location=[location.latitude, location.longitude],
                zoom_start=15,
                width=700,
                height=400
            )
            
            # Marker für das Grundstück hinzufügen
            folium.Marker(
                [location.latitude, location.longitude],
                popup=f"Grundstück: {adresse}",
                tooltip="Ihr Grundstück",
                icon=folium.Icon(color='red', icon='home')
            ).add_to(m)
            
            # Karte anzeigen
            st_folium(m, width=700, height=400)
            
            # Zusätzliche Informationen
            st.info(f"📍 Koordinaten: {location.latitude:.6f}, {location.longitude:.6f}")
            
        else:
            st.warning("⚠️ Adresse konnte nicht gefunden werden. Bitte überprüfen Sie die Eingabe.")
            
    except Exception as e:
        st.error(f"❌ Fehler beim Laden der Karte: {str(e)}")

st.markdown("---")

# Sektion 2: Bewertungsfragen für Hausdesign
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

# Fragen mit Bewertung anzeigen
for i, frage in enumerate(fragen, 1):
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

# Zusammenfassung der Eingaben
if st.button("📋 Zusammenfassung anzeigen", type="primary"):
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

**Hinweise:**
- Für die Kartenfunktion wird eine Internetverbindung benötigt
- Alle Eingaben werden nur lokal gespeichert
""")

# Footer
st.markdown("---")
st.markdown("*Entwickelt für die Hausplanung - Alle Daten werden lokal verarbeitet*")
