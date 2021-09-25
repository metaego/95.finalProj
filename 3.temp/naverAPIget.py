#!/usr/bin/env python3
#-*- codig: utf-8 -*-
import sys
import requests
import json
import pandas as pd
from collections import OrderedDict
import matplotlib.pyplot as plt

client_id = "mvtuf7dccz"
client_secret = "TGXwuEZE3fDZAv408RZ1GFxwhv4k0xQEl5GSIHnH"
url="https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"

headers = {
    "X-NCP-APIGW-API-KEY-ID": client_id,
    "X-NCP-APIGW-API-KEY": client_secret,
    "Content-Type": "application/json"
}

content = '../1.data/resultSamplr_data12.txt'
with open(content, 'r', encoding="utf-8") as result_file:
    content = result_file.read()
    #     ocrResult_final = ocrResult_final + "\n" + content



data = {
  "content": content
}

print("== data ==")
print(data)

print('============= json.dumps =================')
# json.dumps():python객체를 json 데이터로 쓰기, 직렬화, 인코딩
# indent=4: 들여쓰기 옵션(가독성)
# sort_keys=True: key를 기준으로 정렬해서 직렬화
# dictionary를 json으로 변환시(json.dump()) 한글 깨짐 현상 
# strict=False: 제어문자(\r, \n, \t, \o)가 포함된 문자열 처리
print(json.dumps(content, indent="\t", sort_keys=True, ensure_ascii=False))

response = requests.post(url, data=json.dumps(data), headers=headers) # 반환값이 객체임
response_json = response.json()  # json으로 바꿔주는 메소드
rescode = response.status_code

if(rescode == 200):
    print (response.text)
else:
    print("Error : " + response.text)

print()
print("==== 감정분석(response_json) =====")
print(response_json, type(response_json))

# ### json을 csv로 저장
# df = pd.json_normalize(response_json['document'])
# df.to_csv("samplecsv.csv")


# json을 json파일로 저장
# file_data = OrderedDict()
with open('sentiment.js', 'w', encoding='utf-8') as make_file:
    json.dump(response_json, make_file, ensure_ascii=False, indent="\t")

# 데이터 시각화
# 파이 차트 그리기
print('===== 파이차트 그리기 ====')
ration = []
dict_keys = response_json['document'].keys
print(dict_keys)
# for i in dict_keys:
#     print(i)