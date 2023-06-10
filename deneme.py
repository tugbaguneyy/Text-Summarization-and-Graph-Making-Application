import math
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QTextEdit, QComboBox
from PyQt5 import uic
import sys
import networkx as nx
import os
import matplotlib.pyplot as plt
import re
from nltk.metrics.distance import jaccard_distance
from nltk.tokenize import word_tokenize,sent_tokenize
import cumle_skoru_algoritmasi
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import summary
import my_rouge

def calculate_similarity_scores(sentences):
    similarity_scores = {}
    for i in range(len(sentences)):
        sentence1 = sentences[i]
        scores = {}
        for j in range(len(sentences)):
            if i != j:
                sentence2 = sentences[j]
                score = sentence_similarity(sentence1, sentence2)
                scores[sentence2] = score
        similarity_scores[sentence1] = scores
    return similarity_scores

def sentence_similarity(sentence1, sentence2):
    tokens1 = word_tokenize(sentence1.lower())
    tokens2 = word_tokenize(sentence2.lower())
    distance = jaccard_distance(set(tokens1), set(tokens2))
    similarity_score = 1 - distance
    return similarity_score


def generate_summary(G):
    # Node'ları skorlarına göre sırala
    sorted_nodes = sorted(G.nodes(data=True), key=lambda x: x[1]['score'], reverse=True)

    # En yüksek skora sahip olan düğümlerden başlayarak özet oluşturma
    summary = []
    for node, data in sorted_nodes:
        if not any(node in set(summary) for summary_node in summary):
            summary.append(node)

    return summary


