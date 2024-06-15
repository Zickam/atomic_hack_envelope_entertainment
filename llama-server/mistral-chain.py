import os

from langchain_community.llms.llamafile import Llamafile
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


os.system('llama-server/llamafile-0.8.6/bin/llamafile.exe -m ./TinyLlama-1.1B-Chat-v1.0.Q4_0.llamafile')

model_id = 'intfloat/multilingual-e5-large'
model_kwargs = {'device': 'cpu'}
embeddings = HuggingFaceEmbeddings(
        model_name=model_id,
        model_kwargs=model_kwargs
    )


llm = Llamafile()

# Prompt
prompt = PromptTemplate.from_template(
"""
Ты эксперт по базе знаний компании РОСАТОМ. Пользователь задает тебе вопрос, ты отвечаешь на него в чате, используя только контекст базы знаний компании, предоставленной тебе в виде файлов. Твоя задача помочь 
пользователю найти ответ на вопрос, и решить его. Все ответы пиши в контексте процессов, регламентов и документов компании РОСАТОМ. Пользователь это сотрудник компании, твоя задача максимально точно и понятно 
отвечать на вопросы пользователя. Помни, пользователь задает вопросы только в контексте базы знаний компании РОСАТОМ. Отвечай только на заданный вопрос. Не делай повторов предложений. Отвечай так, чтобы 
пользователь мог самостоятельно решить свой вопрос, используя, приложение, документацию, или сайт компании. В ответе описывай шаги по решению вопроса, если оно есть в базе знаний. Не предлагай 
пользователю обращаться в техническую поддержку, ты и есть часть технической поддержки. То чего нет в базе знаний компании ты не знаешь, и ответить не можешь. Никогда не пиши вопрос решен, опиши шаги 
необходимые для решения вопроса.\n\n
Context:\n {context}?\n
Question: \n{question}\n

Answer:"""
)

# Chain
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


chain = {"docs": format_docs} | prompt | llm | StrOutputParser()

vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
# Perform similarity search in the vector database based on the user question
question = "What are the approaches to Task Decomposition?"
docs = vectorstore.similarity_search(question)
chain.invoke(docs)

