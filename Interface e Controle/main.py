import time
from prompt_toolkit import Application
from sympy import root
import interface

# Trocar velocidade por
# TODO: mudar velocidade para PWM no modo manual
# Modo controlado com velocidade linear e angular
# Buffer recirculante para aumentar a velocidade de recepção da serial
# usar thered para acelereção


global Parar 
Parar = False
root = interface.tk.Tk()
root.title("Controle do Robô")
janela = interface.Application(root)

# No meu computador o rádio sempre aparece no com 4
ser = janela.Serial
janela.setManualSpeed(1100,1100)

while True:
    startTime = time.time()
    root.update_idletasks()
    root.update()
    data = janela.msg
    receiveSerialData = janela.click_Serial()
    if janela.SerialState.get():
        try:
            ser.write(data)
        except:
            pass

        if receiveSerialData:
            janela.printSerialData("Dados recebidos do robô:")
            janela.printSerialData(str(ser.read(10)))
            janela.printSerialData("--------------------------")
    else:
        ser = janela.Serial
       
    Parar = janela.fechar()

    if Parar:
        root.destroy()
        break
    endTime = time.time()
    delay = endTime - startTime
    if delay < 0.033:
        time.sleep(0.033 - delay)


