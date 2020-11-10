import math

heat_transfer = 150
t_air = 25
d = 0.0014
l = 0.083
lc = (l + (d / 4))
k = 401
fins = 260

h = float(input("Input value for Convection Heat Transfer, h : "))
A = math.pi * d * lc
m = math.sqrt((4 * h) / (k * d))
Efficiency = ((math.tanh(m * lc)) / (m * lc))

R = 1 / (h * A * Efficiency)


def get_sink_temperature():

    t_heat_sink = ((heat_transfer/fins) * R) + t_air

    return t_heat_sink


def get_fin_temperature(s, t_heat_sink):

    fin_temperature = ((math.cosh((m*(lc - s)))/(math.cosh(m*lc))) * (t_heat_sink - t_air)) + t_air

    return fin_temperature
