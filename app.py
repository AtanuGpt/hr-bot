import os
import faiss
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.vector_stores.faiss import FaissVectorStore
import azure.cognitiveservices.speech as speechsdk

d = 1536
faiss_index = faiss.IndexFlatL2(d)
PERSIST_DIR = "./storage"

load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")

def fetchData(user_question):
    try:
        vector_store = FaissVectorStore.from_persist_dir("./storage")
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store, persist_dir=PERSIST_DIR
        )
        index = load_index_from_storage(storage_context=storage_context)
        query_engine = index.as_query_engine()
        response = query_engine.query(user_question)
        return str(response)
    except:
        return "Error"

#============================================================================================================
WelcomeMessage = """Hello, I am your HR Bot. I would try my best to answer your question from my knowledge-base"""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content=WelcomeMessage)
    ]

#speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
#speech_config.speech_synthesis_voice_name = "en-US-AvaNeural"
#speech_config.speech_synthesis_language = "en-US"
#speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config)

def main():

    st.set_page_config(
        page_title="Chat with HR Bot",
        page_icon=":sparkles:"
    )

    st.header("Chat with HR Bot :sparkles:")   

    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)     

  
    user_question = st.chat_input("Ask your question : ")

    if user_question is not None and user_question != "":
        st.session_state.chat_history.append(HumanMessage(content=user_question))

        with st.chat_message("Human"):
            st.markdown(user_question)
        
        with st.chat_message("AI"):
            with st.spinner("Fetching data ..."):
                response = fetchData(user_question)
                st.markdown(response)
         
        #speech_synthesizer.speak_text(response)
        st.session_state.chat_history.append(AIMessage(content=response))
    
    if "WelcomeMessage" not in st.session_state:
        st.session_state.WelcomeMessage = WelcomeMessage
        #result = speech_synthesizer.speak_text(WelcomeMessage).get()

#============================================================================================================
if __name__ == '__main__':
    main()





