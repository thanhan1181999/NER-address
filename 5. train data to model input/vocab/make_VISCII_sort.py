import numpy as np
import random
from numpy import argmax
import codecs

def dict_of_tags(file_path):
  dic = {}
  index = -1
  for line in open(file_path, encoding='utf-8'):
    char = line.lower()
    try:
      dic[char]
    except:
      index = index + 1
      dic[char]= index
  return list(dic), len(dic)
  
char_vocab_data,len = dict_of_tags("char_vocab_VISCII.txt")
print(char_vocab_data)
print(len)

with open('VISCII_short.txt', 'a',encoding='utf-8') as the_file:
  for char in char_vocab_data:
    the_file.write(char)
the_file.close()
