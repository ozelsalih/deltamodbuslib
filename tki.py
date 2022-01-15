from cgitb import text
from glob import glob
import random
import tkinter as tk
from deltamodbuslib import deltaDriver

root = tk.Tk()
delta = deltaDriver()
m100 = delta.address('M', 100)
d100 = delta.address('D', 100)
y0 = delta.address('Y', 0)
y1 = delta.address('Y', 1)
y2 = delta.address('Y', 2)
y3 = delta.address('Y', 3)
y4 = delta.address('Y', 4)
y5 = delta.address('Y', 5)

delta.setCoil(m100)
delta.resetCoil(m100)
metric = 0
last = int(float(delta.readRegister(d100)))
encoder = 1


def btn_y0f():
    if delta.readCoil(y0):
        delta.resetCoil(y0)
    else:
        delta.setCoil(y0)


def btn_y1f():
    if delta.readCoil(y1):
        delta.resetCoil(y1)
    else:
        delta.setCoil(y1)


def btn_y2f():
    if delta.readCoil(y2):
        delta.resetCoil(y2)
    else:
        delta.setCoil(y2)


def btn_y3f():
    if delta.readCoil(y3):
        delta.resetCoil(y3)
    else:
        delta.setCoil(y3)


def btn_y4f():
    if delta.readCoil(y4):
        delta.resetCoil(y4)
    else:
        delta.setCoil(y4)


def btn_y5f():
    if delta.readCoil(y5):
        delta.resetCoil(y5)
    else:
        delta.setCoil(y5)


def updateEncoder():
    global encoder
    encoder = int(float(delta.readRegister(d100)))
    metric_print()
    root.after(50, updateEncoder)


def metric_print():
    global last
    global metric
    global encoder

    if last != encoder:
        pulse = (encoder-last) / 50
        metric = round(metric + pulse * 0.70, 4)
        last = encoder
        lbl_metric.config(text=f'{metric} mm')


def resetEncoder():
    print("reset")
    delta.setCoil(m100)
    delta.resetCoil(m100)
    lbl_metric.config(text="0")


root.columnconfigure(2, minsize=150)
root.rowconfigure([1, 0], minsize=50)
btn_rst = tk.Button(text="Reset", command=resetEncoder)

btn_y0 = tk.Button(text="y0", command=btn_y0f)
btn_y1 = tk.Button(text="y1", command=btn_y1f)
btn_y2 = tk.Button(text="y2", command=btn_y2f)
btn_y3 = tk.Button(text="y3", command=btn_y3f)
btn_y4 = tk.Button(text="y4", command=btn_y4f)
btn_y5 = tk.Button(text="y5", command=btn_y5f)

lbl_metric = tk.Label(root, text='0')

btn_rst.grid(row=0, column=0, sticky="nsew")
lbl_metric.grid(row=1, column=0)
btn_y0.grid(row=0, column=2)
btn_y1.grid(row=1, column=2)
btn_y2.grid(row=2, column=2)
btn_y3.grid(row=3, column=2)
btn_y4.grid(row=4, column=2)
btn_y5.grid(row=5, column=2)

updateEncoder()
root.mainloop()
