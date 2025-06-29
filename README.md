# Hausplaner - Streamlit Anwendung

Eine interaktive Webanwendung zur Erfassung von Grundstücksdaten und Hausplanungspräferenzen.

## Funktionen

- 📍 **Grundstücksinformationen erfassen**: Größe und Adresse des Baugrundstücks
- 🗺️ **Interaktive Karte**: Automatische Anzeige der Grundstückslage auf einer Karte
- 📝 **Präferenzen-Bewertung**: 10 relevante Fragen zum Hausdesign mit Bewertungsskala (1-5)
- 📋 **Zusammenfassung**: Übersichtliche Darstellung aller Eingaben

## Installation

1. Stellen Sie sicher, dass Python installiert ist
2. Installieren Sie die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```

## Anwendung starten

```bash
streamlit run house_planner.py
```

Die Anwendung öffnet sich automatisch in Ihrem Browser unter `http://localhost:8501`

## Verwendung

1. **Grundstücksdaten eingeben**:
   - Tragen Sie die Größe Ihres Grundstücks in m² ein
   - Geben Sie die vollständige Adresse ein
   - Die Karte wird automatisch geladen und zeigt die Position

2. **Präferenzen bewerten**:
   - Beantworten Sie die 10 Fragen zum Hausdesign
   - Bewerten Sie jede Frage von 1 (unwichtig) bis 5 (sehr wichtig)

3. **Zusammenfassung ansehen**:
   - Klicken Sie auf "Zusammenfassung anzeigen"
   - Ihre Präferenzen werden nach Wichtigkeit sortiert angezeigt

## Technische Details

- **Frontend**: Streamlit
- **Karten**: Folium mit OpenStreetMap
- **Geocoding**: Geopy (Nominatim)
- **Datenverarbeitung**: Lokal, keine externe Speicherung

## Hinweise

- Für die Kartenfunktion ist eine Internetverbindung erforderlich
- Alle Daten werden nur lokal verarbeitet und nicht gespeichert
- Die Adresseingabe sollte möglichst vollständig sein für beste Ergebnisse