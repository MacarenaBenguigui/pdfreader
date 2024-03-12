import os
from dotenv import load_dotenv
import streamlit as st
from llama_index.query_engine import PandasQueryEngine
from prompt import new_prompt, instruction_str, context
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers import PDFReader
from html_code import icon_url, title_html, generate_html_with_icon, html_hide
from archivos import portfolio_engine


load_dotenv()

#Lectura de PDFs

tools = [

     QueryEngineTool(query_engine=portfolio_engine, 
                    metadata=ToolMetadata(
                    name = "portfolio_data",
                    description = " this gives information about the portfolio of Innevapharma",

        ),
    ),
]


llm = OpenAI(model = "gpt-3.5-turbo-16k")
agent = ReActAgent.from_tools(tools, llm = llm, verbose =True, context= context)

query_icon_url = "https://i.postimg.cc/mDCmmtp8/Logo2-sinfondo-x1024.png"
response_icon_url = "https://i.postimg.cc/hts2XXfd/pngaaa-com-3704853.png"

# Interfaz de usuario para ingreso de consultas
st.set_page_config (page_title= "InnevaChatBot", page_icon=icon_url, layout="wide")
st.markdown(title_html, unsafe_allow_html=True)
st.markdown(html_hide, unsafe_allow_html=True)

user_query = st.text_input("¿En que puedo ayudarte hoy?")

if 'queries' not in st.session_state:
    st.session_state['queries'] = []

if user_query:  
    response_object = portfolio_engine.query(user_query)
    response_text = response_object.response
    
    st.session_state['queries'].append({'query': user_query, 'response': response_text})

    st.session_state['query_input'] = ""  

# Muestra las consultas y respuestas previas
for pair in st.session_state['queries']:
     # Generar y mostrar el HTML para la consulta y la respuesta
    query_html = generate_html_with_icon(query_icon_url, pair["query"],icon_size="50px")
    response_html = generate_html_with_icon(response_icon_url, pair["response"],icon_size="50px")

    st.markdown(query_html, unsafe_allow_html=True)
    st.markdown(response_html, unsafe_allow_html=True)
    st.write("---")  # Para añadir una línea divisoria por estética
