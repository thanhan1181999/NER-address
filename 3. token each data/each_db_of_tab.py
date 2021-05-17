from vncorenlp import VnCoreNLP
annotator = VnCoreNLP("../VnCoreNLP-1.1.1.jar", annotators="wseg", max_heap_size='-Xmx500m')
#read file=======================================================
import numpy as np
def read_data(file_path):
  arr = []
  for line in open(file_path, encoding='utf-8'):
    arr.append(line.lower())        
  return np.array(arr)
#================================================================
OBJ                 = read_data('../2. primary data/obj.txt')

OBJ_FEATURE         = read_data('../2. primary data/feature.txt')

PRE                 = read_data('../2. primary data/pre.txt')

LOCATION_NER        = read_data('../2. primary data/ner.txt')

LOCATION_SPECIAL    = read_data('../2. primary data/location_special.txt')

link_file_json_of_location = '../2. primary data/caugiay_processed.json'

# một vài hàm cần dùng ===========================================
# hàm trả về token các phần tử trong 1 mảng
def token_input_data(arr):
  tokens = []
  for item in arr:
    a = annotator.tokenize(item)
    if len(a)>0:
      tokens.append(a[0]) #a[0] là mảng chứa các token tách được của 1 phần tử trong array truyền vào
    else:
      tokens.append([""])
  return tokens

# hàm tạo tag cho các TOKEN
# nhận vào đầu ra của hàm token_input_data, và tag của token ví dụ "OBJ","PRE",...
# define parameter
# arr = token_input_data(OBJ)   OBJ la mang OBJ
# str = "OBJ"                   la ten cua tag
def make_tag_from_tokened_data(arr,str):
  tags = []
  for arr_of_token in arr:
    tag    = "{x}".format(x=str)
    if arr_of_token[0]!="": 
      tag  = [tag]*len(arr_of_token)
    else:
      tag  = [""]
    tags.append(tag)
  return tags

# đánh tag mảng obj ko cần token, chỉ cần split rồi nối lại bởi _
# ví dụ: nhà hàng => nhà_hàng
def convert_data(arr):
  result = []
  for e in arr:
    result.append( "_".join(e.split()) )
  return result

#==========================================================================
#obj
print("OBJ doing tokens ang tags")
OBJ_TOKEN = token_input_data(OBJ)
OBJ_TAG   = make_tag_from_tokened_data(OBJ_TOKEN,"OBJ")
# OBJ_TOKEN = convert_data(OBJ)
# OBJ_TAG = ["OBJ"]*len(OBJ)
#obj_feature
print("OBJ_FEATURE doing tokens ang tags")
OBJ_FEATURE_TOKEN = token_input_data(OBJ_FEATURE)
OBJ_FEATURE_TAG   = make_tag_from_tokened_data(OBJ_FEATURE_TOKEN,"OBJ_FEATURE")
#pre
print("PRE doing tokens ang tags")
PRE_TOKEN = token_input_data(PRE)
PRE_TAG   = make_tag_from_tokened_data(PRE_TOKEN,"PRE")
# PRE_TOKEN = convert_data(PRE)
# PRE_TAG = ["PRE"]*len(PRE)
#location special
print("LOCATION_SPECIAL(is LOCATION_NER) doing tokens ang tags")
LOCATION_SPECIAL_TOKEN = token_input_data(LOCATION_SPECIAL)
LOCATION_SPECIAL_TAG   = make_tag_from_tokened_data(LOCATION_SPECIAL_TOKEN,"LOCATION_NER")
# LOCATION_SPECIAL_TOKEN = convert_data(LOCATION_SPECIAL)
# LOCATION_SPECIAL_TAG = ["LOCATION_NER"]*len(LOCATION_SPECIAL)
#location
print("LOCATION doing tokens ang tags")
LOCATION_TOKEN = []
LOCATION_TAG = []
import json
index_sen = 0
with open(link_file_json_of_location) as json_file:
  data = json.load(json_file)
  for p in data['caugiay']: # duyệt từng câu
    index_sen+=1
    print("sentence "+ str(index_sen))
    # khai báo mảng token và tag của 1 câu
    token_of_a_sentence = []
    tag_of_a_sentence = []
    if p['number']!="":
      number_token = annotator.tokenize(p['number'])[0] # day la token cua number
      number_tag   = [str("LOCATION_HOMENUMBER")]*len(number_token)
      token_of_a_sentence.extend(number_token)
      tag_of_a_sentence.extend(number_tag)
    if p['street']!="":
      street_token = annotator.tokenize(p['street'])[0] # day la token cua street
      street_tag   = [str("LOCATION_STREET")]*len(street_token)
      token_of_a_sentence.extend(street_token)
      tag_of_a_sentence.extend(street_tag)
    if p['locality']!="":
      # ward_token = annotator.tokenize(p['locality'])[0] # day la token cua ward
      # ward_tag   = [str("LOCATION_WARD")]*len(ward_token)
      ward_token = ['_'.join( p['locality'].split() )]
      ward_tag   = ["LOCATION_WARD"]
      token_of_a_sentence.extend(ward_token)
      tag_of_a_sentence.extend(ward_tag)
    if p['county']!="":
      # district_token = annotator.tokenize(p['county'])[0] # day la token cua district
      # district_tag   = [str("LOCATION_DISTRICT")]*len(district_token)
      district_token = ['_'.join( p['county'].split() )]
      district_tag   = ["LOCATION_DISTRICT"]
      token_of_a_sentence.extend(district_token)
      tag_of_a_sentence.extend(district_tag)
    if p['region']!="":
      # province_token = annotator.tokenize(p['region'])[0] # day la token cua province
      # province_tag   = [str("LOCATION_PROVINCE")]*len(province_token)
      province_token = ['_'.join( p['region'].split() )]
      province_tag   = ["LOCATION_PROVINCE"]
      token_of_a_sentence.extend(province_token)
      tag_of_a_sentence.extend(province_tag)
    if p['country']!="":
      # country_token = annotator.tokenize(p['country'])[0] # day la token cua country
      # country_tag   = [str("LOCATION_COUNTRY")]*len(country_token)
      country_token = ['_'.join( p['country'].split() )]
      country_tag   = ["LOCATION_COUNTRY"]
      token_of_a_sentence.extend(country_token)
      tag_of_a_sentence.extend(country_tag)
    if p['country']!="" or p['region']!="":
      token_of_a_sentence.append("10000")
      tag_of_a_sentence.append("LOCATION_POSTCODE")
    
    # khi đã có mảng token và tag của 1 địa chỉ hoàn chỉnh, thêm vào mảng lớn
    LOCATION_TOKEN.append(token_of_a_sentence)
    LOCATION_TAG.append(tag_of_a_sentence)

