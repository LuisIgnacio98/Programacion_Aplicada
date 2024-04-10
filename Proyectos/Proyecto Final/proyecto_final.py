from Raspi_MotorHAT import Raspi_MotorHAT
from gpiozero import DistanceSensor
import RPi.GPIO as GPIO
from time import sleep
import curses
import os

############ MOTORES DC ##############
motor_hat = Raspi_MotorHAT(addr=0x6f)

dc_motor1 = motor_hat.getMotor(1)
dc_motor2 = motor_hat.getMotor(2)
dc_motor3 = motor_hat.getMotor(3)
dc_motor4 = motor_hat.getMotor(4)
######################################

############# Sensor de Colision ############
crash_sensor_pin = 2  
GPIO.setmode(GPIO.BCM)
GPIO.setup(crash_sensor_pin, GPIO.IN)
#############################################

############# Sensor Ultrasonico ###########
echo_pin = 17
trigger_pin = 4
ultrasonic_sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin, threshold_distance=0.2, max_distance=2)
#############################################

############ Camara de PI ##################
#command = f"rpicam-jpeg -t 1 -n -o {file_name } > /dev/null 2>&1"
#os.system(command)
############################################

def mover_adelante():
    dc_motor1.run(Raspi_MotorHAT.FORWARD)
    dc_motor2.run(Raspi_MotorHAT.FORWARD)
    dc_motor3.run(Raspi_MotorHAT.FORWARD)
    dc_motor4.run(Raspi_MotorHAT.FORWARD)       
    
def mover_atras():
    dc_motor1.run(Raspi_MotorHAT.BACKWARD)
    dc_motor2.run(Raspi_MotorHAT.BACKWARD)
    dc_motor3.run(Raspi_MotorHAT.BACKWARD)
    dc_motor4.run(Raspi_MotorHAT.BACKWARD) 
    
def mover_derecha():
#to do

def mover_izquierda():
#to do

def detener():
    dc_motor1.run(Raspi_MotorHAT.RELEASE)
    dc_motor2.run(Raspi_MotorHAT.RELEASE)
    dc_motor3.run(Raspi_MotorHAT.RELEASE)
    dc_motor4.run(Raspi_MotorHAT.RELEASE)  
       
def main(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    stdscr.addstr("Presione A - automatico y M - manual\n")
    
    key = stdscr.getch()
    
    if key == ord('a'):
        while True:
            distancia = ultrasonic_sensor.distance
            mover_adelante()
            
            if distancia < 0.30:
                detener()
                #Logica de doblar

            if GPIO.input(crash_sensor_pin) == GPIO.LOW:
                detener()
                sleep(1.5)

            # To Do Foto
    elif key == ord('m'):
        #todo manual
        
curses.wrapper(main)


