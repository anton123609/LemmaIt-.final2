import streamlit as st
import streamlit.components.v1 as components
import qrcode
from io import BytesIO
import time 

# Importiere deine Kapitel
from chapters import cover, intro, derivation, application 

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Ito's Lemma Presentation",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# --- 2. NAVIGATION & SCROLL LOGIC ---
if "current_page" not in st.session_state:
    st.session_state.current_page = "Cover"

st.sidebar.title("Navigation")

selection = st.sidebar.radio("Go to chapter:", [
    "Cover", 
    "Introduction", 
    "The Derivation", 
    "Visualisation and conclusion"
], key="nav_selection")

# --- DER SCROLL FIX ---
if st.session_state.current_page != selection:
    st.session_state.current_page = selection
    
    placeholder = st.empty()
    with placeholder:
        components.html(
            f"""
                <script>
                    if (window.parent.document.activeElement) {{
                        window.parent.document.activeElement.blur();
                    }}
                    window.parent.scrollTo(0, 0);
                </script>
            """,
            height=0,
            width=0,
        )

# --- 3. QR CODE ---
st.sidebar.divider()
app_url = "https://ito-lemma-pr-si.streamlit.app"

qr_image = qrcode.make(app_url)
img_buffer = BytesIO()
qr_image.save(img_buffer, format="PNG")
img_buffer.seek(0)

st.sidebar.image(img_buffer, caption="Scan Presentation", width=140)
st.sidebar.caption("Journal Review 8 • 2026")

# --- 4. MAIN CONTENT ---
# Wir speichern hier, welche Datei gerade geladen wird
current_file_path = None

if selection == "Cover":
    cover.show()
    current_file_path = "chapters/cover.py"
    
elif selection == "Introduction":
    intro.show()
    current_file_path = "chapters/intro.py"
    
elif selection == "The Derivation":
    derivation.show()
    current_file_path = "chapters/derivation.py"
    
elif selection == "Visualisation and conclusion":
    application.show()
    current_file_path = "chapters/application.py"


# --- 5. SOURCE CODE FOOTER (NEU!) ---
# Dieser Block prüft, ob eine Datei definiert wurde, und zeigt sie an.
if current_file_path:
    st.write("")
    st.write("")
    st.divider()
    
    # Der Expander (zum Ausklappen)
    with st.expander(f"Show Python Code: {selection}"):
        try:
            # Datei öffnen und lesen
            with open(current_file_path, "r", encoding="utf-8") as f:
                code_content = f.read()
            # Als Code-Block anzeigen
            st.code(code_content, language="python")
        except FileNotFoundError:
            st.error(f"File not found: {current_file_path}")