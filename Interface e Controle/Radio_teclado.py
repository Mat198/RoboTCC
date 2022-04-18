import keyboard  # using module keyboard
import time
import serial

SpeedE = 400
SpeedD = 400
v_max = 1300
Parar = False
Rodando = False

# No meu computador o rádio sempre aparece no com 4
ser = serial.Serial('COM5', 115200, timeout=0, parity=serial.PARITY_NONE)


print("tentando conectar serial")
if ser.isOpen():
    print("isOpen")
    ser.close()
    print("fechou")
    ser.open()
    print("abriu a porta serial")

if ser.isOpen():
    # Realiza a tentativa de envio de dados
    try:
        ser.flushInput()
        ser.flushOutput()
        ser.write(str.encode('F0000F0000'))
        Rodando = True
        # Em caso de exception, exibe o erro
    except Exception as e:
        print("ERRO: " + str(e))


try:
    while Rodando:
        dados = ser.write(str.encode('F0000F0000', encoding="ascii"))
        time.sleep(0.033)
        if Parar:
            break
        try:  # used try so that if user pressed other than the given key error will not be shown

            while keyboard.is_pressed('w'):  # Robô anda para frente
                Vel_D = str('{0:.0f}'.format(SpeedD))
                Vel_E = str('{0:.0f}'.format(SpeedE))
                ser.write(str.encode('F' + Vel_D.zfill(4) + 'F' + Vel_E.zfill(4), encoding="ascii"))
                time.sleep(0.033)

            while keyboard.is_pressed('s'):  # Robô anda para trás
                Vel_D = str('{0:.0f}'.format(SpeedD))
                Vel_E = str('{0:.0f}'.format(SpeedE))
                ser.write(str.encode('T' + Vel_D.zfill(4) + 'T' + Vel_E.zfill(4), encoding="ascii"))
                time.sleep(0.033)

            while keyboard.is_pressed('a'):  # Robô gira ao redor do próprio eixo para a esqueda
                Vel_D = str('{0:.0f}'.format(SpeedD * 0.8))
                Vel_E = str('{0:.0f}'.format(SpeedE * 0.8))
                ser.write(str.encode('T' + Vel_D.zfill(4) + 'F' + Vel_E.zfill(4), encoding="ascii"))
                time.sleep(0.033)

            while keyboard.is_pressed('d'):  # Robô gira ao redor do próprio eixo para a direita
                Vel_D = str('{0:.0f}'.format(SpeedD * 0.8))
                Vel_E = str('{0:.0f}'.format(SpeedE * 0.8))
                ser.write(str.encode('F' + Vel_D.zfill(4) + 'T' + Vel_E.zfill(4), encoding="ascii"))
                time.sleep(0.033)

            while keyboard.is_pressed('q'):  # Robô curva para a esqueda
                Vel_D = str('{0:.0f}'.format(SpeedD* 0.7))
                Vel_E = str('{0:.0f}'.format(SpeedE ))
                ser.write(str.encode('F' + Vel_D.zfill(4) + 'F' + Vel_E.zfill(4), encoding="ascii"))
                time.sleep(0.033)

            while keyboard.is_pressed('e'):  # Robô curva para a direita
                Vel_D = str('{0:.0f}'.format(SpeedD))
                Vel_E = str('{0:.0f}'.format(SpeedE* 0.7))
                ser.write(str.encode('F' + Vel_D.zfill(4) + 'F' + Vel_E.zfill(4), encoding="ascii"))
                time.sleep(0.033)

            if keyboard.is_pressed('i'):  # Aumenta a velocidade da roda esquerda
                SpeedE += 100
                SpeedD += 100
                if SpeedE > v_max:
                    SpeedE = v_max
                    print('Velocidade máxima esquerda')
                if SpeedD > v_max:
                    SpeedD = v_max
                    print('Velocidade máxima direita')
                Vel_D = str('{0:.0f}'.format(SpeedD))
                Vel_E = str('{0:.0f}'.format(SpeedE))
                print('Velocidade  esquerda: ' + Vel_E.zfill(4))
                print('Velocidade  direita: ' + Vel_D.zfill(4))
                time.sleep(0.1)

            if keyboard.is_pressed('k'):  # Aumenta a velocidade da roda esquerda
                SpeedE -= 100
                SpeedD -= 100
                if SpeedE < 0:
                    SpeedE = 0
                    print('Velocidade máxima esquerda')
                if SpeedD < 0:
                    SpeedD = 0
                    print('Velocidade máxima direita')
                Vel_D = str('{0:.0f}'.format(SpeedD))
                Vel_E = str('{0:.0f}'.format(SpeedE))
                print('Velocidade  esquerda: ' + Vel_E.zfill(4))
                print('Velocidade  direita: ' + Vel_D.zfill(4))
                time.sleep(0.1)

            if keyboard.is_pressed('l'):  # Aumenta a velocidade da roda direita
                SpeedD += 100
                if SpeedD > v_max:
                    SpeedD = v_max
                    print('Velocidade máxima')
                Vel_D = str('{0:.0f}'.format(SpeedD))
                print('Velocidade  direita: ' + Vel_D.zfill(4))
                time.sleep(0.1)

            if keyboard.is_pressed('.'):  # Aumenta a velocidade da roda direita
                SpeedD -= 100
                if SpeedD < 0:
                    SpeedD = 0
                    print('Velocidade mínima')
                Vel_D = str('{0:.0f}'.format(SpeedD))
                print('Velocidade  direita: ' + Vel_D.zfill(4))
                time.sleep(0.1)

            if keyboard.is_pressed('j'):  # Aumenta a velocidade da roda esquerda
                SpeedE += 100
                if SpeedE > v_max:
                    SpeedE = v_max
                    print('Velocidade máxima')
                Vel_E = str('{0:.0f}'.format(SpeedE))
                print('Velocidade  esquerda: ' + Vel_E.zfill(4))
                time.sleep(0.1)

            if keyboard.is_pressed('n'):  # Aumenta a velocidade da roda esquerda
                SpeedE -= 100
                if SpeedE < 0:
                    SpeedE = 0
                    print('Velocidade máxima')
                Vel_E = str('{0:.0f}'.format(SpeedE))
                print('Velocidade  esquerda: ' + Vel_E.zfill(4))
                time.sleep(0.1)

            if keyboard.is_pressed('h'):  # if key 'q' is pressed
                print('w -> move o robô para a frente')
                print('s -> move o robô para a trás')
                print('a -> roda o robô para a esquerda')
                print('d -> roda o robô para a direita')
                print('q -> curva o robô para a esqueda')
                print('e -> curva o robô para a direita')
                print('i -> aumenta a velocidade do robô')
                print('k -> diminui a velocidade do robô')
                print('l -> aumenta a velocidade da roda direita')
                print('. -> diminui a velocidade da roda direita')
                print('j -> aumenta a velocidade da roda esquerda')
                print('n -> aumenta a velocidade da roda esquerda')
                print('p -> para o programa')
                print('Nada -> o programa envia velocidade 0 para o robô')

                time.sleep(0.5)

            if keyboard.is_pressed('p'):
                Parar = True

        except 1:
            print("Tecla não alocada. Aperte 'h' para ver a lista das teclas alocadas.")
except 2:
    print("Eita")
