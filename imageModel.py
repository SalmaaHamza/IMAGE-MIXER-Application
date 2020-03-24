## This is the abstract class that the students should implement

from modesEnum import Modes
import numpy as np
import cv2
import matplotlib.pyplot as plt

import logging
#Creating an object 
logger=logging.getLogger() 

#Setting the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG) 


class ImageModel():

    """
    A class that represents the ImageModel
    """

    def __init__(self):
        pass

    def __init__(self, imgPath: str):
        self.imgPath = imgPath
        self.imgByte = cv2.imread(self.imgPath,0)
        self.dft = np.fft.fft2(self.imgByte)
        
        self.real = np.real(self.dft )
        self.imaginary =  np.imag(self.dft )
        self.magnitude = np.abs(self.dft )
        self.phase =  np.angle(self.dft )
        
        self.size = self.dft.shape[0]
        self.uniformPhase = np.zeros(self.imgByte.shape,dtype=int)
        self.unifromMag = np.ones(self.imgByte.shape,dtype=int)
        self.width, self.height = self.imgByte.shape
       

    def mix(self, imageToBeMixed: 'ImageModel', magnitudeOrRealRatio: float, phaesOrImaginaryRatio: float, mode: 'Modes') -> np.ndarray:
      
        size1 = int(magnitudeOrRealRatio*self.size)
        completeSize1 = self.size - size1
        print(magnitudeOrRealRatio)
        print(phaesOrImaginaryRatio)
        size2 = int(phaesOrImaginaryRatio*imageToBeMixed.size)
        completeSize2 = imageToBeMixed.size - size2
        logger.info("start mixing") 
       
        if mode == "realAndImaginary":       
            comp1Part1 = self.real[:size1]
            comp1Part2 = imageToBeMixed.real[:completeSize1]
            All_comp1 = self.appnendFun(comp1Part1,comp1Part2)
            
            comp2Part1 = self.imaginary[:completeSize2]
            comp2Part2 = imageToBeMixed.imaginary[:size2]
            All_comp2 = self.appnendFun(comp2Part1,comp2Part2)
        
            outputData = self.transfrom(All_comp1,All_comp2,"RealAndImaginray")
        
        elif mode =="testMagAndPhaseMode":
            comp1Part1 = self.magnitude[:size1]
            comp1Part2 = imageToBeMixed.magnitude[:completeSize1]
            All_comp1 = self.appnendFun(comp1Part1,comp1Part2)
            
            comp2Part1 = self.phase[:completeSize2]
            comp2Part2 = imageToBeMixed.phase[:size2]
            All_comp2 = self.appnendFun(comp2Part1,comp2Part2)
        
            outputData = self.transfrom(All_comp1,All_comp2,"")
            

        elif (mode == "testMagAndUnifromPhaseMode"):
            comp1Part1 = self.magnitude[:size1]
            comp1Part2 = imageToBeMixed.magnitude[:completeSize1]
            All_comp1 = self.appnendFun(comp1Part1,comp1Part2)
            
            comp2Part1 = self.phase[:completeSize2]
            comp2Part2 = imageToBeMixed.uniformPhase[:size2]
            All_comp2 = self.appnendFun(comp2Part2,comp2Part1)
    
            outputData = self.transfrom(All_comp1,All_comp2,"")
        
        elif(mode == "unifromtestMagAndPhaseMode"):
            comp1Part1 = self.uniformMag[:size1]
            comp1Part2 = imageToBeMixed.magnitude[:completeSize1]
            All_comp1 = self.appnendFun(comp1Part1,comp1Part2)
            
            comp2Part1 = self.phase[:completeSize2]
            comp2Part2 = imageToBeMixed.phase[:size2]
            All_comp2 = self.appnendFun(comp2Part2,comp2Part1)

            outputData = self.transfrom(All_comp1,All_comp2,"")
           
        elif (mode == "UtestMagAndUPhaseMode"):
            comp1Part1 = self.unifromMag[:size1]
            comp1Part2 = imageToBeMixed.magnitude[:completeSize1]
            All_comp1 = self.appnendFun(comp1Part1,comp1Part2)
            
            comp2Part1 = self.phase[:completeSize2]
            comp2Part2 = imageToBeMixed.uniformPhase[:size2]
            All_comp2 = self.appnendFun(comp2Part2,comp2Part1)

            outputData = self.transfrom(All_comp1,All_comp2,"")
        logger.info("Finish mixing")            
        return(np.array(outputData))


    def transfrom(self,comp1,comp2,flag):
        logger.info("Transfrom the components from complex forms into time") 
        combined =np.array([])
        if (flag == "RealAndImaginray"):
                   
            combined= comp1 +1j*comp2  
           
        else:
        
            combined = comp1*np.exp(comp2*1j) 
           
        imgCombined =np.real(np.fft.ifft2(combined))
    
        return(imgCombined)

    def appnendFun(self,Data1,Data2):
        Data1 = Data1.tolist()
        Data2 = Data2.tolist()
        for i in Data2:
                Data1.append(i)  
        return(np.array(Data1))
   
  