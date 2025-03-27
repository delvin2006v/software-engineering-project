from langchain_core.language_models.llms import LLM
from typing import Optional, List, Dict, Any, Sequence
import os
from dotenv import load_dotenv
from .utils import output, crntdir
import requests
from .models import Course
import json
from langchain_core.messages import BaseMessage
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.chat_history import BaseChatMessageHistory
from youtube_transcript_api import YouTubeTranscriptApi
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableWithMessageHistory, RunnableLambda
from .sample_admin import embedder, client
import uuid
import markdown

ytt_api = YouTubeTranscriptApi()

chat_dir = crntdir + '/static/chats'


# Load API-Key
load_dotenv()

# LLM Class
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
                "temperature": 0.25,
                "repetition_penalty": 1.2
            }
        }
        response = requests.post(self.api_url, headers=headers, json=payload)
        # return response.text
        result = response.json()
        
        if isinstance(result, dict) and result.get("error"):
            raise Exception(f"HuggingFace API error: {result['error']}")
        print('\n', '-'*30)
        print(result)
        print('\n', '-'*30)
        generated_text = result[0].get("generated_text", "")
        return generated_text.split('<-->')[-1].strip('\n ')

    @property
    def _llm_type(self) -> str:
        return self.model_name

# LLM Object
llm = CustomLLM(model_name="google/gemma-2-2b-it")

# to format the history to string
def format_history(history: List[BaseMessage]) -> str:
    if not history :
        return None
    return "\n".join([f"{msg.type}: {msg.content}" for msg in history])

def format_transcript(transcript) -> str:
    return "\n".join([f"{msg.text}" for msg in transcript])

def format_document(docs) :
    if not docs:
        return None        
    return '\n'.join(doc['entity']['material_content'] for doc in docs)

# to retrieve from sql db
def retrieve_sql_data(course_id, section_id, content_id, question_id=None) :
    course_content = json.loads(Course.query.filter_by(id=course_id).first().content)

    for section in course_content :
        if section['id'] == section_id :
            for content in section['items'] :
                if content['id'] == content_id :
                    if not question_id :
                        return content
                    else :
                        for question in content['questions'] :
                            if question['id'] == question_id :
                                return question
    return None

def retrieve_document(course_id, query) :
    result = client.search(
        collection_name='course_docs',
        data=[embedder(query)],
        filter=f'course_id like \'{course_id}\'',
        limit=3,
        output_fields=['material_name', 'material_content'],
        search_params={
                'metric_type': "COSINE"
        },
        anns_field='embedding'
    )
    if len(result) > 0 :
        return result[0]
    else :
        return None

def format_items(items) :
    return '\n'.join(str(i) + '. ' + items[i] for i in range(len(items)))

def format_cases(cases) :
    return '\n'.join(str(i) + '. ' + cases[i]['input'] + '\n' + cases[i]['output'] for i in range(len(cases)))

#------------------------------------
#           Prepare input
#------------------------------------
def prepare_lecture_input(input_dict) :

    # Parsing the tag
    course_id, section_id, content_id = [int(x) for x in input_dict['tag'].split('-')]
    
    # retrieve lecture data
    lecture_data = retrieve_sql_data(course_id, section_id, content_id)
    document = retrieve_document(course_id, input_dict['user_query'])

    lecture_data['transcript'] = format_transcript(ytt_api.fetch(lecture_data['url'].split('/')[-1]))

    return {
        'lecture_data': lecture_data,
        'history': format_history(input_dict['history']),
        'user_query': input_dict['user_query'],
        'resources': None, # TBA
        'document': format_document(document)
    }

def prepare_assignment_input(input_dict) :

    # Parsing the tag
    course_id, section_id, content_id, question_id = [int(x) for x in input_dict['tag'].split('-')]
    
    # retrieve lecture data
    assignment_data = retrieve_sql_data(course_id, section_id, content_id, question_id)

    # retrieve document
    document = retrieve_document(course_id, input_dict['user_query'])

    return {
        'assignment_data': assignment_data,
        'history': format_history(input_dict['history']),
        'user_query': input_dict['user_query'],
        'resources': None, # TBA
        'document': format_document(document)
    }

