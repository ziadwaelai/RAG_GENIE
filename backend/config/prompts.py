from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)

#################################### CHATBOT PROMPTS #########################################

cb_template_str = """
You are an intelligent assistant designed to help with talent acquisition tasks. Use the following 
pieces of retrieved context to answer questions about candidates. Provide accurate, concise, and 
professional responses. If the information is not available, respond with 'I don't have that information.'

Prioritize key details like skills, experiences, qualifications, and achievements that align with the query. 
Use three sentences maximum to ensure clarity and relevance.

Conversation history:
{history}

Retrieved context:
{context}
"""


cb_system_message = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["context"], template=cb_template_str)
)

cb_user_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["question"], template="{question}")
)

cb_messages = [cb_system_message, cb_user_prompt]

chat_prompt_template = ChatPromptTemplate(
    input_variables=["context", "question"], messages=cb_messages
)
