from PyQt5.QtWidgets import QMainWindow,QApplication,QPushButton,QLabel,QFileDialog
from PyQt5 import uic
import sys
import networkx as nx
import os
import matplotlib.pyplot as plt

class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()

        #UI dosyasını yükle
        uic.loadUi("deneme.ui",self)

        #Widgetlerı tanımla
        self.pushButton=self.findChild(QPushButton,"pushButton")
        self.pushButton_2=self.findChild(QPushButton,"pushButton_2")
        self.label=self.findChild(QLabel,"label")

        #Dropdown Boxa tıkla
        self.pushButton.clicked.connect(self.clicker)
        self.pushButton_2.clicked.connect(self.create_text_graph)
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
    def create_text_graph(self):
        file_path = "C:\\Users\\USER\\Desktop\\yazlab2\\yeni.txt"
        G = nx.Graph()

        # Metin dosyasını oku ve cümleleri düğümlere ekle
        with open(file_path, 'r') as file:
            text = file.read()
            sentences = text.split('. ')  # Cümleleri ayır, eğer başka bir cümle ayracı kullanıyorsanız ona göre güncelleyin
            for sentence in sentences:
                G.add_node(sentence)

        # Cümleler arasındaki ilişkileri kenarlara ekle
        for i in range(len(sentences) - 1):
            current_sentence = sentences[i]
            next_sentence = sentences[i + 1]
            G.add_edge(current_sentence, next_sentence)

        # Grafik çizdirme
        pos = nx.spring_layout(G)  # Düğümlerin konumunu belirleme
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='gray')  # Grafiği çizdirme
        plt.title('Metin Dosyası Grafiği')
        plt.show()


#Appi tanımla
app=QApplication(sys.argv)
UIWindow=UI()
app.exec_()
