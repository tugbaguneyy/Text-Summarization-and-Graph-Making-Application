import nltk
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import string

nltk.download('punkt')  # Tokenization için gerekli olan veri kümesini indirin
nltk.download('stopwords')  # Stop-word elimination için gerekli olan veri kümesini indirin

with open('yeni.txt', 'r') as file:
    text = file.read()

text = text.lower()
tokens = word_tokenize(text)

stemmer = PorterStemmer()
stemmed_tokens = [stemmer.stem(token) for token in tokens]

stop_words = set(stopwords.words('english'))  # İngilizce stop-word'lerini kullanacağımızı varsayalım
filtered_tokens = [token for token in stemmed_tokens if token.lower() not in stop_words]

# Noktalama işaretleri listesini oluşturun
punctuation = set(string.punctuation)

# Metinden noktalama işaretlerini çıkarın
filtered_tokens = [token for token in filtered_tokens if token not in punctuation]

result = ' '.join(filtered_tokens)

file_path = "yeni_dosya.txt"

with open(file_path, 'w') as file:
    file.write(result)

embedding_model = Word2Vec([filtered_tokens], vector_size=100, window=5, min_count=1, workers=4)
sentence_vectors = [embedding_model.wv[word] for word in filtered_tokens]
similarity_matrix = cosine_similarity(sentence_vectors)
print(similarity_matrix)
