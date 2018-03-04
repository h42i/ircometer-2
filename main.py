import network
import time
import gc
import apa
import pwm
import irc
from umqtt.simple import MQTTClient

# Config
wifi_ssid = "HaSi-Kein-Internet-Legacy"
wifi_psk = "bugsbunny"

mqtt_server = "mqtt.hasi"
mqtt_client_name = "ircometer"
mqtt_topic = "hasi/lights/ircometer"

lights_on = True
mqtt_client = None

wifi = None

activity = 0.0

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

    global wifi
    global wifi_ssid
    global wifi_psk
    global mqtt_topic
    global mqtt_server
    global mqtt_client
    global mqtt_client_name

    # Setup Network
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    if not wifi.isconnected():
        print('connecting to network...')
        wifi.connect(wifi_ssid, wifi_psk)
        while not wifi.isconnected():
            pass
    print('network config:', wifi.ifconfig())

    # Setup MQTT
    mqtt_client = MQTTClient(mqtt_client_name, mqtt_server)
    mqtt_client.set_callback(mqtt_callback)
    mqtt_client.connect()
    mqtt_client.subscribe(bytes(mqtt_topic, "utf-8"))

    irc.connect("irc.hackint.org",6667,"#hasi","hasi_ircometer")

def set_amplitude(p):
    if lights_on:
        apa.amplitude(p)
        pwm.amplitude(p)
    else:
        apa.color(0, 0, 0, 0)
        pwm.amplitude(0.0)

def mqtt_callback(topic, msg):
    global lights_on

    message = str(msg, "utf-8")

    if message == "on" and not lights_on:
        print("mqtt on")
        play_animation()
        lights_on = True
    elif message == "off" and lights_on:
        print("mqtt off")
        lights_on = False

def loop():
    global wifi
    global activity
    global mqtt_client

    while True:
        if not wifi.isconnected():
            setup()
        else:
            gc.collect()
            mqtt_client.check_msg()
            if activity >= 0.0001:
                activity -= 0.0001
            if irc.do_server() == 1 and activity <= 0.9:
                activity += 0.1
            #print("activity: " + str(activity))
            set_amplitude(activity)
            time.sleep(0.1)

play_animation()
setup()
loop()
