import openai
import time
import streamlit as st
from html_code import icon_url, title_html, html_hide, styl, response_style
from dotenv import load_dotenv
import os

load_dotenv()


assistant_id = os.getenv("ASSISTANT_ID")
st.session_state.assistant_id = assistant_id

@st.cache_data
def load_data():
    time.sleep(2)

def process_query(user_query):
    user_image_url = "https://i.postimg.cc/15Q5F7Dd/imgbin-avatars-icon-businesswoman-icon-social-icon-png.png"
    assistant_image_url = "https://i.postimg.cc/MZPvpQNG/icon-1.png"

    if 'thread' not in st.session_state:
        st.session_state.thread = st.session_state.client.beta.threads.create()


    messages = st.session_state.client.beta.threads.messages.create(
        thread_id=st.session_state.thread.id,
        role="user",
        content=user_query
    )

    run = st.session_state.client.beta.threads.runs.create(
        thread_id=st.session_state.thread.id,
        assistant_id=st.session_state.assistant_id,
        instructions="Eres un asistente personal, con conocimientos sobre medicina y nuevas tecnologias.Contesta siempre en español y de forma educada"
    )
    while True:
        run_status = st.session_state.client.beta.threads.runs.retrieve(
            thread_id=st.session_state.thread.id,
            run_id=run.id
        )

        if run_status.status == 'completed':
            messages = st.session_state.client.beta.threads.messages.list(
                thread_id=st.session_state.thread.id
                
            )
            if "messages" not in st.session_state:
                st.session_state.messages = []

            for msg in messages.data:
                with st.container():
                    role = msg.role
                    content = msg.content[0].text.value
                    if role == "user":
                        st.markdown(f"<img src='{user_image_url}' style='display: inline-block; max-width: 40px; font-size: 40px; vertical-align: middle; margin-right: 10px;'> {content}", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<img src='{assistant_image_url}' style='display: inline-block; max-width: 40px; font-size: 40px; vertical-align: middle; margin-right: 10px;'> {content}", unsafe_allow_html=True)
                    st.write("---")
            break


def main():
    st.image(icon_url, width=700)
    #st.set_page_config(page_icon=icon_url, layout="centered")
    st.markdown(title_html, unsafe_allow_html=True)
    st.markdown(html_hide, unsafe_allow_html=True)
    st.sidebar.header("Instrucciones")
    st.sidebar.write("Preguntale a InnevaPharma cualquier cosa que desees saber. Ten en cuenta que nuestra IA requiere tiempo para poder contestar a sus preguntas de la mejor forma posible.")
    st.sidebar.image("https://i.postimg.cc/3xmDbwRF/logo-mychat-ia-ok-horizontal.png")


    if 'client' not in st.session_state:
        st.session_state.client = openai.OpenAI()

    if "processed_queries" not in st.session_state:
        st.session_state.processed_queries = []

    user_query = st.chat_input("¿En qué puedo ayudarte hoy?", key="chat")

    if  user_query: 
        st.session_state.processed_queries.append(user_query)
        try:
            with st.spinner("Pensando..."):
                process_query(user_query)
        except Exception as e:
            st.error(f"Ocurrió un error al procesar tu solicitud: {e}")

    load_data()

if __name__ == "__main__":
    main()
