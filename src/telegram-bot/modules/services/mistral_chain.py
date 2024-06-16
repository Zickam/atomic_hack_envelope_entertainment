from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import nltk
nltk.download('stopwords')

print('Embeddings loads...')
model_id = 'intfloat/multilingual-e5-large'
model_kwargs = {'device': 'cpu'}
embeddings = HuggingFaceEmbeddings(
        model_name=model_id,
        model_kwargs=model_kwargs
    )


vectorstore = FAISS.load_local("data/faiss_index", embeddings, allow_dangerous_deserialization=True)

def compress_text(semantic_search_text) -> str:
    text = semantic_search_text

    sentences = sent_tokenize(text.lower())
    stop_words = set(stopwords.words("russian"))

    word_frequencies = {}
    for sentence in sentences:
        words = word_tokenize(sentence)
        for word in words:
            if word not in stop_words:
                if word not in word_frequencies:
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency

    sentence_scores = {}
    for sentence in sentences:
        words = word_tokenize(sentence)
        for word in words:
            if word in word_frequencies:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_frequencies[word]
                else:
                    sentence_scores[sentence] += word_frequencies[word]

    num_sentences = 3
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    summary = ' '.join(summary_sentences)
    return summary



async def get_response(user_question:str) -> str:
    docs = ' '.join(list(map(lambda x: x.page_content, vectorstore.similarity_search(user_question))))
    return compress_text(docs)

