import tkinter as tk
from tkinter import scrolledtext
from tkinter.constants import BOTTOM, HORIZONTAL, LEFT, RIGHT, S
from tkinter import ttk
from PIL import ImageTk, Image
from click import command
from cv2 import FlannBasedMatcher
import serial
import time
import os

#os.system('xset r off')

class Application:
    def __init__(self, master):

        self.msg = str.encode('F0000F0000', encoding="ascii")
        
        self.mainwidget = master
        
        try:

            imagem = Image.open("image.jpg")
            self.foto = ImageTk.PhotoImage(imagem)
            self.lbl = tk.Label(self.mainwidget, image = self.foto)
            self.lbl.grid(row=0,column=0, columnspan= 4)
        except:
            pass

        ############################# PROGRAM LOGGS #####################################
        self.ProgFrame = ttk.LabelFrame(self.mainwidget, text='Program Loggs')
        self.ProgFrame.grid(row = 0,column=0, padx=20, pady=20)

        self.LogDisplay = scrolledtext.ScrolledText(self.ProgFrame, height = 2, width = 40, state="disabled") # ,state="disabled"
        self.LogDisplay.grid(row=2,column=0, columnspan=3)

        ########################## JANELA DE COMUNICAÇÃO SERIAL ##################################
        # Criando Frame para receber dados da Serial
        self.SerialFrame = ttk.LabelFrame(self.mainwidget, text='Serial Receiver')
        self.SerialFrame.grid(row = 1,column=0, padx=20, pady=20)

        # Display de texto da serial
        self.SerialDisplay = scrolledtext.ScrolledText(self.SerialFrame, height = 5, width = 30) # ,state="disabled"
        self.SerialDisplay.grid(row=3,column=0, columnspan=3)

        # Título da caixa de texto do robô
        self.SerialLabel = tk.Label(self.SerialFrame, text = "Dados recebidos da Serial")
        self.SerialLabel.config(font =("Comic Sans", 14))
        self.SerialLabel.grid(row=2,column=0, columnspan=2)
        
        # Check box do auto scroll
        self.scrollState= tk.IntVar()
        self.scrollState.set(1)
        self.SerialRoll = tk.Checkbutton(self.SerialFrame, text='Auto scroll',variable=self.scrollState, onvalue=1, offvalue=0)
        self.SerialRoll.grid(row=4,column=0, columnspan=1)
        
        # Check box Receive Serial Data
        self.SerialState= tk.IntVar()
        self.SerialState.set(0)
        self.SerialData = tk.Checkbutton(self.SerialFrame, text='Serial data',variable=self.SerialState, onvalue=1, offvalue=0)
        self.SerialData.config(state="disable")
        self.SerialData.grid(row=4,column=1, columnspan=1)

        # Parâmetros para conectar Serial
        self.SerialButton = tk.Button(self.SerialFrame, text= "Serial OFF", font=("Arial",12),width=25,bg="red",fg="white", command=self.serialInit)
        self.SerialButton.grid(row=5,column=0, columnspan= 2)
        self.SerialFlag = False
        self.Serial = 0

        ########################## Controle Manual do Robô ##################################
        # Robot Manual Control Frame 

        self.velMD = 1100
        self.velME = 1100
        self.velMax = 3000

        self.ControlFrame = ttk.LabelFrame(self.mainwidget, text='Manual Robot Control')
        self.ControlFrame.grid(row = 2,column=0, padx=20, pady=20)

        self.FrenteButton = tk.Button(self.ControlFrame, text="Frente (W)", font =("Comic Sans", 8), height= 2, width= 16)
        self.FrenteButton.config(command=self.frente)
        self.FrenteButton.grid(row=0,column=1, columnspan=1)

        self.TrasButton = tk.Button(self.ControlFrame, text="Trás (S)", font =("Comic Sans", 8), height= 2, width= 16)
        self.TrasButton.config(command=self.tras)
        self.TrasButton.grid(row=1,column=1, columnspan=1)

        self.TurnLeftButton = tk.Button(self.ControlFrame, text="Virar esquerda (Q)", font =("Comic Sans", 8), height= 2, width= 16)
        self.TurnLeftButton.config(command=self.turnLeft)
        self.TurnLeftButton.grid(row=0,column=0, columnspan=1)

        self.TurnRightButton = tk.Button(self.ControlFrame, text="Virar direita (E)", font =("Comic Sans", 8), height= 2, width= 16)
        self.TurnRightButton.config(command=self.turnRight)
        self.TurnRightButton.grid(row=0,column=2, columnspan=1)

        self.SpinLeftButton = tk.Button(self.ControlFrame, text="Girar esquerda (A)", font =("Comic Sans", 8),height= 2, width= 16)
        self.SpinLeftButton.config(command=self.spinLeft)
        self.SpinLeftButton.grid(row=1,column=0, columnspan=1)

        self.SpinRightButton = tk.Button(self.ControlFrame, text="Girar direita (D)", font =("Comic Sans", 8), height= 2, width= 16)
        self.SpinRightButton.config(command=self.spinRight)
        self.SpinRightButton.grid(row=1,column=2, columnspan=1)

        self.IncSpeedLeftButton = tk.Button(self.ControlFrame, text="Vel esq + (U)", font =("Comic Sans", 8), height= 2, width= 16)
        self.IncSpeedLeftButton.config(command=self.speedUpLeft)
        self.IncSpeedLeftButton.grid(row=2,column=0, columnspan=1)

        self.IncSpeedRightButton = tk.Button(self.ControlFrame, text="Vel dir + (O)", font =("Comic Sans", 8), height= 2, width= 16)
        self.IncSpeedRightButton.config(command=self.speedUpRight)
        self.IncSpeedRightButton.grid(row=2,column=2, columnspan=1)

        self.DecSpeedLeftButton = tk.Button(self.ControlFrame, text="Vel esq - (L)", font =("Comic Sans", 8), height= 2, width= 16)
        self.DecSpeedLeftButton.config(command=self.speedDownLeft)
        self.DecSpeedLeftButton.grid(row=3,column=0, columnspan=1)

        self.DecSpeedRightButton = tk.Button(self.ControlFrame, text="Vel dir - (J)", font =("Comic Sans", 8), height= 2, width= 16)
        self.DecSpeedRightButton.config(command=self.speedDownRight)
        self.DecSpeedRightButton.grid(row=3,column=2, columnspan=1)

        self.IncSpeedButton = tk.Button(self.ControlFrame, text="Vel + (I)", font =("Comic Sans", 8), height= 2, width= 16)
        self.IncSpeedButton.config(command=self.speedUp)
        self.IncSpeedButton.grid(row=2,column=1, columnspan=1)

        self.DecSpeedButton = tk.Button(self.ControlFrame, text="Vel - (K)", font =("Comic Sans", 8), height= 2, width= 16)
        self.DecSpeedButton.config(command=self.speedDown)
        self.DecSpeedButton.grid(row=3,column=1, columnspan=1)



        # Display da velocidade do motor ESQUERDO
        self.velEsqDisplay = tk.Text(self.ControlFrame, width = 5,height = 1)
        self.velEsqDisplay.grid(row=4,column=1, columnspan=1)
        # Título da caixa de texto motor ESQUERDO
        self.velEsqLabel = tk.Label(self.ControlFrame, text = "PWM motor \n esquerdo")
        self.velEsqLabel.config(font =("Comic Sans", 9))
        self.velEsqLabel.grid(row=4,column=0, columnspan=1)

        # Display da velocidade do motor DIREITO
        self.velDirDisplay = tk.Text(self.ControlFrame, width = 5,height = 1)
        self.velDirDisplay.grid(row=5,column=1, columnspan=1)
        # Título da caixa de texto motor DIREITO
        self.velDirLabel = tk.Label(self.ControlFrame, text = "PWM motor \n direito")
        self.velDirLabel.config(font =("Comic Sans", 9))
        self.velDirLabel.grid(row=5,column=0, columnspan=1)

        self.ManualButton = tk.Button(self.ControlFrame, text= "Manual Mode\nOFF", font=("Arial",9),width=12,bg="red",fg="white", command=self.manualInit)
        self.ManualButton.config(state= "disable")
        self.ManualButton.grid(row=4,column=2,columnspan= 2 )
        self.ManualFlag = False

        ########################## Ajuste de Parâmetros do Robô ##################################
        # Robot data Frame 
        self.RobotFrame = ttk.LabelFrame(self.mainwidget, text='Robot Parameters')
        self.RobotFrame.grid(row = 2,column=1, padx=20, pady=20)

        # Configuração dos valores do PID
        # # Setar o PID
        # self.PIDLabel = tk.Label(self.RobotFrame, text = "Controlador PID",font =("Comic Sans", 9))
        # self.PIDLabel.grid(row=0,column=0, columnspan= 2)

        # self.PSet = tk.Text(self.RobotFrame, width = 8,height = 1)
        # self.PSet.grid(row=1,column=1, columnspan=1)
        # # Título da caixa de texto motor DIREITO
        # self.PLabel = tk.Label(self.RobotFrame, text = "P =",font =("Comic Sans", 8))
        # self.PLabel.grid(row=1,column=0, columnspan=1)

        # self.ISet = tk.Text(self.RobotFrame, width = 8,height = 1)
        # self.ISet.grid(row=2,column=1, columnspan=1)
        # # Título da caixa de texto motor DIREITO
        # self.ILabel = tk.Label(self.RobotFrame, text = "I =",font =("Comic Sans", 8))
        # self.ILabel.grid(row=2,column=0, columnspan=1)

        # self.DSet = tk.Text(self.RobotFrame, width = 8,height = 1)
        # self.DSet.grid(row=3,column=1, columnspan=1)
        # # Título da caixa de texto motor DIREITO
        # self.DLabel = tk.Label(self.RobotFrame, text = "D =",font =("Comic Sans", 8))
        # self.DLabel.grid(row=3,column=0, columnspan=1)

        # self.SetPIDButton = tk.Button(self.RobotFrame, text="Set PID", font =("Comic Sans", 8), height= 2, width= 9)
        # self.SetPIDButton.config(command=self.setPID)
        # self.SetPIDButton.grid(row=4,column=0, columnspan=2)

        # # Interface para pegar os valores atuais do PID
        # self.RobotPIDLabel = tk.Label(self.RobotFrame, text = "Robot PID",font =("Comic Sans", 9))
        # self.RobotPIDLabel.grid(row=0,column=2, columnspan= 2)

        # self.RobotP = tk.Text(self.RobotFrame, width = 8,height = 1)
        # self.RobotP.config(state= "disable")
        # self.RobotP.grid(row=1,column=3, columnspan=1)

        # self.RobotPLabel = tk.Label(self.RobotFrame, text = "Robot P =",font =("Comic Sans", 8))
        # self.RobotPLabel.grid(row=1,column=2, columnspan=1)

        # self.RobotI = tk.Text(self.RobotFrame, width = 8,height = 1)
        # self.RobotI.config(state= "disable")
        # self.RobotI.grid(row=2,column=3, columnspan=1)

        # self.RobotILabel = tk.Label(self.RobotFrame, text = "Robot I =",font =("Comic Sans", 8))
        # self.RobotILabel.grid(row=2,column=2, columnspan=1)

        # self.RobotD = tk.Text(self.RobotFrame, width = 8,height = 1)
        # self.RobotD.config(state= "disable")
        # self.RobotD.grid(row=3,column=3, columnspan=1)

        # self.RobotDLabel = tk.Label(self.RobotFrame, text = "Robot D =",font =("Comic Sans", 8))
        # self.RobotDLabel.grid(row=3,column=2, columnspan=1)

        # self.GetPIDButton = tk.Button(self.RobotFrame, text="Get PID", font =("Comic Sans", 8), height= 2, width= 9)
        # self.GetPIDButton.config(command=self.getPID)
        # self.GetPIDButton.grid(row=4,column=2, columnspan=2)

        ########################## Outras funções do programa ##################################

        # Botão para fechar o programa
        self.sair = tk.Button(self.mainwidget, text= "Sair", font=("Arial",12),width=5,bg="red",fg="white", command=self.click_exit)
        self.sair.grid(row=0,column=1)
        self.click = False
        self.flag_exit = False              
    

    def scrollCmd(self):
        pass

    def printSerialData(self,data):

        self.SerialDisplay.configure(state='normal')
        
        if isinstance(data, str):
            self.SerialDisplay.insert(tk.END, data + '\n')
        else:
            self.SerialDisplay.insert(tk.END, str(data) + '\n')
        self.SerialDisplay.configure(state='disabled')
        if self.scrollState.get():
            self.SerialDisplay.see("end")
    
    def printMotorData(self,motEsq,motDir):
        
        self.velDirDisplay.configure(state='normal')
        self.velEsqDisplay.configure(state='normal')

        self.velEsqDisplay.delete('1.0', tk.END)
        self.velDirDisplay.delete('1.0', tk.END)

        # Dados do motor ESQUERDO
        if isinstance(motEsq, str):
            self.velEsqDisplay.insert(tk.END, motEsq + '\n')
        else:
            self.velEsqDisplay.insert(tk.END, str(motEsq) + '\n')

         # Dados do motor DIREITO
        if isinstance(motDir, str):
            self.velDirDisplay.insert(tk.END, motDir + '\n')
        else:
            self.velDirDisplay.insert(tk.END, str(motDir) + '\n')
        
        self.velDirDisplay.configure(state='disabled')
        self.velEsqDisplay.configure(state='disabled')

    def printLoggs(self,data):
        self.LogDisplay.configure(state='normal')
        self.LogDisplay.insert(tk.END, data + "\n")
        self.LogDisplay.configure(state='disabled')
        self.LogDisplay.see("end")

    def setPID(self):
        pass
    
    def getPID(self):
        pass

    def setManualSpeed(self,velME,velMD):
        self.velME = velME
        self.velMD = velMD
        self.printMotorData(velME,velMD)

    def frente(self,event=None):
        if self.ManualFlag:
            Vel_D = str('{0:.0f}'.format(self.velMD))
            Vel_E = str('{0:.0f}'.format(self.velME))
            self.msg = str.encode('F' + Vel_D.zfill(4) + 'F' + Vel_E.zfill(4), encoding="ascii")

    def tras(self,event=None):
        if self.ManualFlag:
            Vel_D = str('{0:.0f}'.format(self.velMD))
            Vel_E = str('{0:.0f}'.format(self.velME))
            self.msg = str.encode('T' + Vel_D.zfill(4) + 'T' + Vel_E.zfill(4), encoding="ascii")

    def spinLeft(self,event=None):
        if self.ManualFlag:
            Vel_D = str('{0:.0f}'.format(self.velMD * 0.8))
            Vel_E = str('{0:.0f}'.format(self.velME * 0.8))
            self.msg = str.encode('T' + Vel_D.zfill(4) + 'F' + Vel_E.zfill(4), encoding="ascii")

    def spinRight(self,event=None):
        if self.ManualFlag:
            Vel_D = str('{0:.0f}'.format(self.velMD * 0.8))
            Vel_E = str('{0:.0f}'.format(self.velME * 0.8))
            self.msg = str.encode('F' + Vel_D.zfill(4) + 'T' + Vel_E.zfill(4), encoding="ascii")

    def turnLeft(self,event=None):
        if self.ManualFlag:
            Vel_D = str('{0:.0f}'.format(self.velMD))
            Vel_E = str('{0:.0f}'.format(self.velME * 0.7))
            self.msg = str.encode('F' + Vel_D.zfill(4) + 'F' + Vel_E.zfill(4), encoding="ascii")
  
    def turnRight(self,event=None):
        if self.ManualFlag:
            Vel_D = str('{0:.0f}'.format(self.velMD * 0.7))
            Vel_E = str('{0:.0f}'.format(self.velME))
            self.msg = (str.encode('F' + Vel_D.zfill(4) + 'F' + Vel_E.zfill(4), encoding="ascii"))
            
    def speedUpLeft(self,event=None):
        self.velME += 100
        if self.velME > self.velMax:
            self.velME = self.velMax
            print('PWM máximo no motor esquerdo')
        Vel_E = str('{0:.0f}'.format(self.velME))
        Vel_D = str('{0:.0f}'.format(self.velMD))
        self.printMotorData(Vel_E.zfill(4),Vel_D.zfill(4))

    def speedUpRight(self,event=None):
        self.velMD += 100
        if self.velMD > self.velMax:
            self.velMD = self.velMax
            print('PWM máxima no motor direito')
        Vel_D = str('{0:.0f}'.format(self.velMD))
        Vel_E = str('{0:.0f}'.format(self.velME))
        self.printMotorData(Vel_E.zfill(4),Vel_D.zfill(4))

    def speedDownLeft(self,event=None):
        self.velME -= 100
        if self.velME < 0:
            self.velME = 0
            print('PWM máximo')
        Vel_E = str('{0:.0f}'.format(self.velME))
        Vel_D = str('{0:.0f}'.format(self.velMD))
        self.printMotorData(Vel_E.zfill(4),Vel_D.zfill(4))

    def speedDownRight(self,event=None):
        self.velMD -= 100
        if self.velMD < 0:
            self.velMD = 0
            print('PWM mínimo')
        Vel_D = str('{0:.0f}'.format(self.velMD))
        Vel_E = str('{0:.0f}'.format(self.velME))
        self.printMotorData(Vel_E.zfill(4),Vel_D.zfill(4))
    
    def speedDown(self,event=None):
        self.velME -= 100
        self.velMD -= 100
        if self.velME < 0:
            self.velME = 0
            print('PWM mínima esquerda')
        if self.velMD  < 0:
            self.velMD  = 0
            print('PWM mínima direita')
        Vel_D = str('{0:.0f}'.format(self.velMD))
        Vel_E = str('{0:.0f}'.format(self.velME))
        self.printMotorData(Vel_E.zfill(4),Vel_D.zfill(4))

    def speedUp(self,event=None):
        self.velME += 100
        self.velMD += 100
        if self.velME > self.velMax:
            self.velME = self.velMax
            self.printLoggs('PWM máximo esquerda')
        if self.velMD > self.velMax:
            self.velMD = self.velMax
            self.printLoggs('PWM máximo direita')
        Vel_D = str('{0:.0f}'.format(self.velMD))
        Vel_E = str('{0:.0f}'.format(self.velME))
        self.printMotorData(Vel_E.zfill(4),Vel_D.zfill(4))

    def click_Serial(self):
        return self.SerialState.get()

    def serialInit(self):
        if not self.SerialFlag:
            try: 
                self.Serial = serial.Serial('COM5', 115200, timeout=0, parity=serial.PARITY_NONE)
                if self.Serial.isOpen():
                    self.Serial.close()
                    self.Serial.open()
                    self.printLoggs("Porta serial aberta!")
                else:
                    self.printLoggs("Falha ao abrir a porta serial.")
            except:
                self.printLoggs("Porta Serial não encontrada.")
                return

            try:
                self.Serial.flushInput()
                self.Serial.flushOutput()
                self.Serial.write(str.encode('F0000F0000'))
            except Exception as e:
                self.printLoggs("Falha ao enviar dados.")
                return
            
            self.SerialButton.config(text="Serial ON",bg="green")
            self.SerialFlag = True
            self.SerialData.config(state="normal")
            self.ManualButton.config(state="normal")

        else:
            try: 
                if self.Serial.isOpen():
                    self.Serial.close()
                    self.printLoggs("Porta Serial fechada!")
            except:
                self.printLoggs("Porta Serial não encontrada!")
                return
            self.SerialButton.config(text="Serial OFF",bg="red")
            self.SerialFlag = False
            self.SerialState.set(0)
            if self.ManualFlag:
                self.ManualButton.config(text="Manual Mode\nOFF",bg="red")
                self.ManualFlag = False
            self.SerialData.config(state="disable")
            self.ManualButton.config(state="disable")
            

    def manualInit(self):
        if not self.ManualFlag:
            self.ManualButton.config(text="Manual Mode\nON",bg="green")
            self.ManualFlag = True
            self.bindings()
        else:
            self.ManualButton.config(text="Manual Mode\nOFF",bg="red")
            self.ManualFlag = False
            self.unbind()
        
    def fechar(self):
        if self.click == True:
            self.flag_exit = True
        return self.flag_exit

    def click_exit(self):
        self.click = True
        return self.click

    def bindings(self):
 
        self.mainwidget.bind('w',self.frente)
        self.mainwidget.bind('s',self.tras)
        self.mainwidget.bind('q', self.turnLeft)
        self.mainwidget.bind('e', self.turnRight)
        self.mainwidget.bind('a', self.spinLeft)
        self.mainwidget.bind('d', self.spinRight)
        self.mainwidget.bind('u', self.speedUpLeft)  
        self.mainwidget.bind('o', self.speedUpRight)
        self.mainwidget.bind('j', self.speedDownLeft)
        self.mainwidget.bind('l', self.speedDownRight)
        self.mainwidget.bind('i', self.speedUp)
        self.mainwidget.bind('k', self.speedDown)
        self.mainwidget.bind("<KeyRelease>", self.releaseAll)
    
    def releaseAll(self,event=None):
        self.msg = str.encode('F0000F0000', encoding="ascii")

    def unbind(self):
        self.mainwidget.unbind('w')
        self.mainwidget.unbind('s')
        self.mainwidget.unbind('q')
        self.mainwidget.unbind('e')
        self.mainwidget.unbind('a')
        self.mainwidget.unbind('d')
        self.mainwidget.unbind('u')
        self.mainwidget.unbind('o')
        self.mainwidget.unbind('j')
        self.mainwidget.unbind('l')
        self.mainwidget.unbind('i')
        self.mainwidget.unbind('k')