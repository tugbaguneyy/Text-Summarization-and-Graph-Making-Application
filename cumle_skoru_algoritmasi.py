import spacy
from nltk import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re


#ÖZEL İSİM ORANI BULMA İŞLEMİ  (P1)

def ozel_isim(text):
    nlp = spacy.load("en_core_web_sm")  # spaCy'de İngilizce dil modelini yükleyin
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

    #print("Özel isimlerin cümle uzunluğuna oranı:", P1)
    return P1

# Kullanım örneği



    # Özel isimleri ekrana yazdırın
    # for entity in named_entities:
    #     print(entity)



#NUMERİK VERİ ORANI BULMA(P2)
def numerik(text):
    sentences = sent_tokenize(text)
    numerical_sentences = []
    for sentence in sentences:
        has_numerical_data = any(char.isdigit() for char in sentence)
        if has_numerical_data:
            numerical_sentences.append(sentence)
    numerical_sentences_count = len(numerical_sentences)
    total_sentence_length = sum(len(sentence) for sentence in sentences)
    P2 = numerical_sentences_count / total_sentence_length
    # print("Numerik Veri Sayısı:", numerical_sentences_count)
    # print("Cümle Uzunluğu Toplamı:", total_sentence_length)
    # print("Numerik Veri / Cümle Uzunluğu Oranı:", P2)
    return P2



#Cümle benzerliği threshold’unu geçen node’ların bulunması (P3) Tresholdu geçen nodeların bağlantı sayısı / Toplam bağlantı sayısı
def threshold(input):
    # print("çalıştı")
    P3=0.0
    return P3

#Başlıkta geçen kelime sayısının oranı(P4)

def baslik(baslik, text):
    baslik = baslik.lower()
    text = text.lower()

    baslik_kelimeleri = baslik.split()
    baslikte_gecen_kelime_sayisi = 0

    cümleler = re.split(r'\.\s*', text)
    for cumle in cümleler:
        kelimeler = re.findall(r'\w+', cumle)
        baslikte_gecen_kelime_sayisi += sum(1 for kelime in kelimeler if kelime in baslik_kelimeleri)

    metin_kelime_sayisi = sum(len(re.findall(r'\w+', cumle)) for cumle in cümleler)

    P4 = baslikte_gecen_kelime_sayisi / metin_kelime_sayisi
    # print(baslikte_gecen_kelime_sayisi)
    # print("Başlıkta geçen kelime sayısının oranı:", P4)
    return P4



#Cümlenin içinde geçen tema kelime sayısı / Cümlenin uzunluğu(P5)

def get_tfidf_scores(sentences):
    # Tüm cümleleri birleştirerek tek bir metin oluşturun
    text = ' '.join(sentences)

    # TF-IDF vektörleştirmesi için TfidfVectorizer'ı kullanın
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text])

    # Kelimeleri ve TF-IDF değerlerini elde edin
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]

    # Her kelimenin TF-IDF değerini bir sözlükte depolayın
    tfidf_dict = {word: tfidf for word, tfidf in zip(feature_names, tfidf_scores)}

    return tfidf_dict

