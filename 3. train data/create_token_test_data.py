import numpy as np
import random
from numpy import argmax
import codecs

import re
def map_number_and_punct(word):
    # check hem va ngach
    num_of_seperate=0
    dem=0
    for char in word:
      if not char.isnumeric() and char!="/":
        dem+=1        
      if char=="/":
        num_of_seperate+=1
    if dem==0:
      if len(word)>1 and num_of_seperate==1:
        return u'<ngach>'
      if len(word)>1 and num_of_seperate>2:
        return u'<hem>'

    # if re.match(r"^[0-9]{2}0{3}$", word):
    #     return u'<postcode>'

    if word.isnumeric():
        word = u'<number>'
    elif word in [u',', u'<', u'.', u'>', u'/', u'?', u'..', u'...', u'....', u':', u';', u'"', u"'", u'[', u'{', u']',
                  u'}', u'|', u'\\', u'`', u'~', u'!', u'@', u'#', u'$', u'%', u'^', u'&', u'*', u'(', u')', u'-', u'+',
                  u'=']:
        word = u'<punct>'

    # word = word.replace("_"," ")
    return word

# from data_trans import read_conll_format
def read_conll_format(input_file):
    with codecs.open(input_file, 'r', 'utf-8') as f:
        word_list = [] 
        tag_list = []
        words = []
        tags = []
        num_sent = 0
        max_length = 0
        max_length_of_a_word = 0
        for line in f:
            line = line.split()
            if len(line) > 0:
                words.append( map_number_and_punct(line[0].lower()) )
                tags.append(line[1])
                max_length_of_a_word = max(max_length_of_a_word, len(line[0]))
            else:
                word_list.append(words)
                tag_list.append(tags)
                sent_length = len(words)
                words = []
                tags = []
                num_sent += 1
                max_length = max(max_length, sent_length)
    return word_list, tag_list, num_sent, max_length, max_length_of_a_word

import numpy as np
import codecs
  
def read_data(input_file):
      with codecs.open(input_file, 'r', 'utf-8') as f:
          word_list = [] 
          words = []
          for line in f:
              line = line.split()
              if len(line) > 0:
                  words.append( line[0].lower())
              else:
                  word_list.append(words)
                  words = []
      return word_list
  
#=============================================================================
from vncorenlp import VnCoreNLP
annotator = VnCoreNLP("../VnCoreNLP-1.1.1.jar", annotators="wseg", max_heap_size='-Xmx500m')

def read_cautruyvan(file_path):
  sens = []
  for line in open(file_path, encoding='utf-8'):
    line = line.replace("\n","")
    sens.append(line.lower())  
  return sens

word_list_train, tag_list_train, num_sent_train, max_length_train, max_length_of_a_word_train = read_conll_format('all data/2_data_train_location_form.txt')
import math
length = num_sent_train
max_sen = 1500

for index in range(math.ceil(length/max_sen)):
  print("DATA {}".format(index))
  link = "split data/data_{}/test/cautruyvan.txt".format(index)
  cautruyvan = read_cautruyvan(link)
  sens_tokend = []
  for sen in cautruyvan:
    sen_tokend = annotator.tokenize(sen)[0]
    sens_tokend.append(sen_tokend)
    
  output = "split data/data_{}/test/data_no_tag_pred.txt".format(index)
  dataset = open(output,"a",encoding='utf8')
  for i in range(len(sens_tokend)):
    for j in range(len(sens_tokend[i])):
      dataset.write(str(sens_tokend[i][j]))
      dataset.write('\n')
    dataset.write('\n')
  dataset.close()

  # so sánh kết quả tách bộ test của bộ tách mới và kết quả tách có sẵn
  link_true = "split data/data_{}/test/data_no_tag.txt".format(index)

  sens_tokend_true = read_data(link_true)

  number_of_sens_has_diff_length = 0

  number_of_sens_has_same_length_but_false = 0

  number_of_sens_true = 0

  for i in range(len(sens_tokend)):
    sen_pre = sens_tokend[i]
    sen_true = sens_tokend_true[i]
    if len(sen_pre)!=len(sen_true):
      number_of_sens_has_diff_length=number_of_sens_has_diff_length+1
    else:
      dem=0
      for j in range(len(sen_pre)):
        if(sen_pre[j]!=sen_true[j]):
          dem+=1
          break
      if dem==0:
        number_of_sens_true=number_of_sens_true+1
      else:
        number_of_sens_has_same_length_but_false=number_of_sens_has_same_length_but_false+1

  print("   number_of_sens_has_diff_length "+ str(number_of_sens_has_diff_length))
  print("   number_of_sens_true "+ str(number_of_sens_true))
  print("   number_of_sens_has_same_length_but_false "+ str(number_of_sens_has_same_length_but_false))
  ti_le = round(100*number_of_sens_true/(number_of_sens_true+number_of_sens_has_diff_length+number_of_sens_has_same_length_but_false),2)
  print("   tỉ lệ số câu tách chính xác/ số câu tách : {}".format(ti_le) )