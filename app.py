import streamlit as st
import requests
import json
import re

# --- CONFIGURAZIONE DATABASE ---
URL_SUPABASE = "https://eeavavlfgeeusijiljfw.supabase.co"
KEY_SUPABASE = "sb_secret_ek8JYAXOKtLfi2VJ8YsPJA_iySl6YMD"

def invia_dati(tabella, record):
    endpoint = f"{URL_SUPABASE}/rest/v1/{tabella}"
    headers = {"apikey": KEY_SUPABASE, "Authorization": f"Bearer {KEY_SUPABASE}", "Content-Type": "application/json", "Prefer": "return=minimal"}
    return requests.post(endpoint, headers=headers, data=json.dumps(record))

def leggi_poesie():
    endpoint = f"{URL_SUPABASE}/rest/v1/Poesie?select=*&order=created_at.desc"
    headers = {"apikey": KEY_SUPABASE, "Authorization": f"Bearer {KEY_SUPABASE}"}
    try:
        res = requests.get(endpoint, headers=headers)
        return res.json() if res.status_code == 200 else []
    except: return []

def conta_sillabe(testo):
    if not testo: return 0
    testo = testo.lower()
    return len(re.findall(r'[aeiouyàèéìòù]+', testo))

# --- ESTETICA "VERSI LIBERI" 2026 ---
st.set_page_config(page_title="Versi Liberi", page_icon="✒️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=EB+Garamond:ital,wght@0,400;1,500&display=swap');
    
    /* FIX FRECCETTE SIDEBAR */
    [data-testid="stSidebarCollapseButton"] {
        color: #d4af37 !important;
        background-color: #1a0f08 !important;
        border: 1px solid #d4af37 !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    /* SFONDO CARTA CREMA CALDO */
    .stApp {
        background-color: #f5eedc !important; 
        background-image: url("https://www.transparenttextures.com/patterns/natural-paper.png");
    }
    
    /* SIDEBAR CUOIO */
    [data-testid="stSidebar"] {
        background-color: #1a0f08 !important;
        border-right: 2px solid #d4af37;
    }
    [data-testid="stSidebar"] * { color: #e5d3b3 !important; }

    /* CAMPI INPUT: Grigio Perla per risaltare */
    .stTextInput input, .stTextArea textarea {
        background-color: #ececec !important; /* Grigio Perla */
        border: 1px solid #d1c7ac !important;
        color: #1a0f08 !important;
        font-family: 'EB Garamond', serif !important;
        font-size: 1.2rem !important;
    }
    
    /* Effetto Focus sui campi */
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #d4af37 !important;
        box-shadow: 0 0 5px rgba(212, 175, 55, 0.5) !important;
    }

    /* CARD POESIA */
    .poesia-card {
        background: #fffef9;
        border: 1px solid #e5d3b3;
        padding: 40px;
        box-shadow: 10px 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 30px;
    }

    /* ICONE SOCIAL ORO */
    .social-icon { 
        width: 32px; 
        filter: sepia(100%) saturate(500%) brightness(80%); 
        margin: 0 8px;
        transition: 0.3s;
    }
    .social-icon:hover { transform: scale(1.25); filter: brightness(110%); }

    /* BOTTONI LINK */
    .btn-custom {
        background-color: #7d1d1d;
        color: #f5eedc !important;
        padding: 12px 25px;
        text-decoration: none;
        font-family: 'Playfair Display', serif;
        display: inline-block;
        margin: 5px;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR E NAVIGAZIONE ---
with st.sidebar:
    st.markdown("<h1 style='text-align:center; font-family:Playfair Display; color:#d4af37;'>Versi Liberi</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; opacity:0.6; font-size:0.8rem;'>L'inchiostro non sbiadisce</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    scelta = st.radio("INDICE", ["🏠 La Scrivania", "📜 La Bacheca", "🎁 Lo Scrigno"])
    
    st.markdown("<br><br>---", unsafe_allow_html=True)
    # SOCIAL: Instagram, Facebook, WhatsApp e Twitter
    st.markdown("""
        <div style="text-align:center;">
            <a href="https://instagram.com" target="_blank"><img class="social-icon" src="https://img.icons8.com/ios-filled/50/ffffff/instagram-new.png"/></a>
            <a href="https://facebook.com" target="_blank"><img class="social-icon" src="https://img.icons8.com/ios-filled/50/ffffff/facebook-new.png"/></a>
            <a href="https://wa.me/391234567890" target="_blank"><img class="social-icon" src="https://img.icons8.com/ios-filled/50/ffffff/whatsapp.png"/></a>
            <a href="https://twitter.com" target="_blank"><img class="social-icon" src="https://img.icons8.com/ios-filled/50/ffffff/twitter.png"/></a>
        </div>
        <p style="text-align:center; font-size:0.7rem; color:#d4af37; margin-top:10px; letter-spacing:1px;">COMMUNITY</p>
    """, unsafe_allow_html=True)

# --- PAGINE ---
if scelta == "🏠 La Scrivania":
    st.markdown("<h1 style='font-family:Playfair Display;'>✒️ Intingi la Penna</h1>", unsafe_allow_html=True)
    
    with st.form("form_scrivania", clear_on_submit=True):
        col1, col2 = st.columns([2,1])
        titolo = col1.text_input("Titolo dell'opera")
        autore = col2.text_input("La tua firma")
        
        testo = st.text_area("I tuoi versi", height=350, placeholder="Scrivi qui i tuoi pensieri...")
        
        # Conteggio sillabe
        sillabe = conta_sillabe(testo)
        st.markdown(f"<p style='text-align:right; font-family:EB Garamond; font-style:italic; color:#7d1d1d;'>Battiti (sillabe): {sillabe}</p>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        musica = c1.text_input("Link YouTube per il sottofondo")
        tag = c2.selectbox("Atmosfera", ["Poesia", "Umanesimo", "Visioni", "Riflessioni"])
        
        if st.form_submit_button("PUBBLICA L'OPERA"):
            if titolo and testo:
                res = invia_dati("Poesie", {
                    "titolo": titolo, 
                    "versi": testo, 
                    "autore": autore if autore else "Anonimo", 
                    "tag": tag, 
                    "video_url": musica
                })
                if res.status_code in [200, 201, 204]:
                    st.success("Versi affidati all'eternità.")
                    st.balloons()

elif scelta == "📜 La Bacheca":
    st.markdown("<h1 style='text-align:center; font-family:Playfair Display;'>Il Pensiero Diffuso</h1>", unsafe_allow_html=True)
    poesie = leggi_poesie()
    for p in poesie:
        st.markdown(f"""
            <div class="poesia-card">
                <small style="color:#7d1d1d; letter-spacing:2px;">{p.get('tag', 'POESIA').upper()}</small>
                <h2 style="font-family:Playfair Display; font-style:italic; font-size:2.5rem;">{p.get('titolo')}</h2>
                <div style="font-family:EB Garamond; font-size:1.6rem; line-height:1.7; white-space:pre-wrap;">{p.get('versi')}</div>
                <p style="text-align:right; margin-top:25px; font-style:italic; opacity:0.8;">— {p.get('autore')}</p>
            </div>
        """, unsafe_allow_html=True)
        if p.get('video_url'):
            st.video(p['video_url'])

elif scelta == "🎁 Lo Scrigno":
    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class="poesia-card" style="text-align:center;">
            <h2 style='font-family:Playfair Display;'>Un Gesto per Versi Liberi</h2>
            <p style='font-family:EB Garamond; font-size:1.4rem; line-height:1.6; padding:15px;'>
                Questa app è gestita per passione ed amore nei confronti dei versi poetici, <br>
                se ti fa piacere con una piccola offerta, ci aiuteresti a gestirla. Grazie.
            </p>
            <br>
            <a href="https://paypal.me/tuonome" class="btn-custom" target="_blank">DONA CON PAYPAL</a>
            <a href="https://stripe.com" class="btn-custom" style="background:#1a0f08;" target="_blank">DONA CON STRIPE</a>
            <p style="margin-top:20px; font-size:0.8rem; opacity:0.5;">Ogni contributo sostiene la cultura indipendente.</p>
        </div>
    """, unsafe_allow_html=True)
