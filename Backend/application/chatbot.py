import os
import requests
import json
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from typing import Optional, List, Dict, Any
from langchain_core.language_models.llms import LLM
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain.chains import LLMChain, RetrievalQA
from langchain.memory import ConversationBufferMemory
from fpdf import FPDF

load_dotenv()

class MyEmbeddings:
    def __init__(self, model_name="jinaai/jina-embeddings-v2-small-en"):
        self.model = SentenceTransformer(model_name, trust_remote_code=True)

    def __call__(self, text):
        if isinstance(text, str):
            return self.model.encode(text)

    def embed_documents(self, documents):
        return self.model.encode(documents)

    def embed_query(self, query):
        return self.model.encode(query)

class CustomLLM(LLM):
    model_name: str
    api_url: Optional[str] = None
    api_token: Optional[str] = None

    def __init__(self, model_name: str, **kwargs):
        kwargs["model_name"] = model_name
        super().__init__(**kwargs)
        self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        self.api_token = os.getenv("HF_API_TOKEN")
        if not self.api_token:
            raise ValueError("Please set the HF_API_TOKEN environment variable.")
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        headers = {"Authorization": f"Bearer {self.api_token}"}
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.7,
                "repetition_penalty": 1.2
            }
        }
        response = requests.post(self.api_url, headers=headers, json=payload)
        result = response.json()
        
        if isinstance(result, dict) and result.get("error"):
            raise Exception(f"HuggingFace API error: {result['error']}")
        
        generated_text = result[0].get("generated_text", "")
        return generated_text

    @property
    def _llm_type(self) -> str:
        return self.model_name

embedding_model = MyEmbeddings()
llm = CustomLLM(model_name="tiiuae/falcon-7b-instruct")

vectorstore = FAISS.load_local(
    r'E:\chatbot\admin\vector_store.bin',
    embedding_model,
    allow_dangerous_deserialization=True
)

# Prompt templates for other contexts
assignment_prompt = PromptTemplate(
    input_variables=["assignment_data", "user_query"],
    template=(
        "You are an AI assistant helping with assignments.\n"
        "Assignment details: {assignment_data}\n"
        "User query: {user_query}\n"
        "Provide a helpful and detailed response."
    )
)

programming_prompt = PromptTemplate(
    input_variables=["problem_statement", "user_query"],
    template=(
        "You are an AI assistant helping with programming assignments.\n"
        "Problem statement: {problem_statement}\n"
        "User query: {user_query}\n"
        "Provide a hint or solution while adhering to academic principles."
    )
)

faq_prompt = PromptTemplate(
    input_variables=["faq_data", "user_query"],
    template=(
        "You are an AI assistant answering frequently asked questions (FAQs).\n"
        "FAQ database: {faq_data}\n"
        "User query: {user_query}\n"
        "Provide the most relevant answer or respond with 'FAQ not found.'"
    )
)

# Chains for other contexts
assignment_chain = LLMChain(llm=llm, prompt=assignment_prompt, verbose=True)
programming_chain = LLMChain(llm=llm, prompt=programming_prompt, verbose=True)
faq_chain = LLMChain(llm=llm, prompt=faq_prompt, verbose=True)


def lecture_query(llm, vectorstore, query):
    prompt_template = """
    You are a document assistant that helps students understand lectures.
    Please provide the most accurate response based solely on the provided context.

    Context:
    {context}

    Question:
    {question}

    Assistant:
    """
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template
    )
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 10}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
    result = qa({"query": query})
    
    assistant_answer = result.get("result", "").strip()
    if "Assistant:" in assistant_answer:
        assistant_answer = assistant_answer.split("Assistant:")[1].strip()
    if "Question:" in assistant_answer:
        assistant_answer = assistant_answer.split("Question:")[0].strip()
    return assistant_answer

memory = ConversationBufferMemory()
chat_history = []

def chatbot(user_context, user_query):
    try:
        context_data = {
            "assignment": "Solve questions on calculus involving derivatives.",
            "programming": "Write a Python function to calculate Fibonacci numbers.",
            "faq": json.dumps({
                "What is Newton's first law?": "An object remains at rest or in uniform motion unless acted upon by a force.",
                "How to find derivatives?": "Use differentiation rules such as the power rule, product rule, etc."
            })
        }

        if user_context == "assignment":
            response = assignment_chain.predict(
                assignment_data=context_data["assignment"],
                user_query=user_query
            )
        elif user_context == "lecture":
            response = lecture_query(llm, vectorstore, user_query)

        elif user_context == "programming":
            response = programming_chain.predict(
                problem_statement=context_data["programming"],
                user_query=user_query
            )
        elif user_context == "faq":
            response = faq_chain.predict(
                faq_data=context_data["faq"],
                user_query=user_query
            )
        else:
            return "Invalid context provided."

        memory.save_context({"input": user_query}, {"output": response})
        return response

    except requests.exceptions.RequestException as e:
        return f"API Connection Error: {str(e)}"
    except Exception as e:
        return f"Processing Error: {str(e)}"

# Rest of the functions remain unchanged
def store_chat(user_input, bot_response):
    global chat_history
    chat_history.append({"User": user_input, "Bot": bot_response})

def export_chat_as_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for chat in chat_history:
        pdf.cell(200, 10, txt=f"User: {chat['User']}", ln=True)
        pdf.cell(200, 10, txt=f"Bot: {chat['Bot']}", ln=True)
    
    pdf.output("chat_history.pdf")

def extract_final_answer(response: str, marker: str = "Provide a helpful and detailed response.") -> str:
    if marker in response:
        return response.split(marker, 1)[-1].strip()
    return response.strip()

if __name__ == "__main__":
    # Test lecture query
    response = chatbot(
        user_context="lecture",
        user_query="Explain Newton's laws of motion"
    )
    print(response)