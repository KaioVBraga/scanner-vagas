from __future__ import division
import sys
import os
import pickle
import numpy as np
from matplotlib import pyplot as plt
import cv2
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from demoTest3 import *

class MyForm(QMainWindow):
	def __init__(self):
		super(QMainWindow, self).__init__();
		self.ui = Ui_MainWindow();
		self.ui.setupUi(self);
		
		self.uniImg = [];
		self.uniHist = [];
		self.uniImg.append(cv2.imread("uniEstLivre0.png"));
		self.uniImg.append(cv2.imread("uniEstLivre1.png"));
		self.uniHist.append(cv2.calcHist([self.uniImg[0]], [0], None, [256], [0, 256]))
		self.uniHist.append(cv2.calcHist([self.uniImg[1]], [0], None, [256], [0, 256]))
		
		self.ui.tabWidget.clear();
	
		self.tabQuant=0;
		
		self.tabs = [];
		self.vagas = [];
		self.cropping = [];
		self.factor = [];
		self.fname = [];
		self.svfname = [];
		self.mQImage = [];
		self.cvVideo = [];
		self.cvImage = [];
		self.cvClone = [];
		self.cvRoi = [];
		self.cvHist = [];
		self.colPos = [];
		
		
		self.layout = [];
		self.horLayout = [];
		self.labelImage = [];
		self.labelEstadoVagas = [];
		self.listWidgetEstadoVagas = [];
		self.pushButtonAddVaga = [];
		self.pushButtonRmVaga = [];
		self.pushButtonRstVaga = [];
		self.pushButtonSaveVaga = [];
		
		self.ui.actionAbrir_Camera.triggered.connect(self.fileOpen);
		self.show();
		
	def fileOpen(self):
		newName = unicode(QFileDialog.getOpenFileName(self, "Open file", "/home"));
		
		if not(newName in self.fname) and ('.' in newName):
			self.fname.append(newName);	
		
			self.tabQuant = self.ui.tabWidget.count();
		
			self.tabs.append(QWidget());
		
			self.ui.tabWidget.addTab(self.tabs[self.tabQuant], "Tab %d" % self.tabQuant)
		
			self.ui.tabWidget.setCurrentIndex(self.tabQuant);
		
			self.vagas.append(list());
			self.cropping.append(False);
			self.factor.append(1);
		
			self.labelImage.append(QLabel());
			self.labelEstadoVagas.append(QLabel("Estado das Vagas"));
			self.listWidgetEstadoVagas.append(QListWidget());
			self.pushButtonAddVaga.append(QPushButton("Adicionar Vaga"));
			self.pushButtonRmVaga.append(QPushButton("Remover Vaga"));
			self.pushButtonRstVaga.append(QPushButton("Resetar Vagas"));
			self.pushButtonSaveVaga.append(QPushButton("Salvar Vagas"));
		
			self.horLayout.append(QHBoxLayout());
			self.layout.append(QGridLayout());
			
			self.horLayout[self.tabQuant].addStretch();
			self.horLayout[self.tabQuant].addWidget(self.labelImage[self.tabQuant]);
			self.horLayout[self.tabQuant].addStretch();
			
			self.layout[self.tabQuant].addLayout(self.horLayout[self.tabQuant], 0, 0, 7, 1);
			self.layout[self.tabQuant].addWidget(self.labelEstadoVagas[self.tabQuant], 1, 1);
			self.layout[self.tabQuant].addWidget(self.listWidgetEstadoVagas[self.tabQuant], 2, 1);
			self.layout[self.tabQuant].addWidget(self.pushButtonAddVaga[self.tabQuant], 3, 1);
			self.layout[self.tabQuant].addWidget(self.pushButtonRmVaga[self.tabQuant], 4, 1);
			self.layout[self.tabQuant].addWidget(self.pushButtonRstVaga[self.tabQuant], 5, 1);
			self.layout[self.tabQuant].addWidget(self.pushButtonSaveVaga[self.tabQuant], 6, 1);
			
			self.layout[self.tabQuant].setColumnStretch(0, 100)
		
			self.ui.tabWidget.setTabText(self.tabQuant,"Camera %d" % (self.tabQuant+1))
			self.tabs[self.tabQuant].setLayout(self.layout[self.tabQuant])
		
			print(self.ui.tabWidget.count());
		
			self.connect(self.pushButtonAddVaga[self.tabQuant], SIGNAL("clicked()"), self.cropImage);
			self.connect(self.pushButtonRmVaga[self.tabQuant], SIGNAL("clicked()"), self.removeImage);
			self.connect(self.pushButtonRstVaga[self.tabQuant], SIGNAL("clicked()"), self.resetImage);
			self.connect(self.pushButtonSaveVaga[self.tabQuant], SIGNAL("clicked()"), self.saveImage);
			self.listWidgetEstadoVagas[self.tabQuant].itemClicked.connect(self.changeSlotColor)
			self.ui.tabWidget.tabCloseRequested.connect(self.removeCurrentTab)
		
			if self.fname[self.tabQuant]:
				self.loadFile();


	def loadFile(self):
		if self.fname[self.tabQuant]:
			self.svfname.append(self.fname[self.tabQuant].split("."));
			self.svfname[self.tabQuant] = self.svfname[self.tabQuant][0]+".txt";
			
			self.cvVideo.append(cv2.VideoCapture(self.fname[self.tabQuant]));
			ret, frame = self.cvVideo[self.tabQuant].read();
			
			self.cvImage.append(frame);
			
			height, width, byteValue = self.cvImage[self.tabQuant].shape;
			byteValue = byteValue * width;
		
			cv2.cvtColor(self.cvImage[self.tabQuant], cv2.COLOR_BGR2RGB, self.cvImage[self.tabQuant]);
			self.cvClone.append(self.cvImage[self.tabQuant].copy());
		
			self.mQImage.append(QImage(self.cvImage[self.tabQuant], width, height, byteValue, QImage.Format_RGB888));
			
			self.cvRoi.append(list());
			self.cvHist.append(list());
			self.colPos.append(-1);
			
			self.vagas[self.tabQuant] = [];
			self.listWidgetEstadoVagas[self.tabQuant].clear();
			
			self.start();
					
			try:
				with open(self.svfname[self.tabQuant], "rb") as fp:
					self.vagas[self.tabQuant] = pickle.load(fp)
					
					for pos in range(len(self.vagas[self.tabQuant])):
						cv2.line(self.cvImage[self.tabQuant], self.vagas[self.tabQuant][pos][0], self.vagas[self.tabQuant][pos][1], (255, 255, 0), 2);
						cv2.line(self.cvImage[self.tabQuant], self.vagas[self.tabQuant][pos][1], self.vagas[self.tabQuant][pos][2], (255, 255, 0), 2);
						cv2.line(self.cvImage[self.tabQuant], self.vagas[self.tabQuant][pos][2], self.vagas[self.tabQuant][pos][3], (255, 255, 0), 2);
						cv2.line(self.cvImage[self.tabQuant], self.vagas[self.tabQuant][pos][0], self.vagas[self.tabQuant][pos][3], (255, 255, 0), 2);
						
						
						self.cvRoi[self.tabQuant].append(self.createRoi(self.cvClone[self.tabQuant], self.vagas[self.tabQuant][pos]));
						
						cvRoiName = self.fname[self.tabQuant].split('/');
						cvRoiName = cvRoiName[len(cvRoiName)-1].split(".")[0];
						cvRoiName += str(pos)+".png";
						
						cv2.imwrite(cvRoiName, self.cvRoi[self.tabQuant][pos]);
						
						self.cvHist[self.tabQuant].append(cv2.calcHist([self.cvRoi[self.tabQuant][pos]], [0], None, [256], [0, 256]))
						
						# print "\nCOMPARACAO DA VAGA %d do ESTACIONAMENTO %d" % (pos+1, self.tabQuant+1)
						# print cv2.compareHist(self.cvHist[self.tabQuant][pos], self.uniHist[0], cv2.HISTCMP_CORREL)
						# print cv2.compareHist(self.cvHist[self.tabQuant][pos], self.uniHist[1], cv2.HISTCMP_CORREL)
						# print cv2.compareHist(self.cvHist[self.tabQuant][pos], self.uniHist[0], cv2.HISTCMP_CORREL) * cv2.compareHist(self.cvHist[self.tabQuant][pos], self.uniHist[1], cv2.HISTCMP_CORREL)
		
						
					height, width, byteValue = self.cvImage[self.tabQuant].shape;
					byteValue = byteValue * width;
					self.mQImage[self.tabQuant] = QImage(self.cvImage[self.tabQuant], width, height, byteValue, QImage.Format_RGB888);
					
					for i in range(0, len(self.vagas[self.tabQuant])):
						if cv2.compareHist(self.cvHist[self.tabQuant][i], self.uniHist[0], cv2.HISTCMP_CORREL) * cv2.compareHist(self.cvHist[self.tabQuant][pos], self.uniHist[1], cv2.HISTCMP_CORREL) > 0.80:
							self.listWidgetEstadoVagas[self.tabQuant].addItem("Vaga "+str(i+1)+" Ocupada");
						else:
							self.listWidgetEstadoVagas[self.tabQuant].addItem("Vaga "+str(i+1)+" Livre");
						
					self.firstShowImage();
			except:
				print("ERROR");
			
			self.firstShowImage()
	
	def mousePressEvent(self, QMouseEvent):
		crntTab = self.ui.tabWidget.currentIndex();
		
		xp = QMouseEvent.pos().x();
		yp = QMouseEvent.pos().y();
		xs = self.mQImage[crntTab].size().width()*self.factor[crntTab];
		ys = self.mQImage[crntTab].size().height()*self.factor[crntTab];
		xip = self.labelImage[crntTab].pos().x();
		yip = self.labelImage[crntTab].pos().y();
		
		xp -= xip+11;
		yp -= yip+44;
		
		if(0<=xp<=xs and 0<=yp<=ys and self.cropping[crntTab]==True):
			xp = int(xp / self.factor[crntTab]);
			yp = int(yp / self.factor[crntTab]);
			lastpos = len(self.vagas[crntTab])-1;
			
			if(len(self.vagas[crntTab][lastpos])==0):
				self.vagas[crntTab][lastpos].append((xp,yp));
			
			else:
				self.vagas[crntTab][lastpos].append((xp,yp));
	
				if len(self.vagas[crntTab][lastpos]) > 1:
					cv2.line(self.cvImage[crntTab], self.vagas[crntTab][lastpos][len(self.vagas[crntTab][lastpos])-2], self.vagas[crntTab][lastpos][len(self.vagas[crntTab][lastpos])-1], (255, 255,0), 2);
				
					height, width, byteValue = self.cvImage[crntTab].shape;
					byteValue = byteValue * width;
					self.mQImage[crntTab] = QImage(self.cvImage[crntTab], width, height, byteValue, QImage.Format_RGB888);	
			
				if len(self.vagas[crntTab][lastpos])==4:
					cv2.line(self.cvImage[crntTab], self.vagas[crntTab][lastpos][0], self.vagas[crntTab][lastpos][3], (255, 255, 0), 2);
					
					height, width, byteValue = self.cvImage[crntTab].shape;
					byteValue = byteValue * width;
					self.mQImage[crntTab] = QImage(self.cvImage[crntTab], width, height, byteValue, QImage.Format_RGB888);
					
					self.cropping[crntTab] = False;
					
					self.showImage();
					
					self.cvRoi[crntTab].append(self.createRoi(self.cvClone[crntTab], self.vagas[crntTab][lastpos]));
						
					cvRoiName = self.fname[crntTab].split('/');
					cvRoiName = cvRoiName[len(cvRoiName)-1].split(".")[0];
					cvRoiName += str(lastpos)+".png";
						
					cv2.imwrite(cvRoiName, self.cvRoi[crntTab][lastpos]);
					
					self.cvHist[crntTab].append(cv2.calcHist([self.cvRoi[crntTab][lastpos]], [0], None, [256], [0, 256]))
					
					# print "\nCOMPARACAO DA VAGA %d do ESTACIONAMENTO %d" % (lastpos+1, crntTab+1)
					# print cv2.compareHist(self.cvHist[crntTab][lastpos], self.uniHist[0], cv2.HISTCMP_CORREL)
					# print cv2.compareHist(self.cvHist[crntTab][lastpos], self.uniHist[1], cv2.HISTCMP_CORREL)
					# print cv2.compareHist(self.cvHist[crntTab][lastpos], self.uniHist[0], cv2.HISTCMP_CORREL) * cv2.compareHist(self.cvHist[crntTab][lastpos], self.uniHist[1], cv2.HISTCMP_CORREL)
					
					if cv2.compareHist(self.cvHist[crntTab][lastpos], self.uniHist[0], cv2.HISTCMP_CORREL) * cv2.compareHist(self.cvHist[crntTab][lastpos], self.uniHist[1], cv2.HISTCMP_CORREL) > 0.80:
						self.listWidgetEstadoVagas[crntTab].item(lastpos).setText("Vaga "+ str(lastpos+1)+" Ocupada");
					else:
						self.listWidgetEstadoVagas[crntTab].item(lastpos).setText("Vaga "+ str(lastpos+1)+" Livre");				
				
				self.showImage();
						
	def resetImage(self):
		crntTab = self.ui.tabWidget.currentIndex();
		
		height, width, byteValue = self.cvClone[crntTab].shape;
		byteValue = byteValue * width;
		self.cvImage[crntTab] = self.cvClone[crntTab].copy();
		self.vagas[crntTab] = [];
		self.listWidgetEstadoVagas[crntTab].clear();
		self.mQImage[crntTab] = QImage(self.cvImage[crntTab], width, height, byteValue, QImage.Format_RGB888);
		
		self.cropping[crntTab] = False;
		
		for i in range(0, len(self.cvRoi[crntTab])):
			cvRoiName = self.fname[crntTab].split('/');
			cvRoiName = cvRoiName[len(cvRoiName)-1].split(".")[0];
			cvRoiName += str(i)+".png";
			os.remove(cvRoiName);
		
		self.cvRoi[crntTab] = [];
		self.cvHist[crntTab] = [];
		
		self.showImage();	
	
	def removeImage(self):
		crntTab = self.ui.tabWidget.currentIndex();
		
		delTextItem = self.listWidgetEstadoVagas[crntTab].currentItem().text();
		posRemove = int(delTextItem.split(" ")[1])-1;
		
		self.cvImage[crntTab] = self.cvClone[crntTab].copy();
		self.vagas[crntTab].remove(self.vagas[crntTab][posRemove]);
		
		for i in range(len(self.cvRoi[crntTab])):
			cvRoiName = self.fname[crntTab].split('/');
			cvRoiName = cvRoiName[len(cvRoiName)-1].split(".")[0];
			cvRoiName += str(i)+".png";
			os.remove(cvRoiName);
		
		self.cvRoi[crntTab] = [];
		self.cvHist[crntTab] = [];
		
		for pos in range(len(self.vagas[crntTab])):
			cv2.line(self.cvImage[crntTab], self.vagas[crntTab][pos][0], self.vagas[crntTab][pos][1], (255, 255,0), 2);
			cv2.line(self.cvImage[crntTab], self.vagas[crntTab][pos][1], self.vagas[crntTab][pos][2], (255, 255,0), 2);
			cv2.line(self.cvImage[crntTab], self.vagas[crntTab][pos][2], self.vagas[crntTab][pos][3], (255, 255,0), 2);
			cv2.line(self.cvImage[crntTab], self.vagas[crntTab][pos][0], self.vagas[crntTab][pos][3], (255, 255,0), 2);
			
			self.cvRoi[crntTab].append(self.createRoi(self.cvClone[crntTab], self.vagas[crntTab][pos]));
						
			cvRoiName = self.fname[crntTab].split('/');
			cvRoiName = cvRoiName[len(cvRoiName)-1].split(".")[0];
			cvRoiName += str(pos)+".png";
				
			cv2.imwrite(cvRoiName, self.cvRoi[crntTab][pos]);
			
			self.cvHist[crntTab].append(cv2.calcHist([self.cvRoi[crntTab][pos]], [0], None, [256], [0, 256]))
				
		height, width, byteValue = self.cvImage[crntTab].shape;
		byteValue = byteValue * width;
		self.mQImage[crntTab] = QImage(self.cvImage[crntTab], width, height, byteValue, QImage.Format_RGB888);
		
		for i in range(posRemove+1, len(self.listWidgetEstadoVagas[crntTab])):
			if cv2.compareHist(self.cvHist[crntTab][i-1], self.uniHist[0], cv2.HISTCMP_CORREL) * cv2.compareHist(self.cvHist[crntTab][i-1], self.uniHist[1], cv2.HISTCMP_CORREL)> 0.80:
				self.listWidgetEstadoVagas[crntTab].item(i).setText("Vaga "+ str(i)+" Ocupada");
			else:
				self.listWidgetEstadoVagas[crntTab].item(i).setText("Vaga "+ str(i)+" Livre");
		
		self.listWidgetEstadoVagas[crntTab].takeItem(self.listWidgetEstadoVagas[crntTab].currentRow());
		
		self.showImage();
		
	def cropImage(self):
		crntTab = self.ui.tabWidget.currentIndex();
		
		if(self.cropping[crntTab] == False):
			self.cropping[crntTab] = True;
			self.vagas[crntTab].append([]);
			self.listWidgetEstadoVagas[crntTab].addItem("Vaga "+str(len(self.vagas[crntTab])));
	
	def saveImage(self):
		crntTab = self.ui.tabWidget.currentIndex();
		
		if self.cropping[crntTab] == False:
			with open(self.svfname[crntTab], "wb") as fp:
				pickle.dump(self.vagas[crntTab], fp)
	
	def showImage(self, percent=None):
		crntTab = self.ui.tabWidget.currentIndex();
		# print "Current tab is %d" % crntTab
		
		self.factor[crntTab] = 1;
		if(self.mQImage[crntTab].width()>1000):
			self.factor[crntTab] = 1000/self.mQImage[crntTab].width();
			
		if(self.factor[crntTab]*self.mQImage[crntTab].height()>500):
			self.factor[crntTab] = 500/self.mQImage[crntTab].height();
		
		width = self.mQImage[crntTab].width() * self.factor[crntTab];
		height = self.mQImage[crntTab].height() * self.factor[crntTab];
		image = self.mQImage[crntTab].scaled(width, height, Qt.KeepAspectRatio)
		self.labelImage[crntTab].setMinimumSize(width, height)
		self.labelImage[crntTab].setMaximumSize(width, height)
		self.labelImage[crntTab].setPixmap(QPixmap.fromImage(image))
	
	def firstShowImage(self, percent=None):
		self.factor[self.tabQuant] = 1;
		if(self.mQImage[self.tabQuant].width()>1000):
			self.factor[self.tabQuant] = 1000/self.mQImage[self.tabQuant].width();
			
		if(self.factor[self.tabQuant]*self.mQImage[self.tabQuant].height()>500):
			self.factor[self.tabQuant] = 500/self.mQImage[self.tabQuant].height();
		
		width = self.mQImage[self.tabQuant].width() * self.factor[self.tabQuant];
		height = self.mQImage[self.tabQuant].height() * self.factor[self.tabQuant];
		image = self.mQImage[self.tabQuant].scaled(width, height, Qt.KeepAspectRatio)
		self.labelImage[self.tabQuant].setMinimumSize(width, height)
		self.labelImage[self.tabQuant].setMaximumSize(width, height)
		self.labelImage[self.tabQuant].setPixmap(QPixmap.fromImage(image))
	
	def changeSlotColor(self):
		crntTab = self.ui.tabWidget.currentIndex();
	
		actTextItem = self.listWidgetEstadoVagas[crntTab].currentItem().text();
		self.colPos[crntTab] = int(actTextItem.split(" ")[1])-1;
	
		self.cvImage[crntTab] = self.cvClone[crntTab].copy();
		
		for pos in range(len(self.vagas[crntTab])):
			if pos != self.colPos[crntTab]:
				cv2.line(self.cvImage[crntTab], self.vagas[crntTab][pos][0], self.vagas[crntTab][pos][1], (255, 255,0), 2);
				cv2.line(self.cvImage[crntTab], self.vagas[crntTab][pos][1], self.vagas[crntTab][pos][2], (255, 255,0), 2);
				cv2.line(self.cvImage[crntTab], self.vagas[crntTab][pos][2], self.vagas[crntTab][pos][3], (255, 255,0), 2);
				cv2.line(self.cvImage[crntTab], self.vagas[crntTab][pos][0], self.vagas[crntTab][pos][3], (255, 255, 0), 2);
		
		if self.colPos[crntTab] != -1:
			cv2.line(self.cvImage[crntTab], self.vagas[crntTab][self.colPos[crntTab]][0], self.vagas[crntTab][self.colPos[crntTab]][1], (0, 255, 0), 3);
			cv2.line(self.cvImage[crntTab], self.vagas[crntTab][self.colPos[crntTab]][1], self.vagas[crntTab][self.colPos[crntTab]][2], (0, 255, 0), 3);
			cv2.line(self.cvImage[crntTab], self.vagas[crntTab][self.colPos[crntTab]][2], self.vagas[crntTab][self.colPos[crntTab]][3], (0, 255, 0), 3);
			cv2.line(self.cvImage[crntTab], self.vagas[crntTab][self.colPos[crntTab]][0], self.vagas[crntTab][self.colPos[crntTab]][3], (0, 255, 0), 3);
				
		height, width, byteValue = self.cvImage[crntTab].shape;
		byteValue = byteValue * width;
		self.mQImage[crntTab] = QImage(self.cvImage[crntTab], width, height, byteValue, QImage.Format_RGB888);
		
		self.showImage();
	
	def createRoi(self, clone, refPt):
		clone = cv2.cvtColor(clone, cv2.COLOR_RGB2BGR);
		mask = np.zeros(clone.shape, dtype=np.uint8);
		roi_corners = np.array([[refPt[0], refPt[1], refPt[2], refPt[3]]], dtype=np.int32);
		channel_count = clone.shape[2]; 
		ignore_mask_color = (255,)*channel_count;
		cv2.fillConvexPoly(mask, roi_corners, ignore_mask_color);
		roi = cv2.bitwise_and(clone, mask);
		roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY);
		
		xbig = 0
		xsmall = 0
		for j in range(len(refPt)):
			if j==0 or refPt[j][0] > xbig:
				xbig = refPt[j][0]
			
			if j==0 or refPt[j][0] < xsmall:
				xsmall = refPt[j][0]
		
		ybig = 0
		ysmall = 0
		for i in range(len(refPt)):
			if i==0 or refPt[i][1] > ybig:
				ybig = refPt[i][1]
			
			if i==0 or refPt[i][1] < ysmall:
				ysmall = refPt[i][1]
		
		roi = roi[ysmall:ybig, xsmall:xbig]
		
		return roi;
	
	def removeCurrentTab(self, currentIndex):
		# print "Length of self.vagas == %d" % len(self.vagas);
		# print "Current Index is %d" % currentIndex;
		
		for i in range(0, len(self.cvRoi[currentIndex])):
			cvRoiName = self.fname[currentIndex].split('/');
			cvRoiName = cvRoiName[len(cvRoiName)-1].split(".")[0];
			cvRoiName += str(i)+".png";
			os.remove(cvRoiName);
		
		self.cvRoi.remove(self.cvRoi[currentIndex]);
		
		self.vagas.remove(self.vagas[currentIndex]);
		self.cropping.remove(self.cropping[currentIndex]);
		self.factor.remove(self.factor[currentIndex]);
		self.fname.remove(self.fname[currentIndex]);
		self.svfname.remove(self.svfname[currentIndex]);
		self.mQImage.remove(self.mQImage[currentIndex]);
		self.cvImage.remove(self.cvImage[currentIndex]);
		self.cvClone.remove(self.cvClone[currentIndex]);
		self.cvHist.remove(self.cvHist[currentIndex]);
		
		self.layout.remove(self.layout[currentIndex]);
		self.labelImage.remove(self.labelImage[currentIndex]);
		self.labelEstadoVagas.remove(self.labelEstadoVagas[currentIndex]);
		self.listWidgetEstadoVagas.remove(self.listWidgetEstadoVagas[currentIndex]);
		self.pushButtonAddVaga.remove(self.pushButtonAddVaga[currentIndex]);
		self.pushButtonRmVaga.remove(self.pushButtonRmVaga[currentIndex]);
		self.pushButtonRstVaga.remove(self.pushButtonRstVaga[currentIndex]);
		self.pushButtonSaveVaga.remove(self.pushButtonSaveVaga[currentIndex]);
		
		self.tabs.remove(self.tabs[currentIndex]);
		
		self.ui.tabWidget.removeTab(currentIndex);
		
		# print "\nNEW Length of self.vagas == %d\n\n" % len(self.vagas);
	
	def closeEvent(self, QCloseEvent):
		for currentIndex in range(len(self.cvRoi)):
			for i in range(len(self.cvRoi[currentIndex])):
				cvRoiName = self.fname[currentIndex].split('/');
				cvRoiName = cvRoiName[len(cvRoiName)-1].split(".")[0];
				cvRoiName += str(i)+".png";
				os.remove(cvRoiName);
	
	def nextFrameSlot(self):
		crntTab = self.ui.tabWidget.currentIndex();
		ret, frame = self.cvVideo[crntTab].read();
		self.cvImage[crntTab] = frame;
		height, width, byteValue = self.cvImage[crntTab].shape;
		byteValue = byteValue * width;
		cv2.cvtColor(self.cvImage[crntTab], cv2.COLOR_BGR2RGB, self.cvImage[crntTab]);
		self.cvClone[crntTab] = self.cvImage[crntTab].copy();
		self.mQImage[crntTab] = QImage(self.cvImage[crntTab], width, height, byteValue, QImage.Format_RGB888);
		
		for i in range(0, len(self.cvRoi[crntTab])):
			cvRoiName = self.fname[crntTab].split('/');
			cvRoiName = cvRoiName[len(cvRoiName)-1].split(".")[0];
			cvRoiName += str(i)+".png";
			os.remove(cvRoiName);
		
		self.cvRoi[crntTab] = [];
		self.cvHist[crntTab] = [];
		
		for pos in range(len(self.vagas[crntTab])):
			if pos != self.colPos[crntTab]:
				cv2.line(self.cvImage[crntTab], self.vagas[crntTab][pos][0], self.vagas[crntTab][pos][1], (255, 255,0), 2);
				cv2.line(self.cvImage[crntTab], self.vagas[crntTab][pos][1], self.vagas[crntTab][pos][2], (255, 255,0), 2);
				cv2.line(self.cvImage[crntTab], self.vagas[crntTab][pos][2], self.vagas[crntTab][pos][3], (255, 255,0), 2);
				cv2.line(self.cvImage[crntTab], self.vagas[crntTab][pos][0], self.vagas[crntTab][pos][3], (255, 255, 0), 2);
		
			self.cvRoi[crntTab].append(self.createRoi(self.cvClone[crntTab], self.vagas[crntTab][pos]));
						
			cvRoiName = self.fname[crntTab].split('/');
			cvRoiName = cvRoiName[len(cvRoiName)-1].split(".")[0];
			cvRoiName += str(pos)+".png";
			
			cv2.imwrite(cvRoiName, self.cvRoi[crntTab][pos]);
		
			self.cvHist[crntTab].append(cv2.calcHist([self.cvRoi[crntTab][pos]], [0], None, [256], [0, 256]))
		
		
			
			if cv2.compareHist(self.cvHist[crntTab][pos], self.uniHist[0], cv2.HISTCMP_CORREL) * cv2.compareHist(self.cvHist[crntTab][pos], self.uniHist[1], cv2.HISTCMP_CORREL) > 0.80:
				self.listWidgetEstadoVagas[crntTab].item(pos).setText("Vaga "+ str(pos+1)+" Ocupada");
			else:
				self.listWidgetEstadoVagas[crntTab].item(pos).setText("Vaga "+ str(pos+1)+" Livre");
		
		if self.colPos[crntTab] != -1:
			cv2.line(self.cvImage[crntTab], self.vagas[crntTab][self.colPos[crntTab]][0], self.vagas[crntTab][self.colPos[crntTab]][1], (0, 255, 0), 3);
			cv2.line(self.cvImage[crntTab], self.vagas[crntTab][self.colPos[crntTab]][1], self.vagas[crntTab][self.colPos[crntTab]][2], (0, 255, 0), 3);
			cv2.line(self.cvImage[crntTab], self.vagas[crntTab][self.colPos[crntTab]][2], self.vagas[crntTab][self.colPos[crntTab]][3], (0, 255, 0), 3);
			cv2.line(self.cvImage[crntTab], self.vagas[crntTab][self.colPos[crntTab]][0], self.vagas[crntTab][self.colPos[crntTab]][3], (0, 255, 0), 3);
		
		
		
		self.showImage();

	def start(self):
		self.timer = QTimer()
		self.timer.timeout.connect(self.nextFrameSlot)
		self.timer.start(1000./30)
	
if __name__=="__main__":
	app = QApplication(sys.argv);
	w = MyForm();
	w.show();
	sys.exit(app.exec_());
