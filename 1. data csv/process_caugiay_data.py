# chương trình này sẽ xử lý dữ liệu dữ liệu cầu giấy
# đầu tiên sẽ lowercase, và bỏ dấu ,
# bước 1: xử lý name.default để lưu thành NER.txt
#     chỉ lấy những tên không phải là ghép của số nhà và tên đường
# bước 2 và 3: xử lý number,street,ward,district,province,country
#   bước 3: xử lý số nhà
#     1. nếu số nhà không chứa số => gán là trống
#     2. nếu có dạng "số9", thì sẽ chuyển thành "số 9"
#     3. nếu có dạng "103-A12", thì sẽ chuyển thành "103 - A12"
#     4. nếu có chứa ["phố ","đường","duong","ngách","hẻm","ngõ","lô","tổ"], thì sẽ bỏ từ chỗ bắt đầu 
#         đoạn text đến hết
#   bước 2: xử lý tên đường
#     1. nếu tên đường là số => gán là trống
#     2. nếu có chứa số nhà => bỏ đoạn text là số nhà
#     3. nếu tên đường có chứa ["ward", "xã", "phường", "thị trấn", "quận", "huyện","district","thị xã",
#         "thành phố","province","hà nội","việt nam"] thì bỏ từ chỗ bắt đầu đoạn text đến hết
# bước 4: loại bỏ những bản ghi trùng lặp

# ================START ĐẦU TIÊN=====================
import pandas as pd 
names = ["address_parts.number","address_parts.street","parent.locality","parent.county","parent.region","parent.country","name.default","layer"]

data = pd.read_csv('caugiay.csv', encoding='utf8',usecols=names)
# fill "" to empty data
data['address_parts.number'] = data['address_parts.number'].fillna("")
data['address_parts.street'] = data['address_parts.street'].fillna("")
data['parent.locality'] = data['parent.locality'].fillna("")
data['parent.county'] = data['parent.county'].fillna("")
data['parent.region'] = data['parent.region'].fillna("")
data['parent.country'] = data['parent.country'].fillna("")
data['name.default'] = data['name.default'].fillna("")
data['layer'] = data['layer'].fillna("")
# lowercase + bỏ dấu ,
print("begin lowercase + bỏ dấu , ...")
for index in range(len(data)):
  data['address_parts.number'][index] = data['address_parts.number'][index].lower().replace(',',' ').replace('_',' ')
  data['address_parts.street'][index] = data['address_parts.street'][index].lower().replace(',',' ').replace('_',' ').replace('-',' ')
  data['parent.locality'][index]      = data['parent.locality'][index][2:-2].lower()
  data['parent.county'][index]       = data['parent.county'][index][2:-2].lower()
  data['parent.region'][index]        = data['parent.region'][index][2:-2].lower()
  data['parent.country'][index]       = data['parent.country'][index][2:-2].lower()
  data['name.default'][index]         = data['name.default'][index].lower().replace(',',' ').replace('-',' ').replace('&',' ').replace('_',' ').replace('[',' ').replace(']',' ').replace('"',' ')
print("end lowercase + bỏ dấu ,")
print('\n')
# ================END ĐẦU TIÊN=====================

# bỏ trường locaity (xã) ở bản ghi (random có thể bỏ hoặc không)
import random
for index in range(len(data)):
  x = random.randint(1, 10)
  if x % 2 == 0 :
    data['parent.locality'][index]=""

# bỏ trường country (quốc gia) ở bản ghi (random có thể bỏ hoặc không)
import random
for index in range(len(data)):
  x = random.randint(1, 10)
  if x % 2 == 0 :
    data['parent.country'][index]=""

# ================START BƯỚC 1=====================
print("begin get ner...")
caugiay_ner = []
for index in range(len(data)):
  # housenumber = data['address_parts.number'][index]
  # street = data['address_parts.street'][index]
  name = data['name.default'][index]
  layer = data['layer'][index]
  # if name!="" and (housenumber+" "+street)!=name:
  if layer=="venue":
    caugiay_ner.append(name)
