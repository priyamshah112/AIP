#tf-idf is used for marching best answer from dataset to match for answer relevancy
#tf(t,d) = count of t in d / number of words in d
#df(t) = occurrence of t in documents
#idf(t) = log(N/(df + 1))
#tf-idf(t, d) = tf(t, d) * log(N/(df + 1))

#https://towardsdatascience.com/tf-idf-for-document-ranking-from-scratch-in-python-on-real-world-dataset-796d339a4089

#https://github.com/williamscott701/Information-Retrieval/blob/master/2.%20TF-IDF%20Ranking%20-%20Cosine%20Similarity%2C%20Matching%20Score/TF-IDF.ipynb

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter
from num2words import num2words

import nltk
import os
import string
import numpy as np
import copy
import pandas as pd
import pickle
import re
import math
nltk.download('stopwords')
#nltk.download('punkt')

#Preprocessing
def convert_lower_case(data):
    return np.char.lower(data)

def remove_stop_words(data):
    stop_words = stopwords.words('english')
    words = word_tokenize(str(data))
    new_text = ""
    for w in words:
        if w not in stop_words and len(w) > 1:
            new_text = new_text + " " + w
    return new_text

def remove_punctuation(data):
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', '')
    return data

def remove_apostrophe(data):
    return np.char.replace(data, "'", "")

def stemming(data):
    stemmer= PorterStemmer()
    
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + stemmer.stem(w)
    return new_text

def convert_numbers(data):
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        try:
            w = num2words(int(w))
        except:
            a = 0
        new_text = new_text + " " + w
    new_text = np.char.replace(new_text, "-", " ")
    return new_text

def preprocess(data):
    data = convert_lower_case(data)
    data = remove_punctuation(data) #remove comma seperately
    data = remove_apostrophe(data)
    data = remove_stop_words(data)
    data = convert_numbers(data)
    data = stemming(data)
    data = remove_punctuation(data)
    data = convert_numbers(data)
    data = stemming(data) #needed again as we need to stem the words
    data = remove_punctuation(data) #needed again as num2word is giving few hypens and commas fourty-one
    data = remove_stop_words(data) #needed again as num2word is giving stop words 101 - one hundred and one
    return data

processed_text = []

# Extracting Data
def extract_data(relevant_answers,my_answer,N):
  for i in range(N):
    processed_text.append(word_tokenize(str(preprocess(relevant_answers[i]))))
  t= document_frequency_calculate(relevant_answers,my_answer,N)
  return t

DF = {}
total_vocab_size = len(DF)
total_vocab = [x for x in DF]

# Calculating Document frequency of words
def document_frequency_calculate(relevant_answers,my_answer,N):  
  for i in range(N):
      tokens = processed_text[i]
      for w in tokens:
          try:
              DF[w].add(i)
          except:
              DF[w] = {i}

  for i in DF:
      DF[i] = len(DF[i])
      
  global total_vocab_size
  total_vocab_size = len(DF)
  global total_vocab
  total_vocab = [x for x in DF]
  t = tf_idf_calculate(relevant_answers,my_answer,N)
  return t

def doc_freq(word):
    c = 0
    try:
        c = DF[word]
    except:
        pass
    return c

tf_idf = {}

def tf_idf_calculate(relevant_answers,my_answer,N):
  doc = 0
  for i in range(N):
      
      tokens = processed_text[i]
      
      counter = Counter(tokens + processed_text[i])
      words_count = len(tokens + processed_text[i])
      
      for token in np.unique(tokens):
          
          tf = counter[token]/words_count
          df = doc_freq(token)
          idf = np.log((N+1)/(df+1))
          
          tf_idf[doc, token] = tf*idf

      doc += 1
  t = cosine_similarity(8, my_answer,relevant_answers,N)
  return t

def cosine_sim(a, b):
    cos_sim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
    return cos_sim

def vectorizing_tfidf(relevant_answers,my_answer,N):
  total_vocab_size = len(DF)
  D = np.zeros((N, total_vocab_size))
  for i in tf_idf:
   try:
      ind = total_vocab.index(i[1])
      i0=i[0]
      D[i0][ind] = tf_idf[i]
   except:
     pass
  return D

def gen_vector(tokens,N):
    Q = np.zeros((len(total_vocab)))
    counter = Counter(tokens)
    words_count = len(tokens)
    query_weights = {}
    for token in np.unique(tokens):
        tf = counter[token]/words_count
        df = doc_freq(token)
        idf = math.log((N+1)/(df+1))
        try:
            ind = total_vocab.index(token)
            Q[ind] = tf*idf
        except:
            pass
    return Q

def cosine_similarity(k,query,relevant_answers,N):
    D = vectorizing_tfidf(relevant_answers,query,N)
    preprocessed_query = preprocess(query)
    tokens = word_tokenize(str(preprocessed_query))
    d_cosines = []    
    query_vector = gen_vector(tokens,N)
    for d in D:
        d_cosines.append(cosine_sim(query_vector, d))
    print("d cosine ",d_cosines)
    out = np.array(d_cosines).argsort()[-k:][::-1]
    print("out ",out)
    final_score = int(round(max(d_cosines)*100,2)/20)
    return final_score 

def scoring(relevant_answers,my_answer):
  N=len(relevant_answers)
  score = extract_data(relevant_answers,my_answer,N)
  return score