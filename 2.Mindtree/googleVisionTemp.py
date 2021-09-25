import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
# from google.cloud.vision import types

### 환경변수 설정(Google에 요청을 보내면 이 키를 확인 해서 등록된 사용자인지 확인하는 듯)
# (예시)
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/motive/Data_Study/MindTree/key/future-glider-321504-43423412617f3.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C://selfStudy/temp1/my-key.json'

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    '../data/data5.jpg') # 사진 파일 상대경로 (저는 resources 폴더 아래에 사진을 넣었습니다.)

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

# 텍스트 추출하기
response_text = client.text_detection(image=image)
words = response_text.text_annotations

print("------------아래는 분석한 Label입니다.---------------")
for label in labels:
    print(label.description)

print("------------아래는 뽑은 텍스트 입니다---------------")
for word in words:
    print(word.description)