from gpiozero import MCP3008, Device
from gpiozero.pins.rpigpio import RPiGPIOFactory
from Raspi_MotorHAT import Raspi_MotorHAT
from time import sleep
from clima import obtener_clima

# Constantes
LIMITE_SECO = 0.3
LIMITE_HUMEDO = 0.7
MOTOR_SPEED = 150
DELAY_TIME = 4

# Inicialización de dispositivos
Device.pin_factory = RPiGPIOFactory()
motor_hat = Raspi_MotorHAT(addr=0x6f)
dc_motor = motor_hat.getMotor(1)
dc_motor.setSpeed(MOTOR_SPEED)
sensor_humedad = MCP3008(channel=0)
sensor_luz = MCP3008(channel=1)

def leer_valor_humedad():
    valor = sensor_humedad.value
    porcentaje_humedad = ((valor - LIMITE_SECO) / (LIMITE_HUMEDO - LIMITE_SECO)) * 100
    porcentaje_humedad = max(0, min(100, porcentaje_humedad)) 
    return porcentaje_humedad

def leer_valor_fotocelda():
    valor = sensor_luz.value
    valor_porcentaje = valor * 100
    return valor_porcentaje

def verificar_estado_planta(porciento_luz, porciento_humedad, temp_clima, estado_clima):
    if porciento_luz > 50:
        if porciento_humedad < 30:
            dc_motor.run(Raspi_MotorHAT.FORWARD)
            sleep(15)
            dc_motor.run(Raspi_MotorHAT.RELEASE)
        else:
            if porciento_humedad < 50:
                print("Buena luminosidad, pero el suelo está húmedo.")
            else:
                print("El suelo está muy húmedo")    
    else:
        if porciento_luz < 15:
            print("Poca luminosidad, no necesidad de mojar planta.")
        else:
            if estado_clima.lower() == "rainy" or estado_clima.lower() == "partly cloudy":
                print("El clima es lluvioso, no es necesario regar las plantas.")
            else:
                if temp_clima > 25:  # Ajusta el umbral de temperatura según tus necesidades
                    print("Temperatura alta ({:.2f}°C), riego necesario.".format(temp_clima))
                    dc_motor.run(Raspi_MotorHAT.FORWARD)
                    sleep(15)
                    dc_motor.run(Raspi_MotorHAT.RELEASE)
                else:
                    print("Temperatura adecuada ({:.2f}°C), no es necesario regar en este momento.".format(temp_clima))

def main():
    try:
        while True:
            porciento_luz = leer_valor_fotocelda()
            porciento_humedad = leer_valor_humedad()
            temp_clima , estado_clima = obtener_clima()
            
            print("Valor de la fotocelda: {:.2f}%  Valor de humedad: {:.2f}%".format(porciento_luz, porciento_humedad))
            print("Temperatura: {}°C".format(temp_clima))
            print("Estado del clima: {}".format(estado_clima))
            print("-----------------------------------------------------\n")
            
            verificar_estado_planta(porciento_luz, porciento_humedad, temp_clima, estado_clima)
            
            sleep(DELAY_TIME)
    except KeyboardInterrupt:
        print("Interrupción de teclado. Deteniendo el sistema.")
        dc_motor.run(Raspi_MotorHAT.RELEASE)

if __name__ == "__main__":
    main()