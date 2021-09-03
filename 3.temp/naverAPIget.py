#!/usr/bin/env python3
#-*- codig: utf-8 -*-
import sys
import requests
import json

client_id = "mvtuf7dccz"
client_secret = "TGXwuEZE3fDZAv408RZ1GFxwhv4k0xQEl5GSIHnH"
url="https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"

headers = {
    "X-NCP-APIGW-API-KEY-ID": client_id,
    "X-NCP-APIGW-API-KEY": client_secret,
    "Content-Type": "application/json"
}

content = './1.data/resultSamplr_data12.txt'
with open(content, 'r', encoding="utf-8") as result_file:
    content = result_file.read()
    #     ocrResult_final = ocrResult_final + "\n" + content



data = {
  "content": content
}

# json.dumps():python객체를 json 데이터로 쓰기, 직렬화, 인코딩
# indent=4: 들여쓰기 옵션(가독성)
# sort_keys=True: key를 기준으로 정렬해서 직렬화
# dictionary를 json으로 변환시(json.dump()) 한글 깨짐 현상 
# strict=False: 제어문자(\r, \n, \t, \o)가 포함된 문자열 처리
print(json.dumps(content, indent=4, sort_keys=True, ensure_ascii=False))

response = requests.post(url, data=json.dumps(data), headers=headers)
rescode = response.status_code

if(rescode == 200):
    print (response.text)
else:
    print("Error : " + response.text)

# 추가 해야할 일
# 필요한 데이터 추출하기
# 보기 편하게 content만 가져오기
print()
print("==== 감정분석 =====")
# print(requests.args.get('document'))
# print(requests.args.get['sentences']['content'], requests.args.get['sentences']['sentiment'], requests.args.get['sentences']['highlights'])