#location ner
print("LOCATION_NER doing tokens ang tags")
from sklearn.model_selection import train_test_split
if len(LOCATION_NER)>len(LOCATION_TOKEN):
  size = round(len(LOCATION_TOKEN)/len(LOCATION_NER),2)
  ner_rest, ner_take = train_test_split(LOCATION_NER, test_size=size)
  LOCATION_NER = ner_take
LOCATION_NER_TOKEN = token_input_data(LOCATION_NER)
LOCATION_NER_TAG   = make_tag_from_tokened_data(LOCATION_NER_TOKEN,"LOCATION_NER")
# LOCATION_NER_TOKEN = convert_data(LOCATION_NER)
# LOCATION_NER_TAG = ["LOCATION_NER"]*len(LOCATION_NER)
LOCATION_NER_TOKEN.extend(LOCATION_SPECIAL_TOKEN)
LOCATION_NER_TAG.extend(LOCATION_SPECIAL_TAG)

#========cong viec tiep theo la noi obj vs obj_feature=====================
FULL_OBJ_TOKEN = []
FULL_OBJ_TAG   = [] 
for a in range(len(OBJ)):
  #voi moi loai nhan LOCATION_ ghep vao theo thu tu
  full_obj = []
  full_obj_tag = []
  for b in range(len(OBJ_TOKEN[a])):
    full_obj.append(OBJ_TOKEN[a][b])
    full_obj_tag.append(OBJ_TAG[a][b])
  # full_obj.append(OBJ_TOKEN[a])
  # full_obj_tag.append(OBJ_TAG[a])
  
  for b in range(len(OBJ_FEATURE_TOKEN[a])):
    full_obj.append(OBJ_FEATURE_TOKEN[a][b])
    full_obj_tag.append(OBJ_FEATURE_TAG[a][b])
  
  FULL_OBJ_TOKEN.append( list(filter(lambda a: a != "", full_obj)) )
  FULL_OBJ_TAG.append( list(filter(lambda a: a != "", full_obj_tag)) )

#========================open and write====================================
print("saving to txt file ...")
dataset = open("obj.txt","a",encoding='utf8')
for i in range(len(FULL_OBJ_TOKEN)):
  for j in range(len(FULL_OBJ_TOKEN[i])):
    dataset.write(str(FULL_OBJ_TOKEN[i][j]))
    dataset.write('\t')
    dataset.write(str(FULL_OBJ_TAG[i][j]))
    dataset.write('\n')
  dataset.write('\n')
