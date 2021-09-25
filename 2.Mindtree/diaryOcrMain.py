from datetime import datetime
import os
from hanspell import spell_checker
from konlpy.tag import Kkma
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
font_path = "/Users/wonmoonsong/Library/Fonts/NanumSquare_acB.ttf"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

import json

# 구글 API 라이브러리 import와 key 설정
from google.cloud import vision
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './diaryocr-d3168619e3da.json'

# NAVER CLOVA API
import sys
import requests
clovaAPI_url="https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"
clovaAPI_headers = {"X-NCP-APIGW-API-KEY-ID": "fmcyn3rk8o",
                    "X-NCP-APIGW-API-KEY": "l1xoRWP5ZtEvlNFPeS6xoNUpG9ExOxgQI2YrHygV",
                    "Content-Type": "application/json"}


###########################################################
## Main Function
###########################################################
def startMamT(userID, imgFileName):
    resultFileName = "./Results/" + userID + "_" + os.path.basename(imgFileName) + ".mamT"
    existResult = os.path.isfile(resultFileName)

    # existResult = False
    if existResult:
        print(getTimeStr(), "There is Previous Analysis Result, already")

        wordFreqDict, emotionDict, positiveAssoWordFreqDict, negativeAssoWordFreqDict = loadPreviousResult(resultFileName)
        execVisualization(wordFreqDict, emotionDict, positiveAssoWordFreqDict, negativeAssoWordFreqDict)


    else:
        posTagger = Kkma()
        posResult = posTagger.pos("시작")
        print(getTimeStr(), "POS Tagger (KKma) is initialized..")

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

        if ocrResultText != None:
            if len(ocrResultText) == 0:
                print(getTimeStr(), "There is not any Text in Your Image..")
                print(getTimeStr(), "Program Exit..")
                return

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
        ## Todo: 빈도 분석 외 추가 분석 요소 검토
        wordFreqDict = {}
        print(getTimeStr(), "=== Step-3.1 ===")
        print(getTimeStr(), "Text Analysis (Word Frequency) is Started..")
        wordsList = getInterestWordsList(posTagger, ocrResultText_final)
        wordFreqDict = getWordFrequency(wordsList)
        print(getTimeStr(), "Text Analysis (Word Frequency) is Finished..")

        print(">> Text Analysis (Word Frequency) Result:")
        print(wordFreqDict)
        print()



        #########################################################
        ## 3-2. 감정 분석 결과 가져오기 - API >> 결과 저장 필요
        ## 내 요건에 맞는(적합한) 사용 가능 기술 서칭 해보기, 여의치가 않음..
        ## 우선, 긍/부정 감정분석으로 구현해보기 (네이버 클로바, IBM Watson, Google API)
        ## Todo: 다중 감성 분석으로 적용 할 수 있는 방법, 문장별 긍부정 결과를 활용할 수 있는 방법 고민
        print(getTimeStr(), "=== Step-3.2 ===")
        print(getTimeStr(), "Text Analysis (Emotion Recognition) is Started..")
        emotionDict = getEmotionResult(ocrResultText_final)
        print(getTimeStr(), "Text Analysis (Emotion Recognition) is Finished..")

        print(">> Text Analysis (Emotion Recognition) Result:")
        print(emotionDict)
        print()

        #########################################################
        ## 3-3. 추가 분석 - 감성별 연관어 분석 (감성별 빈발단어 추출)
        print(getTimeStr(), "=== Step-3.3 ===")
        print(getTimeStr(), "Sentiment Association Words Analysis is Started..")
        positiveSentence, negativeSentence = getSentimentSentences(emotionDict)

        positiveAssoWordFreqDict = []
        negativeAssoWordFreqDict = []

        if (len(positiveSentence) > 0):
            positiveAssoWordFreqDict = getWordFrequency(getInterestWordsList(posTagger, positiveSentence))
        if (len(negativeSentence) > 0):
            negativeAssoWordFreqDict = getWordFrequency(getInterestWordsList(posTagger, negativeSentence))
        print(getTimeStr(), "Sentiment Association Words Analysis is Finished..")

        print(">> Positive Associated Words Frequent List Result:")
        print(">>", positiveAssoWordFreqDict)
        print(">> Negative Associated Words Frequent List Result:")
        print(">>", negativeAssoWordFreqDict)






        #########################################################
        ## 4. 분석 결과 저장하기
        print(getTimeStr(), "=== Step-4 ===")
        saveResult(resultFileName, wordFreqDict, emotionDict, positiveAssoWordFreqDict, negativeAssoWordFreqDict)
        print(getTimeStr(), "Result Saved: '{0}'".format(resultFileName))

        # execVisualization(wordFreqDict, emotionDict)





