from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from langchain_community.embeddings import SentenceTransformerEmbeddings
import numpy as np


#embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
model_name = "sentence-transformers/all-mpnet-base-v2"
# Create the embedding function
embedding_function = HuggingFaceEmbeddings(model_name=model_name)



#embedding_model = "dunzhang/stella_en_400M_v5"
#model = SentenceTransformer("dunzhang/stella_en_400M_v5", trust_remote_code=True)
"""
model = SentenceTransformer(
     "dunzhang/stella_en_400M_v5",
     trust_remote_code=True,
     device="cpu",
     config_kwargs={"use_memory_efficient_attention": False, "unpad_inputs": False}
 )


print(model.encode("playyyyyyyyyyyyyyyy"))

class SentenceTransformerEmbeddings:
    def __init__(self, model_name="dunzhang/stella_en_400M_v5"):
        self.model = SentenceTransformer(
            model_name,
            trust_remote_code=True,
            device="cpu",
            config_kwargs={"use_memory_efficient_attention": False, "unpad_inputs": False}
        )
    
    def embed_documents(self, texts):
        batch_size = 5
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = self.model.encode(batch)
            embeddings.extend(batch_embeddings.tolist())
        return embeddings
    
    def embed_query(self, text):
        embedding = self.model.encode(text)
        # Convert to list if numpy array
        if isinstance(embedding, np.ndarray):
            embedding = embedding.tolist()
        return embedding

# Create the embedding model using the wrapper
embedding_model = SentenceTransformerEmbeddings()


"""


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024,
    chunk_overlap=80,
    length_function=len,
    separators=["\n\n", "\n", ".", " ", ""]
)
