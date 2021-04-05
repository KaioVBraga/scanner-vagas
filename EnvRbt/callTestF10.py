#Este programa faz uso do demoTest3, que e uma interface grafica feita no qtcreator 4
#Aluno: Kaio Vinycius Braga dos Santos
#Orientador: Roberto de Carvalho

from __future__ import division
import sys
import os
import pickle
import numpy as np
from matplotlib import pyplot as plt
import cv2
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from demoTest3 import *

#Myform e a classe/GUI principal, e nela que sera exibido as Tabs e que possuira uma barra de menu 
class MyForm(QMainWindow):

	#Metodo de inicializacao
	def __init__(self):
		super(QMainWindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		
		#Inicializacao das Tab Widget, juntamente de sua quantidade e outras informacoes, como nome dos arquivos, widgets de imagem, de video e etc
		#A maioria destes esta em formato de lista, pois estou dando um foco grande na Tab Widget
		
		#self.ui.tabWidget e a Tab Widget usada neste codigo
		self.ui.tabWidget.clear()
		#self.tabQuant variavel global que armazena a quantidade de tabs no codigo
		self.tabQuant=0
		#self.tabs e uma list() global que armazena todos os Widgets que sao usados como tabs da Tab Widget
		self.tabs = []
		#self.vagas e uma list() global que armazena todos os Conjuntos de Vagas (um Conjunto de Vagas e um grupo de vagas que pertence a uma imagem/video)
		self.vagas = []
		#self.cropping e uma list() global que armazena o estado de todas imagens/videos, sendo este estando gropado ou nao
		self.cropping = []
		#self.factor e uma list() global que armazena a proporcao de todas imagens/videos, impedindo entao que sua largura/altura (durante a self.showImage()) exceda o limite
		self.factor = []
		#self.fname e uma list() global que armazena o nome de todas imagens/videos abertos
		self.fname = []
		#self.svfname e uma list() global que armazena o nome de todos arquivos de ROI de imagens/videos abertos
		self.svfname = []
		#self.mQImage e uma list() global que armazena todas as imagens em formato aceito pelo PyQt
		self.mQImage = []
		#self.cvVideo e uma list() global que armazena todas as videos em formato aceito pelo OpenCV
		self.cvVideo = []
		#self.cvImage e uma list() global que armazena todas as imagens em formato aceito pelo OpenCV
		self.cvImage = []
		#self.cvClone e uma list() global que armazena todas as formas sem alteracao das self.cvImage
		self.cvClone = []
		#self.cvRoi e uma list() global que armazena todas as ROI's
		self.cvRoi = []
		#self.layout e uma list() global que armazena todas as GridLayouts utilizadas nas self.tabs
		self.layout = []
		#self.horLayout e uma list() global que armazena todas as HBoxLayouts utilizadas para posicionar as self.labelImage
		self.horLayout = []
		#self.labelImage e uma list() global que armazena todas as Labels usadas para mostrar as self.mQImage
		self.labelImage = []
		#self.labelEstadoVagas e uma list() global que armazena todas as Labels que mostram o texto "Estado das Vagas" dentro das self.tabs
		self.labelEstadoVagas = []
		#self.listWidgetEstadoVagas e uma list() global que armazena todas as List Widgets que (no futuro irao) mostrar o Estado das Vagas (ocupada/livre)
		self.listWidgetEstadoVagas = []
		#self.pushButtonAddVaga e uma list() global que armazena os botoes de todas as self.tabs que adicionam uma nova vaga
		self.pushButtonAddVaga = []
		#self.pushButtonRmVaga e uma list() global que armazena os botoes de todas as self.tabs que removem uma vaga
		self.pushButtonRmVaga = []
		#self.pushButtonRstVaga e uma list() global que armazena os botoes de todas as self.tabs que resetam todas as vagas de um item da self.tabs
		self.pushButtonRstVaga = []
		#self.pushButtonSaveVaga e uma list() global que armazena os botoes de todas as self.tabs que salva todas as vagas de um item da self.tabs
		self.pushButtonSaveVaga = []
		
		#Action que ocorre quando gatilhada, sua funcao e abrir um arquivo de video
		self.ui.actionAbrir_Camera.triggered.connect(self.fileOpen)
		self.show()
		
	#Metodo utilizado para abrir um video
	#Dentro do mesmo sera determinado se um arquivo foi selecionado
	#Juntamente, serao feitas as atribuicoes de importantes widgets, como: layouts de imagens/videos, labels dos mesmos, proporcoes de imagem, botoes, listas e etc
	def fileOpen(self):
		newName = unicode(QFileDialog.getOpenFileName(self, "Open file", "/home"))
		
		if not(newName in self.fname) and ('.' in newName):
			self.fname.append(newName)	
		
			self.tabQuant = self.ui.tabWidget.count()
			self.tabs.append(QWidget())
			self.ui.tabWidget.addTab(self.tabs[self.tabQuant], "Tab %d" % self.tabQuant)
			self.ui.tabWidget.setCurrentIndex(self.tabQuant)
		
			self.vagas.append(list())
			self.cropping.append(False)
			self.factor.append(1)
			
			#Inicializacao de cada item de cada list de Interface, como: botoes, labels e list wigets
			self.labelImage.append(QLabel())
			self.labelEstadoVagas.append(QLabel("Estado das Vagas"))
			self.listWidgetEstadoVagas.append(QListWidget())
			self.pushButtonAddVaga.append(QPushButton("Adicionar Vaga"))
			self.pushButtonRmVaga.append(QPushButton("Remover Vaga"))
			self.pushButtonRstVaga.append(QPushButton("Resetar Vagas"))
			self.pushButtonSaveVaga.append(QPushButton("Salvar Vagas"))
		
			#'Setando' o layout que de posicionamento interno da self.labelImage[self.tabQuant] 		
			self.horLayout.append(QHBoxLayout())
			self.layout.append(QGridLayout())
			self.horLayout[self.tabQuant].addStretch()
			self.horLayout[self.tabQuant].addWidget(self.labelImage[self.tabQuant])
			self.horLayout[self.tabQuant].addStretch()
			
			#'Setando' o Layout de cada tab em formato de grade
			self.layout[self.tabQuant].addLayout(self.horLayout[self.tabQuant], 0, 0, 7, 1)
			self.layout[self.tabQuant].addWidget(self.labelEstadoVagas[self.tabQuant], 1, 1)
			self.layout[self.tabQuant].addWidget(self.listWidgetEstadoVagas[self.tabQuant], 2, 1)
			self.layout[self.tabQuant].addWidget(self.pushButtonAddVaga[self.tabQuant], 3, 1)
			self.layout[self.tabQuant].addWidget(self.pushButtonRmVaga[self.tabQuant], 4, 1)
			self.layout[self.tabQuant].addWidget(self.pushButtonRstVaga[self.tabQuant], 5, 1)
			self.layout[self.tabQuant].addWidget(self.pushButtonSaveVaga[self.tabQuant], 6, 1)
			
			self.layout[self.tabQuant].setColumnStretch(0, 100)
		
			self.ui.tabWidget.setTabText(self.tabQuant,"Camera %d" % (self.tabQuant+1))
			self.tabs[self.tabQuant].setLayout(self.layout[self.tabQuant])
		
			print self.ui.tabWidget.count()
			
			#Conectando os slots e signals de cada tab
			self.connect(self.pushButtonAddVaga[self.tabQuant], SIGNAL("clicked()"), self.cropImage)
			self.connect(self.pushButtonRmVaga[self.tabQuant], SIGNAL("clicked()"), self.removeImage)
			self.connect(self.pushButtonRstVaga[self.tabQuant], SIGNAL("clicked()"), self.resetImage)
			self.connect(self.pushButtonSaveVaga[self.tabQuant], SIGNAL("clicked()"), self.saveImage)
			self.listWidgetEstadoVagas[self.tabQuant].itemClicked.connect(self.changeSlotColor)
			self.ui.tabWidget.tabCloseRequested.connect(self.removeCurrentTab)
		
			if self.fname[self.tabQuant]:
				self.loadFile()

	#Metodo utilizado para carregar uma imagem/video selecionado pelo usuario, juntamente, se houver, seu arquivo de ROI's
	def loadFile(self):
		if self.fname[self.tabQuant]:
			###print(self.fname[self.tabQuant])
			###print(type(self.fname[self.tabQuant]))
			
			#Gerando um item da self.svfname
			self.svfname.append(self.fname[self.tabQuant].split("."))
			self.svfname[self.tabQuant] = self.svfname[self.tabQuant][0]+".txt"
			
			#Recebendo um video
			self.cvVideo.append(cv2.VideoCapture(self.fname[self.tabQuant]))
			ret, frame = self.cvVideo[self.tabQuant].read()
			
			#Pegando o primeiro frame do video, colocando o como imagem apenas, para que nao ocorra a reproducao do mesmo
			self.cvImage.append(frame)
			
			#Gerando um item para self.cvClone e self.mQImage
			height, width, byteValue = self.cvImage[self.tabQuant].shape
			byteValue = byteValue * width
			cv2.cvtColor(self.cvImage[self.tabQuant], cv2.COLOR_BGR2RGB, self.cvImage[self.tabQuant])
			self.cvClone.append(self.cvImage[self.tabQuant].copy())
			self.mQImage.append(QImage(self.cvImage[self.tabQuant], width, height, byteValue, QImage.Format_RGB888))
			
			#Inicializando as ROI's das vagas da Tab que esta sendo aberta
			self.cvRoi.append(list())
			
			#Inicializando as vagas da Tab que esta sendo aberta
			self.vagas[self.tabQuant] = []
			self.listWidgetEstadoVagas[self.tabQuant].clear()
			
			#Se houver um arquivo de ROI's, dentro deste 'try'	sera feito o processamento desses	
			try:
				with open(self.svfname[self.tabQuant], "rb") as fp:
					self.vagas[self.tabQuant] = pickle.load(fp)
					
					for pos in range(len(self.vagas[self.tabQuant])):
						#Uma vaga e desenhada utilizando quatro pontos, que neste caso estao armazenados em self.vagas[self.tabQuant][pos]
						cv2.line(self.cvImage[self.tabQuant], self.vagas[self.tabQuant][pos][0], self.vagas[self.tabQuant][pos][1], (255, 255, 0), 2)
						cv2.line(self.cvImage[self.tabQuant], self.vagas[self.tabQuant][pos][1], self.vagas[self.tabQuant][pos][2], (255, 255, 0), 2)
						cv2.line(self.cvImage[self.tabQuant], self.vagas[self.tabQuant][pos][2], self.vagas[self.tabQuant][pos][3], (255, 255, 0), 2)
						cv2.line(self.cvImage[self.tabQuant], self.vagas[self.tabQuant][pos][0], self.vagas[self.tabQuant][pos][3], (255, 255, 0), 2)
						
						
						#Uma ROI e gerada com base nas vagas que foram criadas
						self.cvRoi[self.tabQuant].append(self.createRoi(self.cvClone[self.tabQuant], self.vagas[self.tabQuant][pos]))
						cvRoiName = self.fname[self.tabQuant].split('/')
						cvRoiName = cvRoiName[len(cvRoiName)-1].split(".")[0]
						cvRoiName += str(pos)+".png"
						cv2.imwrite(cvRoiName, self.cvRoi[self.tabQuant][pos])
						
						###h = cv2.calcHist([self.cvRoi[self.tabQuant][pos]], [0], None, [256], [0, 256])
						###plt.figure()
						###plt.title("Histograma P&B")
						###plt.xlabel("Intensidade")
						###plt.ylabel("Qtde de Pixels")
						###plt.plot(h)
						###plt.xlim([0, 256])
						###plt.show()
						
					height, width, byteValue = self.cvImage[self.tabQuant].shape
					byteValue = byteValue * width
					self.mQImage[self.tabQuant] = QImage(self.cvImage[self.tabQuant], width, height, byteValue, QImage.Format_RGB888)
					
					#List Widget sendo alimentada
					for i in range(0, len(self.vagas[self.tabQuant])):
						self.listWidgetEstadoVagas[self.tabQuant].addItem("Vaga "+str(i+1))
						
					self.firstShowImage()
			except:
				print("ERROR")
			
			self.firstShowImage()
	
	#Este metodo e chamado toda vez que o usuario clicar no programa
	#A ideia basica e que este ira cropar a imagem quando self.cropping for verdadeiro
	def mousePressEvent(self, QMouseEvent):
		#Pegando o indice/posicao da Tab que esta aberta no momento
		crntTab = self.ui.tabWidget.currentIndex()
		
		#Pegando posicoes (x,y) dos cliques
		xp = QMouseEvent.pos().x()
		yp = QMouseEvent.pos().y()
		
		#Pegando o tamanho da imagen
		xs = self.mQImage[crntTab].size().width()*self.factor[crntTab]
		ys = self.mQImage[crntTab].size().height()*self.factor[crntTab]
		
		#Pegando a posicao da imagem
		xip = self.labelImage[crntTab].pos().x()
		yip = self.labelImage[crntTab].pos().y()
		
		#Fazendo correcoes de cliques
		xp -= xip+11
		yp -= yip+44
		
		#Se os cliques ocorrerem dentro da imagem, e o usuario tiver apertado o botao "Adicionar Vaga", sera entao adicionada uma nova vaga ao programa
		if(0<=xp<=xs and 0<=yp<=ys and self.cropping[crntTab]==True):
			#Imagem e colocada nas suas proporcoes originais
			xp = int(xp / self.factor[crntTab])
			yp = int(yp / self.factor[crntTab])
			
			#A nova vaga tera seu indice como sendo o ultimo da self.vagas[crntTab]
			lastpos = len(self.vagas[crntTab])-1
			
			#De maneira geral, um ponto sera adicionado a self.vagas[crntTab][lastpos]
			#Depois que um ponto for adicionado, a cada novo ponto sera feita uma linha amarela
			#Quando houverem quatro linhas amarelas, teremos uma vaga e self.cropping[crntTab] passa a ser falsa
			#Quando uma vaga estiver formada, a mesma tera uma ROI criada para si
			if(len(self.vagas[crntTab][lastpos])==0):
				self.vagas[crntTab][lastpos].append((xp,yp))
			
			else:
				self.vagas[crntTab][lastpos].append((xp,yp))
	
				if len(self.vagas[crntTab][lastpos]) > 1:
					cv2.line(self.cvImage[crntTab], self.vagas[crntTab][lastpos][len(self.vagas[crntTab][lastpos])-2], self.vagas[crntTab][lastpos][len(self.vagas[crntTab][lastpos])-1], (255, 255,0), 2)
				
					height, width, byteValue = self.cvImage[crntTab].shape
					byteValue = byteValue * width
					self.mQImage[crntTab] = QImage(self.cvImage[crntTab], width, height, byteValue, QImage.Format_RGB888)	
			
				if len(self.vagas[crntTab][lastpos])==4:
					cv2.line(self.cvImage[crntTab], self.vagas[crntTab][lastpos][0], self.vagas[crntTab][lastpos][3], (255, 255, 0), 2)
					
					height, width, byteValue = self.cvImage[crntTab].shape
					byteValue = byteValue * width
					self.mQImage[crntTab] = QImage(self.cvImage[crntTab], width, height, byteValue, QImage.Format_RGB888)
					
					self.cropping[crntTab] = False
					
					self.showImage()
					
					self.cvRoi[crntTab].append(self.createRoi(self.cvClone[crntTab], self.vagas[crntTab][lastpos]))
						
					cvRoiName = self.fname[crntTab].split('/')
					cvRoiName = cvRoiName[len(cvRoiName)-1].split(".")[0]
					cvRoiName += str(lastpos)+".png"
						
					cv2.imwrite(cvRoiName, self.cvRoi[crntTab][lastpos])
					
					###h = cv2.calcHist([self.cvRoi[crntTab][lastpos]], [0], None, [256], [0, 256])
					###plt.figure()
					###plt.title("Histograma P&B")
					###plt.xlabel("Intensidade")
					###plt.ylabel("Qtde de Pixels")
					###plt.plot(h)
					###plt.xlim([0, 256])
					###plt.show()
									
				self.showImage()
	
	#Este metodo tem como funcao resetar todas as vagas de uma self.tab					
	def resetImage(self):
		#Pegando o indice/posicao da Tab que esta aberta no momento
		crntTab = self.ui.tabWidget.currentIndex()
		
		#A imagem passara ser igual a self.cvClone, que e a basicamente a imagem sera "limpa"
		#As vagas serao excluidas
		#A list Widget sera limpa
		#self.cropping passara a ser falsa
		height, width, byteValue = self.cvClone[crntTab].shape
		byteValue = byteValue * width
		self.cvImage[crntTab] = self.cvClone[crntTab].copy()
		self.vagas[crntTab] = []
		self.listWidgetEstadoVagas[crntTab].clear()
		self.mQImage[crntTab] = QImage(self.cvImage[crntTab], width, height, byteValue, QImage.Format_RGB888)
		
		self.cropping[crntTab] = False
		
		#Todas as ROI's serao apagadas
		for i in range(0, len(self.cvRoi[crntTab])):
			cvRoiName = self.fname[crntTab].split('/')
			cvRoiName = cvRoiName[len(cvRoiName)-1].split(".")[0]
			cvRoiName += str(i)+".png"
			os.remove(cvRoiName)
		
		self.cvRoi[crntTab] = []
		
		self.showImage()	
	
	#Este metodo tem como funcao remover apenas uma vaga
	def removeImage(self):
		#Pegando o indice/posicao da Tab que esta aberta no momento
		crntTab = self.ui.tabWidget.currentIndex()
		
		#Pega o indice da vaga selecionada
		delTextItem = self.listWidgetEstadoVagas[crntTab].currentItem().text()
		posRemove = int(delTextItem.split(" ")[1])-1
		
		#Renomeia todas as vagas da list Widget, a partir do indice selecionado, subtraindo 1
		for i in range(posRemove+1, len(self.listWidgetEstadoVagas[crntTab])):
			self.listWidgetEstadoVagas[crntTab].item(i).setText("Vaga "+ str(i))
		
		#Reinicia a self.cvImage
		self.cvImage[crntTab] = self.cvClone[crntTab].copy()
		#self.vagas[crntTab] tem a vaga com o indice selecionado removido
		self.vagas[crntTab].remove(self.vagas[crntTab][posRemove])
		
		#Remove a ROI de acordo com a vaga
		for i in range(len(self.cvRoi[crntTab])):
			cvRoiName = self.fname[crntTab].split('/')
			cvRoiName = cvRoiName[len(cvRoiName)-1].split(".")[0]
			cvRoiName += str(i)+".png"
			os.remove(cvRoiName)
		
		#Reinicia a self.cvRoi
		self.cvRoi[crntTab] = []
		
		#Redesenha as vagas restantes na self.cvImage, juntamente, gera outras ROI's baseadas nas vagas existentes
		for pos in range(len(self.vagas[crntTab])):
			cv2.line(self.cvImage[crntTab], self.vagas[crntTab][pos][0], self.vagas[crntTab][pos][1], (255, 255,0), 2)
			cv2.line(self.cvImage[crntTab], self.vagas[crntTab][pos][1], self.vagas[crntTab][pos][2], (255, 255,0), 2)
			cv2.line(self.cvImage[crntTab], self.vagas[crntTab][pos][2], self.vagas[crntTab][pos][3], (255, 255,0), 2)
			cv2.line(self.cvImage[crntTab], self.vagas[crntTab][pos][0], self.vagas[crntTab][pos][3], (255, 255,0), 2)
			
			self.cvRoi[crntTab].append(self.createRoi(self.cvClone[crntTab], self.vagas[crntTab][pos]))
						
			cvRoiName = self.fname[crntTab].split('/')
			cvRoiName = cvRoiName[len(cvRoiName)-1].split(".")[0]
			cvRoiName += str(pos)+".png"
				
			cv2.imwrite(cvRoiName, self.cvRoi[crntTab][pos])
				
		height, width, byteValue = self.cvImage[crntTab].shape
		byteValue = byteValue * width
		self.mQImage[crntTab] = QImage(self.cvImage[crntTab], width, height, byteValue, QImage.Format_RGB888)
		
		#Remove a row da vaga selecionada
		self.listWidgetEstadoVagas[crntTab].takeItem(self.listWidgetEstadoVagas[crntTab].currentRow())
		
		self.showImage()
		
	#Este metodo tem como funcao criar habilitar o cropping de uma imagem/video	
	def cropImage(self):
		#Pegando o indice/posicao da Tab que esta aberta no momento
		crntTab = self.ui.tabWidget.currentIndex()
		
		if(self.cropping[crntTab] == False):
			self.cropping[crntTab] = True
			self.vagas[crntTab].append([])
			self.listWidgetEstadoVagas[crntTab].addItem("Vaga "+str(len(self.vagas[crntTab])))
	
	#Este metodo tem como funcao salvar uma imagem/video
	def saveImage(self):
		crntTab = self.ui.tabWidget.currentIndex()
		
		if self.cropping[crntTab] == False:
			with open(self.svfname[crntTab], "wb") as fp:
				pickle.dump(self.vagas[crntTab], fp)
	
	#Este metodo tem como funcao mostrar uma imagem/video (no caso um item da self.mQImage na self.labelImage)
	def showImage(self, percent=None):
		#Pegando o indice/posicao da Tab que esta aberta no momento
		crntTab = self.ui.tabWidget.currentIndex()
		###print "Current tab is %d" % crntTab
		
		#self.factor[crntTab] e inicializado com 1, o que significa que a imagem mantem suas dimensoes normais
		#Mas, caso esta tenha altura > 500 ou largura > 1000, este sera redimensionado
		self.factor[crntTab] = 1
		if(self.mQImage[crntTab].width()>1000):
			self.factor[crntTab] = 1000/self.mQImage[crntTab].width()
			
		if(self.factor[crntTab]*self.mQImage[crntTab].height()>500):
			self.factor[crntTab] = 500/self.mQImage[crntTab].height()
		
		#Aqui a imagem e escalada para suas novas proporcoes, a label e ajustada para o tamanho novo da imagem, entao a imagem e "printada" na label
		width = self.mQImage[crntTab].width() * self.factor[crntTab]
		height = self.mQImage[crntTab].height() * self.factor[crntTab]
		image = self.mQImage[crntTab].scaled(width, height, Qt.KeepAspectRatio)
		self.labelImage[crntTab].setMinimumSize(width, height)
		self.labelImage[crntTab].setMaximumSize(width, height)
		self.labelImage[crntTab].setPixmap(QPixmap.fromImage(image))
		###self.ui.horizontalTabWidget.setWidth(1000)
	
	#Este metodo e o mesmo que o self.showImage, cuja unica diferenca e seu indice, segurando entao que uma imagem sera printada quando aberta
	#Este metodo tem como funcao mostrar uma imagem/video (no caso um item da self.mQImage na self.labelImage)
	def firstShowImage(self, percent=None):
		#self.factor[crntTab] e inicializado com 1, o que significa que a imagem mantem suas dimensoes normais
		#Mas, caso esta tenha altura > 500 ou largura > 1000, este sera redimensionado
		self.factor[self.tabQuant] = 1
		if(self.mQImage[self.tabQuant].width()>1000):
			self.factor[self.tabQuant] = 1000/self.mQImage[self.tabQuant].width()
			
		if(self.factor[self.tabQuant]*self.mQImage[self.tabQuant].height()>500):
			self.factor[self.tabQuant] = 500/self.mQImage[self.tabQuant].height()
		
		#Aqui a imagem e escalada para suas novas proporcoes, a label e ajustada para o tamanho novo da imagem, entao a imagem e "printada" na label
		width = self.mQImage[self.tabQuant].width() * self.factor[self.tabQuant]
		height = self.mQImage[self.tabQuant].height() * self.factor[self.tabQuant]
		image = self.mQImage[self.tabQuant].scaled(width, height, Qt.KeepAspectRatio)
		self.labelImage[self.tabQuant].setMinimumSize(width, height)
		self.labelImage[self.tabQuant].setMaximumSize(width, height)
		self.labelImage[self.tabQuant].setPixmap(QPixmap.fromImage(image))
		###self.ui.horizontalTabWidget.setWidth(1000)
	
	#Este metodo tem como funcao mudar a cor de uma vaga
	#Em geral, as vagas sao desenhadas com linhas amarelas, mas quando sao selecionadas atraves da list Widget, a vaga selecionada passa a ficar verde
	def changeSlotColor(self):
		#Pegando o indice/posicao da Tab que esta aberta no momento
		crntTab = self.ui.tabWidget.currentIndex()
		
		#Pega o indice da vaga selecionada
		actTextItem = self.listWidgetEstadoVagas[crntTab].currentItem().text()
		posActual = int(actTextItem.split(" ")[1])-1
		
		#Reinicia a self.cvImage
		self.cvImage[crntTab] = self.cvClone[crntTab].copy()
		
		#Redesenha as vagas restantes na self.cvImage, juntamente, gera outras ROI's baseadas nas vagas existentes
		#As vagas nao selecionadas ficam amarelas (255, 255, 0)
		#As vagas selecionadas ficam verdes (0, 255, 0)
		
		for pos in range(len(self.vagas[crntTab])):
			if pos != posActual:
				cv2.line(self.cvImage[crntTab], self.vagas[crntTab][pos][0], self.vagas[crntTab][pos][1], (255, 255,0), 2)
				cv2.line(self.cvImage[crntTab], self.vagas[crntTab][pos][1], self.vagas[crntTab][pos][2], (255, 255,0), 2)
				cv2.line(self.cvImage[crntTab], self.vagas[crntTab][pos][2], self.vagas[crntTab][pos][3], (255, 255,0), 2)
				cv2.line(self.cvImage[crntTab], self.vagas[crntTab][pos][0], self.vagas[crntTab][pos][3], (255, 255, 0), 2)	
		
		cv2.line(self.cvImage[crntTab], self.vagas[crntTab][posActual][0], self.vagas[crntTab][posActual][1], (0, 255, 0), 3)
		cv2.line(self.cvImage[crntTab], self.vagas[crntTab][posActual][1], self.vagas[crntTab][posActual][2], (0, 255, 0), 3)
		cv2.line(self.cvImage[crntTab], self.vagas[crntTab][posActual][2], self.vagas[crntTab][posActual][3], (0, 255, 0), 3)
		cv2.line(self.cvImage[crntTab], self.vagas[crntTab][posActual][0], self.vagas[crntTab][posActual][3], (0, 255, 0), 3)
				
		height, width, byteValue = self.cvImage[crntTab].shape
		byteValue = byteValue * width
		self.mQImage[crntTab] = QImage(self.cvImage[crntTab], width, height, byteValue, QImage.Format_RGB888)
	
		self.showImage()
	
	#Este metodo tem como funcao gerar uma roi
	def createRoi(self, clone, refPt):
		clone = cv2.cvtColor(clone, cv2.COLOR_RGB2BGR)
		mask = np.zeros(clone.shape, dtype=np.uint8)
		roi_corners = np.array([[refPt[0], refPt[1], refPt[2], refPt[3]]], dtype=np.int32)
		channel_count = clone.shape[2] 
		ignore_mask_color = (255,)*channel_count
		cv2.fillConvexPoly(mask, roi_corners, ignore_mask_color)
		roi = cv2.bitwise_and(clone, mask)
		roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
		
		return roi
	
	#Este metodo tem como funcao remover de maneira limpa a Tab Widget selecionada
	def removeCurrentTab(self, currentIndex):
		###print "Length of self.vagas == %d" % len(self.vagas)
		###print "Current Index is %d" % currentIndex
		
		for i in range(0, len(self.cvRoi[currentIndex])):
			cvRoiName = self.fname[currentIndex].split('/')
			cvRoiName = cvRoiName[len(cvRoiName)-1].split(".")[0]
			cvRoiName += str(i)+".png"
			os.remove(cvRoiName)
		
		self.cvRoi.remove(self.cvRoi[currentIndex])
		
		self.vagas.remove(self.vagas[currentIndex])
		self.cropping.remove(self.cropping[currentIndex])
		self.factor.remove(self.factor[currentIndex])
		self.fname.remove(self.fname[currentIndex])
		self.svfname.remove(self.svfname[currentIndex])
		self.mQImage.remove(self.mQImage[currentIndex])
		self.cvImage.remove(self.cvImage[currentIndex])
		self.cvClone.remove(self.cvClone[currentIndex])
		self.cvVideo.remove(self.cvVideo[currentIndex])
		
		self.layout.remove(self.layout[currentIndex])
		self.labelImage.remove(self.labelImage[currentIndex])
		self.labelEstadoVagas.remove(self.labelEstadoVagas[currentIndex])
		self.listWidgetEstadoVagas.remove(self.listWidgetEstadoVagas[currentIndex])
		self.pushButtonAddVaga.remove(self.pushButtonAddVaga[currentIndex])
		self.pushButtonRmVaga.remove(self.pushButtonRmVaga[currentIndex])
		self.pushButtonRstVaga.remove(self.pushButtonRstVaga[currentIndex])
		self.pushButtonSaveVaga.remove(self.pushButtonSaveVaga[currentIndex])
		
		self.tabs.remove(self.tabs[currentIndex])
		
		self.ui.tabWidget.removeTab(currentIndex)
		
		###print "\nNEW Length of self.vagas == %d\n\n" % len(self.vagas)
	
	#Este metodo tem como funcao remover todas as ROI's no momento em que o programa e fechado
	def closeEvent(self, QCloseEvent):
		for currentIndex in range(len(self.cvRoi)):
			for i in range(len(self.cvRoi[currentIndex])):
				cvRoiName = self.fname[currentIndex].split('/')
				cvRoiName = cvRoiName[len(cvRoiName)-1].split(".")[0]
				cvRoiName += str(i)+".png"
				os.remove(cvRoiName)
	
if __name__=="__main__":
	app = QApplication(sys.argv)
	w = MyForm()
	w.show()
	sys.exit(app.exec_())