# export to file
ner_file = open("../2. primary data/ner.txt","a",encoding='utf8')
for i in range(len(caugiay_ner)):
  ner_file.write(str(caugiay_ner[i]))
  ner_file.write('\n')
ner_file.close()
len_ner = len(caugiay_ner)
print("{} ner".format(len_ner))
print("end get ner")
print('\n')
# result:
#   10481 ner
# ================END BƯỚC 1=======================



# ================START BƯỚC 2 xử lý tên đường=====================
fail_text = ["ward", "xã", "phường", "thị trấn", "quận", "huyện","district","thị xã","thành phố","province","hà nội","việt nam"]
def has_fail_text(string):
  for fail in fail_text:
    r = string.find(fail)
    if r!= -1:
      return r
  return -1

def check_housenumber_in_street(idx_of_record):
  result=""
  number = data['address_parts.number'][idx_of_record]
  street = data['address_parts.street'][idx_of_record]
  max_of_result = 7
  for i in range(max_of_result,0,-1):
    if number.endswith(street[:i]):
      result = street[:i]
      return result
  return result

print("begin xử lý tên đường...")
for index in range(len(data)):
  if data['address_parts.street'][index]!="":

    # 1. nếu tên đường là số => gán là trống
    street = data['address_parts.street'][index]
    if street.isnumeric():
      data['address_parts.street'][index]=""

    # 2. nếu có chứa số nhà => bỏ đoạn text là số nhà
    housenumber = data['address_parts.number'][index]
    street = data['address_parts.street'][index]
    if housenumber!="" and street!="":
      check_start = check_housenumber_in_street(index)
      if check_start!="":
        data['address_parts.street'][index] = data['address_parts.street'][index].replace(check_start,"")

    # 3. nếu tên đường có chứa ["ward", "xã", "phường", "thị trấn", "quận", "huyện","district","thị xã",
    #         "thành phố","province","hà nội","việt nam"] thì bỏ từ chỗ bắt đầu đoạn text đến hết
    index_of_fail_word = has_fail_text(data['address_parts.street'][index])
    if (index_of_fail_word != -1):
      data['address_parts.street'][index]=data['address_parts.street'][index][:index_of_fail_word]

    # 4. convert sao cho giữa mỗi từ là 1 dấu cách
    data['address_parts.street'][index] = ' '.join( data['address_parts.street'][index].split() )
print("end xử lý tên đường")
print("\n")
# ================END BƯỚC 2 xử lý tên đường=======================



# ================START BƯỚC 3 xử lý số nhà=====================
print("begin xử lý số nhà...")
for index in range(len(data)):
  if data['address_parts.number'][index]!="":
    # 1. nếu số nhà không chứa số => gán là trống
    def hasNumbers(inputString):
      return any(char.isdigit() for char in inputString)
    housenumber = data['address_parts.number'][index]
    if not hasNumbers(housenumber):
      data['address_parts.number'][index]=""

    # 2. nếu có dạng "số9", thì sẽ chuyển thành "số 9"
    housenumber = data['address_parts.number'][index]
    if "số" in housenumber and "số " not in housenumber:
      idx = housenumber.index("số")
      data['address_parts.number'][index] = housenumber[:idx+2] + ' ' + housenumber[idx+2:]

    # 3. nếu có dạng "103-A12", thì sẽ chuyển thành "103 - A12"
    housenumber = data['address_parts.number'][index]
    if "-" in housenumber and " - " not in housenumber:
      idx = housenumber.index("-")
      data['address_parts.number'][index] = housenumber[:idx] + ' - ' + housenumber[idx+1:]

    # 4. nếu có chứa ["phố ","đường","duong","ngách","hẻm","ngõ","lô","tổ"] thì sẽ bỏ từ chỗ bắt đầu
    housenumber = data['address_parts.number'][index]
    text_invalid = ["phố ","đường","duong","ngách","hẻm","ngõ","lô","tổ"]
    for special in text_invalid:
      if special in housenumber:
        idx = housenumber.index(special)
        data['address_parts.number'][index] = housenumber[0:idx]

    # 5. convert sao cho giữa mỗi từ là 1 dấu cách
    data['address_parts.number'][index] = ' '.join( data['address_parts.number'][index].split() )
