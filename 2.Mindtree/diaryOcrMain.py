from datetime import datetime
import os
from hanspell import spell_checker
from konlpy.tag import Kkma
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json

# 구글 API 라이브러리 import와 key 설정
from google.cloud import vision
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './diaryocr-d3168619e3da.json'


###########################################################
## Main Function
###########################################################
def startMamT(userID, imgFileName):
    resultFileName = "./Results/" + userID + "_" + os.path.basename(imgFileName) + ".mamT"

    if os.path.isfile(resultFileName):
        print(getTimeStr(), "Ther is Previous Analysis Result, already")

        wordFreqSet = loadPreviousResult(resultFileName)

        # 워드 클라우드 시각화 영역
        wordcloud = WordCloud(font_path='/Users/wonmoonsong/Library/Fonts/NanumSquare_acB.ttf',
                              background_color='white', colormap="Accent_r",
                              width=1500, height=1000).generate_from_frequencies(wordFreqSet)
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.show()



    else:
        #########################################################
        ## 1. 이미지로부터 텍스트 추출하기
        ## Todo: 필기체 이미지로부터 OCR 결과의 정확도를 높이기 위한 방법 고민 필요
        useGoogleAPI = False
        print(getTimeStr(), "=== Step-1 ===")
        print(getTimeStr(), "OCR Process is Started..")
        ocrResultText = getOCRResult(imgFileName, useGoogleAPI)
        print(getTimeStr(), "OCR Process is Finished..")

        print(">> OCR Result (Google API):")
        print(ocrResultText)
        print()

        #########################################################
        ## 2. 텍스트 전처리 하기 (텍스트 분석 전 정제)
        ## Todo: 오 후처리 결과에 대한 고찰 필요
        print(getTimeStr(), "=== Step-2 ===")
        print(getTimeStr(), "OCRResult Postprossing is Started..")
        ocrResultText_final = getOCRPostprocessing(ocrResultText)
        print(getTimeStr(), "OCRResult Postprossing is Finished..")

        print(">> OCR Result Post-Processing (hanspell):")
        print(ocrResultText_final)
        print()


        #########################################################
        ## 3-1. 텍스트 마이닝 하기 - 빈발단어 워드클라우드 등
        ## Todo: 빈도 분석 외 추가 분석 요소 검토 (연관어 분석 등)
        print(getTimeStr(), "=== Step-3.1 ===")
        print(getTimeStr(), "Text Analysis (Word Frequency) is Started..")
        posTagger = Kkma()
        posResult = posTagger.pos("시작")
        print(getTimeStr(), "POS Tagger (KKma) is initialized..")
        wordsList = getInterestWordsList(posTagger, ocrResultText_final)
        wordFreqSet = getWordFrequency(wordsList)
        print(getTimeStr(), "Text Analysis (Word Frequency) is Finished..")

        print(">> Text Analysis (Word Frequency) Result:")
        print(wordFreqSet)
        print()

        ## 워드 클라우드 시각화 영역
        # wordcloud = WordCloud(font_path='/Users/wonmoonsong/Library/Fonts/NanumSquare_acB.ttf',
        #                       background_color='white', colormap="Accent_r",
        #                       width=1500, height=1000).generate_from_frequencies(wordFreqSet)
        # plt.imshow(wordcloud)
        # plt.axis('off')
        # plt.show()


        #########################################################
        ## 3-2. 감정 분석 결과 가져오기 - API >> 결과 저장 필요
        ## 내 요건에 맞는(적합한) 사용 가능 기술 서칭 해보기, 여의치가 않음..
        ## 우선, 긍/부정 감정분석으로 구현해보기 (네이버 클로바, IBM Watson, Google API)
        emotionResultSet = {}

        #########################################################
        ## 4. 분석 결과 저장하기
        print(getTimeStr(), "=== Step-4 ===")
        saveResult(resultFileName, wordFreqSet, emotionResultSet)
        print(getTimeStr(), "Result Saved: '{0}'".format(resultFileName))



###########################################################
## Sub Functions
###########################################################
## 4. 결과 저장
def saveResult(resultFileName, wordFreqSet, emotionResultSet):
    with open(resultFileName, "w") as json_file:
        json.dump(wordFreqSet, json_file, ensure_ascii=False)

##
def loadPreviousResult(resultFileName):
    wordFreqSet = {}

    with open(resultFileName, "r") as st_json:
        wordFreqSet = json.load(st_json)

    return wordFreqSet






## 3-1.b 빈발단어 정보 구하기
def getWordFrequency(wordList):
    wordFreqSet = {}

    for word in wordList:
        if word in wordFreqSet:
            wordFreqSet[word] = wordFreqSet[word] + 1
        else:
            wordFreqSet[word] = 1

    return wordFreqSet

## 3-1.a 주요 단어 목록 뽑기
def getInterestWordsList(posTagger, targetStr):
    print(getTimeStr(), "POS Tagging is Started..")
    posResult = posTagger.pos(targetStr)

    interestWordList = []
    for pos in posResult:
        if pos[1][0] in {"I", "M", "N", "O", "U", "V"}:
            if len(pos[0]) > 1:
                interestWordList.append(pos[0])
    print(getTimeStr(), "{0} interest words of total {1} pos-tagging Result are extracted..".format(len(interestWordList), len(posResult)))

    return interestWordList


## 2. 텍스트 전처리 - 텍스트 분석 입력 결과의 정제를 위한 OCR 결과 텍스트 후처리 하기
def getOCRPostprocessing(ocrResultText):
    # hanspell 라이브러리를 이용한 띄어쓰기 및 오탈자 수정
    hanspellResult = spell_checker.check(ocrResultText)
    hanspellResultText = hanspellResult.checked

    return hanspellResultText


## 1. 이미지 내 텍스트 추출 - 이미지로부터 OCR 결과 가져오기
def getOCRResult(imgFileName, useAPI):
    ocrResult_final = ""

    if useAPI == False:
        print(getTimeStr(), "OCR Exec Option: \"False\". Getting Result from Test File..")

        # test 파일로부터 결과를 받아오기
        testFileName = 'resultSamplr_data11.txt'
        with open(testFileName, 'r', encoding="utf-8") as result_file:
            content = result_file.read()
            ocrResult_final = ocrResult_final + "\n" + content
    else:
        print(getTimeStr(), "OCR Exec Option: \"True\". Getting Result from Google API..")

        # 대상 이미지를 컴퓨터 메모리로 불러오고, 구글 API에 전달하기
        with open(imgFileName, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)

        # 구글 API 라이브러리 사용을 위한 instance 생성
        client = vision.ImageAnnotatorClient()

        # OCR 실행 요청 및 결과 받아 오기
        response = client.text_detection(image=image)
        ocrResults = response.text_annotations
        ocrResult_final = ocrResults[0].description

    # 여러줄인 경우, 한 줄로 붙여서 결과를 반환
    finalResult = ocrResult_final.replace("\n", " ").strip()
    return finalResult


###########################################################
# main execution
def getTimeStr():
    return "[" + str(datetime.now()) + "]"

if __name__ == "__main__":
    print(getTimeStr(), "Start - Mam Training")

    userID = "moonie"
    imgFileName = "data/pc_img.png"

    startMamT(userID, imgFileName)

    print(getTimeStr(), "Finish - Mam Training")
