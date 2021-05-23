from sklearn.model_selection import train_test_split
import os
# dirName = 'tempDir'
# try:
#     # Create target Directory
#     os.mkdir(dirName)
#     print("Directory " , dirName ,  " Created ") 
# except FileExistsError:
#     print("Directory " , dirName ,  " already exists")

# import math
# len = 20000
# max_sen = 3500 # số câu nhiều nhất có thể load cho mỗi lần train (vì có 12GB RAM)

# arr = []
# for index in range(math.ceil(len/max_sen)):
#   begin = index*max_sen
#   end = min(index*max_sen+max_sen,len)
#   arr.append([begin, end])

# print(arr)

# các hàm đọc data===================================
def read_cautruyvan(file_path):
  sens = []
  for line in open(file_path, encoding='utf-8'):
    line = line.replace("\n","")
    sens.append(line.lower())  
  return sens

def read_data(file_path):
  tokens = []
  tags = []
  tweet_tokens = []
  tweet_tags = []
  for line in open(file_path, encoding='utf-8'):
    line = line.strip()
    if not line:
      if tweet_tokens:
        tokens.append(tweet_tokens)
        tags.append(tweet_tags)
        tweet_tokens = []
        tweet_tags = []
    else:
        token, tag = line.split() # Replace all urls with token
        tweet_tokens.append(token)
        tweet_tags.append(tag)        
  return tokens, tags, len(tokens)
# đọc data===========================================
print("đang đọc data...")
data_1_tokens, data_1_tags, data_1_len  = read_data("all data/1_data_train_location_ner_form.txt")
data_2_tokens, data_2_tags, data_2_len = read_data("all data/2_data_train_location_form.txt")
data_3_tokens, data_3_tags, data_3_len = read_data("all data/3_data_train_location.txt")
print(data_1_len)
print(data_2_len)
print(data_3_len)
cautruyvan_1 = read_cautruyvan("all data/1_cautruyvan.txt")
cautruyvan_2 = read_cautruyvan("all data/2_cautruyvan.txt")
cautruyvan_3 = read_cautruyvan("all data/3_cautruyvan.txt")

cautruyvan_token_1 = read_cautruyvan("all data/1_cautruyvan_token.txt")
cautruyvan_token_2 = read_cautruyvan("all data/2_cautruyvan_token.txt")
cautruyvan_token_3 = read_cautruyvan("all data/3_cautruyvan_token.txt")
size_test = 0.2
size_validate = 0.125

# tạo thư mục chứa dữ liệu train
import math
length = min(data_1_len,data_2_len)
max_sen = 1500 # số câu nhiều nhất có thể load cho mỗi lần train là 1500 * 3 (vì có 12GB RAM)

arr = []
for index in range(math.ceil(length/max_sen)):
  begin = index*max_sen
  end = min(index*max_sen+max_sen,length)
  arr.append([begin, end])
print(arr)

for index in range(math.ceil(length/max_sen)):
  dirName = "split data/data_{}".format(index)
  try:
    # Create target Directory
    os.mkdir(dirName)
    os.mkdir(dirName + str("/train"))
    os.mkdir(dirName + str("/test"))
    os.mkdir(dirName + str("/val"))
  except FileExistsError:
    print("Directory " , dirName ,  " already exists")

