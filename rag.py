import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from llama_index.readers.file import PyMuPDFReader
from llama_index.core import SimpleDirectoryReader
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
import tempfile

# Charger les variables d'environnement
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configuration globale de LlamaIndex
Settings.llm = OpenAI(api_key=OPENAI_API_KEY, model="gpt-4o-mini")
Settings.embed_model = OpenAIEmbedding(api_key=OPENAI_API_KEY, model="text-embedding-3-small")
Settings.text_splitter = SentenceSplitter(chunk_size=500, chunk_overlap=50)

# Initialiser ChromaDB
chroma_client = chromadb.PersistentClient(path="./storage")
chroma_collection = chroma_client.get_or_create_collection("documents")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# Variable globale pour l'index
index = None


def index_document(uploaded_file):
    """
    Reçoit un fichier uploadé via Streamlit,
    l'indexe et le sauvegarde dans ChromaDB.
    """
    global index

    # Sauvegarder le fichier temporairement sur le disque
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = os.path.join(tmp_dir, uploaded_file.name)
        with open(tmp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Lire le document selon son type
        if uploaded_file.name.lower().endswith(".pdf"):
            reader = PyMuPDFReader()
            documents = reader.load(file_path=tmp_path)
        else:
            documents = SimpleDirectoryReader(tmp_dir).load_data()

        # Créer l'index avec ChromaDB comme vector store
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            show_progress=True
        )

    return index


def query(question: str) -> str:
    """
    Reçoit une question, cherche les chunks pertinents
    et retourne la réponse générée par Gemini.
    """
    global index

    if index is None:
        # Si aucun doc n'a été indexé dans cette session, charger depuis ChromaDB
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)

    query_engine = index.as_query_engine(similarity_top_k=3)
    response = query_engine.query(question)
    return str(response)