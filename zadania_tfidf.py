#from os import listdir
import numpy as np
import operator
from sklearn import naive_bayes, svm
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords, reuters
import re
import math
cachedStopWords = stopwords.words("english")
min_length = 3

class corpus:
    def __init__(self):
        self.tfidf_representer = tf_idf()
        self.documents = []
        self.categories = reuters.categories()
        self.cat_dict = {}
        iterator = 0
        for category in self.categories:
            iterator = iterator + 1
            self.cat_dict[iterator] = category
            for docid in reuters.fileids(category):
                doc_class = iterator
                if docid.startswith("train"):
                    train = 1
                elif docid.startswith("test"):
                    train = 0
                else:
                    raise
                text = reuters.raw(docid)
                doc = document(text, doc_class, train)
                self.add_document(doc)
        self.initialize_vocabulary()
    def add_document(self, document):
        self.documents.append(document)
        self.tfidf_representer.add_document(document)

    def get_train_documents(self):
        train = []
        for doc in self.documents:
            if doc.train == 1:
                train.append(doc.text)
        return train

    def initialize_vocabulary(self):
        vocabulary = {}
        inverse_vocabulary = {}
        self.vocabulary = {}
        self.inverse_vocabulary = {}
        vocabulary_sizes = {}
        i = 0
        for doc in self.documents:
            for word in doc.get_unique_words():
                if word not in inverse_vocabulary:
                    vocabulary_sizes[i] = 0
                    vocabulary[i] = word
                    inverse_vocabulary[word] = i
                    i += 1
                else:
                    vocabulary_sizes[inverse_vocabulary[word]] += 1

        sorted_sizes = sorted(vocabulary_sizes.items(), key=operator.itemgetter(1), reverse=True)
     #   print(sorted_sizes)

        keys_sorted = sorted_sizes[:300]
    #    print(keys_sorted)
        keys_sorted2 = []
        for x in keys_sorted:
            keys_sorted2.append(x[0])

        iterator = 0
        for i in range(len(vocabulary)):
            if i in keys_sorted2:
                self.vocabulary[iterator] = vocabulary[i]
                self.inverse_vocabulary[vocabulary[i]] = iterator
                iterator += 1

    def get_svm_vectors(self,Train = 0, Test = 0):
        Xs = []
        ys = []
        for doc in self.documents:
            if Train == 1 and doc.train == 0:
                continue
            if Test == 1 and doc.train == 1:
                continue
            x = doc.get_vector(self.inverse_vocabulary, self.tfidf_representer)
            y = doc.doc_class
            Xs.append(x)
            ys.append(y)
        return (Xs,ys)

class document:
    def __init__(self, text, doc_class = 1, train = 1):
        self.doc_class = doc_class
        self.train = train
        self.text = text
        self.preprocessed_text = []
    def preprocessing(self,raw_tokens):
        no_stopwords = [token for token in raw_tokens if token not in cachedStopWords]
        stemmed_tokens = []
        stemmer = PorterStemmer()
        for token in no_stopwords:
            stemmed_tokens.append(stemmer.stem(token))
        p = re.compile('[a-zA-Z]+')
        pattern_checked = []
        for stem in stemmed_tokens:
            if p.match(stem) and len(stem) >= min_length:
                pattern_checked.append(stem)
        return pattern_checked

    def get_preprocessed_tokens(self):
        if len(self.preprocessed_text) == 0:
            self.preprocessed_text = self.preprocessing(self.text.split())
        else:
            return self.preprocessed_text

        return self.preprocessed_text

    def get_unique_words(self):
        word_list = []

        for word in self.preprocessing(self.text.split()):
            if not word in word_list:
                word_list.append(word)
        return word_list


    def get_vector(self,inverse_vocabulary, representer):
        lng = len(inverse_vocabulary)
        vector = [0 for i in range(300)]
        for word in self.preprocessing(self.text.split()):
            if word in inverse_vocabulary.keys():
                vector[inverse_vocabulary[word]] = representer.tfidf(word, self)    #Multinomial model
                #poprzednio:
                #vector[inverse_vocabulary[word]] = 1
        return vector

#    def get_vector(self,inverse_vocabulary):
#        lng = len(inverse_vocabulary)
#        vector = [0 for i in range(300)]
#        for word in self.preprocessing(self.text.split()):
#            if word in inverse_vocabulary.keys():
#                vector[inverse_vocabulary[word]] = 1
#        return vector


class tf_idf:

    def __init__(self):
        self.D = 0.0
        self.df = {}
    def add_document(self, document):
        self.D += 1.0
        for token in document.get_unique_words():
            if token not in self.df:
                self.df[token] = 1.0
            else:
                self.df[token] += 1.0
    def idf(self,token):
        return math.log(self.D/self.df[token])
    def tf(self,token,document):
        liczba_wystapien_tokenu = 0.0
        liczba_tokenow = 0.0
        for t in document.get_preprocessed_tokens():
            liczba_tokenow += 1.0
            if t == token:
                liczba_wystapien_tokenu += 1.0
        return liczba_wystapien_tokenu/liczba_tokenow
    def tfidf(self,token, document):
        return self.tf(token,document) * self.idf(token)



def MyClassification(X, y, XT, yt, Klasyfikator):
    klasyfikator = Klasyfikator
    klasyfikator.fit(X, y)
    pozytywne = 0
    wszystkie = 0
    for i, x in enumerate(XT):
        wszystkie += 1
        klasa = klasyfikator.predict(x)
        if klasa == yt[i]:
            pozytywne = pozytywne + 1
    s = str(klasyfikator.__class__.__name__) + '\n'
    s += str("pozytywne: " + str(pozytywne)) + '\n'
    s += str("wszystkie: " + str(wszystkie))+ '\n'
    s += str(str(float(pozytywne)/float(wszystkie) * 100) + '%')+ '\n'
    return s




crp = corpus()
(X,y) = crp.get_svm_vectors(Train = 1)
print("starting fitting procedure")
#klasyfikator.fit(X,y)
(XT,yt) = crp.get_svm_vectors(Test = 1)

#klasyfikator = naive_bayes.MultinomialNB()
#klasyfikator.fit(X,y)
s1 = MyClassification(X, y, XT, yt, naive_bayes.MultinomialNB())
s2 = MyClassification(X, y, XT, yt, naive_bayes.BernoulliNB())
s3 = MyClassification(X, y, XT, yt, svm.SVC())
print(s1)
print(s2)
print(s3)

""""
pozytywne = 0
wszystkie = 0
for i,x in enumerate(XT):
    wszystkie += 1
    klasa = klasyfikator.predict(x)
    if klasa == yt[i]:
        pozytywne = pozytywne + 1

print(pozytywne)
print(wszystkie)
#testy:
print("dlugosc X:")
print(len(X))
print("dlugosc y:")
print(len(y))
print("dlugosc XT:")
print(len(XT))
print("dlugosc yt:")
print(len(yt))
print("dlugosc vectora w XT:")
print(len(XT[0]))
print(len(XT[1]))
print (XT[1])
"""
