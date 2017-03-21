# preprocessing z wykorzystaniem stemmer'a portera
#from test2 import tf_idf
#from test2 import feature_values
from sklearn import svm
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import re
cachedStopWords = stopwords.words("english")
min_length = 3

from os import listdir


class corpus:
    def __init__(self, dir_pos, dir_neg):
        self.dir_pos = dir_pos
        self.dir_neg = dir_neg
        self.documents = []
        for i, file in enumerate(listdir(dir_neg)):
            if i < 300:
                fs = open(dir_neg + "\\" + file, 'r')
                text = fs.read()
                positive = 0
                train = 0
                doc = document(text, positive, train)
                self.add_document(doc)
            else:
                fs = open(dir_neg + "\\" + file, 'r')
                text = fs.read()
                positive = 0
                train = 1
                doc = document(text, positive, train)
                self.add_document(doc)

                # negdocs.append(open(dir_neg + "\\" + file, 'r').read())

        for i, file in enumerate(listdir(dir_pos)):
            if i < 300:
                fs = open(dir_pos + "\\" + file, 'r')
                text = fs.read()
                positive = 1
                train = 0
                doc = document(text, positive, train)
                self.add_document(doc)

            else:
                fs = open(dir_pos + "\\" + file, 'r')
                text = fs.read()
                positive = 1
                train = 1
                doc = document(text, positive, train)
                self.add_document(doc)

                # posdocs.append(open(dir_pos + "\\" + file, 'r').read())
        self.initialize_vocabulary()

    def add_document(self, document):
         self.documents.append(document)
    def get_train_documents(self):
        train = []
        for doc in self.documents:
            if doc.train == 1:
                train.append(doc.text)
        return train

    #def get_representer(self):
    #    return tf_idf(self.get_train_documents())
    def initialize_vocabulary(self):
        self.vocabulary = {}
        self.inverse_vocabulary = {}
        for i, doc in enumerate(self.documents):
            for word in doc.get_unique_words():
                if word not in self.vocabulary:
                    self.vocabulary[i] = word
                    self.inverse_vocabulary[word] = i

    def get_svm_vectors(self, Train = 0, Test = 0):
        Xs = []
        Ys = []
        for doc in self.documents:
            if Train == 1 and doc.train == 0:
                continue
            if Test == 1 and doc.train == 1:
                continue
            x = doc.get_vector(self.inverse_vocabulary)
            y = doc.positive
            Xs.append(x)
            Ys.append(y)
        return Xs, Ys
class document:
    def __init__(self, text, positive = 1, train = 1):
        self.positive = positive
        self.train = train
        self.text = text
   # def get_feature_values(self, representer):
    #    return feature_values(self.text, representer)
    def preprocessing(self, raw_tokens):
        no_stopwords = [token for token in raw_tokens if token not in cachedStopWords]
        stemmed_tokens = []
        stemmer = PorterStemmer()
        for token in no_stopwords:
            stemmed_tokens.append((stemmer.stem(token)))
        p = re.compile('[a-zA-Z]+');
        pattern_checked = []
        for stem in stemmed_tokens:
            if p.match(stem) and len(stem) >= min_length:
                pattern_checked.append(stem)
        return pattern_checked
    def get_unique_words(self):
        word_list = []

        for word in self.preprocessing(self.text.split()):
            if not word in word_list:
                word_list.append(word)
        return word_list
    def get_vector(self, inverse_vocabulary):
        lng = len(inverse_vocabulary)
        vector = [0 for i in range(lng)]
        for word in self.preprocessing(self.text.split()):
            vector[inverse_vocabulary[word]] = 1
        return vector


klasyfikator = svm.SVC(kernel="linear")
crp = corpus("C:\\Users\\s0146074\\Desktop\\txt_sentoken\\pos", "C:\\Users\\s0146074\\Desktop\\txt_sentoken\\neg")
#print(crp.documents[0].get_feature_values(crp.get_representer()))
#negdocs = []
#posdocs = []
#dir_neg = "C:\\Users\\s0146074\\Desktop\\txt_sentoken\\pos"
#dir_pos = "C:\\Users\\s0146074\\Desktop\\txt_sentoken\\neg"
#print(crp.inverse_vocabulary["pirate"])

(X,y) = crp.get_svm_vectors(Train=1)
print("starting fitting procedure")
klasyfikator.fit(X,y)

(XT,yt) = crp.get_svm_vectors(Test=1)
pozytywne = 0
wszystkie = 0
for i,x in enumerate(XT):
    wszystkie += 1
    klasa = klasyfikator.predict(x)
    if klasa == yt[i]:
        pozytywne = pozytywne + 1



print(pozytywne)
print(wszystkie)