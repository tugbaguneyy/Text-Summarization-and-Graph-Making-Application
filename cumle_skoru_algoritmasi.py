import spacy
from nltk import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


#ÖZEL İSİM ORANI BULMA İŞLEMİ  (P1)
def ozel_isim():

    nlp = spacy.load("en_core_web_sm")  # spaCy'de İngilizce dil modelini yükleyin

    with open("yeni.txt", "r") as file: #işlem görmemiş metni kullandım çünküişlem görmüş haliyle yanlış çalışıyor.
        text = file.read()

    doc = nlp(text)
    named_entities = []  # Özel isimleri tutmak için bir liste

    num_named_entities = 0  # Özel isim sayısını tutmak için değişken
    num_tokens = 0  # Toplam kelime sayısını tutmak için değişken

    for sentence in doc.sents:
        for token in sentence:
            num_tokens += 1
            if token.ent_type_ == "PERSON":  # Sadece "PERSON" etiketine sahip özel isimleri sayın
                num_named_entities += 1
                named_entities.append(token.text)

    # Özel isim sayısı / Cümle uzunluğu oranını hesaplayın
    if num_tokens > 0:
        P1 = num_named_entities / num_tokens
    else:
        P1 = 0

    print("Özel isimlerin cümle uzunluğuna oranı:", P1)

    # Özel isimleri ekrana yazdırın
    # for entity in named_entities:
    #     print(entity)



#NUMERİK VERİ ORANI BULMA(P2)
def numerik():
    with open("yeni.txt", "r") as file:
        text= file.read()
    sentences = sent_tokenize(text)
    numerical_sentences = []
    for sentence in sentences:
        has_numerical_data = any(char.isdigit() for char in sentence)
        if has_numerical_data:
            numerical_sentences.append(sentence)
    numerical_sentences_count = len(numerical_sentences)
    total_sentence_length = sum(len(sentence) for sentence in sentences)
    P2 = numerical_sentences_count / total_sentence_length
    print("Numerik Veri Sayısı:", numerical_sentences_count)
    print("Cümle Uzunluğu Toplamı:", total_sentence_length)
    print("Numerik Veri / Cümle Uzunluğu Oranı:", P2)



#Cümle benzerliği threshold’unu geçen node’ların bulunması (P3) Tresholdu geçen nodeların bağlantı sayısı / Toplam bağlantı sayısı
def threshold(input):
    print("çalıştı")

#Başlıkta geçen kelime sayısının oranı(P4)
def baslik():
    with open('yeni.txt', 'r') as file:
        text = file.read()
        file.seek(0)
        baslik = file.readline().strip()
    baslik_kelimeleri = baslik.split()
    cumleler = text.split(". ")  # Cümleleri ayırın (eğer cümleler nokta ile ayrılmışsa)
    baslikte_gecen_kelime_sayisi = 0

    for cumle in cumleler:
        kelimeler = cumle.split()
        for kelime in kelimeler:
            if kelime in baslik_kelimeleri:
                baslikte_gecen_kelime_sayisi += 1
                break  # Her bir cümlede sadece bir kez kontrol etmek için
    cumle_sayisi = len(cumleler)
    cumle_uzunlugu = len(text)
    P4 = baslikte_gecen_kelime_sayisi / cumle_uzunlugu
    print("Başlıkta geçen kelime sayısının oranı",P4)

#Cümlenin içinde geçen tema kelime sayısı / Cümlenin uzunluğu(P5)


def td_idf():

    # Metin dosyasını oku ve küçük harflere dönüştür
    with open("yeni.txt", "r") as file:
        text = file.read()

    # Cümleleri ayırın
    sentences = text.split('. ')

    # Tüm kelimeleri birleştirin
    all_words = ' '.join(sentences)

    # TF-IDF değerlerini hesaplamak için TfidfVectorizer kullanın
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([all_words])

    # TF-IDF değerlerini ve kelimeleri birleştirin
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = zip(feature_names, np.ravel(tfidf_matrix.sum(axis=0)))

    # Tema kelime sayısını belirlemek için yüzde değerini hesaplayın
    total_words = len(feature_names)
    theme_words_count = int(total_words * 0.1)

    # Tema kelime listesini oluşturun
    theme_words = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)[:theme_words_count]

    # Tema kelime sayısını ve toplam kelime sayısını hesaplayın
    num_theme_words = len(theme_words)
    total_words = len(all_words.split())

    # Tema kelime oranını bulun
    P5 = num_theme_words / total_words

    print("Tema Kelime Sayısı:", num_theme_words)
    print("Toplam Kelime Sayısı:", total_words)
    print("Tema Kelime Oranı:", P5)
#%10 problemi devam ediyor





