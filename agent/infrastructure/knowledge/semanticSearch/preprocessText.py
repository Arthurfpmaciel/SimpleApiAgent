import re
import string
import nltk
import unicodedata

pt_stopwords = set(nltk.corpus.stopwords.words('portuguese'))
# remover pontuações
def remove_punctuation(text):
    return re.sub(f"[{re.escape(string.punctuation)}]", " ", str(text))
# remover números
def remove_digits(text):
    return re.sub(r'\d+', ' ', text)
# remover caracteres noascii
def remove_noascii(text):
    return text.encode("ascii", "ignore").decode()
# obter stopwords de uma lingua
def get_stopwords(language='portuguese'):
    return set(nltk.corpus.stopwords.words(language))
# tokenizar texto
def tokenize(text):
    return text.split()
# remover stopwords
def remove_stopwords(tokens,stopwords,minsize = 1):
    tokens = [word for word in tokens if word not in stopwords and len(word)>=minsize]
    return ' '.join(tokens)
# mudar letras para mínusculo
def lower_text(text):
    return text.lower()
# remover espaços em branco
def remove_ws(text):
    return re.sub(r'\s+', ' ', text).strip()
# remover acentos
def remove_accent(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

def clean_text(text):
    text = lower_text(text)
    text = remove_accent(text)
    text = remove_noascii(text)
    # text = remove_punctuation(text)
    text = remove_ws(text)
    return text

# limpeza de texto profunda
def clean_text_deep(text):
    text = clean_text(text)
    # text = remove_punctuation(text)
    text = remove_digits(text)
    text = remove_stopwords(tokenize(text),pt_stopwords,3)
    text = remove_ws(text)
    return text