def summarize(text, num_sentences=4):
    # Metni cümlelere ayırma
    sentences = sent_tokenize(text)

    # Cümleleri vektörlere dönüştürme
    vectorizer = TfidfVectorizer(tokenizer=word_tokenize, stop_words='english')
    sentence_vectors = vectorizer.fit_transform(sentences)

    # Benzerlik matrisini hesaplama
    similarity_matrix = cosine_similarity(sentence_vectors, sentence_vectors)

    # Benzerlik matrisinden graf oluşturma
    graph = nx.from_numpy_array(similarity_matrix)

    # Cümlelerin TextRank skorlarını hesaplama
    scores = nx.pagerank(graph)

    # Skorlara göre cümleleri sıralama
    ranked_sentences = sorted(((scores[i], sentence) for i, sentence in enumerate(sentences)), reverse=True)

    # İstenen sayıda cümleyi seçme
    summary_sentences = [sentence for _, sentence in ranked_sentences[:num_sentences]]

    # Özeti birleştirme
    summary = ' '.join(summary_sentences)
     # Summary'yi dosyaya yazma
    with open("summary.txt", "w") as file:
        file.write(summary)

    return summary


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # UI dosyasını yükle
        uic.loadUi("deneme.ui", self)

        #Widgetlerı tanımla
        self.pushButton=self.findChild(QPushButton,"pushButton")
        self.pushButton_2=self.findChild(QPushButton,"pushButton_2")
        self.label=self.findChild(QLabel,"label")
        self.label_2=self.findChild(QLabel,"label_2")
        self.textedit=self.findChild(QTextEdit,"textEdit")
        self.pushButton_3=self.findChild(QPushButton,"pushButton_3")
        self.label_3=self.findChild(QLabel,"label_3")
        self.combobox=self.findChild(QComboBox,"comboBox")
        self.label_4=self.findChild(QLabel,"label_4")
        self.label_5=self.findChild(QLabel,"label_5")
        self.textedit_2=self.findChild(QTextEdit,"textEdit_2")
        self.textedit_3=self.findChild(QTextEdit,"textEdit_3")
        self.pushButton_4=self.findChild(QPushButton,"pushButton_4")
        self.pushButton_5=self.findChild(QPushButton,"pushButton_5")
        self.label_6=self.findChild(QLabel,"label_6")
        self.textedit_4=self.findChild(QTextEdit,"textEdit_4")



        #Dropdown Boxa tıkla
        self.pushButton.clicked.connect(self.clicker)
        self.pushButton_2.clicked.connect(self.create_text_graph)
        self.pushButton_3.clicked.connect(self.buttonClicked)
        self.pushButton_4.clicked.connect(self.buttonClicked2)
        self.pushButton_5.clicked.connect(self.buttonClicked3)
        #Appi göster
        self.show()

    def clicker(self):
        #self.label.setText("Bastın")
        #dosya açma
        fname=QFileDialog.getOpenFileName(self,"Open File","","All Files (*);;Python Files (*.py)")
        new_filename="yeni.txt"
        new_file_path = os.path.join(os.path.dirname(fname[0]), new_filename)
        os.rename(fname[0], new_file_path)
        if fname:
            self.label.setText(fname[0])

    def buttonClicked(self):
        threshold = self.textedit.toPlainText()
        cumle_skoru_algoritmasi.threshold(threshold)
        return threshold
    
    def buttonClicked2(self):
        threshold2 = self.textedit_2.toPlainText()
        return threshold2
    def buttonClicked3(self):
        file_path = "C:\\Users\\USER\\Desktop\\yazlab2\\yeni.txt"

        with open(file_path, "r") as file:
            metin = file.read()
            satirlar = metin.split("\n")  # Metni satırlara bölelim
            baslik1 = satirlar[0].strip()  # İlk satır başlık olarak kabul edilir ve boşlukları temizlenir

            metin_cumleler = ' '.join(satirlar[1:])  # Metindeki tüm satırları birleştirerek tek bir metin oluşturun

        summary =summarize(metin_cumleler,math.ceil(len(satirlar)/3))
        self.textedit_3.setText(summary)
        skor=my_rouge.get_rouge_scores2()
        self.textedit_4.setText(str(skor))

    def create_text_graph(self):
        file_path = "C:\\Users\\USER\\Desktop\\yazlab2\\yeni.txt"
        G = nx.Graph()
        threshold = float(self.buttonClicked())
        

        sum_scores=cumle_skoru_algoritmasi.algoritma()

        # Metin dosyasını oku ve cümleleri düğümlere ekle
        with open(file_path, "r") as file:
            metin = file.read()
            satirlar = metin.split("\n")  # Metni satırlara bölelim
            baslik1 = satirlar[0].strip()  # İlk satır başlık olarak kabul edilir ve boşlukları temizlenir

            metin_cumleler = ' '.join(satirlar[1:])  # Metindeki tüm satırları birleştirerek tek bir metin oluşturun
            sentences = re.split(r'\.\s*', metin_cumleler)  # Metni noktaya göre cümlelere ayırın

            sentences = [cumle for cumle in sentences if cumle.strip() != '']

            # Her cümle için skor değeri alınması gerekiyor
            for i, sentence in enumerate(sentences):
                G.add_node(sentence, score=sum_scores[i])  # Her düğümün score değerini `sum_scores` listesinden alınarak ekleyin


            similarity_scores = calculate_similarity_scores(sentences)

            # Cümleler arasındaki ilişkileri kenarlara ekle
            for i in range(len(sentences) - 1):
                current_sentence = sentences[i]
                for j in range(i + 1, len(sentences)):
                    next_sentence = sentences[j]
                    similarity_score = similarity_scores[current_sentence][next_sentence]
                    G.add_edge(current_sentence, next_sentence, similarity=similarity_score)

        # self.graph değişkenine G'yi atama
        self.graph = G
        # Grafik çizdirme
        plt.figure()  # Yeni bir matplotlib figürü oluştur

        pos = nx.spring_layout(G, k=0.5, iterations=50)  # Düğümlerin konumunu belirleme (k değerini ayarlayarak düzeni ayarlayabilirsiniz)

        # Düğüm boyutlarını belirleme
        node_sizes = [1500] * len(sentences)

        # Düğüm renklerini belirleme
        node_colors = []
        for node in G.nodes():
            score = G.nodes[node]['score']
            if score is None or score < threshold:
                node_colors.append('skyblue')
            else:
                neighbors = list(G.neighbors(node))
                similarity_scores = [G.edges[(node, neighbor)]['similarity'] for neighbor in neighbors]
                num_similar_connections = sum(score >= threshold for score in similarity_scores)
                node_colors.append('skyblue')

        nx.draw(G, pos, with_labels=False, node_color=node_colors, node_size=node_sizes, edge_color='gray')  # Grafiği çizdirme

        # Kenarların benzerlik skorlarını yeşil olarak yazdırma
        for edge in G.edges():
            similarity_score = G.edges[edge]['similarity']
            x1, y1 = pos[edge[0]]
            x2, y2 = pos[edge[1]]
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            plt.text(mid_x, mid_y, f"Benzerlik: {similarity_score:.2f}", color='green', ha='center', va='center')

        # Düğüler üzerinde cümle numaralarını, cümle skorlarını ve benzerlik skorlarını yazdırma
        for i, node in enumerate(G.nodes()):
            x, y = pos[node]
            sentence_score = G.nodes[node]['score']
            similarity_scores = [G.edges[(node, neighbor)]['similarity'] for neighbor in G.neighbors(node)]
            num_similar_connections = sum(score >= threshold for score in similarity_scores)

            # Skor yazısını kırmızı renkte yazdırma
            plt.text(x, y-0.05, f"Cümle {i+1}", color='black', ha='center', va='center')
            plt.text(x, y, f"Skor: {sentence_score:.2f}", color='red', ha='center', va='center')

               # Benzerlik skorlarını yazdırma
            similarity_scores_str = ", ".join([f"{score:.2f}" for score in similarity_scores])
            plt.text(x, y+0.1, f"Benzerlik: {similarity_scores_str}", color='gray', ha='center', va='center')

            # Bağlantı sayısını sarı renkte yazdırma
            plt.text(x, y+0.05, f"Bağlantı Sayısı: {num_similar_connections}", color='gold', ha='center', va='center')

        plt.title(baslik1)
        plt.show()




# App'i tanımla
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()