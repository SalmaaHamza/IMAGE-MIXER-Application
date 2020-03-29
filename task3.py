
import sys
import pandas as pd 
import pyqtgraph as pg
from PyQt5 import QtWidgets,QtCore,QtGui,uic 
from PyQt5.QtGui import QIcon, QPixmap
import cv2
import img1 as ui
import numpy as np
from PIL import Image
import glob,os
import logging
from modesEnum import Modes
from imageModel import ImageModel as image
logging.basicConfig(filename="newfile.log", 
            format='%(asctime)s %(message)s', 
            filemode='w') 
#Creating an object 
logger=logging.getLogger() 

#Setting the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG) 


class MyWindow(QtWidgets.QMainWindow):
   
    def __init__(self, parent=None):
       
                
        
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)
      
        self.choose = [self.ui.option1,self.ui.option2]
        self.output = [self.ui.output1,self.ui.output2]
        self.open = [self.ui.actionimg1,self.ui.actionimg2]
        self.compimgs = ["FT_Mag","FT_Phase","FT_Real","FT_Imag"]
        # for i in range (len(self.open)):
        self.open[0].triggered.connect(lambda : self.getfiles(0))
        self.open[1].triggered.connect(lambda : self.getfiles(1)) 
        self.ui.actionExit.triggered.connect(self.Exit)
        self.choose[0].activated.connect(lambda:self.options(0))
        self.choose[1].activated.connect(lambda:self.options(1))
        self.save_removed = []
        self.complete_size=[0,0]
        self.value =[0,0]
        self.size = 0
        self.out_dispaly = 0
        self.index =[]
        self.ImgData = [0,0]
        self.rmvFlag = True

        # for i in range(self.output):
        #    self.output.activated.connect()
        self.mix_comp = [self.ui.compchosen1,self.ui.compchosen2]   
        # for i in range(len(self.mix_comp)):
        self.mix_comp[0].activated.connect(lambda:self.mix_options(0))
        self.mix_comp[1].activated.connect(lambda:self.mix_options(1))
        self.ChooseImage = [self.ui.imagechosen1,self.ui.imagechosen2]
        self.ChooseImage[0].activated.connect(lambda : self.check_imgs(0))
        self.ChooseImage[1].activated.connect(lambda : self.check_imgs(1))
        self.mixing_data=[[],[]]
        self.allcomponent=[[],[]]
        self.image =[]
        self.output_display = 0
        self.ui.outputoptions.activated.connect(self.outputFlag)
       
        self.Img_viewer = [self.ui.org_img1,self.ui.org_img2,self.ui.comp_img1,self.ui.comp_img2,self.ui.img_out1,self.ui.img_out2]

        self.magChoose = ["Phase","uniform phase","Options"]
    
        self.phaseChoose = ["Magnitude","uniform magnitude","Options"]
        self.realChoose = ["Imaginary","Options"]
        self.imagChoose = ["Real","Options"]
        self.all_optionsExists = ["Options","Imaginary","Magnitude","uniform magnitude","Phase","uniform phase","Real"]
     
        self.ratioMixing = [self.ui.ratio2_2 ,self.ui.ratio2]
        self.ratioMixing[0].valueChanged.connect(lambda:self.sliderRatio(0))
        self.ratioMixing[1].valueChanged.connect(lambda:self.sliderRatio(1))
     
        self.List_imagesData = [[],[]]
        self.statusFlag =[0,0]
        self.value = [0,0]
        
        self.imags=[[],[]]
        self.path=["",""]
             
       
    def getfiles(self,imgflag):
     
        self.path[imgflag],extention = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "",
             "(*.jpg);;(*.png);;(*.jpeg)")
     
        path = self.path[imgflag]
        self.imags[imgflag] = image(path)
        width = self.imags[imgflag].width
        height = self.imags[imgflag].height

        pixmap = QPixmap(path)
        logger.info("Open Image"+str(imgflag))
        self.List_imagesData[imgflag] = [width,height]
   
        if ((self.List_imagesData[0] != []) & (self.List_imagesData[1] != [])):
            if (self.check_size()):
                self.display(pixmap,imgflag)          
             
            else:
                pass
        else:
            self.display(pixmap,imgflag)
           
    def check_size(self):
        if (self.List_imagesData[0][0] == self.List_imagesData[1][0] )& (self.List_imagesData[0][1]== self.List_imagesData[1][1]):
          
            same_size = True
            logger.info("Two images have the same size")
        else:
            self.ui.statusBar.showMessage("The two images Don't have the same Size")
            logger.error("The Two images don't have the same size") 
            same_size = False
        return(same_size)
       
    def display(self,pixmap,flag):
        w =self.Img_viewer[flag].width()
        h =self.Img_viewer[flag].height()
        self.Img_viewer[flag].clear()  
        self.Img_viewer[flag].setPixmap(pixmap.scaled(w,h,QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation))
        logger.info("Display Image")
        return 
    
      
    def options(self,flag):     
        filename = ''
        Data =[]
        logger.info("combobox"+str(flag)+"Clicked")   
        if ( self.choose[flag].currentText() == "FT_Mag"):
            Data = 20*np.log(self.imags[flag].magnitude )
            logger.info("FT_Mag Component is selected")   
        elif( self.choose[flag].currentText() == "FT_Phase"):
            Data = self.imags[flag].phase
            logger.info("FT_Phase Component is selected") 
        elif(self.choose[flag].currentText()== "FT_Real"):
            Data = self.imags[flag].real  
            logger.info("FT_real Component is selected") 
        elif(self.choose[flag].currentText() == "FT_Imag"):
            Data = self.imags[flag].imaginary
            logger.info("Imag Component is selected") 
        else:
            logger.warning("Nothing is selected") 
        
        if (len(Data) > 0):
            self.allcomponent[flag] = Data   
            self.save(flag,self.allcomponent[flag],flag+2)
        else:
            logger.warning("Nothing is selected To display") 

    def save(self,flag,allcompdata,labelNo):
        checkflag = flag
        if len(allcompdata)  > 0 :
            if (self.imags[flag] == []):
                flag = 0
            else:
                pass
            allcompdata =np.array(allcompdata).reshape(self.imags[flag].width,self.imags[flag].height).astype(np.uint8)
            filename = QtGui.QImage(allcompdata,allcompdata.shape[0],allcompdata.shape[1],QtGui.QImage.Format_Grayscale8)
            pixmap = QPixmap(filename)
            self.display(pixmap,labelNo)

    def mix_options(self,flag):
        self.savedItems = []  
        self.rmvFlag = True
        if str(self.mix_comp[flag].currentText())=="Magnitude":
            self.savedItems = self.magChoose
            
            self.statusFlag[flag]=1
            logger.info("Magnitude is selected as component  " +str(flag+1)) 

        elif str(self.mix_comp[flag].currentText())=="Phase":
            self.savedItems = self.phaseChoose
           
            self.statusFlag[flag]=2
            logger.info("Phase is selected as component  " +str(flag+1)) 


        elif str(self.mix_comp[flag].currentText())=="Real":
            self.save_removed = self.realChoose
            self.statusFlag[flag]=3
            logger.info("Real is selected as component  " +str(flag+1)) 

        elif str(self.mix_comp[flag].currentText())=="Imaginary":
            self.savedItems = self.imagChoose
            self.statusFlag[flag]=4
            logger.info("Imaginary is selected as component  " +str(flag+1)) 

        elif str(self.mix_comp[flag].currentText())=="uniform magnitude":
            self.savedItems = self.magChoose
            self.statusFlag[flag]=5
            logger.info("unifrom magnitude is selected as component  " +str(flag+1)) 
        elif str(self.mix_comp[flag].currentText())=="uniform phase":
            self.savedItems = self.phaseChoose
            self.statusFlag[flag]=6
            
            logger.info("unifrom phase is selected as component  " +str(flag+1)) 
        
        elif str(self.mix_comp[flag].currentText())=="Options":
            self.rmvFlag = False
            self.savedItems = self.all_optionsExists 

        Elements = self.savedItems  
      
        if (len(Elements)>0):
            if (self.rmvFlag):
                if (self.statusFlag[flag] == 5 and self.statusFlag[not(flag)]==6) or (self.statusFlag[flag] == 6 and self.statusFlag[not(flag)]==5):
                    Element = Elements[1]
                    Elements[1] = Elements[0]
                    Elements[0] = Element
                   
                self.mix_comp[not(flag)].clear()
                for element in Elements:
                        self.mix_comp[not(flag)].addItem(element)
            else:
                self.mix_comp[flag].clear()
                for element in Elements:
                        self.mix_comp[flag].addItem(element)

            

            self.Mixer_equations()
 
    def Exit(self):
        for infile in glob.glob("*.png"):
            os.remove(str(infile))
        
    def check_imgs(self,flag):
        
        if str(self.ChooseImage[flag].currentText()) ==  "Img_1":
            self.ImgData[flag] = 1
            logger.info("Image 1 is selected as input " +str(flag+1)) 
    
        elif str(self.ChooseImage[flag].currentText()) ==  "Img_2":
            self.ImgData[flag] = 2
            logger.info("Image 1 is selected as input " +str(flag+1)) 
        else:
            logger.warning("No image if selected as input till now") 
        self.Mixer_equations()
      
    def sliderRatio(self,flag):   
        ratio = self.ratioMixing[flag].value()
        self.value[flag] = 0.01 * ratio 
        logger.warning("Value of slider"+str(flag+1)+"changed")      
        self.Mixer_equations()
  
    def Mixer_equations(self):
        Data= [self.imags[self.ImgData[0]-1],self.imags[self.ImgData[1]-1]]
        outputData = np.array([])
            
        
        for i in range(2):  
      
        
            if(self.statusFlag[i] == 3 & self.statusFlag[not(i)] == 4):
            # Real -- Imag
                logger.info("Real of input 1 $ imaginary of input 2") 
                outputData = Data[i].mix(Data(not(i)),self.value[i] ,self.value[not(i)],Modes.realAndImaginary)

                
            elif(self.statusFlag[i] == 4) & (self.statusFlag[not(i)] == 3):
                #Real -- Imag
                outputData = Data[not(i)].mix(Data[i],self.value[not(i)] ,self.value[i],Modes.realAndImaginary)
                logger.info("Real of input 1 $ imaginary of input 2") 
        
            elif(self.statusFlag[i] == 1)&(self.statusFlag[not(i)] == 2):
                #Mag  --- Phase
            
                outputData = Data[i].mix(Data[not(i)],self.value[i] ,self.value[not(i)],Modes.magnitudeAndPhase)
                logger.info("Real of input 1 $ imaginary of input 2") 

            elif(self.statusFlag[not(i)] == 1)&(self.statusFlag[i] == 2):
                #Mag -- Phase
                outputData = Data[not(i)].mix(Data[i],self.value[not(i)] ,self.value[i],Modes.magnitudeAndPhase)
                logger.info("Real of input 1 $ imaginary of input 2") 
            
            elif(self.statusFlag[i] == 1)&(self.statusFlag[not(i)] == 6):
                #Mag -- unifromPhase
                outputData = Data[i].mix(Data[not(i)],self.value[i] ,self.value[not(i)],Modes.magnitudeAndUnifromPhase)
                logger.info("Magnitude of input 1 $ unifromPhase of input 2") 

            elif(self.statusFlag[i] == 6)&(self.statusFlag[not(i)] == 1):
                #Mag -- UnifromPhase
                outputData = Data[not(i)].mix(Data[i],self.value[not(i)] ,self.value[i],Modes.magnitudeAndUnifromPhase)
                logger.info("Magnitude of input 2 $ unifromPhase of input 1") 
            
            elif(self.statusFlag[i] == 2) & (self.statusFlag[not(i)] == 5):
                #Mag -- UnifromPhase
                outputData = Data[i].mix(Data[not(i)],self.value[i] ,self.value[not(i)],Modes.unifromMagnitudeAndPhase)
                logger.info("unifromMagnitude of input 1 $ Phase of input 2") 
            
            elif(self.statusFlag[i] == 5 )&( self.statusFlag[not(i)] == 2):
                #Mag -- UnifromPhase
                outputData = Data[not(i)].mix(Data[i],self.value[not(i)] ,self.value[i],Modes.unifromMagnitudeAndPhase)
                logger.info("unifromMagnitude of input 2 $ Phase of input 1") 
        
            elif (self.statusFlag[i] == 5) & (self.statusFlag[not(i)] == 6):
              
                outputData = Data[i].mix(Data[not(i)],self.value[i] ,self.value[not(i)],Modes.unifromMagnitudeAndUnifromPhase)
                logger.info("unifromMagnitude of input 1 $ unifromPhase of input 2") 
        
            elif (self.statusFlag[i] == 6 )& (self.statusFlag[not(i)] == 5):
           
                outputData = Data[not(i)].mix(Data[i],self.value[not(i)] ,self.value[i],Modes.unifromMagnitudeAndUnifromPhase)
                logger.info("unifromMagnitude of input 2 $ unifromPhase of input 1") 
                
            else:
                pass
        
        
    
    
        self.update_Image(outputData)

    def outputFlag(self):
        if (str(self.ui.outputoptions.currentText())=="Output_1"):
            self.output_display = 1
            
        else:
             self.output_display = 2

    def update_Image(self,Data):
        flag = self.output_display-1
      
        image = self.image
        if (flag>=0)&(len(Data)>0):
            self.save(flag,Data,flag+4)
           
        else:
            pass
      


          

                
            


            









        
            


        



        
    










if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow() 
    window.show()
    sys.exit(app.exec_())