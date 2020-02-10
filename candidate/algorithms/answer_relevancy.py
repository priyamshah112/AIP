from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
import requests
from bs4 import BeautifulSoup
import lxml
from googleapiclient import discovery
from googleapiclient.discovery import build
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk
from candidate.algorithms.scoring import scoring
nltk.download('punkt')
LANGUAGE = "english"
SENTENCES_COUNT = 10
relevant_answers = []

def summarized_data_from_url(url):
  parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
  stemmer = Stemmer(LANGUAGE)
  summarizer = Summarizer(stemmer)
  summarizer.stop_words = get_stop_words(LANGUAGE)
  temp_ans =[]
  for sentence in summarizer(parser.document, SENTENCES_COUNT):
      #print(sentence)
      temp_ans.append(str(sentence))
  relevant_answers.append("".join(temp_ans))

headers_Get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }


def general_question_answer(q):
    s = requests.Session()
    q = '+'.join(q.split())
    url = 'https://www.google.com/search?q=' + q + '&ie=utf-8&oe=utf-8'
    r = s.get(url, headers=headers_Get)

    soup = BeautifulSoup(r.text, "html.parser")
    output = []
    for searchWrapper in soup.find_all('div', {'class':'r'}): 
        url = searchWrapper.find('a')["href"] 
        output.append(url)
    #print(output,"\n")
    for i in output:
      summarized_data_from_url(i)

#question = "What do you mean by DevOps"
#my_answer = 'DevOps (development and operations) is an enterprise software development phrase used to mean a type of agile relationship between development and IT operations. The goal of DevOps is to change and improve the relationship by advocating better communication and collaboration between these two business units.'
#general_question_answer(question)
#print(scoring(relevant_answers,my_answer))