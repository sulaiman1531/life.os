import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document

VECTOR_STORE_PATH = "./faiss_memory"

class MemoryStore:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.vector_store = None
        if self.api_key:
            try:
                self.embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=self.api_key)
                self._load_or_create()
            except Exception as e:
                print("Failed to initialize embeddings/FAISS due to API issue:", e)
                self.vector_store = None
    
    def _load_or_create(self):
        if os.path.exists(VECTOR_STORE_PATH):
            try:
                self.vector_store = FAISS.load_local(VECTOR_STORE_PATH, self.embeddings, allow_dangerous_deserialization=True)
            except Exception as e:
                print("Failed to load FAISS index:", e)
                self.vector_store = FAISS.from_documents([Document(page_content="System Initialized.")], self.embeddings)
        else:
            self.vector_store = FAISS.from_documents([Document(page_content="System Initialized.")], self.embeddings)
            
    def add_memory(self, text: str, metadata: dict = None):
        if not self.vector_store:
            return
        try:
            doc = Document(page_content=text, metadata=metadata or {})
            self.vector_store.add_documents([doc])
            self.vector_store.save_local(VECTOR_STORE_PATH)
        except Exception as e:
            print("Could not add memory:", e)
        
    def search_memory(self, query: str, k: int = 3):
        if not self.vector_store:
            return []
        try:
            results = self.vector_store.similarity_search(query, k=k)
            return [doc.page_content for doc in results]
        except Exception as e:
            print("Could not search memory:", e)
            return []

# Global singleton
memory = MemoryStore()
