# concate câu truy vấn
print("đang tổng hợp câu truy vấn...")
def read_cautruyvan(file_path):
  sens = []
  for line in open(file_path, encoding='utf-8'):
    line = line.replace("\n","")
    sens.append(line.lower())  
  return sens

cautruyvan_1 = read_cautruyvan("1_cautruyvan.txt")
cautruyvan_2 = read_cautruyvan("2_cautruyvan.txt")
cautruyvan_3 = read_cautruyvan("3_cautruyvan.txt")
cautruyvan = []
cautruyvan.extend(cautruyvan_1)
cautruyvan.extend(cautruyvan_2)
cautruyvan.extend(cautruyvan_3)

cautruyvan_file = open("cautruyvan.txt","a",encoding='utf8')
for j in range(len(cautruyvan)):
  cautruyvan_file.write(str(cautruyvan[j]))
  cautruyvan_file.write('\n')
cautruyvan_file.close()

print("có {} câu truy vấn".format(len(cautruyvan)))

# concate cau truy vấn token (giống concate câu truy vấn)
print("đang tổng hợp câu truy vấn đã token...")

cautruyvan_token_1 = read_cautruyvan("1_cautruyvan_token.txt")
cautruyvan_token_2 = read_cautruyvan("2_cautruyvan_token.txt")
cautruyvan_token_3 = read_cautruyvan("3_cautruyvan_token.txt")
cautruyvan_token = []
cautruyvan_token.extend(cautruyvan_token_1)
cautruyvan_token.extend(cautruyvan_token_2)
cautruyvan_token.extend(cautruyvan_token_3)

cautruyvan_token_file = open("cautruyvan_token.txt","a",encoding='utf8')
for j in range(len(cautruyvan_token)):
  cautruyvan_token_file.write(str(cautruyvan_token[j]))
  cautruyvan_token_file.write('\n')
cautruyvan_token_file.close()

print("có {} câu truy vấn".format(len(cautruyvan_token)))
# concate data train 1 2 3=============================================================
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

data_train_1_tokens, data_train_1_tags, data_train_1_len  = read_data("1_data_train_location_ner_form.txt")
data_train_2_tokens, data_train_2_tags, data_train_2_len = read_data("2_data_train_location_form.txt")
data_train_3_tokens, data_train_3_tags, data_train_3_len = read_data("3_data_train_location.txt")
data_train_tokens = []
data_train_tokens.extend(data_train_1_tokens)
data_train_tokens.extend(data_train_2_tokens)
data_train_tokens.extend(data_train_3_tokens)
data_train_tags = []
data_train_tags.extend(data_train_1_tags)
data_train_tags.extend(data_train_2_tags)
data_train_tags.extend(data_train_3_tags)
data_train_len = data_train_1_len + data_train_2_len + data_train_3_len

train_dataset = open("data_train.txt","a",encoding='utf8')
train_dataset_no_tag = open("data_train_no_tag.txt","a",encoding='utf8')
for i in range(len(data_train_tokens)):
  sentence_token = data_train_tokens[i]
  sentence_tag   = data_train_tags[i]
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
len_sen = len(data_train_tokens)
print("Có {} câu tìm kiếm".format(len(data_train_tokens)))












# def read_data(self,file_path):
#   tokens = []
#   tags = []
#   tweet_tokens = []
#   tweet_tags = []
#   for line in open(file_path, encoding='utf-8'):
#     line = line.strip()
#     if not line:
#       if tweet_tokens:
#         tokens.append(tweet_tokens)
#         tags.append(tweet_tags)
#         tweet_tokens = []
#         tweet_tags = []
#     else:
#         token, tag = line.split() # Replace all urls with token
#         tweet_tokens.append(token)
#         tweet_tags.append(tag)        
#   return tokens, tags, len(tokens)