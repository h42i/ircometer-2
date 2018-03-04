import network
import time
import gc
import apa
import pwm

# Config
wifi_ssid = "HaSi-Kein-Internet-Legacy"
wifi_psk = "bugsbunny"

def play_animation():
    apa.color(255, 255, 255, 31)
    pwm.amplitude(0.25)
    time.sleep(0.1)

    apa.color(255, 255, 255, 0)
    pwm.amplitude(0.0)
    time.sleep(0.1)

    apa.color_r(255, 255, 255, 31)
    pwm.amplitude(0.5)
    time.sleep(0.2)

    apa.color(255, 255, 255, 0)
    pwm.amplitude(0.0)
    time.sleep(0.1)

    apa.color_l(255, 255, 255, 31)
    pwm.amplitude(1.0)
    time.sleep(0.5)

    apa.color(255, 255, 255, 0)
    pwm.amplitude(0.0)
    time.sleep(0.5)

    apa.color_r(255, 255, 255, 31)
    pwm.amplitude(1.0)
    time.sleep(0.2)
    apa.color_l(255, 255, 255, 31)
    time.sleep(0.1)
    apa.color_r(255, 255, 255, 0)
    time.sleep(0.2)
    apa.color_r(255, 255, 255, 31)
    time.sleep(0.2)

    for i in range(255):
        apa.color(255-i, 255, 255-i, 31)
        pwm.amplitude(100/(i+1))

    set_amplitude(0.0)

def setup():
    print('Setting up...')

    global wifi_ssid
    global wifi_psk

    # Setup Network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(wifi_ssid, wifi_psk)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

    #print('Botting up...')
    #bot = telepot.Bot('490366497:AAGEZ_-dabSrBHVx0svm8ZfwUYd_sIlqBik')
    #bot.getMe()

def set_amplitude(p):
    apa.amplitude(p)
    pwm.amplitude(p)

def loop():
    while True:
        gc.collect()
        time.sleep(1)

play_animation()
setup()
loop()