def prepare_programming_assignment_input(input_dict) :

    # Parsing the tag
    course_id, section_id, content_id = [int(x) for x in input_dict['tag'].split('-')]

    programming_assignment_data = retrieve_sql_data(course_id, section_id, content_id)

    return {
        'programming_assignment_data': programming_assignment_data,
        'history': format_history(input_dict['history']),
        'user_query': input_dict['user_query'],
        'code': input_dict['code'],
        'resources': None, # TBA
        'document': None
    }

def prepare_course_doubt_input(input_dict) :
    course_id = int(input_dict['tag'])

    document = retrieve_document(course_id, input_dict['user_query'])

    return {
        'history': format_history(input_dict['history']),
        'user_query': input_dict['user_query'],
        'document': format_document(document),
        'resources': None # TBA
    }

#------------------------------------
#        Prompt sub templates
#------------------------------------

header = '''
    You are an AI-Agent helping students to clear their doubts regarding the course.
    The instructions are given in the INSTRUCTIONS section.

    INSTRUCTIONS:
    - Be kind and polite in answering the student queries.
    - Some sections may or may not exist
    - The CONTEXT section determines the context of the query.
    - The DATA section contains the data, use this to answer the user query.
    - The QUERY section contains the student query that needs to be answered.
    - Give your answer in the Markdown format.

    '''

footer = '''<-->'''

history_temp = '''
    HISTORY:
    {}
    '''

doc_temp = '''
    DOCUMENT:
    {}
    '''

res_temp = '''
    RESOURCES:
    {}
'''

query_temp = '''
    QUERY:
    {}
'''
#------------------------------------
#        Prompt Gen Functions
#------------------------------------

# function to create prompt
def make_prompt(context, data, history, document, resources, query) :

    prompt_string = header + context

    if data :
        prompt_string += data

    if history :
        prompt_string += history

    if document :
        prompt_string += document

    if resources :
        prompt_string += resources

    prompt_string += query
    prompt_string += footer

    return prompt_string

# Lecture prompt
def lecture_prompt(input_dict) :
    context = '''
    CONTEXT:
    - Answer the QUERY regarding the video. video transcript and title is given in the DATA section.
    
    '''

    data = f'''
    DATA:
        TITLE:
            {input_dict['lecture_data']['title']}
        TRANSCRIPT:
            {input_dict['lecture_data']['transcript']}
    
    '''

    history = None
    if input_dict['history'] :
        history = history_temp.format(input_dict['history'])

    document = None
    if input_dict['document'] :
        document = doc_temp.format(input_dict['document'])

    resources = None
    if input_dict['resources'] :
        respources = res_temp.format(input_dict['resource'])

    query = query_temp.format(input_dict['user_query'])

    return make_prompt(context, data, history, document, resources, query)

def practice_assignment_prompt(input_dict) :
    context = '''
    CONTEXT:
    - Answer the QUERY regarding the practice assignment question. 
    The QUESTION is given in the DATA section, along with options and answer. 
    Assist the student to solve the question, instead of providing direct answer.
    Some questions may contain multiple correct answers.
    '''

    data = f'''
    DATA:
        QUESTION:
            {input_dict['assignment_data']['question']}
        OPTIONS:
            {format_items(input_dict['assignment_data']['options'])}
        ANSWER:
            {format_items(input_dict['assignment_data']['answer'])}
    '''
    history = None
    if input_dict['history'] :
        history = history_temp.format(input_dict['history'])

    document = None
    if input_dict['document'] :
        document = doc_temp.format(input_dict['document'])

    resources = None
    if input_dict['resources'] :
        respources = res_temp.format(input_dict['resource'])

    query = query_temp.format(input_dict['user_query'])

    return make_prompt(context, data, history, document, resources, query)

