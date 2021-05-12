# lưu file location

import numpy as np
import random
# read file

class ProcessData:
  def __init__(self):
    self.location_tokens, self.location_tags, self.location_len = self.read_data("../3. token each data/location.txt")

  #read file
  def read_data(self,file_path):
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
  #============== print to file =============================
  def export(self):
    # lưu dữ liệu train với các câu tìm kiếm có form từ location
    train_dataset = open("3_data_train_location.txt","a",encoding='utf8')
    train_dataset_no_tag = open("3_data_train_no_tag_location.txt","a",encoding='utf8')
    for i in range(len(self.location_tokens)):
      sentence_token = self.location_tokens[i]
      sentence_tag   = self.location_tags[i]
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
    len_sen = len(self.location_tokens)
    print("Có {} location".format(len(self.location_tokens)))
    print("location_form có {len_sen} sentence".format(len_sen=len_sen))

my_process_data  = ProcessData()

my_process_data.export()

