##biblioteka do rysowania wykresów##
## import  nazwa biblioteki  as alias
import matplotlib.pyplot as plt
##odwołując się do biblioteki piszemy plt.funkcja


##czytanie danych##
##zadeklarowanie tablic
x = []
y = []
c = []
##otwarcie pliku
##plik = open(sciezka* + nazwa_pliku)
f = open('train')
##iterowanie po liniach
for line in f:
    ##dzielimy według spacji i zapisujemy w odpowiednich tablicach
    ##pamiętamy o tym ,że w pliku są zapisane litery, a my potrzebujemy liczby
    x.append(float(line.split()[0]))
    y.append(float(line.split()[1]))
    c.append(float(line.split()[2]))

print(x)
print(y)

##ustawienie pola widzenia na diagramie
plt.axis([-10,10,-10,10])
##stworzenie diagramu wszystkich punktów
##plt.plot(xy , ygreki, kształt, color = kolor
plt.plot(x,y,'ro', color = 'red')


##wyświetlenie diagramu
plt.show()