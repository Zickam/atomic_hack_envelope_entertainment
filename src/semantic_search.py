from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


model_id = 'intfloat/multilingual-e5-large'
model_kwargs = {'device': 'cuda'}
embeddings = HuggingFaceEmbeddings(
        model_name=model_id,
        model_kwargs=model_kwargs
    )


def get_semantic_response(user_question:str) -> list:
    new_db = FAISS.load_local("../data/faiss_index", embeddings, allow_dangerous_deserialization=True)
    return new_db.similarity_search(user_question)