def theme_word_selection():
    with open("yeni.txt", "r") as file:
        metin = file.read()
        
    satirlar = metin.split("\n")  # Metni satırlara bölelim
    baslik1 = satirlar[0].strip()  # İlk satır başlık olarak kabul edilir ve boşlukları temizlenir

    metin_cumleler = ' '.join(satirlar[1:])  # Metindeki tüm satırları birleştirerek tek bir metin oluşturun
    cumleler = re.split(r'\.\s*', metin_cumleler)  # Metni noktaya göre cümlelere ayırın

    cumleler = [cumle for cumle in cumleler if cumle.strip() != '']

    # Tüm cümlelerin TF-IDF değerlerini hesaplayın
    tfidf_dict = get_tfidf_scores(cumleler)

    # Tüm cümlelerin kelime-TF-IDF çiftlerini tutmak için boş bir liste oluşturun
    kelime_tfidf_listesi = []
    toplam_kelime_sayisi = 0

    for cumle in cumleler:
        # Cümlenin kelimelerini alın
        kelimeler = re.findall(r'\w+', cumle)
        # Kelime sayısını toplam kelime sayısına ekleyin
        toplam_kelime_sayisi += len(kelimeler)

        # Cümlenin her kelimesinin TF-IDF değerlerini alın ve listeye ekleyin
        for kelime in kelimeler:
            tfidf = tfidf_dict.get(kelime, 0)
            if tfidf > 0:  # TF-IDF değeri 0 olan kelimeleri dikkate almayın
                kelime_tfidf_listesi.append((kelime, tfidf))

    # Kelime-TF-IDF çiftlerini TF-IDF değerine göre büyükten küçüğe sıralayın
    kelime_tfidf_listesi.sort(key=lambda x: x[1], reverse=True)
    kelime_tfidf_listesi_filtreli = []
    kelimeler = set()  # Tekil kelimeleri tutmak için bir küme oluşturuyoruz

    for kelime, tfidf in kelime_tfidf_listesi:
        if kelime not in kelimeler:
            kelimeler.add(kelime)
            kelime_tfidf_listesi_filtreli.append((kelime, tfidf))

    # # Filtrelenmiş kelime-TF-IDF çiftlerini ekrana yazdırın
    # for kelime, tfidf in kelime_tfidf_listesi_filtreli:
    #  print(f"Kelime: {kelime}, TF-IDF: {tfidf}")



    # Theme kelime sayısı kadar kelimeyi theme_words listesine ekleyen kod
    theme_word_count = int(toplam_kelime_sayisi / 10)
    theme_words = []

    # kelime_tfidf_listesi'nden en yüksek TF-IDF değerine sahip kelimeyi bulup theme_words listesine ekleyin
    for i in range(theme_word_count):
        max_tfidf_word = max(kelime_tfidf_listesi_filtreli, key=lambda x: x[1])
        theme_words.append(max_tfidf_word[0])
        kelime_tfidf_listesi_filtreli.remove(max_tfidf_word)

    # # Theme kelimeleri yazdırın
    # print("Theme Kelimeler:")
    # for word in theme_words:
    #     print(word)
    return theme_words

def theme_word_oran(text):
    theme_words = theme_word_selection()  # theme_words listesini al
    words = text.split()  # metni kelimelere ayır

    word_count = len(words)  # metindeki toplam kelime sayısı
    theme_word_count = sum(word in theme_words for word in words)  # tema kelimelerinin metindeki toplam sayısı

    P5 = theme_word_count / word_count  # oranı hesapla

    return P5



def algoritma():
    with open("yeni.txt", "r") as file:
        metin = file.read()
    satirlar = metin.split("\n")  # Metni satırlara bölelim
    baslik1 = satirlar[0].strip()  # İlk satır başlık olarak kabul edilir ve boşlukları temizlenir

    metin_cumleler = ' '.join(satirlar[1:])  # Metindeki tüm satırları birleştirerek tek bir metin oluşturun
    cumleler = re.split(r'\.\s*', metin_cumleler)  # Metni noktaya göre cümlelere ayırın

    cumleler = [cumle for cumle in cumleler if cumle.strip() != '']
    
    x=len(cumleler)
    i=0
    results = []  # Sonuçları depolamak için boş bir liste oluşturun
    sum=[] #Toplam skoru tutan liste

    while i < x:
        p1 = ozel_isim(cumleler[i])
        p2 = numerik(cumleler[i])
        p3 = threshold(0)
        p4 = baslik(baslik1, cumleler[i])
        p5 = theme_word_oran(cumleler[i])

        result = {
            'P1': p1,
            'P2': p2,
            'P3': p3,
            'P4': p4,
            'P5': p5
        }

        results.append(result)  # Sonucu listeye ekleyin
        sum.append(p1+p2+p3+p4+p5)
        i += 1
    return sum

       
    # for result in results:
    #     print("P1:", result['P1'])
    #     print("P2:", result['P2'])
    #     print("P3:", result['P3'])
    #     print("P4:", result['P4'])
    #     print("P5:", result['P5'])
    #     print() 
    # for a in range(len(sum)):
    #     print(a," . cümle skoru",sum[a])


#algoritma()



