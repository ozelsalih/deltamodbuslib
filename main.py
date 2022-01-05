from deltamodbuslib import deltaDriver
from deltamodbuslib import deltaDriver

delta = deltaDriver()
m100 = delta.address('M', 100)
y3 = delta.address('Y', 3)

delta.setCoil(m100)
delta.setCoil(y3)
delta.resetCoil(m100)
delta.resetCoil(y3)