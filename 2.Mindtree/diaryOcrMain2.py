from datetime import datetime
import os

# 구글 API 라이브러리 import와 key 설정
from google.cloud import vision
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './diaryocr-d3168619e3da.json'



def startMamT():
    # ############################################################
    # # 1. image data file loading
    # ############################################################
    # # 대상 이미지 파일 이름
    # imgFileName = "data/data11.jpg"
    #
    # # 대상 이미지를 컴퓨터 메모리로 불러오고, 구글 API에 전달하기
    # with open(imgFileName, 'rb') as image_file:
    #     content = image_file.read()
    # image = vision.Image(content=content)
    #
    # ############################################################
    # # 2. using google vision api
    # ############################################################
    # # 구글 API 라이브러리 사용을 위한 instance 생성
    # client = vision.ImageAnnotatorClient()
    #
    # # OCR 실행 요청 및 결과 받아 오기
    # response = client.text_detection(image=image)
    # ocrResults = response.text_annotations
    #
    # # OCR 결과 출력
    # print('Text >')
    # for rs in ocrResults:
    #     print(rs.description)\

    ocrResult_final = loadResultSample('resultSamplr_data11.txt')
    print(ocrResult_final)





    print(getTimeStr(), "OCR using Google API is Finished Successfully..")

def loadResultSample(resultFile):
    res = ''
    with open(resultFile, 'r') as result_file:
        content = result_file.read()
        res = res + "\n" + content
    return res




###########################################################
# main execution
def getTimeStr():
    return "[" + str(datetime.now()) + "]"


if __name__ == "__main__":
    print(getTimeStr(), "Start - Mam Training Recognition")
    startMamT()
    print(getTimeStr(), "Finish - Mam Training Recognition")
