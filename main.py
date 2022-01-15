from deltamodbuslib import deltaDriver
import os

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

delta = deltaDriver()
m100 = delta.address('M', 100)
d100 = delta.address('D', 100)
delta.setCoil(m100)
delta.resetCoil(m100)
last = int(float(delta.readRegister(d100)))
encoder = 1
metric = 0
while True:
    encoder = int(float(delta.readRegister(d100)))
    if last != encoder:

        pulse = (encoder-last) / 50
        metric = round(metric + pulse * 0.70, 4)
        last = encoder  # 50 pulse 0.70
        clearConsole()

        print(
            f"""
encoder:{encoder}
pulse:  {pulse}
metric: {metric}mm
cevap: {delta.response[1:]}
""")
