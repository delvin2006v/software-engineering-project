import os
import requests
import json
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any
from langchain_core.language_models.llms import LLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from fpdf import FPDF

load_dotenv()

import os
import requests
from typing import List, Optional

# Custom LLM class
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

# the custom LLM using the API endpoint
llm = CustomLLM(model_name="tiiuae/falcon-7b-instruct")

# prompt templates
assignment_prompt = PromptTemplate(
    input_variables=["assignment_data", "user_query"],
    template=(
        "You are an AI assistant helping with assignments.\n"
        "Assignment details: {assignment_data}\n"
        "User query: {user_query}\n"
        "Provide a helpful and detailed response."
        
    )
)

lecture_prompt = PromptTemplate(
    input_variables=["lecture_data", "user_query"],
    template=(
        "You are an AI assistant helping students understand lectures.\n"
        "Lecture content: {lecture_data}\n"
        "User query: {user_query}\n"
        "Provide a clear and concise explanation."
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

#LLM chain with the prompts and llms
assignment_chain = LLMChain(llm=llm, prompt=assignment_prompt, verbose=True)
lecture_chain = LLMChain(llm=llm, prompt=lecture_prompt, verbose=True)
programming_chain = LLMChain(llm=llm, prompt=programming_prompt, verbose=True)
faq_chain = LLMChain(llm=llm, prompt=faq_prompt, verbose=True)

# memory and chat history
memory = ConversationBufferMemory()
chat_history = []

def chatbot(user_context, user_query):
    """
    Enhanced chatbot function with proper input handling.
    """
    try:
        context_data = {
            "assignment": "Solve questions on calculus involving derivatives.",
            "lecture": "Today's lecture is about Newton's laws of motion.",
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
            response = lecture_chain.predict(
                lecture_data=context_data["lecture"],
                user_query=user_query
            )
            
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

        # Save interaction in conversation memory
        memory.save_context(
            {"input": user_query},
            {"output": response}
        )
        return response

    except requests.exceptions.RequestException as e:
        return f"API Connection Error: {str(e)}"
    except Exception as e:
        return f"Processing Error: {str(e)}"

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
    """
    Returns everything after the marker in the given response.
    """
    if marker in response:
        return response.split(marker, 1)[-1].strip()
    return response.strip()

if __name__ == "__main__":
    # Example usage
    response = chatbot(
        user_context="assignment",
        user_query="Can you explain how to find derivatives?"
    )
    
    print(response)
    