def graded_assignment_prompt(input_dict) :
    context = '''
    CONTEXT:
    - Answer the QUERY regarding the graded assignment question. 
    The QUESTION is given in the DATA section, along with options and answer.
     Assist the student to solve the question, instead of providing direct answer. 
     Refuse to give direct answers, since this question is graded.
    '''

    data = f'''
    DATA:
        QUESTION:
            {input_dict['assignment_data']['question']}
        OPTIONS:
            {format_items(input_dict['assignment_data']['options'])}
        ANSWER:
            {format_items(input_dict['assignment_data']['answer'])}
    '''
    history = None
    if input_dict['history'] :
        history = history_temp.format(input_dict['history'])

    document = None
    if input_dict['document'] :
        document = doc_temp.format(input_dict['document'])

    resources = None
    if input_dict['resources'] :
        respources = res_temp.format(input_dict['resource'])

    query = query_temp.format(input_dict['user_query'])

    return make_prompt(context, data, history, document, resources, query)

def programming_assignment_prompt(input_dict) :
    context = '''
    CONTEXT
    - Answer the QUERY regarding the programming assignment question. 
    The QUESTION is given in the DATA. CODE contains the code written by the student, as an attempt to solve the question.
     CODE is evaluated based on the TEST CASES provided in the DATA section.
     Each CASE contains the INPUT and the expected OUTPUT.
    '''

    data = f'''
    DATA:
        QUESTION:
            {input_dict['programming_assignment_data']['question']}
        TEST CASES:
            {format_cases(input_dict['programming_assignment_data']['cases'])}
        python\'\'\'
            {input_dict['code']}
        \'\'\'
    '''
    history = None
    if input_dict['history'] :
        history = history_temp.format(input_dict['history'])

    document = None
    if input_dict['document'] :
        document = doc_temp.format(input_dict['document'])

    resources = None
    if input_dict['resources'] :
        respources = res_temp.format(input_dict['resource'])

    query = query_temp.format(input_dict['user_query'])

    return make_prompt(context, data, history, document, resources, query)

def course_doubt_prompt(input_dict) :
    context = '''
    CONTEXT
    - Answer the QUERY regarding the course content. 
    DOCUMENT section contains support material for answering the query.
    '''

    data = ''

    history = None
    if input_dict['history'] :
        history = history_temp.format(input_dict['history'])

    document = None
    if input_dict['document'] :
        document = doc_temp.format(input_dict['document'])

    resources = None
    if input_dict['resources'] :
        respources = res_temp.format(input_dict['resource'])

    query = query_temp.format(input_dict['user_query'])

    return make_prompt(context, data, history, document, resources, query)

#------------------------------------
#            LLM Chains
#------------------------------------

lecture_chain = RunnableLambda(prepare_lecture_input) | RunnableLambda(lecture_prompt) | llm
practice_assignment_chain = RunnableLambda(prepare_assignment_input) | RunnableLambda(practice_assignment_prompt) | llm
graded_assignment_chain = RunnableLambda(prepare_assignment_input) | RunnableLambda(graded_assignment_prompt) | llm
programming_assignment_chain = RunnableLambda(prepare_programming_assignment_input) | RunnableLambda(programming_assignment_prompt) | llm
course_doubt_chain = RunnableLambda(prepare_course_doubt_input) | RunnableLambda(course_doubt_prompt) | llm

# from json to BaseMessages
def messages_from_dict(messages):
    msgs = []
    for msg in messages :
        if msg['role'] == 'user':
            msgs.append(HumanMessage(content=msg['message']))
        elif msg['role'] == 'agent':
            msgs.append(AIMessage(content=msg['message']))
    return msgs

def dict_from_messages(messages):
    msgs = []
    for msg in messages :
        if isinstance(msg, HumanMessage):
            msgs.append({
                'role': 'user',
                'message': msg.content
            })
        elif isinstance(msg, AIMessage):
            msgs.append({
                'role': 'agent',
                'message': msg.content
            })
    return msgs