def split_each_data(index):
  global data_1_tokens
  global data_2_tokens
  global data_3_tokens

  global data_1_tags
  global data_2_tags
  global data_3_tags

  global cautruyvan_1
  global cautruyvan_2
  global cautruyvan_3

  global cautruyvan_token_1
  global cautruyvan_token_2
  global cautruyvan_token_3

  global size_validate
  global size_test

  global arr
  global length
  global max_sen

  begin = arr[index][0]
  end = arr[index][1]
  
  print("data {}".format(index))
  print("  {}".format(begin))
  print("  {}".format(end))

  data_2_tokens_x = data_2_tokens[begin:end]
  data_3_tokens_x = data_3_tokens[begin:end]

  data_2_tags_x = data_2_tags[begin:end]
  data_3_tags_x = data_3_tags[begin:end]
  
  cautruyvan_2_x = cautruyvan_2[begin:end]
  cautruyvan_3_x = cautruyvan_3[begin:end]

  cautruyvan_token_2_x = cautruyvan_token_2[begin:end]
  cautruyvan_token_3_x = cautruyvan_token_3[begin:end]

  if index==math.ceil(length/max_sen):
    cautruyvan_token_1_x = cautruyvan_token_1[begin:]
    cautruyvan_1_x = cautruyvan_1[begin:]
    data_1_tokens_x = data_1_tokens[begin:]
    data_1_tags_x = data_1_tags[begin:]
  else:
    cautruyvan_token_1_x = cautruyvan_token_1[begin:end]
    cautruyvan_1_x = cautruyvan_1[begin:end]
    data_1_tokens_x = data_1_tokens[begin:end]
    data_1_tags_x = data_1_tags[begin:end]

  # print(len(cautruyvan_token_1))
  # print(len(cautruyvan_1))
  # print(len(data_1_tokens))
  # print(len(data_1_tokens))

  # print(len(cautruyvan_token_2))
  # print(len(cautruyvan_2))
  # print(len(data_2_tokens))
  # print(len(data_2_tokens))

  # print(len(cautruyvan_token_2))
  # print(len(cautruyvan_2))
  # print(len(data_2_tokens))
  # print(len(data_2_tokens))

  # chia data==========================================
  print("  đang chia data...")

  cautruyvan_1_rest, cautruyvan_1_test, cautruyvan_token_1_rest, cautruyvan_token_1_test, data_1_tokens_rest, data_1_tokens_test, data_1_tags_rest, data_1_tags_test   = train_test_split(cautruyvan_1_x, cautruyvan_token_1_x, data_1_tokens_x, data_1_tags_x, test_size=size_test)
  cautruyvan_2_rest, cautruyvan_2_test, cautruyvan_token_2_rest, cautruyvan_token_2_test, data_2_tokens_rest, data_2_tokens_test, data_2_tags_rest, data_2_tags_test   = train_test_split(cautruyvan_2_x, cautruyvan_token_2_x, data_2_tokens_x, data_2_tags_x, test_size=size_test)
  cautruyvan_3_rest, cautruyvan_3_test, cautruyvan_token_3_rest, cautruyvan_token_3_test, data_3_tokens_rest, data_3_tokens_test, data_3_tags_rest, data_3_tags_test   = train_test_split(cautruyvan_3_x, cautruyvan_token_3_x, data_3_tokens_x, data_3_tags_x, test_size=size_test)

  cautruyvan_1_train, cautruyvan_1_val, cautruyvan_token_1_train, cautruyvan_token_1_val, data_1_tokens_train, data_1_tokens_val, data_1_tags_train, data_1_tags_val   = train_test_split(cautruyvan_1_rest, cautruyvan_token_1_rest, data_1_tokens_rest, data_1_tags_rest, test_size=size_validate)
  cautruyvan_2_train, cautruyvan_2_val, cautruyvan_token_2_train, cautruyvan_token_2_val, data_2_tokens_train, data_2_tokens_val, data_2_tags_train, data_2_tags_val   = train_test_split(cautruyvan_2_rest, cautruyvan_token_2_rest, data_2_tokens_rest, data_2_tags_rest, test_size=size_validate)
  cautruyvan_3_train, cautruyvan_3_val, cautruyvan_token_3_train, cautruyvan_token_3_val, data_3_tokens_train, data_3_tokens_val, data_3_tags_train, data_3_tags_val   = train_test_split(cautruyvan_3_rest, cautruyvan_token_3_rest, data_3_tokens_rest, data_3_tags_rest, test_size=size_validate)
  #~~~~~~~~~~~~~~~
  cautruyvan_train = []
  cautruyvan_train.extend(cautruyvan_1_train)
  cautruyvan_train.extend(cautruyvan_2_train)
  cautruyvan_train.extend(cautruyvan_3_train)
  cautruyvan_val = []
  cautruyvan_val.extend(cautruyvan_1_val)
  cautruyvan_val.extend(cautruyvan_2_val)
  cautruyvan_val.extend(cautruyvan_3_val)
  cautruyvan_test = []
  cautruyvan_test.extend(cautruyvan_1_test)
  cautruyvan_test.extend(cautruyvan_2_test)
  cautruyvan_test.extend(cautruyvan_3_test)
  #~~~~~~~~~~~~~~~
  cautruyvan_token_train = []
  cautruyvan_token_train.extend(cautruyvan_token_1_train)
  cautruyvan_token_train.extend(cautruyvan_token_2_train)
  cautruyvan_token_train.extend(cautruyvan_token_3_train)
  cautruyvan_token_val = []
  cautruyvan_token_val.extend(cautruyvan_token_1_val)
  cautruyvan_token_val.extend(cautruyvan_token_2_val)
  cautruyvan_token_val.extend(cautruyvan_token_3_val)
  cautruyvan_token_test = []
  cautruyvan_token_test.extend(cautruyvan_token_1_test)
  cautruyvan_token_test.extend(cautruyvan_token_2_test)
  cautruyvan_token_test.extend(cautruyvan_token_3_test)
  #~~~~~~~~~~~~~~~
  data_tokens_train = []
  data_tokens_train.extend(data_1_tokens_train)
  data_tokens_train.extend(data_2_tokens_train)
  data_tokens_train.extend(data_3_tokens_train)
  data_tokens_val = []
  data_tokens_val.extend(data_1_tokens_val)
  data_tokens_val.extend(data_2_tokens_val)
  data_tokens_val.extend(data_3_tokens_val)
  data_tokens_test = []
  data_tokens_test.extend(data_1_tokens_test)
  data_tokens_test.extend(data_2_tokens_test)
  data_tokens_test.extend(data_3_tokens_test)
  #~~~~~~~~~~~~~~~
  data_tags_train = []
  data_tags_train.extend(data_1_tags_train)
  data_tags_train.extend(data_2_tags_train)
  data_tags_train.extend(data_3_tags_train)
  data_tags_val = []
  data_tags_val.extend(data_1_tags_val)
  data_tags_val.extend(data_2_tags_val)
  data_tags_val.extend(data_3_tags_val)
  data_tags_test = []
  data_tags_test.extend(data_1_tags_test)
  data_tags_test.extend(data_2_tags_test)
  data_tags_test.extend(data_3_tags_test)
  #~~~~~~~~~~~~~~~
  print("  đang ghi data...")
  dirName = "split data/data_{}/".format(index)
  # train
  # cautruyvan
  cautruyvan_file = open(dirName+"train/cautruyvan.txt","a",encoding='utf8')
  for j in range(len(cautruyvan_train)):
    cautruyvan_file.write(str(cautruyvan_train[j]))
    cautruyvan_file.write('\n')
  cautruyvan_file.close()

  cautruyvan_file = open(dirName+"val/cautruyvan.txt","a",encoding='utf8')
  for j in range(len(cautruyvan_val)):
    cautruyvan_file.write(str(cautruyvan_val[j]))
    cautruyvan_file.write('\n')
  cautruyvan_file.close()

  cautruyvan_file = open(dirName+"test/cautruyvan.txt","a",encoding='utf8')
  for j in range(len(cautruyvan_test)):
    cautruyvan_file.write(str(cautruyvan_test[j]))
    cautruyvan_file.write('\n')
  cautruyvan_file.close()

  # print("Có {} câu tìm kiếm train".format(len(cautruyvan_train)))
  # print("Có {} câu tìm kiếm val".format(len(cautruyvan_val)))
  # print("Có {} câu tìm kiếm test".format(len(cautruyvan_test)))

  # câu truy vấn token
  cautruyvan_token_file = open(dirName+"train/cautruyvan_token.txt","a",encoding='utf8')
  for j in range(len(cautruyvan_token_train)):
    cautruyvan_token_train[j] = cautruyvan_token_train[j].replace(" _"," ")
    cautruyvan_token_train[j] = cautruyvan_token_train[j].replace(" _ "," ")
    cautruyvan_token_train[j] = cautruyvan_token_train[j].replace("_ "," ")
    cautruyvan_token_file.write(str(cautruyvan_token_train[j]))
    cautruyvan_token_file.write('\n')
  cautruyvan_token_file.close()

  all_cautruyvan_token_file = open("cautruyvan_token_to_train_RDR.txt","a",encoding='utf8')
  for j in range(len(cautruyvan_token_train)):
    all_cautruyvan_token_file.write(str(cautruyvan_token_train[j]))
    all_cautruyvan_token_file.write('\n')
  all_cautruyvan_token_file.close()

  all_cautruyvan_token_file = open("../RDRsegmenter/train/Train_gold.txt","a",encoding='utf8')
  for j in range(len(cautruyvan_token_train)):
    all_cautruyvan_token_file.write(str(cautruyvan_token_train[j]))
    all_cautruyvan_token_file.write('\n')
  all_cautruyvan_token_file.close()

  cautruyvan_token_file = open(dirName+"val/cautruyvan_token.txt","a",encoding='utf8')
  for j in range(len(cautruyvan_token_val)):
    cautruyvan_token_file.write(str(cautruyvan_token_val[j]))
    cautruyvan_token_file.write('\n')
  cautruyvan_token_file.close()

  cautruyvan_token_file = open(dirName+"test/cautruyvan_token.txt","a",encoding='utf8')
  for j in range(len(cautruyvan_token_test)):
    cautruyvan_token_file.write(str(cautruyvan_token_test[j]))
    cautruyvan_token_file.write('\n')
  cautruyvan_token_file.close()

  # print("Có {} câu tìm kiếm đã token train".format(len(cautruyvan_token_train)))
  # print("Có {} câu tìm kiếm đã token val".format(len(cautruyvan_token_val)))
  # print("Có {} câu tìm kiếm đã token test".format(len(cautruyvan_token_test)))

  # câu truy vấn đã gán nhãn
  train_dataset = open(dirName+"train/data.txt","a",encoding='utf8')
  train_dataset_no_tag = open(dirName+"train/data_no_tag.txt","a",encoding='utf8')
  for i in range(len(data_tokens_train)):
    sentence_token = data_tokens_train[i]
    sentence_tag   = data_tags_train[i]
    for j in range(len(sentence_token)):
      train_dataset.write(str(sentence_token[j]))
      train_dataset_no_tag.write(str(sentence_token[j]))
      train_dataset.write(' ')
      train_dataset.write(str(sentence_tag[j]))
      train_dataset.write('\n')
      train_dataset_no_tag.write('\n')
    train_dataset.write('\n')
    train_dataset_no_tag.write('\n')
  train_dataset.close()
  train_dataset_no_tag.close()
  len_sen = len(data_tokens_train)

  train_dataset = open(dirName+"val/data.txt","a",encoding='utf8')
  train_dataset_no_tag = open(dirName+"val/data_no_tag.txt","a",encoding='utf8')
  for i in range(len(data_tokens_val)):
    sentence_token = data_tokens_val[i]
    sentence_tag   = data_tags_val[i]
    for j in range(len(sentence_token)):
      train_dataset.write(str(sentence_token[j]))
      train_dataset_no_tag.write(str(sentence_token[j]))
      train_dataset.write(' ')
      train_dataset.write(str(sentence_tag[j]))
      train_dataset.write('\n')
      train_dataset_no_tag.write('\n')
    train_dataset.write('\n')
    train_dataset_no_tag.write('\n')
  train_dataset.close()
  train_dataset_no_tag.close()
  len_sen = len(data_tokens_val)

  train_dataset = open(dirName+"test/data.txt","a",encoding='utf8')
  train_dataset_no_tag = open(dirName+"test/data_no_tag.txt","a",encoding='utf8')
  for i in range(len(data_tokens_test)):
    sentence_token = data_tokens_test[i]
    sentence_tag   = data_tags_test[i]
    for j in range(len(sentence_token)):
      train_dataset.write(str(sentence_token[j]))
      train_dataset_no_tag.write(str(sentence_token[j]))
      train_dataset.write(' ')
      train_dataset.write(str(sentence_tag[j]))
      train_dataset.write('\n')
      train_dataset_no_tag.write('\n')
    train_dataset.write('\n')
    train_dataset_no_tag.write('\n')
  train_dataset.close()
  train_dataset_no_tag.close()
  len_sen = len(data_tokens_test)

  # print("Có {} câu tìm kiếm gán nhãn để train".format(len(data_tokens_train)))
  # print("Có {} câu tìm kiếm gán nhãn để val".format(len(data_tokens_val)))
  # print("Có {} câu tìm kiếm gán nhãn để test".format(len(data_tokens_test)))

for index in range(math.ceil(length/max_sen)):
  split_each_data(index)