import machine

pwm = machine.PWM(machine.Pin(15), freq = 1000)

def amplitude(p):
    pwm.duty(int(p * 1023))
