import networkx as nx
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import cumle_skoru_algoritmasi

file_path = "C:\\Users\\USER\\Desktop\\yazlab2\\yeni.txt"

with open(file_path, "r") as file:
            metin = file.read()
            satirlar = metin.split("\n")  # Metni satırlara bölelim
            baslik1 = satirlar[0].strip()  # İlk satır başlık olarak kabul edilir ve boşlukları temizlenir

            metin_cumleler = ' '.join(satirlar[1:])  # Metindeki tüm satırları birleştirerek tek bir metin oluşturun



def summarize(text, num_sentences=4):
    P1=cumle_skoru_algoritmasi.ozel_isim(text)
    P2=cumle_skoru_algoritmasi.numerik(text)
    P3=cumle_skoru_algoritmasi.threshold(text)
    P4=cumle_skoru_algoritmasi.baslik(text,text)
    P5=cumle_skoru_algoritmasi.get_tfidf_scores(text)
    
    sentences = sent_tokenize(text)

   
    vectorizer = TfidfVectorizer(tokenizer=word_tokenize, stop_words='english')
    sentence_vectors = vectorizer.fit_transform(sentences)

    
    similarity_matrix = cosine_similarity(sentence_vectors, sentence_vectors)

   
    graph = nx.from_numpy_array(similarity_matrix)

    
    scores = nx.pagerank(graph)

    all=P1+P2+P3+P4+P5
    ranked_sentences = sorted(((scores[i], sentence) for i, sentence in enumerate(sentences)), reverse=True)

    
    summary_sentences = [sentence for _, sentence in ranked_sentences[:num_sentences]]

    
    summary = ' '.join(summary_sentences)

     # Summary'yi dosyaya yazma
    with open("summary.txt", "w") as file:
        file.write(summary)

    return summary


#print(textrank_summarize(metin_cumleler,5))




