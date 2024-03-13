import os
from dotenv import load_dotenv
import streamlit as st
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.agent import ReActAgent, OpenAIAgent
from llama_index.llms.openai import OpenAI
from html_code import icon_url, title_html, generate_html_with_icon, html_hide, styl
from archivos import portfolio_engine, adjuvant_engine,suppplement_engine,opdivo_engine


load_dotenv()

#Lectura de PDFs

tools = [

     QueryEngineTool(query_engine=portfolio_engine, 
                    metadata=ToolMetadata(
                    name = "portfolio_data",
                    description = " Nos da informacion sobre innevapharma y sus productos",

        ),
    ),
       QueryEngineTool(query_engine=adjuvant_engine, 
                    metadata=ToolMetadata(
                    name = "adjuvant_data",
                    description = "Nos da informacion sobre adjuvant y sus productos",

        ),
    ),
     QueryEngineTool(query_engine=suppplement_engine, 
                    metadata=ToolMetadata(
                    name = "suppplement_data",
                    description = "Nos da informacion sobre los suplementos y sus productos",

        ),
    ),
      QueryEngineTool(query_engine=opdivo_engine, 
                    metadata=ToolMetadata(
                    name = "opdivo_data",
                    description = "Nos da informacion sobre opdivio y sus productos",

        ),
    ),
]


#ChatGPT
context= "La función principal de este agente es asistir a los usuarios proporcionando información precisa sobre los PDFs que el usuario sube a la aplicación, de forma educada, sin decir nunca que es una IA y tampoco hacer referencia jamás al nombre del archivo que tiene adjunto.Además, siempre responderá en español, independientemente del lenguaje del PDF. Dará respuestas largas donde explique bien todo sobre lo que habla. Siempre que termines una frase, y siempre dará respuestas en Español"
llm = OpenAI(model = "gpt-3.5-turbo-16k")
agent = ReActAgent.from_tools(tools, llm = llm, 
                              verbose = True, 
                              context= "Todas tus respuestas serán siempre en español. La función principal de este agente es asistir a los usuarios proporcionando información precisa sobre los PDFs que el usuario sube a la aplicación, de forma educada, sin decir nunca que es una IA y tampoco hacer referencia jamás al nombre del archivo que tiene adjunto.Además, siempre responderá en español, independientemente del lenguaje del PDF. Dará respuestas largas donde explique bien todo sobre lo que habla. Siempre que termines una frase, dices miaw, y siempre dará respuestas en Español" )



#APP configuration
st.set_page_config (page_title= "InnevaChatBot", page_icon=icon_url, layout="wide")
st.markdown(title_html, unsafe_allow_html=True)
st.markdown(html_hide, unsafe_allow_html=True)


if "widget" not in st.session_state:
    st.session_state.widget = ""
if "queries" not in st.session_state:
    st.session_state['queries'] = []
if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []
if "context" not in st.session_state:
    st.session_state['context'] = context

#Por si solo quieres seleccionar un PDF (ahora mismo te puede responder sobre todos, pero tarda más)
engine_options = ["portfolio_data", "adjuvant_data", "suppplement_data", "opdivo_data"]
#selected_engine = st.selectbox("Select the query engine:", engine_options)
selected_engine = engine_options


def update_context_with_query(user_query, response_text):
    new_entry = {"query": user_query, "response": response_text}
    st.session_state['chat_history'].append(new_entry)
    # Re-construir y actualizar el contexto basado en el historial de chat completo
    st.session_state['context'] = "\n".join([f"Pregunta: {entry['query']}\nRespuesta: {entry['response']}" for entry in st.session_state['chat_history']])


# Función para manejar la entrada de consulta y añadirla a 'queries'
def submit_text():
    user_query = st.session_state.widget.strip()
    st.session_state.widget = ""
    if user_query:
         with st.spinner("Pensando..."):
            update_context_with_query(user_query, "")
            try:
                response_object = agent.query(f"{st.session_state.get('context', '')} {user_query}")
                response_text = response_object.response if hasattr(response_object, 'response') else "Respuesta no disponible"
                update_context_with_query(user_query, response_text)
            except Exception as e:
                response_text = f"Error al procesar la consulta: {e}"

            st.session_state['queries'].append({'query': user_query, 'response': response_text})
           

if st.button('Borrar Historial de Chat'):
    st.session_state['queries'] = []
    st.session_state['chat_history'] = []
    st.session_state['context'] = []
    st.experimental_rerun()


# Crear un input de texto para nuevas consultas
with st.form("query_form"):
    user_input = st.text_input("¿En qué puedo ayudarte hoy?", value="", key="widget")
    submitted = st.form_submit_button("Enviar", on_click=submit_text)

query_icon_url = "https://i.postimg.cc/15Q5F7Dd/imgbin-avatars-icon-businesswoman-icon-social-icon-png.png"
response_icon_url = "https://i.postimg.cc/mDCmmtp8/Logo2-sinfondo-x1024.png"

for pair in st.session_state.get('queries', []):
    query_html = generate_html_with_icon(query_icon_url, pair["query"], icon_size="50px")
    response_html = generate_html_with_icon(response_icon_url, pair["response"], icon_size="50px")
    st.markdown(query_html, unsafe_allow_html=True)
    st.markdown(response_html, unsafe_allow_html=True)
    st.write("---")  # Para añadir una línea divisoria por estética   Tengo este script para manejar las lecturas de PDFs  u otros documentos y obtener respuestas sobre el