#------------------------------------
#        Chat Storage System
#------------------------------------

# global temp storage
store_dict = {}
store_msg = {}

class FileChatMessageHistory(BaseChatMessageHistory, BaseModel):
    storage_path:  str = Field(default_factory=str)
    session_id: str = Field(default_factory=str)
    messages: List[BaseMessage] = Field(default_factory=list)

    def load_messages(self):
        if not self.messages :
            try :    
                with open(os.path.join(self.storage_path, str(self.session_id)) + '.json', 'r') as f:
                    msgs = json.loads(f.read())
                    store_dict[self.session_id] = msgs
                    self.messages = messages_from_dict(msgs)
                    f.close()
            except:
                pass

    def info(self, chat_dir, session_id) :
        self.storage_path = chat_dir
        self.session_id = session_id
        self.load_messages()

    def add_message(self, message) -> None:
        message.content = message.content.replace('\n\n\n', '\n').replace('\n\n', '\n')
        self.messages.append(message)
        messages = dict_from_messages(self.messages)
        store_dict[self.session_id] = messages
        with open(os.path.join(self.storage_path, str(self.session_id)) + '.json', 'w') as f:
            f.write(json.dumps(messages))
            f.close()

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        for message in messages :
            self.add_message(message)

    def clear(self):
       pass

# get history method
def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store_msg :
        chat_history = FileChatMessageHistory()
        chat_history.info(chat_dir, session_id)
        store_msg[session_id] = chat_history
    return store_msg[session_id]

#------------------------------------
#           History Chains
#------------------------------------

lecture_history_chain = RunnableWithMessageHistory(
    lecture_chain,
    get_by_session_id,
    input_messages_key='user_query',
    history_messages_key='history'
)
practice_assignment_history_chain = RunnableWithMessageHistory(
    practice_assignment_chain,
    get_by_session_id,
    input_messages_key='user_query',
    history_messages_key='history'
)
graded_assignment_history_chain = RunnableWithMessageHistory(
    graded_assignment_chain,
    get_by_session_id,
    input_messages_key='user_query',
    history_messages_key='history'
)
programming_assignment_history_chain = RunnableWithMessageHistory(
    programming_assignment_chain,
    get_by_session_id,
    input_messages_key='user_query',
    history_messages_key='history'
)
course_doubt_history_chain = RunnableWithMessageHistory(
    course_doubt_chain,
    get_by_session_id,
    input_messages_key='user_query',
    history_messages_key='history'
)

#------------------------------------
#           ChatBot Function
#------------------------------------
def chatbot(context, tag, query, session_id=None, code=None, resources=0) :
    if session_id  == None and session_id != 0:
        session_id = str(uuid.uuid4())

    config = {"configurable": {"session_id": session_id}}
    
    info = {
            'user_query': query,
            'tag': tag,
            'resources': resources
        }
    if context == 'lecture' :
        response = lecture_history_chain.invoke(info, config=config)
    elif context == 'practice-assignment':
        response = practice_assignment_history_chain.invoke(info, config=config)
    elif context == 'graded-assignment' :
        response = graded_assignment_history_chain.invoke(info, config=config)
    elif context == 'programming-assignment' :
        info['code'] = code
        response = programming_assignment_history_chain.invoke(info, config=config)
    elif context == 'course':
        response = course_doubt_chain.invoke(info, config=config)

    return {
        'message': response,
        'session_id': session_id
    }

def fetch_history(session_id, is_html) :
    s = dict_from_messages(get_by_session_id(session_id).messages)
    copy = s.copy()
    if not is_html :
        return copy
    for i in range(len(s)):
        if s[i]['role'] == 'agent' :
            copy[i]['message'] = markdown.markdown(copy[i]['message'], 
                output='html', 
                extensions=['fenced_code', 'nl2br']
            ).replace('\n', '<br>').replace('><br><','><')


    return copy
