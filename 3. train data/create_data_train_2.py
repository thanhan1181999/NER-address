# ta sẽ tạo câu train bằng cách: với mỗi địa chỉ xã,huyện,tỉnh 
# ta sẽ chọn 1 mẫu câu train, trong mẫu câu đó, chọn tiếp tục obj... tương ứng

import numpy as np
import random
# read file

class ProcessData:
  def __init__(self):
    #this is a result
    self.tokens = []
    self.tags = []
    # this is a data obj, fullobj, pre, location from txt file
    self.obj_tokens, self.obj_tags, self.obj_len = self.read_data("../2. token each data/obj.txt")
    self.pre_tokens, self.pre_tags, self.pre_len = self.read_data("../2. token each data/pre.txt")
    self.location_tokens, self.location_tags, self.location_len = self.read_data("../2. token each data/location.txt")
    # self.special_tokens, self.special_tags, self.special_len = self.read_data("../3. token each data/location_special.txt")
    #form sentence
    self.FORM_SENTENCE_TOKENS = [
      # basic 
      # ["LOCATION"],
      # form define
      ["OBJ","PRE","LOCATION"],
      # form 1
      ["tìm","OBJ","PRE","LOCATION"],
      ["tìm","cho","tôi","OBJ","PRE","LOCATION"],
      ["tìm","các","OBJ","PRE","LOCATION"],
      ["tìm","cho","tôi","các","OBJ","PRE","LOCATION"],
      # form 1.1 repalce tim by tim_kiem
      ["tìm_kiếm","OBJ","PRE","LOCATION"],
      ["tìm_kiếm","cho","tôi","OBJ","PRE","LOCATION"],
      ["tìm_kiếm","các","OBJ","PRE","LOCATION"],
      ["tìm_kiếm","cho","tôi","các","OBJ","PRE","LOCATION"],
      # form 1.2 repalce tim by liệt_kê
      ["liệt_kê","cho","tôi","OBJ","PRE","LOCATION"],
      ["liệt_kê","các","OBJ","PRE","LOCATION"],
      ["liệt_kê","cho","tôi","các","OBJ","PRE","LOCATION"],
      # some other form
      ["PRE","LOCATION", "có", "OBJ", "nào", "không","?"],
      ["không_biết","PRE","LOCATION", "có","OBJ","nào","không?"],
      ["có","OBJ","nào","PRE","LOCATION","không"],
    ]
    self.FORM_SENTENCE_TAGS = [
      # basic 
      # ["LOCATION"],
      # form
      ["OBJ","PRE","LOCATION"],
      # form 1
      ["UNKNOW","OBJ","PRE","LOCATION"],
      ["UNKNOW","UNKNOW","UNKNOW","OBJ","PRE","LOCATION"],
      ["UNKNOW","UNKNOW","OBJ","PRE","LOCATION"],
      ["UNKNOW","UNKNOW","UNKNOW","UNKNOW","OBJ","PRE","LOCATION"],
      # form 1.1
      ["UNKNOW","OBJ","PRE","LOCATION"],
      ["UNKNOW","UNKNOW","UNKNOW","OBJ","PRE","LOCATION"],
      ["UNKNOW","UNKNOW","OBJ","PRE","LOCATION"],
      ["UNKNOW","UNKNOW","UNKNOW","UNKNOW","OBJ","PRE","LOCATION"],
      # form 1.2 
      ["UNKNOW","UNKNOW","UNKNOW","OBJ","PRE","LOCATION"],
      ["UNKNOW","UNKNOW","OBJ","PRE","LOCATION"],
      ["UNKNOW","UNKNOW","UNKNOW","UNKNOW","OBJ","PRE","LOCATION"],
      # some other form
      ["PRE","LOCATION", "UNKNOW", "OBJ", "UNKNOW", "UNKNOW","UNKNOW"],
      ["UNKNOW","PRE","LOCATION", "UNKNOW","OBJ","UNKNOW","UNKNOW"],
      ["UNKNOW","OBJ","UNKNOW","PRE","LOCATION","UNKNOW"],
    ]
    self.FORM_SENTENCE_LEN = len(self.FORM_SENTENCE_TOKENS)
    self.index_of_arr_obj = -1
    self.index_of_arr_pre = -1
    self.index_of_arr_form = -1
    self.index_of_arr_location = -1

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
  
  # ham nay thay 1 form ra thanh 1 cau cu the ( co ca tokens va tags )
  def change_tag_to_real_text(self,form_token,form_tag):
    # thay location truoc
    if "LOCATION" in form_token:
      index = form_token.index("LOCATION")
      self.index_of_arr_location = (self.index_of_arr_location+1)%self.location_len
      form_token.remove("LOCATION")
      form_tag.remove("LOCATION")
      form_token[index:0] = self.location_tokens[self.index_of_arr_location]
      form_tag[index:0] =  self.location_tags[self.index_of_arr_location]
    # thay cac thanh phan con lai
    # co vi tri, thay form_token[vi tri do] = doi tuong khac
    if "OBJ" in form_token:
      index = form_token.index("OBJ")
      self.index_of_arr_obj = (self.index_of_arr_obj+1)%self.obj_len
      form_token.remove("OBJ")
      form_tag.remove("OBJ")
      form_token[index:0] = self.obj_tokens[self.index_of_arr_obj]
      form_tag[index:0] =  self.obj_tags[self.index_of_arr_obj]
    if "PRE" in form_token:
      index = form_token.index("PRE")
      self.index_of_arr_pre = (self.index_of_arr_pre+1)%self.pre_len
      form_token.remove("PRE")
      form_tag.remove("PRE")
      form_token[index:0] = self.pre_tokens[self.index_of_arr_pre]
      form_tag[index:0] =  self.pre_tags[self.index_of_arr_pre]
    return form_token,form_tag

  # ham nay thay 1 form ra thanh 1 cau cu the ( co ca tokens va tags )
  # def change_tag_to_real_text_special(self,form_token,form_tag):
  #   # thay location truoc
  #   if "LOCATION" in form_token:
  #     index = form_token.index("LOCATION")
  #     self.index_of_arr_location = (self.index_of_arr_location+1)%self.special_len
  #     form_token.remove("LOCATION")
  #     form_tag.remove("LOCATION")
  #     form_token[index:0] = self.special_tokens[self.index_of_arr_location]
  #     form_tag[index:0] =  self.special_tags[self.index_of_arr_location]
  #   # thay cac thanh phan con lai
  #   # co vi tri, thay form_token[vi tri do] = doi tuong khac
  #   if "OBJ" in form_token:
  #     index = form_token.index("OBJ")
  #     self.index_of_arr_obj = (self.index_of_arr_obj+1)%self.obj_len
  #     form_token.remove("OBJ")
  #     form_tag.remove("OBJ")
  #     form_token[index:0] = self.obj_tokens[self.index_of_arr_obj]
  #     form_tag[index:0] =  self.obj_tags[self.index_of_arr_obj]
  #   if "PRE" in form_token:
  #     index = form_token.index("PRE")
  #     self.index_of_arr_pre = (self.index_of_arr_pre+1)%self.pre_len
  #     form_token.remove("PRE")
  #     form_tag.remove("PRE")
  #     form_token[index:0] = self.pre_tokens[self.index_of_arr_pre]
  #     form_tag[index:0] =  self.pre_tags[self.index_of_arr_pre]
  #   return form_token,form_tag

  def create_tokens_and_tags_of_sentence(self):
    # for i in range(len(self.obj_tokens)):
    #   self.index_of_arr_form = (self.index_of_arr_form+1)%self.FORM_SENTENCE_LEN
    #   form_token = self.FORM_SENTENCE_TOKENS[self.index_of_arr_form].copy()
    #   form_tag   = self.FORM_SENTENCE_TAGS[self.index_of_arr_form].copy()
    #   print("doing sentence {i}".format(i=i))
    #   token, tag = self.change_tag_to_real_text_special(form_token,form_tag)
    #   self.tokens.append(token)
    #   self.tags.append(tag)

    for i in range(len(self.location_tokens)):
      self.index_of_arr_form = (self.index_of_arr_form+1)%self.FORM_SENTENCE_LEN
      form_token = self.FORM_SENTENCE_TOKENS[self.index_of_arr_form].copy()
      form_tag   = self.FORM_SENTENCE_TAGS[self.index_of_arr_form].copy()
      print("doing sentence {i}".format(i=i))
      token, tag = self.change_tag_to_real_text(form_token,form_tag)
      self.tokens.append(token)
      self.tags.append(tag)
  #============== print to file =============================
  def export(self):
    # lưu dữ liệu train với các câu tìm kiếm có form từ location
    train_dataset = open("2_data_train_location_form.txt","a",encoding='utf8')
    train_dataset_no_tag = open("2_data_train_no_tag_location_form.txt","a",encoding='utf8')
    for i in range(len(self.tokens)):
      sentence_token = self.tokens[i]
      sentence_tag   = self.tags[i]
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
    len_sen = len(self.tokens)
    print("Có {} location".format(len(self.location_tokens)))
    print("Có {} obj".format(self.obj_len))
    print("location_form có {len_sen} sentence".format(len_sen=len_sen))

my_process_data  = ProcessData()

my_process_data.create_tokens_and_tags_of_sentence()

my_process_data.export()

