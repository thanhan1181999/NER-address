from vncorenlp import VnCoreNLP
annotator = VnCoreNLP("../VnCoreNLP-1.1.1.jar", annotators="wseg", max_heap_size='-Xmx500m')

def read_cautruyvan(file_path):
  sens = []
  for line in open(file_path, encoding='utf-8'):
    line = line.replace("\n","")
    sens.append(line.lower())  
  return sens

cautruyvan = read_cautruyvan("../4. train data/test/cautruyvan.txt")

data_no_tag_new = "../6. train model/data_no_tag_pre.txt"

sens_tokend = []
for sen in cautruyvan:
  sen_tokend = annotator.tokenize(sen)[0]
  sens_tokend.append(sen_tokend)

print("saving to txt file ...")
dataset = open(data_no_tag_new,"a",encoding='utf8')
for i in range(len(sens_tokend)):
  for j in range(len(sens_tokend[i])):
    dataset.write(str(sens_tokend[i][j]))
    dataset.write('\n')
  dataset.write('\n')
dataset.close()

# so sánh kết quả tách bộ test của bộ tách mới và kết quả tách có sẵn
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
sens_tokend_true = read_data("../4. train data/test/data_no_tag.txt")

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

print("number_of_sens_has_diff_length "+ str(number_of_sens_has_diff_length))
print("number_of_sens_true "+ str(number_of_sens_true))
print("number_of_sens_has_same_length_but_false "+ str(number_of_sens_has_same_length_but_false))
ti_le = round(100*number_of_sens_true/(number_of_sens_true+number_of_sens_has_diff_length+number_of_sens_has_same_length_but_false),2)
print("tỉ lệ số câu tách chính xác/ số câu tách sai : {}".format(ti_le) )