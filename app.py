import streamlit as st
from PIL import Image
from crew import AnthomAICrew

LOGO = Image.open("media/logo.webp")
st.set_page_config(page_title="AnthemAI Agents - The €15k You Didn't Spend", layout="centered")

with st.sidebar:
    st.image(LOGO)
    st.markdown("---")
    st.markdown(
        "### How it works\n"
        "1. Enter literally any topic\n\n"
        "2. Pick a music genre\n\n"
        "3. Click the button\n\n"
        "4. Congratulations, you just saved €15,000\n\n"
    )
    st.markdown("---")
    st.markdown(
        "### The Magic Behind The Savings\n"
        "**Research Agent** → Googles your topic like an unpaid intern\n\n"
        "**Lyrics Agent** → Writes your anthem (no conservatory degree required)\n\n"
        "**Suno Agent** → Generates two songs because why pay a studio?\n\n"
    )

st.markdown("<h1 style='text-align: center;'>🎵 AnthemAI </h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Inspired by : <a href='https://executivedigest.sapo.pt/centeno-tera-gasto-15-mil-euros-num-hino-a-glorificar-o-seu-mandato-no-banco-de-portugal/' target='_blank'>Article</a></h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Cost: €0.00 | Savings: €15,000.00</p>", unsafe_allow_html=True)
st.markdown("---")

topic = st.text_area(
    "What's your anthem about?", 
    height=80, 
    value="",
    placeholder="e.g., 'My glorious leadership' or 'That bank I run'"
)

genre = st.text_area(
    "Pick your genre:", 
    height=80, 
    value="",
    placeholder="e.g., 'Epic Orchestral' or 'Motivational Pop'"
)

st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("💸 Save €15k", use_container_width=True, type="primary"):
        if not (topic and genre):
            st.warning("Even free anthems need a topic and genre!")
        else:
            with st.spinner("AI agents working for free..."):
                anthomai = AnthomAICrew(topic, genre)
                result = anthomai.run()
                
            st.success("✅ Your anthem is ready! That'll be €0, please.")
            st.markdown(result)
            st.balloons()

st.markdown("---")
st.caption("Disclaimer: No Portuguese bank budgets were harmed in the making of this app")