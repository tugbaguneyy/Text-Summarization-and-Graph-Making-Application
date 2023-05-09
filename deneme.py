from PyQt5.QtWidgets import QMainWindow,QApplication,QPushButton,QLabel,QFileDialog,QTextEdit,QComboBox
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
        self.label_2=self.findChild(QLabel,"label_2")
        self.textedit=self.findChild(QTextEdit,"textEdit")
        self.pushButton_3=self.findChild(QPushButton,"pushButton_3")
        self.label_3=self.findChild(QLabel,"label_3")
        self.combobox=self.findChild(QComboBox,"comboBox")
        self.label_4=self.findChild(QLabel,"label_4")
        self.textedit_2=self.findChild(QTextEdit,"textEdit_2")
        self.pushButton_4=self.findChild(QPushButton,"pushButton_4")


        #Dropdown Boxa tıkla
        self.pushButton.clicked.connect(self.clicker)
        self.pushButton_2.clicked.connect(self.create_text_graph)
        self.pushButton_3.clicked.connect(self.buttonClicked)
        self.pushButton_4.clicked.connect(self.buttonClicked2)
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
        text = self.textedit.toPlainText()
        return text
    
    def buttonClicked2(self):
        text2 = self.textedit_2.toPlainText()
        return text2

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
