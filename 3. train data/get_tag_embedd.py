import numpy as np
import requests
import codecs
import _pickle as pickle
import time

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

def read_conll_format(input_file):
    with codecs.open(input_file, 'r', 'utf-8') as f:
        word_list = [] 
        tag_list = []
        words = []
        tags = []
        num_sent = 0
        max_length = 0
        for line in f:
            line = line.split()
            if len(line) > 0:
                words.append(map_number_and_punct(line[0].lower()))
                tags.append(line[1])
            else:
                word_list.append(words)
                tag_list.append(tags)
                sent_length = len(words)
                words = []
                tags = []
                num_sent += 1
                max_length = max(max_length, sent_length)
    return word_list, tag_list, num_sent, max_length

# def map_number_and_punct(word):
#     if any(char.isdigit() for char in word):
#         word = u'<number>'
#     elif word in [u',', u'<', u'.', u'>', u'/', u'?', u'..', u'...', u'....', u':', u';', u'"', u"'", u'[', u'{', u']',
#                   u'}', u'|', u'\\', u'`', u'~', u'!', u'@', u'#', u'$', u'%', u'^', u'&', u'*', u'(', u')', u'-', u'+',
#                   u'=']:
#         word = u'<punct>'
#     return word
#============================get tag_list=====================================
# word_list_1, tag_list_1, num_sent_1, max_length_1 = read_conll_format('../4. train data/1_data_train_location_ner_form.txt')
# name_of_out_file_1 = 'tag_embedd_1.txt'

# word_list_train, tag_list_train, num_sent_train, max_length_train = read_conll_format('train/data.txt')
# name_of_out_file_train = 'train/tag_embedd.txt'
# word_list_val, tag_list_val, num_sent_val, max_length_val = read_conll_format('val/data.txt')
# name_of_out_file_val = 'val/tag_embedd.txt'

# word_list_test, tag_list_test, num_sent_test, max_length_test = read_conll_format('test/data.txt')
# name_of_out_file_test = 'test/tag_embedd.txt'

# print("num_sent_train : {}".format(num_sent_train))
# print("num_sent_val     : {}".format(num_sent_val))
# print("num_sent_test : {}".format(num_sent_test))
#============================create dic of tag================================
# def dict_of_tags(tag_list):
#     dic = {'pad': 0}
#     index = 0
#     for tags in tag_list:
#         for tag in tags:
#             try:
#                 dic[tag]
#             except:
#                 index = index + 1
#                 dic[tag]= index
#     return dic, len(dic)

# dic_of_tag, len_of_dic_tag = dict_of_tags(tag_list)
# print(dic_of_tag)
# print(len_of_dic_tag)

dic_of_tag = {'pad': 0, 'LOCATION_HOMENUMBER': 1, 'LOCATION_STREET': 2, 'LOCATION_WARD': 3, 'LOCATION_DISTRICT': 4, 'LOCATION_PROVINCE': 5, 'LOCATION_COUNTRY': 6, 'LOCATION_POSTCODE': 7, 'LOCATION_NER': 8, 'OBJ': 9, 'OBJ_FEATURE': 10, 'PRE': 11, 'UNKNOW': 12 }
# dic_of_tag = {'pad': 0, 'LOCATION_HOMENUMBER': 1, 'LOCATION_STREET': 2, 'LOCATION_WARD': 3, 'LOCATION_DISTRICT': 4, 'LOCATION_PROVINCE': 5, 'LOCATION_COUNTRY': 6, 'LOCATION_POSTCODE': 7, 'LOCATION_NER': 8, 'OBJ': 9, 'OBJ_FEATURE': 10, 'PRE': 11, 'UNKNOW': 12 }
len_of_dic_tag = len(dic_of_tag)
#===========================encode tag_list by dic_of_tags================
def encode_Tag_list_by_Dic_of_tags(tag_list,dic,len_of_a_sentence):
    encodeTag_of_many_sentence = []
    for tags_of_a_sentence in tag_list:
        # print(tags_of_a_sentence)
        encode_of_a_sentence = np.zeros(len_of_a_sentence)
        for i in range(len(tags_of_a_sentence)):
            tag = tags_of_a_sentence[i]
            
            encode_of_a_sentence[i] = dic[tag]
        encodeTag_of_many_sentence.append(encode_of_a_sentence)
    return np.array(encodeTag_of_many_sentence)

