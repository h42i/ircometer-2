# This file is executed on every boot (including wake-boot from deepsleep)
import gc
import webrepl
gc.collect()
webrepl.start()
