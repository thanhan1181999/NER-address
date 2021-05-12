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

word_list_3 = read_data("3_data_train_no_tag_location.txt")
word_list_2 = read_data("2_data_train_no_tag_location_form.txt")
word_list_1 = read_data("1_data_train_no_tag_location_ner_form.txt")
outfile_3_1 = "3_cautruyvan_token.txt"
outfile_3_2 = "3_cautruyvan.txt"
outfile_2_1 = "2_cautruyvan_token.txt"
outfile_2_2 = "2_cautruyvan.txt"
outfile_1_1 = "1_cautruyvan_token.txt"
outfile_1_2 = "1_cautruyvan.txt"

# dữ liệu train 3=======================================
# câu sau khi token=======
sentences_token = []
for sentence in word_list_3:
  sen=" ".join(sentence)
  sentences_token.append(sen)

tenduong = open(outfile_3_1,"a",encoding='utf8')
for e in sentences_token:
  tenduong.write(e)
  tenduong.write('\n')
tenduong.close()
#câu thực tế=========
sentences = []
for sentence in word_list_3:
  for idx in range(len(sentence)):
    sentence[idx] = ' '.join( sentence[idx].split('_') )
  sen = " ".join(sentence)
  sentences.append(sen)

tenduong = open(outfile_3_2,"a",encoding='utf8')
for e in sentences:
  tenduong.write(e)
  tenduong.write('\n')
tenduong.close()



# dữ liệu train 2=======================================
# câu sau khi token=======
sentences_token = []
for sentence in word_list_2:
  sen=" ".join(sentence)
  sentences_token.append(sen)

tenduong = open(outfile_2_1,"a",encoding='utf8')
for e in sentences_token:
  tenduong.write(e)
  tenduong.write('\n')
tenduong.close()
#câu thực tế=========
sentences = []
for sentence in word_list_2:
  for idx in range(len(sentence)):
    sentence[idx] = ' '.join( sentence[idx].split('_') )
  sen = " ".join(sentence)
  sentences.append(sen)

tenduong = open(outfile_2_2,"a",encoding='utf8')
for e in sentences:
  tenduong.write(e)
  tenduong.write('\n')
tenduong.close()


# dữ liệu train 1=======================================
# câu sau khi token=======
sentences_token = []
for sentence in word_list_1:
  sen=" ".join(sentence)
  sentences_token.append(sen)

tenduong = open(outfile_1_1,"a",encoding='utf8')
for e in sentences_token:
  tenduong.write(e)
  tenduong.write('\n')
tenduong.close()
#câu thực tế=========
sentences = []
for sentence in word_list_1:
  for idx in range(len(sentence)):
    sentence[idx] = ' '.join( sentence[idx].split('_') )
  sen = " ".join(sentence)
  sentences.append(sen)

tenduong = open(outfile_1_2,"a",encoding='utf8')
for e in sentences:
  tenduong.write(e)
  tenduong.write('\n')
tenduong.close()
#=================================================================================================== 
# from vncorenlp import VnCoreNLP
# annotator = VnCoreNLP("../VnCoreNLP-1.1.1.jar", annotators="wseg", max_heap_size='-Xmx500m')

# word_list_real = []
# for sen in sentences:
#   a = annotator.tokenize(sen)[0]
#   word_list_real.append(a)

# length = len(word_list)

# number_sen_token_fail = 0
# number_sen_token_true = 0

# false_index = []
# for index in range(length):
#   words = word_list[index]
#   words_real = word_list_real[index]
#   if len(words)!=len(words_real):
#     number_sen_token_fail+=1
#     false_index.append(index)
#   else:
#     dem=0
#     for idx in range(len(words)):
#       if words[idx]!=words_real[idx]:
#         dem+=1
#         break
#     if dem>0:
#       number_sen_token_fail+=1
#       false_index.append(index)
#     else:
#       number_sen_token_true+=1


# print(length)
# print("fail : {}".format(number_sen_token_fail))
# print("true : {}".format(number_sen_token_true))

# for idx in false_index:
#   words = set(word_list[idx])
#   words_real = set(word_list_real[idx])
#   word_list[idx] = list(words-words_real)
#   word_list_real[idx] = list(words_real-words)


# tenduong = open("check_token.txt","a",encoding='utf8')

# for idx in false_index:
#   words = word_list[idx]
#   words_real = word_list_real[idx]
#   for word in words:
#     tenduong.write(word)
#     tenduong.write(" ")
#     tenduong.write('\n')
#   tenduong.write('------')
#   tenduong.write('\n')
#   for word_real in words_real:
#     tenduong.write(word_real)
#     tenduong.write(" ")
#     tenduong.write('\n')
#   tenduong.write('\n')

# tenduong.close()




