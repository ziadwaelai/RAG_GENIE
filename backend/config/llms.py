from langchain_community.chat_models import ChatOllama
from langchain_core.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

llama3 = ChatOllama(
    base_url='http://localhost:11434',
    model="llama3.2",
    temperature=0,
    streaming=True,
    callback_manager=callback_manager
)
memory=ConversationBufferMemory()
chat=ConversationChain(
    llm=llama3,
    memory=memory,
    callback_manager=callback_manager
)