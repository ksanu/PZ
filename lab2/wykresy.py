import matplotlib.pyplot as plt


x = []
y = []
c = []


x1 = []
y1 = []

x2 = []
y2 = []

x3 = []
y3 = []

f = open('treningowy')
#Iiterowanie po liniach

for line in f:
    #dzielimy według spacji i zapisujemy w tablicach
    x.append(float(line.split()[0]))
    y.append(float(line.split()[1]))
    c.append(float(line.split()[2]))

for i in range(len(x)):
    if(c[i] == 1):
        x1.append(x[i])
        y1.append(y[i])
    if (c[i] == 0):
        x2.append(x[i])
        y2.append(y[i])
    if (c[i] == -1):
        x3.append(x[i])
        y3.append(y[i])

plt.axis([-10,10,-10,10])
#stworzenie diagramu wszystkich punktów
plt.plot(x1,y1,'ro', color = 'red')
plt.plot(x2,y2,'ro', color = 'blue')
plt.plot(x3,y3,'ro', color = 'white')

plt.show()


