# engine.py
import os
import chromadb
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Load environment variables
load_dotenv()

# --- MODEL CONFIGURATION ---
# Switching to 1.5-flash for a much higher Free Tier Quota (RPM/RPD)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1)
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

COLLECTION_NAME = "current_active_pdf"

# Professional RAG Prompt
template = """
You are a "PDF Document Assistant". Use the provided context to answer the question accurately.
If the answer is not in the context, state that you cannot find the information in this document.

Context: {context}
History: {history}
Question: {question}

Answer:"""
prompt = ChatPromptTemplate.from_template(template)

def process_pdf(file_path):
    """Parses PDF and completely resets the vector memory to prevent hallucinations."""
    try:
        # 1. Force Reset the In-Memory Collection
        client = chromadb.EphemeralClient() 
        try:
            client.delete_collection(COLLECTION_NAME)
            print(f"🗑️ Memory Cleared for new document.")
        except Exception:
            pass

        # 2. Load and Chunk PDF
        loader = PyPDFLoader(file_path)
        data = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
        splits = text_splitter.split_documents(data)
        
        # 3. Create Fresh Vector Store
        vector_store = Chroma.from_documents(
            documents=splits, 
            embedding=embeddings_model,
            collection_name=COLLECTION_NAME,
            client=client
        )
        
        return vector_store.as_retriever(search_kwargs={'k': 4})
    except Exception as e:
        print(f"❌ Error in indexing: {e}")
        return None

def get_chat_response(message, history, retriever):
    """Retrieves context, generates answer, and appends page citations."""
    if retriever is None:
        yield "Please upload and initialize a PDF first."
        return

    try:
        # 1. Retrieval of Chunks and Metadata
        docs = retriever.invoke(message)
        
        # 2. Extract unique page numbers (PyPDFLoader is 0-indexed)
        pages = sorted(list(set([str(doc.metadata.get('page', 0) + 1) for doc in docs])))
        citation = f"\n\n📍 **Source:** Page(s) {', '.join(pages)}"

        # 3. Format History for Contextual Awareness
        formatted_history = ""
        for entry in history:
            role = entry.get("role", "user")
            content = entry.get("content", "")
            formatted_history += f"{role}: {content}\n"

        # 4. RAG Chain Definition
        rag_chain = (
            {
                "context": lambda x: "\n\n".join(d.page_content for d in docs), 
                "question": RunnablePassthrough(), 
                "history": lambda x: formatted_history
            }
            | prompt 
            | llm 
            | StrOutputParser()
        )

        # 5. Streaming output with Citation append
        partial_message = ""
        for chunk in rag_chain.stream(message):
            partial_message += chunk
            yield partial_message
        
        # Add citations at the very end of the stream
        yield partial_message + citation

    except Exception as e:
        # Graceful Quota Handling
        if "429" in str(e):
            yield "⚠️ **Quota Limit Reached.** Please wait 60 seconds. Gemini 1.5 Flash allows more requests, but you may be moving too fast for the free tier!"
        else:
            yield f"⚠️ **An Error Occurred:** {str(e)}"