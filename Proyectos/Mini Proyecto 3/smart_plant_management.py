from gpiozero import MCP3008, Device
from gpiozero.pins.rpigpio import RPiGPIOFactory
from Raspi_MotorHAT import Raspi_MotorHAT
from time import sleep
from clima import obtener_clima

# Esto para evitar un warning que siempre sale.
Device.pin_factory = RPiGPIOFactory()

############# Bomba de agua (DC 12V) ##################
motor_hat = Raspi_MotorHAT(addr=0x6f)
dc_motor = motor_hat.getMotor(1)
dc_motor.setSpeed(150)
#######################################################

############ Sensor Humedad en Tierra #################
sensor_humedad = MCP3008(channel=0)
limite_seco = 0.3 # Limites comunmente utilizados para saber si la tierra esta humedad o seca.
limite_humedo = 0.7
#######################################################

############ Sensor Humedad en Tierra #################
sensor_luz = MCP3008(channel=1)
#######################################################
 
############# Variables #################
porciento_luz = 0
porciento_humedad = 0
temp_clima = 0
estado_clima = ""
########################################

def leer_valor_humedad():
    valor = sensor_humedad.value
    porcentaje_humedad = ((valor - limite_seco) / (limite_humedo - limite_seco)) * 100
    porcentaje_humedad = max(0, min(100, porcentaje_humedad)) 
    return porcentaje_humedad

def leer_valor_fotocelda():
    valor = sensor_luz.value
    valor_porcentaje = valor * 100
    return valor_porcentaje

def main():
    try:
        while True:
            porciento_luz = leer_valor_fotocelda()
            porciento_humedad = leer_valor_humedad()
            temp_clima , estado_clima = obtener_clima()
            
            print("Valor de la fotocelda: {:.2f}%  Valor de humedad: {:.2f}%".format(porciento_luz, porciento_humedad))
            print("Temperatura: {}°C".format(temp_clima))
            print("Estado del clima: {}".format(estado_clima))
            print("-----------------------------------------------------")
            print("                                                     ")
            
            if porciento_luz > 50:
                if porciento_humedad < 30:
                    dc_motor.run(Raspi_MotorHAT.FORWARD)
                    sleep(15)
                    dc_motor.run(Raspi_MotorHAT.RELEASE)
                else:
                    if porciento_humedad < 50:
                        print("Buena luminosidad, pero el suelo esta humedo.")
                    else:
                        print("El suelo esta muy humedo")    
            else:
                if porciento_luz < 15:
                    print("Poca luminosidad, no necesidad de mojar planta.")

            print("                                                     ")
            sleep(4)
    except KeyboardInterrupt:
        print("Interrupción de teclado. Deteniendo el sistema.")
        dc_motor.run(Raspi_MotorHAT.RELEASE)
    
main()
