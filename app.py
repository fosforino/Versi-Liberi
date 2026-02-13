import streamlit as st
import requests
import json
import random

# --- CONFIGURAZIONE ---
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
        return res.json()
    except: return []

# --- ESTETICA ---
st.set_page_config(page_title="Versi Liberi", page_icon="✒️")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@1,700&family=Lora&display=swap');
    .stApp { background-color: #fdf6e3; }
    h1 { font-family: 'Playfair Display', serif; color: #8b4513; text-align: center; }
    .poesia-card {
        background-color: #ffffff; padding: 30px; border-radius: 12px;
        border-left: 6px solid #e76f51; box-shadow: 0 10px 20px rgba(0,0,0,0.05); margin-bottom: 30px;
    }
    .testo-card { font-family: 'Lora', serif; font-size: 1.25em; line-height: 1.7; white-space: pre-wrap; }
    .sostieni-btn { text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGAZIONE ---
scelta = st.sidebar.radio("Vai a:", ["🏠 Scrivania", "📜 Bacheca", "🎁 Sostieni lo Scrigno"])

if scelta == "🏠 Scrivania":
    st.title("Lo Scrigno delle Idee")
    st.image("https://images.unsplash.com/photo-1519791883288-dc8bd696e667?w=800", use_container_width=True)
    
    with st.form("form_creazione"):
        col1, col2 = st.columns(2)
        tit = col1.text_input("Titolo")
        aut = col2.text_input("Firma")
        txt = st.text_area("I tuoi versi o pensieri...", height=250)
        yt_link = st.text_input("Link Video YouTube (opzionale)", placeholder="https://www.youtube.com/watch?v=...")
        tg = st.selectbox("Categoria", ["Poesia", "Umanesimo", "Politica Culturale", "Visioni"])
        
        if st.form_submit_button("Affida allo Scrigno"):
            if tit and txt:
                res = invia_dati("Poesie", {"titolo": tit, "versi": txt, "autore": aut if aut else "Anonimo", "tag": tg, "video_url": yt_link})
                if res.status_code in [200, 201, 204]:
                    st.success("Pubblicato con successo!")
                    st.balloons()

elif scelta == "📜 Bacheca":
    st.title("Il Pensiero Diffuso")
    poesie = leggi_poesie()
    for p in poesie:
        with st.container():
            st.markdown(f"""<div class="poesia-card">
                <h2 style='margin:0;'>{p['titolo']}</h2>
                <p style='color:#e76f51;'>di {p['autore']} — {p['tag']}</p>
                <div class="testo-card">{p['versi']}</div>
            </div>""", unsafe_allow_html=True)
            # Se c'è un video, lo mostriamo sotto la card
            if p.get('video_url'):
                st.video(p['video_url'])
            st.markdown("---")

elif scelta == "🎁 Sostieni lo Scrigno":
    st.title("Un gesto di cultura")
    st.markdown("""
    Questo spazio è libero, gratuito e privo di pubblicità. 
    Se credi nel valore di questi pensieri e vuoi aiutarmi a sostenere le spese di manutenzione, 
    puoi offrire un contributo libero.
    """)
    st.button("☕ Offri un caffè simbolico (Link PayPal/Stripe)")
    st.info("Nota: Questa è una funzione dimostrativa. Inseriremo il tuo link reale tra poco!")
