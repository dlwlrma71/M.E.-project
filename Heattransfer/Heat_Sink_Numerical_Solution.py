import matplotlib.pyplot as plt
import Heat_sink_Data as get

T_cpu = None
L = 0
Heat_Transfer = 150
T_heat_sink = get.get_sink_temperature()
delta = 0.00005
R_heat_sink = delta/(401*0.00159)
R_thermal_paste = delta/(70*0.00159)
n = 0
Temperature = []
x = []
T_old = T_heat_sink
#Temperature_list = open("TemperatureList.txt", "a")
#Distance_list = open("DistanceList.txt", "a")

while L < 0.004:

    if L < 0.003:
        R = R_heat_sink
    elif 0.004 > L > 0.003:
        R = R_thermal_paste

    T_new = (Heat_Transfer * R) + T_old
    T_old = T_new
    n = n + 1
    L = L + delta

    Temperature.append(T_new)
    x.append(L)

    #Temperature_list.write(str(T_new) + "\n")
    #Distance_list.write(str(L) + "\n")

    print(str(T_new) + " at L = " + str(L))

Temperature.reverse()

while 0.004 < L < 0.094:

    s = L - 0.004
    T_new = get.get_fin_temperature(s, T_heat_sink)
    Temperature.append(T_new)
    x.append(L)
    L = L+delta
    #Temperature_list.write(str(T_new) + "\n")
    #Distance_list.write(str(L) + "\n")
    print(str(T_new) + " at L = " + str(L))


plt.plot(x, Temperature, color='red', linewidth=2)

plt.xlabel("Distance")
plt.ylabel("Temperature")

T_max = max(Temperature)

plt.show()

print("Tmax is " + str(T_max))

#Temperature_list.close()
#Distance_list.close()