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

# câu truy vấn token làm dữ liệu train cho RDR
def read_cautruyvan(file_path):
  sens = []
  for line in open(file_path, encoding='utf-8'):
    line = line.replace("\n","")
    sens.append(line.lower())  
  return sens

# concate cau truy vấn token (giống concate câu truy vấn)
print("đang tổng hợp câu truy vấn đã token...")

word_list_train, tag_list_train, num_sent_train, max_length_train, max_length_of_a_word_train = read_conll_format('all data/2_data_train_location_form.txt')
import math
length = num_sent_train
max_sen = 1500

cautruyvan_token = []
for index in range(math.ceil(length/max_sen)):
  link = "split data/data_{}/train/cautruyvan_token.txt".format(index)
  cautruyvan_token_x = read_cautruyvan(link)
  cautruyvan_token.extend(cautruyvan_token_x)

cautruyvan_token_file = open("split data/cautruyvan_token_train.txt","a",encoding='utf8')
for j in range(len(cautruyvan_token)):
  cautruyvan_token_file.write(str(cautruyvan_token[j]))
  cautruyvan_token_file.write('\n')
cautruyvan_token_file.close()

print("có {} câu truy vấn đã token tron dữ liêu train".format(len(cautruyvan_token)))