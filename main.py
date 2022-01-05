from deltamodbuslib import deltaDriver
from time import perf_counter

delta = deltaDriver()
m100 = delta.address('M', 100)

print("\n------------------------")
tic = perf_counter()
delta.setCoil(m100)
toc = perf_counter()
print("setCoil:", format(toc - tic, '0.4f'))
print("------------------------")

print("\n------------------------")
tic = perf_counter()
delta.resetCoil(m100)
toc = perf_counter()
print("resetCoil:", format(toc - tic, '0.4f'))
print("------------------------")

