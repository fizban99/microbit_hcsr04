from hcsr04 import HCSR04
from microbit import sleep, button_a, display


sonar = HCSR04()
while True:
    if button_a.is_pressed():
        distance = round(sonar.distance_mm()/10)
        if distance < 10:
            display.show(str(distance))
        else:
            display.scroll(str(distance))
        while button_a.is_pressed():
            sleep(100)
    sleep(100)
