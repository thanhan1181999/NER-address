import numpy as np
import codecs
def read_data(input_file):
    with codecs.open(input_file, 'r', 'utf-8') as f:
        word_list = [] 
        words = []
        for line in f:
            line = line.split()
            if len(line) > 0:
                words.extend( line )
            else:
                word_list.append(words)
                words = []
    return word_list

def read_sentence(input_file):
    with codecs.open(input_file, 'r', 'utf-8') as f:
        word_list = [] 
        for line in f:
            word_list.append(line)
    return word_list

query_sentence = read_sentence("3_cautruyvan.txt")

from vncorenlp import VnCoreNLP
annotator = VnCoreNLP("../VnCoreNLP-1.1.1.jar", annotators="wseg", max_heap_size='-Xmx500m')

word_list_use_model_seg = []
for sen in query_sentence:
  a = annotator.tokenize(sen)[0]
  word_list_use_model_seg.append(a)

word_list_primary = read_data("3_cautruyvan_token.txt")
# word_list_use_model_seg = read_data("3_cautruyvan.txt.WSeg")

length = len(word_list_primary)

number_sen_token_fail = 0
number_sen_token_true = 0

false_index = []
for index in range(length):
  words = word_list_primary[index]
  words_real = word_list_use_model_seg[index]
  if len(words)!=len(words_real):
    number_sen_token_fail+=1
    false_index.append(index)
  else:
    dem=0
    for idx in range(len(words)):
      if words[idx]!=words_real[idx]:
        dem+=1
        break
    if dem>0:
      number_sen_token_fail+=1
      false_index.append(index)
    else:
      number_sen_token_true+=1


print(length)
print("fail : {}".format(number_sen_token_fail))
print("true : {}".format(number_sen_token_true))

for idx in false_index:
  words = word_list_primary[index]
  words_real = word_list_use_model_seg[index]
  word_list_primary[idx] = list(words-words_real)
  word_list_use_model_seg[idx] = list(words_real-words)


tenduong = open("check_token.txt","a",encoding='utf8')

for idx in false_index:
  words = word_list_primary[index]
  words_real = word_list_use_model_seg[index]
  for word in words:
    tenduong.write(word)
    tenduong.write(" ")
    tenduong.write('\n')
  tenduong.write('------')
  tenduong.write('\n')
  for word_real in words_real:
    tenduong.write(word_real)
    tenduong.write(" ")
    tenduong.write('\n')
  tenduong.write('\n')

tenduong.close()