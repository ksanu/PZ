from sklearn import svm
import matplotlib.pyplot as plt



klasyfikator = svm.SVC()
X = [[2,1],[3,4],[4,7]]
c = [1,0,1]
klasyfikator.fit(X,c)

print(klasyfikator.predict([3,2]))


def load_data(filename):
    X = []
    for line in open(filename):
        tokens = line.split()
        X.append([float(tokens[0]),float(tokens[1]),float(tokens[2])])
    return(X)


def draw_data(X):
    x1 = []
    y1 = []

    x2 = []
    y2 = []

    x3 = []
    y3 = []

    for [x,y,c] in X:
        if (c == 1):
            x1.append(x)
            y1.append(y)
        if (c == 0):
            x2.append(x)
            y2.append(y)
        if (c == -1):
            x3.append(x)
            y3.append(y)

    plt.axis([-10, 10, -10, 10])
    # stworzenie diagramu wszystkich punktów
    plt.plot(x1, y1, 'ro', color='red')
    plt.plot(x2, y2, 'ro', color='blue')
    plt.plot(x3, y3, 'ro', color='white')

    plt.show()



def classify(X):
    Xs = []
    ys = []

    for [x,y,c] in X:
        if c == 1 or c == 0:
            Xs.append([x,y])
            ys.append(c)
    clf = svm.SVC()
    clf.fit(Xs,ys)
    for i in range(len(X)):
        if X[i][2] == -1:
            X[i][2] = clf.predict([X[i][0],X[i][1]])
    return X


draw_data(classify(load_data('treningowy')))