dataset.close()

#pre
# chú ý: ta sẽ lấy ngẫu nhiên len(LOCATION_TOKEN) ner 
dataset = open("pre.txt","a",encoding='utf8')
for i in range(len(PRE_TOKEN)):
  for j in range(len(PRE_TOKEN[i])):
    dataset.write(str(PRE_TOKEN[i][j]))
    dataset.write('\t')
    dataset.write(str(PRE_TAG[i][j]))
    dataset.write('\n')
  dataset.write('\n')
# for i in range(len(PRE_TOKEN)):
#   dataset.write(str(PRE_TOKEN[i]))
#   dataset.write('\t')
#   dataset.write(str(PRE_TAG[i]))
#   dataset.write('\n')
#   dataset.write('\n')

dataset.close()

# LOCATION_SPECIAL
# dataset = open("location_special.txt","a",encoding='utf8')
# # for i in range(len(LOCATION_SPECIAL_TOKEN)):
# #   for j in range(len(LOCATION_SPECIAL_TOKEN[i])):
# #     dataset.write(str(LOCATION_SPECIAL_TOKEN[i][j]))
# #     dataset.write('\t')
# #     dataset.write(str(LOCATION_SPECIAL_TAG[i][j]))
# #     dataset.write('\n')
# #   dataset.write('\n')
# for i in range(len(LOCATION_SPECIAL_TOKEN)):
#   dataset.write(str(LOCATION_SPECIAL_TOKEN[i]))
#   dataset.write('\t')
#   dataset.write(str(LOCATION_SPECIAL_TAG[i]))
#   dataset.write('\n')
#   dataset.write('\n')

dataset.close()

# LOCATION_NER
dataset = open("location_ner.txt","a",encoding='utf8')
for i in range(len(LOCATION_NER_TOKEN)):
  for j in range(len(LOCATION_NER_TOKEN[i])):
    dataset.write(str(LOCATION_NER_TOKEN[i][j]))
    dataset.write('\t')
    dataset.write(str(LOCATION_NER_TAG[i][j]))
    dataset.write('\n')
  dataset.write('\n')

# for i in range(len(LOCATION_NER_TOKEN)):
#   dataset.write(str(LOCATION_NER_TOKEN[i]))
#   dataset.write('\t')
#   dataset.write(str(LOCATION_NER_TAG[i]))
#   dataset.write('\n')
#   dataset.write('\n')

dataset.close()

# location homenumber + street + ward + district + province + country + postcode
dataset = open("location.txt","a",encoding='utf8')
for i in range(len(LOCATION_TOKEN)):
  for j in range(len(LOCATION_TOKEN[i])):
    dataset.write(str(LOCATION_TOKEN[i][j]))
    dataset.write('\t')
    dataset.write(str(LOCATION_TAG[i][j]))
    dataset.write('\n')
  dataset.write('\n')
dataset.close()

# location_all là tất cả các location gồm:
#       location(số nhà->postcode)
#       location spicial
for idx in range(len(LOCATION_SPECIAL_TAG)):
  LOCATION_SPECIAL_TAG[idx] = [LOCATION_SPECIAL_TAG[idx]]
for idx in range(len(LOCATION_SPECIAL_TOKEN)):
  LOCATION_SPECIAL_TOKEN[idx] = [LOCATION_SPECIAL_TOKEN[idx]]

# LOCATION_ALL_TAG = []
# LOCATION_ALL_TAG.extend(LOCATION_SPECIAL_TAG)
# LOCATION_ALL_TAG.extend(LOCATION_TAG)
# LOCATION_ALL_TOKEN = []
# LOCATION_ALL_TOKEN.extend(LOCATION_SPECIAL_TOKEN)
# LOCATION_ALL_TOKEN.extend(LOCATION_TOKEN)
# dataset = open("location_all.txt","a",encoding='utf8')
# for i in range(len(LOCATION_ALL_TOKEN)):
#   for j in range(len(LOCATION_ALL_TOKEN[i])):
#     dataset.write(str(LOCATION_ALL_TOKEN[i][j]))
#     dataset.write('\t')
#     dataset.write(str(LOCATION_ALL_TAG[i][j]))
#     dataset.write('\n')
#   dataset.write('\n')
# dataset.close()

print('\n')
print("Có {} obj.".format(len(OBJ)))
print("Có {} pre.".format(len(PRE)))
print("Có {} ner.".format(len(LOCATION_NER)))
# print("Có {} location_special.".format(len(LOCATION_SPECIAL)))
print("Có {} location.".format(index_sen))
# print("Có {} location_all.".format(len(LOCATION_ALL_TOKEN)))