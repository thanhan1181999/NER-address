import numpy as np
import requests
import codecs
import _pickle as pickle
import time

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

def map_number_and_punct(word):
    if any(char.isdigit() for char in word):
        word = u'<number>'
    elif word in [u',', u'<', u'.', u'>', u'/', u'?', u'..', u'...', u'....', u':', u';', u'"', u"'", u'[', u'{', u']',
                  u'}', u'|', u'\\', u'`', u'~', u'!', u'@', u'#', u'$', u'%', u'^', u'&', u'*', u'(', u')', u'-', u'+',
                  u'=']:
        word = u'<punct>'
    return word
#============================get tag_list=====================================
# word_list_1, tag_list_1, num_sent_1, max_length_1 = read_conll_format('../4. train data/1_data_train_location_ner_form.txt')
# name_of_out_file_1 = 'tag_embedd_1.txt'

# word_list_2, tag_list_2, num_sent_2, max_length_2 = read_conll_format('../4. train data/2_data_train_location_form.txt')
# name_of_out_file_2 = 'tag_embedd_2.txt'

# word_list_3, tag_list_3, num_sent_3, max_length_3 = read_conll_format('../4. train data/3_data_train_location.txt')
# name_of_out_file_3 = 'tag_embedd_3.txt'

word_list, tag_list, num_sent, max_length = read_conll_format('../4. train data/data_train.txt')
name_of_out_file = 'tag_embedd.txt'

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

dic_of_tag = {'pad': 0, 'LOCATION_HOMENUMBER': 1, 'LOCATION_STREET': 2, 'LOCATION_WARD': 3, 'LOCATION_DISTRICT': 4, 'LOCATION_PROVINCE': 5, 'LOCATION_COUNTRY': 6, 'LOCATION_POSTCODE': 7, 'LOCATION_SPECIAL': 8, 'LOCATION_NER': 9, 'OBJ': 10, 'OBJ_FEATURE': 11, 'PRE': 12, 'UNKNOW': 13 }
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
tag_list_encode = encode_Tag_list_by_Dic_of_tags(tag_list,dic_of_tag,42)
print(tag_list_encode.shape)
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

tag_onehot = create_onehot(tag_list_encode, tag_dim = 14, num_word_in_sentence = 42,name_of_out_file = name_of_out_file)
print(tag_onehot.shape)