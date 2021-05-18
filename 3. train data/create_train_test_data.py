from sklearn.model_selection import train_test_split
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
data_1_tokens, data_1_tags, data_1_len  = read_data("1_data_train_location_ner_form.txt")
data_2_tokens, data_2_tags, data_2_len = read_data("2_data_train_location_form.txt")
data_3_tokens, data_3_tags, data_3_len = read_data("3_data_train_location.txt")

data_1_tokens = data_1_tokens[0:1499]
data_2_tokens = data_2_tokens[0:1499]
data_3_tokens = data_3_tokens[0:1499]
data_1_tags = data_1_tags[0:1499]
data_2_tags = data_2_tags[0:1499]
data_3_tags = data_3_tags[0:1499]
cautruyvan_1 = read_cautruyvan("1_cautruyvan.txt")[0:1499]
cautruyvan_2 = read_cautruyvan("2_cautruyvan.txt")[0:1499]
cautruyvan_3 = read_cautruyvan("3_cautruyvan.txt")[0:1499]

cautruyvan_token_1 = read_cautruyvan("1_cautruyvan_token.txt")[0:1499]
cautruyvan_token_2 = read_cautruyvan("2_cautruyvan_token.txt")[0:1499]
cautruyvan_token_3 = read_cautruyvan("3_cautruyvan_token.txt")[0:1499]
# chia data==========================================
print("đang chia data...")
size_test = 0.2
cautruyvan_1_rest, cautruyvan_1_test, cautruyvan_token_1_rest, cautruyvan_token_1_test, data_1_tokens_rest, data_1_tokens_test, data_1_tags_rest, data_1_tags_test   = train_test_split(cautruyvan_1, cautruyvan_token_1, data_1_tokens, data_1_tags, test_size=size_test)
cautruyvan_2_rest, cautruyvan_2_test, cautruyvan_token_2_rest, cautruyvan_token_2_test, data_2_tokens_rest, data_2_tokens_test, data_2_tags_rest, data_2_tags_test   = train_test_split(cautruyvan_2, cautruyvan_token_2, data_2_tokens, data_2_tags, test_size=size_test)
cautruyvan_3_rest, cautruyvan_3_test, cautruyvan_token_3_rest, cautruyvan_token_3_test, data_3_tokens_rest, data_3_tokens_test, data_3_tags_rest, data_3_tags_test   = train_test_split(cautruyvan_3, cautruyvan_token_3, data_3_tokens, data_3_tags, test_size=size_test)
size_validate = 0.125
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
print("đang ghi data...")
# train
# cautruyvan
cautruyvan_file = open("train/cautruyvan.txt","a",encoding='utf8')
for j in range(len(cautruyvan_train)):
  cautruyvan_file.write(str(cautruyvan_train[j]))
  cautruyvan_file.write('\n')
cautruyvan_file.close()

cautruyvan_file = open("val/cautruyvan.txt","a",encoding='utf8')
for j in range(len(cautruyvan_val)):
  cautruyvan_file.write(str(cautruyvan_val[j]))
  cautruyvan_file.write('\n')
cautruyvan_file.close()

cautruyvan_file = open("test/cautruyvan.txt","a",encoding='utf8')
for j in range(len(cautruyvan_test)):
  cautruyvan_file.write(str(cautruyvan_test[j]))
  cautruyvan_file.write('\n')
cautruyvan_file.close()

print("Có {} câu tìm kiếm train".format(len(cautruyvan_train)))
print("Có {} câu tìm kiếm val".format(len(cautruyvan_val)))
print("Có {} câu tìm kiếm test".format(len(cautruyvan_test)))

# câu truy vấn token
cautruyvan_token_file = open("train/cautruyvan_token.txt","a",encoding='utf8')
for j in range(len(cautruyvan_token_train)):
  cautruyvan_token_file.write(str(cautruyvan_token_train[j]))
  cautruyvan_token_file.write('\n')
cautruyvan_token_file.close()

cautruyvan_token_file = open("val/cautruyvan_token.txt","a",encoding='utf8')
for j in range(len(cautruyvan_token_val)):
  cautruyvan_token_file.write(str(cautruyvan_token_val[j]))
  cautruyvan_token_file.write('\n')
cautruyvan_token_file.close()

cautruyvan_token_file = open("test/cautruyvan_token.txt","a",encoding='utf8')
for j in range(len(cautruyvan_token_test)):
  cautruyvan_token_file.write(str(cautruyvan_token_test[j]))
  cautruyvan_token_file.write('\n')
cautruyvan_token_file.close()

print("Có {} câu tìm kiếm đã token train".format(len(cautruyvan_token_train)))
print("Có {} câu tìm kiếm đã token val".format(len(cautruyvan_token_val)))
print("Có {} câu tìm kiếm đã token test".format(len(cautruyvan_token_test)))

# câu truy vấn đã gán nhãn
train_dataset = open("train/data.txt","a",encoding='utf8')
train_dataset_no_tag = open("train/data_no_tag.txt","a",encoding='utf8')
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

train_dataset = open("val/data.txt","a",encoding='utf8')
train_dataset_no_tag = open("val/data_no_tag.txt","a",encoding='utf8')
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

train_dataset = open("test/data.txt","a",encoding='utf8')
train_dataset_no_tag = open("test/data_no_tag.txt","a",encoding='utf8')
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

print("Có {} câu tìm kiếm gán nhãn để train".format(len(data_tokens_train)))
print("Có {} câu tìm kiếm gán nhãn để val".format(len(data_tokens_val)))
print("Có {} câu tìm kiếm gán nhãn để test".format(len(data_tokens_test)))