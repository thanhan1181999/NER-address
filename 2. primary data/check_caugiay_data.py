# check các mẫu câu địa chỉ có trong dữ liệu cầu giấy
# kết quả:
# _number_street_locality_county_region_country : 3323
# _street_locality_county_region_country : 390
# _locality_county_region_country : 8
# _number_locality_county_region_country : 107

# cần tạo các form mới từ 3323 câu đầy đủ, và 107 câu thiếu tên đường
# 144 xuân thủy cầu giấy hà nội - số nhà, đường, huyện, (thiếu xã), tỉnh, quốc gia => 3323
# xuân thủy cầu giấy hà nội - đường, huyện, tỉnh, quốc gia => 390

# cầu giấy hà nội
# cầu giấy hà nội việt nam
# cầu giấy hà nội việt nam 10000


# tức là:
# có 3323 câu có đầy đủ các yếu tố
# có 390 câu không có số nhà
# có 8 câu ko có số nhà, tên đường
# có 107 câu có số nhà mà không có tên đường

set_of_record = {"pad":0} # to check sentence is exist ?
set_of_record.clear()

import json

link_file_json_of_location = 'caugiay_processed.json'

with open(link_file_json_of_location) as json_file:
  data = json.load(json_file)
  for p in data['caugiay']: # duyệt từng câu
    number = p['number']
    street = p['street']
    locality = p['locality']
    county = p['county']
    region = p['region']
    country = p['country']
    key = ""
    if number!="":
      key+="_number"
    if street!="":
      key+="_street"
    if locality!="":
      key+="_locality"
    if county!="":
      key+="_county"
    if region!="":
      key+="_region"
    if country!="":
      key+="_country"
    if key in set_of_record:
      set_of_record[key]=set_of_record[key]+1
    else:
      set_of_record[key]=1

for key in set_of_record:
  print("{} : {}".format(key,set_of_record[key]) ) 
