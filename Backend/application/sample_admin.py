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
            response = requests.post(self.api_url, headers=headers, json=payload)
            result = response.json()
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

fields_2 =  [
        FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True, max_length=20),
        FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=512, max_length=512),
        FieldSchema(name='course_id', dtype=DataType.VARCHAR, max_length=3),
        FieldSchema(name='title', dtype=DataType.VARCHAR, max_length=500),
        FieldSchema(name='description', dtype=DataType.VARCHAR, max_length=2000),
        FieldSchema(name='material_content', dtype=DataType.VARCHAR, max_length=2000)
    ]

schema = CollectionSchema(fields, description='Course Doc')
schema_2 = CollectionSchema(fields_2, description='Reference links')

if 'course_docs' not in client.list_collections() :
    collection = client.create_collection('course_docs', schema=schema)

if 'reference_links' not in client.list_collections() :
    collection2 = client.create_collection('reference_links', schema=schema_2)

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

if 'vector_index' not in client.list_indexes(collection_name='reference_links'):
    client.create_index(
        collection_name='reference_links',
        index_params=index_params,
        sync=False
    )

if client.get_collection_stats('reference_links')['row_count'] == 0 :
    links = [
        {
            'course_id': '1',
            'title': 'What is Python? | Python Explained in 2 Minutes For BEGINNERS.',
            'description': ' how to start learning Python for free and what is python ',
            'material_content': 'https://www.youtube.com/watch?v=QoIRX37VZpo'
        },
        {
            'course_id': '1',
            'title': 'Replit in 60 seconds',
            'description': "Learn how Replit's cloud-native environment, AI-assisted features, and collaborative tools make coding accessible to all skill levels. Explore integrated features like databases and deployments, and even code on your phone with the Replit app ",
            'material_content': 'https://www.youtube.com/watch?v=TiHq41h3nDo'
        },
        {
            'course_id': '1',
            'title': 'Python Tutorial in 30 Minutes (Crash Course for Absolute Beginners)',
            'description': "In this tutorial, we’ll be looking at comments, variables, data types, strings, booleans, operators, lists, tuples, sets, dictionaries, loops, objects and a lot more!!",
            'material_content': 'https://www.youtube.com/watch?v=WEm3EUdicDg'
        },
        {
            'course_id': '1',
            'title': 'Python for Everybody (PY4E)',
            'description': "Everything about python",
            'material_content': 'https://www.py4e.com/lessons'
        },

    ]

    print(embedder(links[0]['description']))
    for link in links :
        link['embedding'] = embedder(link['description'])

    client.insert(collection_name='reference_links', data=links)


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

    res = delete_file(course_id, old_title)

    res = uploaded_file(upload_file_path, course_id, new_title)