from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize

import nltk
nltk.download('stopwords')
text = "Для выделения ключевых предложений из текста на Python можно воспользоваться библиотекой Natural Language Toolkit (NLTK) и модулем Summarizer. Для начала необходимо предобработать текст, токенизировать его на предложения, привести в нижний регистр и удалить стоп-слова. Затем можно использовать модуль Summarizer для создания краткой выжимки:"

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

print(summary)