# tag_list_encode_1 = encode_Tag_list_by_Dic_of_tags(tag_list_1,dic_of_tag,42)
# print(tag_list_encode_1.shape)
# tag_list_encode_2 = encode_Tag_list_by_Dic_of_tags(tag_list_2,dic_of_tag,42)
# print(tag_list_encode_2.shape)
# tag_list_encode_3 = encode_Tag_list_by_Dic_of_tags(tag_list_3,dic_of_tag,42)
# print(tag_list_encode_3.shape)
# tag_list_train_encode = encode_Tag_list_by_Dic_of_tags(tag_list_train,dic_of_tag,42)
# tag_list_val_encode = encode_Tag_list_by_Dic_of_tags(tag_list_val,dic_of_tag,42)
# tag_list_test_encode = encode_Tag_list_by_Dic_of_tags(tag_list_test,dic_of_tag,42)
# print(tag_list_train_encode.shape)
# print(tag_list_val_encode.shape)
# print(tag_list_test_encode.shape)
#==========================create one hot vector from tag_encode==========
def create_onehot(sens_encodes, tag_dim, num_word_in_sentence,name_of_out_file):
    X = np.zeros([len(sens_encodes), num_word_in_sentence, tag_dim])
    for i in range(len(sens_encodes)):# duyet tung cau
        for j in range(len(sens_encodes[i])):# duyet tung tu trong cau
            index = sens_encodes[i][j].astype(np.int64)
            X[i,j,index] = 1

    X = X.reshape(X.shape[0]*X.shape[1], X.shape[2])
    fileout = open(name_of_out_file, 'a+', encoding='utf8')
    np.savetxt(fileout, X)
    fileout.close()
    return X

# tag_onehot_1 = create_onehot(tag_list_encode_1, tag_dim = 14, num_word_in_sentence = 42,name_of_out_file = name_of_out_file_1)
# print(tag_onehot_1.shape)
# tag_onehot_2 = create_onehot(tag_list_encode_2, tag_dim = 14, num_word_in_sentence = 42,name_of_out_file = name_of_out_file_2)
# print(tag_onehot_2.shape)
# tag_onehot_3 = create_onehot(tag_list_encode_3, tag_dim = 14, num_word_in_sentence = 42,name_of_out_file = name_of_out_file_3)
# print(tag_onehot_3.shape)

# tag_onehot_train = create_onehot(tag_list_train_encode, tag_dim = 13, num_word_in_sentence = 42,name_of_out_file = name_of_out_file_train)
# print(tag_onehot_train.shape)
# tag_onehot_val = create_onehot(tag_list_val_encode, tag_dim = 13, num_word_in_sentence = 42,name_of_out_file = name_of_out_file_val)
# print(tag_onehot_val.shape)
# tag_onehot_test = create_onehot(tag_list_test_encode, tag_dim = 13, num_word_in_sentence = 42,name_of_out_file = name_of_out_file_test)
# print(tag_onehot_test.shape)

word_list_train, tag_list_train, num_sent_train, max_length_train = read_conll_format('all data/2_data_train_location_form.txt')
import math
length = num_sent_train
max_sen = 1500
for index in range(math.ceil(length/max_sen)):
  print("data {}".format(index))
  
  link_train = "split data/data_{}/train/data.txt".format(index)
  link_val = "split data/data_{}/val/data.txt".format(index)
  link_test = "split data/data_{}/test/data.txt".format(index)
  out_train = "split data/data_{}/train/tag_embedd.txt".format(index)
  out_val = "split data/data_{}/val/tag_embedd.txt".format(index)
  out_test = "split data/data_{}/test/tag_embedd.txt".format(index)

  word_list_train, tag_list_train, num_sent_train, max_length_train = read_conll_format(link_train)
  word_list_val, tag_list_val, num_sent_val, max_length_val = read_conll_format(link_val)
  word_list_test, tag_list_test, num_sent_test, max_length_test = read_conll_format(link_test)

  tag_list_train_encode = encode_Tag_list_by_Dic_of_tags(tag_list_train,dic_of_tag,42)
  tag_list_val_encode = encode_Tag_list_by_Dic_of_tags(tag_list_val,dic_of_tag,42)
  tag_list_test_encode = encode_Tag_list_by_Dic_of_tags(tag_list_test,dic_of_tag,42)

  tag_onehot_train = create_onehot(tag_list_train_encode, tag_dim = 13, num_word_in_sentence = 42,name_of_out_file = out_train)
  tag_onehot_val = create_onehot(tag_list_val_encode, tag_dim = 13, num_word_in_sentence = 42,name_of_out_file = out_val)
  tag_onehot_test = create_onehot(tag_list_test_encode, tag_dim = 13, num_word_in_sentence = 42,name_of_out_file = out_test)
  
  print("----------------------")