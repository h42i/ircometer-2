# This file is executed on every boot (including wake-boot from deepsleep)
import gc
import webrepl
import network

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.config(dhcp_hostname='ircometer')

gc.collect()
webrepl.start()