print("end xử lý số nhà")
print("\n")
# ================END BƯỚC 3 xử lý số nhà=======================

# bỏ những bản ghi có số nhà, nhưng ko có tên đường
for index in range(len(data)):
  if data['address_parts.street'][index]=="" and data['address_parts.number'][index]!="":
    data['address_parts.number'][index]=""

# ================START BƯỚC 4 loại bỏ trùng lặp và lưu file=====================
print("Ban đầu có {} bản ghi".format(len(data)))
print("đang lọc...")

def map_number_and_punct(word):
    # check hem va ngach
    num_of_seperate=0
    dem=0
    for char in word:
      if not char.isnumeric() and char!="/":
        dem+=1        
      if char=="/":
        num_of_seperate+=1

    if dem==0:
      if len(word)>1 and num_of_seperate==1:
        return u'<ngach>'
      if len(word)>1 and num_of_seperate>1:
        return u'<hem>'
    # check word is special char
    if word.isnumeric():
        word = u'<number>'
    elif word in [u',', u'<', u'.', u'>', u'/', u'?', u'..', u'...', u'....', u':', u';', u'"', u"'", u'[', u'{', u']',
                  u'}', u'|', u'\\', u'`', u'~', u'!', u'@', u'#', u'$', u'%', u'^', u'&', u'*', u'(', u')', u'-', u'+',
                  u'=']:
        word = u'<punct>'
    return word

from vncorenlp import VnCoreNLP
annotator = VnCoreNLP("../VnCoreNLP-1.1.1.jar", annotators="wseg", max_heap_size='-Xmx500m')

import json
need_data={}
need_data['caugiay']=[]

set_of_record = {"pad"} # to check sentence is exist ?
set_of_record.clear()
# len(concatate_data)
for index in range(len(data)):
  print("sen {}".format(index))

  number = data['address_parts.number'][index]
  street = data['address_parts.street'][index]
  locality = data['parent.locality'][index]
  county = data['parent.county'][index]
  region = data['parent.region'][index]
  country = data['parent.country'][index]

  arr_number = annotator.tokenize(number.lower())
  arr_street = annotator.tokenize(street.lower())
  # arr_locality = annotator.tokenize(locality.lower())
  # arr_county = annotator.tokenize(county.lower())
  # arr_region = annotator.tokenize(region.lower())
  # arr_country = annotator.tokenize(country.lower())

  concate_token = []
  
  if number!="":
    concate_token.extend(arr_number[0])
  
  if street!="":
    concate_token.extend(arr_street[0])
  
  if locality!="":
    # concate_token.extend(arr_locality[0])
    concate_token.append(locality)
  
  if county!="":
    # concate_token.extend(arr_county[0])
    concate_token.append(county)

  if region!="":
    # concate_token.extend(arr_region[0])
    concate_token.append(region)
  
  if country!="":
    # concate_token.extend(arr_country[0])
    concate_token.append(country)
  
  for idx in range(len(concate_token)):
    element = concate_token[idx]
    concate_token[idx] = map_number_and_punct(element)
  
  concate_token = ' '.join(concate_token)

  if concate_token not in set_of_record:
    set_of_record.add(concate_token)
    need_data['caugiay'].append({
      'number':number,
      'street':street,
      'locality':locality,
      'county':county,
      'region':region,
      'country':country
    })

# print(len(set_of_record))
print("Sau khi lọc, còn lại {} bản ghi".format(len(need_data['caugiay'])))

print("Đang lưu ra file...")
with open('../2. primary data/caugiay_processed.json', 'w',encoding='utf8') as outfile:
  json.dump(need_data, outfile,ensure_ascii=False)
print("Lưu thành công")
# ================END BƯỚC 4 loại bỏ trùng lặp và lưu file=======================