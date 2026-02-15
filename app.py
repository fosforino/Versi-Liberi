import streamlit as st
import requests
import json
import base64
from fpdf import FPDF

# --- CONFIGURAZIONE DATABASE (SUPABASE) ---
URL_SUPABASE = st.secrets["SUPABASE_URL"]
KEY_SUPABASE = st.secrets["SUPABASE_KEY"]

# --- LOGICA BACKEND ---

def invia_opera(record):
    endpoint = f"{URL_SUPABASE}/rest/v1/Poesie"
    headers = {
        "apikey": KEY_SUPABASE, 
        "Authorization": f"Bearer {KEY_SUPABASE}", 
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    return requests.post(endpoint, headers=headers, data=json.dumps(record))

def carica_bacheca():
    endpoint = f"{URL_SUPABASE}/rest/v1/Poesie?select=*"
    headers = {"apikey": KEY_SUPABASE, "Authorization": f"Bearer {KEY_SUPABASE}"}
    res = requests.get(endpoint, headers=headers)
    return res.json() if res.status_code == 200 else []

def verifica_limite_demo(autore_nome):
    endpoint = f"{URL_SUPABASE}/rest/v1/Poesie?select=id&autore=eq.{autore_nome}"
    headers = {"apikey": KEY_SUPABASE, "Authorization": f"Bearer {KEY_SUPABASE}"}
    try:
        res = requests.get(endpoint, headers=headers)
        return len(res.json()) if res.status_code == 200 else 0
    except: return 0

def esporta_pdf(titolo, testo, autore):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", 'B', 22)
    pdf.cell(0, 20, titolo.upper(), ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Times", 'I', 14)
    pdf.multi_cell(0, 10, testo, align='C')
    return pdf.output(dest="S").encode("latin-1", "replace")

# --- INIZIALIZZAZIONE SESSIONE ---
if 'is_pro' not in st.session_state:
    st.session_state.is_pro = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Poeta_Anonimo"

# --- INTERFACCIA E CSS ---
st.set_page_config(page_title="Versi Liberi", page_icon="✒️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display&family=EB+Garamond&display=swap');
    
    .stApp { background-color: #f5eedc; background-image: url("https://www.transparenttextures.com/patterns/natural-paper.png"); }
    [data-testid="stSidebar"] { background-color: #1a0f08 !important; }
    [data-testid="stSidebar"] * { color: #d4af37 !important; }
    
    .demo-banner { 
        background-color: #1a0f08; color: #d4af37; padding: 15px; border-radius: 10px; 
        text-align: center; margin-bottom: 25px; border: 1px solid #d4af37; font-family: 'Playfair Display';
    }
    
    .poesia-card { 
        background: white; padding: 30px; border-radius: 15px; border-left: 8px solid #d4af37; 
        margin-bottom: 30px; box-shadow: 5px 5px 15px rgba(0,0,0,0.05); font-family: 'EB Garamond', serif;
    }
    
    .plan-card { 
        background: white; padding: 40px; border-radius: 20px; text-align: center; 
        box-shadow: 10px 10px 30px rgba(0,0,0,0.05); border: 1px solid #e5d3b3;
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGAZIONE SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>Versi Liberi</h1>", unsafe_allow_html=True)
    scelta = st.radio("STANZA:", ["Home", "Scrittoio", "Bacheca", "Piani"])
    st.markdown("---")
    st.write("📱 Social: WhatsApp | Instagram")

# --- LOGICA PAGINE ---

if scelta == "Home":
    st.markdown("<h1 style='text-align:center; font-family:Playfair Display; color:#1a0f08;'>Benvenuto nel tuo Spazio Creativo</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:1.2em;'>Dove ogni parola trova la sua casa.</p>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1455390582262-044cdead277a?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80")

elif scelta == "Scrittoio":
    st.markdown("<h1 style='font-family:Playfair Display;'>✒️ Lo Scrittoio</h1>", unsafe_allow_html=True)
    
    n_salvati = verifica_limite_demo(st.session_state.user_name)
    
    if not st.session_state.is_pro:
        st.markdown(f'<div class="demo-banner">✨ MODALITÀ DEMO: {n_salvati} di 3 salvataggi usati</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="demo-banner" style="background:#d4af37; color:#1a0f08;">💎 PROFILO PRO ATTIVO</div>', unsafe_allow_html=True)

    titolo = st.text_input("Titolo dell'opera", placeholder="L'anima del vento...")
    testo = st.text_area("Inizia a scrivere i tuoi versi...", height=300)
    link_yt = st.text_input("Link YouTube (opzionale)", placeholder="Incolla il link del video o della base musicale...")

    # Metriche
    c1, c2, c3 = st.columns(3)
    c1.metric("Parole", len(testo.split()))
    c2.metric("Versi", len([r for r in testo.split('\n') if r.strip()]))
    c3.metric("Sillabe", sum(1 for c in testo if c.lower() in "aeiouàèéìòù"))

    st.markdown("---")
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("🚀 PUBBLICA IN BACHECA", use_container_width=True):
            if not st.session_state.is_pro and n_salvati >= 3:
                st.error("Limite demo raggiunto. Passa a PRO per pubblicare ancora!")
            elif titolo and testo:
                payload = {
                    "titolo": titolo,
                    "versi": testo,
                    "autore": st.session_state.user_name,
                    "youtube_link": link_yt
                }
                res = invia_opera(payload)
                if res.status_code in [200, 201]:
                    st.success("L'opera è ora immortale nella Bacheca!")
                    st.balloons()
                else:
                    st.error(f"Errore tecnico: {res.text}")
            else:
                st.warning("Titolo e Versi sono necessari per la pubblicazione.")

    with col_btn2:
        if titolo and testo:
            pdf_bytes = esporta_pdf(titolo, testo, st.session_state.user_name)
            st.download_button("📄 SCARICA PDF", pdf_bytes, file_name=f"{titolo}.pdf", use_container_width=True)

elif scelta == "Bacheca":
    st.markdown("<h1 style='font-family:Playfair Display;'>📜 La Bacheca Comunitaria</h1>", unsafe_allow_html=True)
    poesie = carica_bacheca()
    
    if not poesie:
        st.info("La bacheca è ancora vuota. Sii il primo a scrivere!")
    
    for p in reversed(poesie):
        with st.container():
            st.markdown(f"""
            <div class="poesia-card">
                <h2 style="color:#1a0f08; margin-bottom:0;">{p['titolo']}</h2>
                <p style="color:#7d1d1d; font-style:italic; margin-top:0;">di {p['autore']}</p>
                <div style="white-space: pre-wrap; font-size:1.2em; line-height:1.6;">{p['versi']}</div>
            </div>
            """, unsafe_allow_html=True)
            if p.get('youtube_link'):
                st.video(p['youtube_link'])
            st.markdown("<br>", unsafe_allow_html=True)

elif scelta == "Piani":
    st.markdown("<h1 style='text-align:center; font-family:Playfair Display;'>Scegli il tuo Destino</h1>", unsafe_allow_html=True)
    p1, p2 = st.columns(2)
    with p1:
        st.markdown('<div class="plan-card"><h2>Mensile</h2><h1>3,99€</h1><p>Versi Illimitati<br>Bacheca Privata</p></div>', unsafe_allow_html=True)
        if st.button("ATTIVA MENSILE", key="m"):
            st.session_state.is_pro = True
            st.success("Sei ora un utente PRO!")
    with p2:
        st.markdown('<div class="plan-card"><h2>Annuale</h2><h1>39,90€</h1><p>AI Inspirer<br>Tutte le funzioni</p></div>', unsafe_allow_html=True)
        if st.button("ATTIVA ANNUALE", key="a"):
            st.session_state.is_pro = True
            st.success("Sei ora un utente PRO Annuale!")
