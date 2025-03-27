from typing import Optional
import os
from dotenv import load_dotenv
from .utils import crntdir
import requests
from langchain.schema import Document
import json
from pymilvus import MilvusClient, FieldSchema, CollectionSchema, DataType
from langchain_core.embeddings.embeddings import Embeddings
from pdf2image import convert_from_path
import pytesseract
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

# Load API-Key
load_dotenv()

# Embedding class
class MyEmbeddings(Embeddings):
    model_name: str
    api_url: Optional[str] = None
    api_token: Optional[str] = None
    def __init__(self, model_name: str, **kwargs):
        kwargs["model_name"] = model_name
        super().__init__()
        self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        self.api_token = os.getenv("HF_API_TOKEN")
        if not self.api_token:
            raise ValueError("Please set the HF_API_TOKEN environment variable.")

    def encode(self, prompt) :
        headers = {"Authorization": f"Bearer {self.api_token}"}
        payload = {
            "inputs": prompt,
        }
        response = requests.post(self.api_url, headers=headers, json=payload)
        try:
            result = response.json()
            return result
        except:
            result = None
            print(response.content)
        if isinstance(result, dict) and result.get("error"):
            raise Exception(f"HuggingFace API error: {result['error']}")
        
        generated_text = result[0].get("generated_text", "")
        return generated_text
    def __call__(self, text):
        return self.encode(text)

    def embed_documents(self, documents):
        return self.encode(documents)

    def embed_query(self, query):
        return self.encode(query)

embedder = MyEmbeddings("jinaai/jina-embeddings-v2-small-en")

# client
client = MilvusClient(crntdir + '/instance/vector.db')

# Vector Store
fields =  [
        FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True, max_length=20),
        FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=512, max_length=512),
        FieldSchema(name='course_id', dtype=DataType.VARCHAR, max_length=3),
        FieldSchema(name='material_name', dtype=DataType.VARCHAR, max_length=500),
        FieldSchema(name='material_content', dtype=DataType.VARCHAR, max_length=5000)
    ]

schema = CollectionSchema(fields, description='Course Doc')

if 'course_docs' not in client.list_collections() :
    collection = client.create_collection('course_docs', schema=schema)

index_params = MilvusClient.prepare_index_params()

index_params.add_index(
    field_name="embedding",
    metric_type="COSINE",
    index_type="IVF_FLAT",
    index_name="vector_index",
    params={ "nlist": 128 }
)

if 'vector_index' not in client.list_indexes(collection_name='course_docs'):
    client.create_index(
        collection_name="course_docs",
        index_params=index_params,
        sync=False # Whether to wait for index creation to complete before returning. Defaults to True.
    )


def requires_ocr(pdf_path):
    """Check if OCR is needed by attempting to extract text."""
    try:
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        for page in pages[:5]:
            if page.page_content.strip():
                return False
        return True
    except Exception as e:
        return True

def perform_ocr(pdf_path):
    """Perform OCR on a PDF and return extracted text as Document objects."""
    images = convert_from_path(pdf_path)  
    docs = []
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        docs.append(Document(page_content=text, metadata={"page": i + 1, "source": os.path.basename(pdf_path)}))
    return docs

def load_pdf(file_path):
    """Load and split text-based PDF into pages."""
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    pdf_name = os.path.basename(file_path)
    for page in pages:
        page.metadata["source"] = pdf_name
    return pages

def split_text(pages, chunk_size, chunk_overlap):
    """Split text into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(pages)
    return docs

def load_or_create_vector_store():
    """Load or create the vector store."""
    if os.path.exists(VECTOR_STORE_FILE):
        return FAISS.load_local(VECTOR_STORE_FILE, embedding_model, allow_dangerous_deserialization=True)
    else:
        return None

def update_vector_store(new_docs, course_id, material_name):
    """Update the vector store with new documents."""
    records = []
    for doc in new_docs :
        records.append({
            'embedding': embedder(doc.page_content),
            'course_id': str(course_id),
            'material_name': material_name,
            'material_content': doc.page_content
            })
    
    client.insert(collection_name='course_docs', data=records)

def process_uploaded_file(file_path):
    """Process uploaded file with or without OCR."""
    if requires_ocr(file_path):
        return perform_ocr(file_path)
    else:
        return load_pdf(file_path)

def upload_file(upload_file_path, course_id, title):

    if upload_file:
        all_docs = []

        docs = process_uploaded_file(upload_file_path)
        docs = split_text(docs, 1000, 200)
        all_docs.extend(docs)


        if all_docs:
            update_vector_store(all_docs, course_id, title)

def delete_file(course_id, title):
    
    res = client.delete(
        collection_name='course_docs',
        filter=f'course_id like \'{course_id}\' and material_name like \'{title}\''
    )

def update_file(upload_file_path, course_id, old_title, new_title) :

    res = delte_file(course_id, old_title)

    res = uploaded_file(upload_file_path, course_id, new_title)
