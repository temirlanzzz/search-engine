import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
def tokenize_text(text: str) -> list[str]:
    #lowercase
    text = text.lower()
    #remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    #split into words
    words = text.split(' ')
    #remove stopwords
    stopwords = nltk.corpus.stopwords.words('english')
    words = [word for word in words if word not in stopwords]
    #stemmer
    stemmer = nltk.stem.PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in words]
    return stemmed_words






