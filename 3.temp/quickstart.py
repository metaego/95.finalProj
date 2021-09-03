# import io 
# import os


# from google.cloud import vision
# # from google.cloud.vision import 

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'sound-invention-321504-f8b38787552b.json'


# # Instantiates(예를 들어 설명하다) a client 
# client = vision.ImageAnnotatorClient()


# # The name of the image file to annotate
# file_name = os.path.join(
#     os.path.dirname(__file__),
#     'resources/diary.jpg')

# # 이미지에서 메모리로 로드
# with io.open(file_name, 'rb') as image_file:
#     content = image_file.read()


# image = vision.Image(content=content)

# # 이미지에서 라벨 탐색
# response = client,label_detection(image=image)
# labels = response.label_annotations

# # 텍스트 추출하기
# response_text = client.text_detection(image=image)
# words = response_text.text_annotations


# print("------------아래는 분석한 Label입니다.---------------")
# print("Labels:")
# for label in labels:
#     print(label.description)

# print("------------아래는 뽑은 텍스트 입니다---------------")
# for word in words:
#     print(word.description)



# 동기님 스크립트

# import io
# import os

# # Imports the Google Cloud client library
# from google.cloud import vision
# # from google.cloud.vision import types

# ### 환경변수 설정(Google에 요청을 보내면 이 키를 확인 해서 등록된 사용자인지 확인하는 듯)
# # (예시)
# # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/motive/Data_Study/MindTree/key/future-glider-321504-43423412617f3.json'
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'sound-invention-321504-0577e361834c.json'

# # Instantiates a client
# client = vision.ImageAnnotatorClient()

# # The name of the image file to annotate
# file_name = os.path.join(
#     os.path.dirname(__file__),
#     'resources/diary.jpg') # 사진 파일 상대경로 (저는 resources 폴더 아래에 사진을 넣었습니다.)

# # Loads the image into memory
# with io.open(file_name, 'rb') as image_file:
#     content = image_file.read()

# image = vision.Image(content=content)

# # Performs label detection on the image file
# response = client.label_detection(image=image)
# labels = response.label_annotations

# # 텍스트 추출하기
# response_text = client.text_detection(image=image)
# words = response_text.text_annotations

# print("------------아래는 분석한 Label입니다.---------------")
# for label in labels:
#     print(label.description)

# print("------------아래는 뽑은 텍스트 입니다---------------")
# for word in words:
#     print(word.description)




import io 
import os 

def implicit():
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)

    

# Imports the Google Cloud client library 
from google.cloud import vision 

# Instantiates a client 
client = vision.ImageAnnotatorClient() 

# The name of the image file to annotate
file_name = os.path.abspath('../resources/diary.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file: 
    content = image_file.read()

image = vision.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

print('Labels:')
for label in labels: 
    print(label.description)


