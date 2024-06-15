import warnings
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp

warnings.filterwarnings("ignore")

model_id = 'intfloat/multilingual-e5-large'
model_kwargs = {'device': 'cuda'}
embeddings = HuggingFaceEmbeddings(
        model_name=model_id,
        model_kwargs=model_kwargs
    )


def get_pdf_text(pdf_docs):
    text = " "
    # Iterate through each PDF document path in the list
    for pdf in pdf_docs:
        # Create a PdfReader object for the current PDF document
        pdf_reader = PdfReader(pdf)
        # Iterate through each page in the PDF document
        for page in pdf_reader.pages:
            # Extract text from the current page and append it to the 'text' string
            text += page.extract_text()

    # Return the concatenated text from all PDF documents
    return text


def get_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=256)
    chunks = text_splitter.split_text(text)
    return chunks



def get_vector_store(text_chunks):     

    # Create a vector store using FAISS from the provided text chunks and embeddings
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)

    # Save the vector store locally with the name "faiss_index"
    vector_store.save_local("faiss_index")
    
    
    
    
def get_conversational_chain():
    # Define a prompt template for asking questions based on a given context
    prompt_template = """
Ты эксперт по базе знаний компании РОСАТОМ. Пользователь задает тебе вопрос, ты отвечаешь на него в чате, используя только контекст базы знаний компании, предоставленной тебе в виде файлов. Твоя задача помочь 
пользователю найти ответ на вопрос, и решить его. Все ответы пиши в контексте процессов, регламентов и документов компании РОСАТОМ. Пользователь это сотрудник компании, твоя задача максимально точно и понятно 
отвечать на вопросы пользователя. Помни, пользователь задает вопросы только в контексте базы знаний компании РОСАТОМ. Отвечай только на заданный вопрос. Не делай повторов предложений. Отвечай так, чтобы 
пользователь мог самостоятельно решить свой вопрос, используя, приложение, документацию, или сайт компании. В ответе описывай шаги по решению вопроса, если оно есть в базе знаний. Не предлагай 
пользователю обращаться в техническую поддержку, ты и есть часть технической поддержки. То чего нет в базе знаний компании ты не знаешь, и ответить не можешь. Никогда не пиши вопрос решен, опиши шаги 
необходимые для решения вопроса.\n\n
Context:\n {context}?\n
Question: \n{question}\n

Answer:
    """

    # Initialize a ChatGoogleGenerativeAI model for conversational AI
    model = LlamaCpp(
    model_path="atomic_hack_envelope_entertainment\\data\\model\\model-q4_K.gguf",  # Путь к модели
    temperature=0.1,  # Температура для управления степенью случайности в ответах
    max_tokens=512,  # Максимальное количество токенов в ответе
    max_length=1000,  # Максимальная длина текста (в символах)
    # callback_manager=callback_manager,  # Менеджер коллбэков
    f16_kv=True,
    n_batch=512,
    verbose=False,  # Отключение подробного вывода  # Увеличиваем максимальное количество новых токенов
    n_ctx=35000,
    n_gpu_layers=-1,  # -1 для максимального использования GPU, 0 для CPU
)

    # Create a prompt template with input variables "context" and "question"
    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    # Load a question-answering chain with the specified model and prompt
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain



def user_input(user_question):
    # Create embeddings for the user question using a Google Generative AI model

    # Load a FAISS vector database from a local file
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    retriever = new_db.as_retriever(search_type="similarity", search_kwargs={"k": 1})
    print(retriever)
    # Perform similarity search in the vector database based on the user question
    docs = new_db.similarity_search(user_question)
    print(docs)
    # Obtain a conversational question-answering chain
    chain = get_conversational_chain()

    # Use the conversational chain to get a response based on the user question and retrieved documents
    response = chain(
        {"input_documents": docs, "question": user_question}, return_only_outputs=True
    )

    # Print the response to the console
    print(response)

    # Display the response in a Streamlit app (assuming 'st' is a Streamlit module
    
    
    
# text = get_pdf_text(['test.pdf'])
# chunks = get_chunks(text)
# get_vector_store(chunks)
get_semantic_response('Оплата')