###########################################################
## Sub Functions
###########################################################
## 감성별 문장 반환
def getSentimentSentences(emotionDict):
    positiveSentence = ""
    negativeSentence = ""

    for sentenceDict in emotionDict["sentences"]:
        if sentenceDict["sentiment"] == "positive":
            positiveSentence = positiveSentence + "\n" + sentenceDict["content"]
        elif sentenceDict["sentiment"] == "negative":
            negativeSentence = negativeSentence + "\n" + sentenceDict["content"]

    return positiveSentence, negativeSentence



## 시각화
def execVisualization(wordFreqDict, emotionDict, positiveAssoWordFreqDict, negativeAssoWordFreqDict):

    # 워드 클라우드 시각화 영역
    if (wordFreqDict != None) and (len(wordFreqDict) > 0):
        wordcloud = WordCloud(font_path='/Users/wonmoonsong/Library/Fonts/NanumSquare_acB.ttf',
                              background_color='white', colormap="Accent_r",
                              width=1500, height=1000).generate_from_frequencies(wordFreqDict)
        plt.subplot(321)
        plt.title('Words Cloud of Total Text')
        plt.imshow(wordcloud)
        plt.axis('off')
        # plt.show()
    else:
        print("There is not any WordFrequency Result to Visualize")

    # 감성분석 결과에 대한 시각화
    if (emotionDict != None) and (len(emotionDict) > 0):
        positive_val = emotionDict["document"]["confidence"]["positive"]
        neutral_val = emotionDict["document"]["confidence"]["neutral"]
        negative_val = emotionDict["document"]["confidence"]["negative"]

        ratio = [positive_val, neutral_val, negative_val]
        labels = ['긍정', '중립', '부정']
        colors = ['#33ffff', '#aaaaaa', '#ffcccc']
        wedgeprops = {'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}

        plt.subplot(323)
        plt.title('Sentiment Analysis')
        plt.pie(ratio, labels=labels, autopct='%.1f%%', startangle=260, counterclock=False, colors=colors,
                wedgeprops=wedgeprops)
        # plt.show()
    else:
        print("There is not any Emotion Result to Visualize")

    # 감성별 연관어 분석 결과에 대한 시각화
    positive_wordcloud = WordCloud(font_path='/Users/wonmoonsong/Library/Fonts/NanumSquare_acB.ttf',
                                   background_color='#dddddd', colormap="Accent_r",
                                   width=1500, height=1000).generate_from_frequencies(positiveAssoWordFreqDict)
    negative_wordcloud = WordCloud(font_path='/Users/wonmoonsong/Library/Fonts/NanumSquare_acB.ttf',
                                   background_color='#dddddd', colormap="Accent_r",
                                   width=1500, height=1000).generate_from_frequencies(negativeAssoWordFreqDict)

    plt.subplot(325)
    plt.title('Positive Words')
    plt.imshow(positive_wordcloud)
    plt.axis('off')

    plt.subplot(326)
    plt.title('Negative Words')
    plt.imshow(negative_wordcloud)
    plt.axis('off')

    plt.show()





## 4. 결과 저장
def saveResult(resultFileName, wordFreqDict, emotionResultSet, positiveAssoWordFreqDict, negativeAssoWordFreqDict):
    finalResultSet = {}
    finalResultSet["wordFreq"] = wordFreqDict
    finalResultSet["emotion"] = emotionResultSet
    finalResultSet["positiveAssoWordFreqDict"] = positiveAssoWordFreqDict
    finalResultSet["negativeAssoWordFreqDict"] = negativeAssoWordFreqDict

    with open(resultFileName, "w") as json_file:
        json.dump(finalResultSet, json_file, ensure_ascii=False, indent="\t")

## 이전의 결과 파일에서 내용을 불러오기
def loadPreviousResult(resultFileName):

    with open(resultFileName, "r") as st_json:
        jsonData = json.load(st_json)

    return jsonData["wordFreq"], jsonData["emotion"], jsonData["positiveAssoWordFreqDict"], jsonData["negativeAssoWordFreqDict"]

## 3-2
def getEmotionResult(targetStr):
    resultDict = {}
    data = { "content": targetStr }

    response = requests.post(clovaAPI_url, data=json.dumps(data), headers=clovaAPI_headers)
    if (response.status_code == 200):
        responseDict = json.loads(response.text)
        resultDict = responseDict
    else:
        print(getTimeStr(), "NAVER CLOVA API Error !!!")
        resultDict = {}

    return resultDict


## 3-1.b 빈발단어 정보 구하기
def getWordFrequency(wordList):
    wordFreqSet = {}

    for word in wordList:
        if word in wordFreqSet:
            wordFreqSet[word] = wordFreqSet[word] + 1
        else:
            wordFreqSet[word] = 1

    return wordFreqSet

## 3-1.a 쥐요 단어 목록 뽑기
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







