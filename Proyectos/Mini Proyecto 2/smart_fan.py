from gpiozero import DistanceSensor
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from Raspi_PWM_Servo_Driver import PWM
from threading import Thread
import adafruit_dht
import board
import time
from gpiozero import LED

################# Variable #################
tiempo_ejecucion = 3
tiempo_actual = 0
############################################

##################  Ultrasonic ##################
echo_pin = 17
trigger_pin = 4
ultrasonic_sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin, threshold_distance=0.2, max_distance=2)
################################################

##################### Sensor Temp ###################
# dht_device = adafruit_dht.DHT11(board.D26)
#####################################################

######################## Motor DC #####################
motor_hat = Raspi_MotorHAT(addr=0x6f)
dc_motor = motor_hat.getMotor(2)
dc_motor.setSpeed(150) # Velocidad base
######################################################

######################## Motor Stepper #####################
stepper_motor = motor_hat.getStepper(200, 2)  # 200 pasos por vuelta, stepper motor en el puerto 1
######################################################

def guardar_posicion_stepper(posicion):
    with open('posicion_stepper.txt', 'w') as file:
        file.write(str(posicion))

def leer_posicion_stepper():
    try:
        with open('posicion_stepper.txt', 'r') as file:
            posicion = int(file.read())
        return posicion
    except FileNotFoundError:
        return 0  # Si el archivo no existe, devuelve la posición inicial (0)

            
def control_abanico():
    try:
        while True:
            distancia = ultrasonic_sensor.distance
            tiempo_actual = 0
            if distancia < 0.5:
                print("Objeto detectado a {} metros.".format(distancia))
                
                # Encender el motor DC (abanico)
                dc_motor.run(Raspi_MotorHAT.FORWARD)

                posicion_inicial = leer_posicion_stepper()
                time.sleep(0.8)
                while tiempo_actual < tiempo_ejecucion:   
                # Girar el stepper motor durante 15 segundos

                    stepper_motor.step(100, Raspi_MotorHAT.FORWARD, Raspi_MotorHAT.DOUBLE)  # Mueve 100 pasos en sentido horario
                    time.sleep(1)
                    # Segunda lectura del sensor ultrasónico
                    segunda_lectura = ultrasonic_sensor.distance
                    
                    if segunda_lectura < 0.5:
                        break
                    stepper_motor.step(100, Raspi_MotorHAT.BACKWARD, Raspi_MotorHAT.DOUBLE)  
                    time.sleep(1)
                    tiempo_actual += 1
                    
                stepper_motor.step(posicion_inicial, Raspi_MotorHAT.BACKWARD, Raspi_MotorHAT.DOUBLE)  
                guardar_posicion_stepper(posicion_inicial)
                
                # Seguir ejecutando el motor DC durante 10 segundos más
                # TODO: Quitar estos 10 segundos o reducir
                time.sleep(60)
                dc_motor.run(Raspi_MotorHAT.RELEASE)
            
            else:
 
                print("Ningún objeto detectado.")
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("Interrupción de teclado. Deteniendo el abanico.")
        dc_motor.run(Raspi_MotorHAT.RELEASE)


control_abanico()