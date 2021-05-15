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

    if re.match(r"^[0-9]{2}0{3}$", word):
        return u'<postcode>'

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
# read file
def read_char_vocab(file_path):
  char_vocab = []
  for line in open(file_path, encoding='utf-8'):
    char_vocab.append(line.splitlines()[0].lower())      
  return char_vocab
# run read char vocab==========begin=======================================
char_vocab_data = read_char_vocab("vocab/VISCII_short.txt")
# char_vocab_data = read_char_vocab("char_vocab_VISCII.txt")
# print(char_vocab_data)
LEN_OF_VOCAB = len(char_vocab_data) # len of onehot vector
print('length of vocab : '+str(LEN_OF_VOCAB))
# define a mapping of chars to integers
# char_to_int = dict((char_vocab_data[i], i) for i in range(LEN_OF_VOCAB))
# int_to_char = dict((i, char_vocab_data[i]) for i in range(LEN_OF_VOCAB))
def char_to_int(char_vocab_data):
  dic = {}
  index = -1
  for char in char_vocab_data:
    try:
      dic[char]
    except:
      index = index + 1
      dic[char]=index 
  return dic
def int_to_char(char_vocab_data):
  dic = {}
  index = -1
  for char in char_vocab_data:
    try:
      dic[char]
    except:
      index = index + 1
      dic[index]=char
  return dic
char_to_int = char_to_int(char_vocab_data)
int_to_char = int_to_char(char_vocab_data)

# for key in int_to_char:
#   print(str(key)+" : "+str(int_to_char[key]))

# define input string
word_list_train, tag_list_train, num_sent_train, max_length_train, max_length_of_a_word_train = read_conll_format('../4. train data/train/data.txt')
name_of_out_file_train = 'train/char_encode.txt'
word_list_val, tag_list_val, num_sent_val, max_length_val, max_length_of_a_word_val = read_conll_format('../4. train data/val/data.txt')
name_of_out_file_val = 'val/char_encode.txt'
# word_list_1, tag_list_1, num_sent_1, max_length_1, max_length_of_a_word_1 = read_conll_format('../4. train data/1_data_train_location_ner_form.txt')
# name_of_out_file_1 = 'char_encode_1.txt'
# print("max_length_of_a_sentence_1 : {}".format(max_length_1))
# print("max_length_of_a_word_1     : {}".format(max_length_of_a_word_1))
print("max_length_of_a_sentence_train : {}".format(max_length_train))
print("max_length_of_a_word_train     : {}".format(max_length_of_a_word_train))
print("max_length_of_a_sentence_val : {}".format(max_length_val))
print("max_length_of_a_word_val     : {}".format(max_length_of_a_word_val))

# word_list, tag_list, num_sent, max_length, max_length_of_a_word = read_conll_format('../4. train data/data_train.txt')
# name_of_out_file = 'char_encode.txt'

print(max_length_of_a_word_train)
max_length_of_a_sentence = 42
max_length_of_a_word     = 32



#=================start====================================================
def char_encode_word_list(word_list,max_length_of_a_sentence,max_length_of_a_word,name_of_out_file):
  # len(word_list)
  word_list_encoded = np.zeros([len(word_list), max_length_of_a_sentence, max_length_of_a_word])
  for i in range(len(word_list)):
    
    sentence = word_list[i] # words is a sentence | ['i','am','an']
    sentence_encoded = np.zeros([max_length_of_a_sentence,max_length_of_a_word]) # 25*25
    for j in range(len(sentence)):  
      # word to encoded, like [12,3,4,20,0,0,0,0,0]
      word = sentence[j].lower()
      # integer_encoded = [char_to_int[char] for char in word]
      word_encoded = np.zeros(max_length_of_a_word)
      for k in range(len(word)):
        char = word[k]
        try:
          word_encoded[k]= char_to_int[char]
        except:
          print("error : " + str(char)+" "+str(word)+" "+str(len(word)))
          word_encoded[k]= char_to_int['[unk]']

      # sentence encoded
      sentence_encoded[j] = word_encoded

    word_list_encoded[i] = sentence_encoded

  print(word_list_encoded.shape)

  X = word_list_encoded
  X = X.reshape(X.shape[0]*X.shape[1],X.shape[2])
  X = X.astype(np.int64)

  fileout = open(name_of_out_file, 'a+', encoding='utf8')
  
  np.savetxt(fileout, X)
  fileout.close()

  return word_list_encoded

# char_encode_1 = char_encode_word_list(word_list_1,42,32,name_of_out_file_1)

char_encode_train = char_encode_word_list(word_list_train,42,32,name_of_out_file_train)

char_encode_val = char_encode_word_list(word_list_val,42,32,name_of_out_file_val)

# char_encode = char_encode_word_list(word_list,42,32,name_of_out_file)