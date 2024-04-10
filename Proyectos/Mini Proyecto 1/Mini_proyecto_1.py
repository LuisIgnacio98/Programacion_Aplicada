import curses
import os
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from datetime import datetime
import argparse

#Inicializando el Servo
pin_servo_horizontal = 2
pin_servo_vertical = 3
pigpio_factory = PiGPIOFactory()

servo_horizontal = AngularServo(pin_servo_horizontal, min_angle=0, max_angle=180, pin_factory=pigpio_factory)
servo_vertical = AngularServo(pin_servo_vertical, min_angle=0, max_angle=180, pin_factory=pigpio_factory)


def main(stdscr):
    # Imprimiendo instrucciones.
    stdscr.clear()
    curses.curs_set(0)
    stdscr.addstr("Presiona '→' giro a la derecha.\n")
    stdscr.addstr("Presiona '←' giro a la izquierda.\n")
    stdscr.addstr("Presiona '+' aumentar velocidad de giro.\n")
    stdscr.addstr("Presiona '-' disminuir velocidad de giro.\n")
    stdscr.addstr("Presiona 'Enter' realizar captura.\n")
    stdscr.addstr("Presiona 'q' para salir.\n")
    
    # Variables de angulo y velocidad correspondientes.
    angulo_horizontal = 90
    angulo_vertical = 90
    
    
    constante_velocidad = args.velocidad
    
    
    #Inicializando el servo a angulo declarado.
    servo_horizontal.angle = angulo_horizontal
    servo_vertical.angle = angulo_vertical
    
    while True:
        # Captura de tecla
        """ 
        '→' giro a la derecha.
        '←' giro a la izquierda.
        '+' aumentar velocidad
        '-' disminuir velocidad
        'Enter' realizar captura
        'q' para salir
        """
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == curses.KEY_RIGHT:
            angulo_horizontal -= constante_velocidad
            angulo_horizontal = max(0, angulo_horizontal)  
            servo_horizontal.angle = angulo_horizontal
        elif key == curses.KEY_LEFT:
            angulo_horizontal += constante_velocidad
            angulo_horizontal = min(180, angulo_horizontal) 
            servo_horizontal.angle = angulo_horizontal 
        elif key == curses.KEY_UP:
            angulo_vertical -= constante_velocidad
            angulo_vertical = max(0, angulo_vertical)  
            servo_vertical.angle = angulo_vertical    
        elif key == curses.KEY_DOWN:
            angulo_vertical += constante_velocidad
            angulo_vertical = min(180, angulo_vertical) 
            servo_vertical.angle = angulo_vertical       
        elif key == ord('+'):
            if constante_velocidad + 25 > 180:
               print("No se puede aumentar mas de velocidad.")
            else:
                constante_velocidad += 25
                print("Velocidad aumento a " + str(constante_velocidad) + "\n")
        elif key == ord('-'):
            if constante_velocidad - 25 < 0:
                print("No se puede disminuir mas de velocidad.\n")
            else:
                constante_velocidad -= 25
                print("Velocidad disminuyo a " + str(constante_velocidad) + "\n")
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
                # Obtener la fecha y hora actual
                fecha_hora_actual = datetime.now()

                # Formatear la fecha y hora en el formato deseado
                fecha_hora_formateada = fecha_hora_actual.strftime('%Y-%m-%d_%H-%M-%S')
                file_name = f"captura_{fecha_hora_formateada}_a_{angulo_vertical}_v_{angulo_horizontal}_h.jpg"            
            
                print( "Captura Realizada. Guardada como JPG con el nombre: " + file_name)
            
                command = f"rpicam-jpeg -t 1 -n -o {file_name } > /dev/null 2>&1"
                os.system(command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="velocidad")
    parser.add_argument("--velocidad", type=int, default=25, help="velocidad")
    args = parser.parse_args()
    
curses.wrapper(main)
