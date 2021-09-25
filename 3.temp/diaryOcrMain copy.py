from datetime import datetime
import os
from konlpy.tag import Hannanum, Kkma, Komoran, Okt
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt



# 구글 API 라이브러리 import와 key 설정
from google.cloud import vision
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../구글키주소입력.json'


def startMamT():
    # ############################################################
    # # 1. image data file loading
    # ############################################################
    # # # 대상 이미지 파일 이름
    # imgFileName = "../data/data11.jpg"
    
    # # # 대상 이미지를 컴퓨터 메모리로 불러오고, 구글 API에 전달하기
    # with open(imgFileName, 'rb') as image_file:
    #     content = image_file.read()
    # image = vision.Image(content=content)
    
    # # ############################################################
    # # # 2. using google vision api
    # # ############################################################
    # # # 구글 API 라이브러리 사용을 위한 instance 생성
    # client = vision.ImageAnnotatorClient()
    
    # # # OCR 실행 요청 및 결과 받아 오기
    # response = client.text_detection(image=image)
    # ocrResults = response.text_annotations
    
    # # # OCR 결과 출력
    # print('Text >')
    # for rs in ocrResults:
    #     print(rs.description)\


    ##################
    ### loading from result sample
    ocrResult_final = loadResultSample('../1.data/resultSamplr_data12.txt')
    # print(ocrResult_final)

    # 0. OCR를 이용해서, 이미지로부터 텍스트를 추출한다( 원하는 결과만 가져온다)

    # 1. 모든 결과를 한 줄로 붙인다
    ocrResult_final_preprocessing = ocrResult_final.replace("\n", " ").strip()
    # print(ocrResult_final_preprocessing)

    # 2. nlp 라이브러리 등을 이용해서 보정한다
    # > konlpy-> py-hanspell
    #    2.1. 띄어쓰기, 문장 분리 등
    ''''
    result: 맞춤법 검사 성공 여부를 나타냄
    original: 검사 전의 문장
    checked: 맞춤법 검사 후의 문장
    errors: 맞춤법 오류 수
    words: Checked.words
    time: 총 요청 시간
    '''
    from hanspell import spell_checker

    strCheckedspell = spell_checker.check(ocrResult_final_preprocessing)
    # print(strCheckedspell) # <class 'hanspell.response.Checked'>

    # 한글 text 스펠링 확인 후 str 타입으로 변환
    # print("======== text_before_analysis ======")
    global text_before_analysis
    text_before_analysis = " ".join(list(strCheckedspell.words.keys()))
    # text_before_analysis ="형태소분석을위한테스트문장입니다. 과제하기 정말 귀찮네요."

    # 3-1. 감성 분석 결과 가져오기 - API >>> 결과 저장 필요
    # 내 요건에 맞는(적합한) 사용 가능 기술 서칭 해보기
    

    # 3-2. '2.1'의 결과로 텍스트를 분석 -API 결과 저장 필요
    # 내 요건에 맞는(적합한) 사용 가능 기술 서칭 해보기


    # 1) 형태소 분석 -> 형태소(어간/어근, 어떤 품사를), konlpy
    # 2) 불용어 처리
    # 3) 구문분석
    # 4) 분석 대상 선정 / 분석
    # 워드 클라우드 그림 그려보기


    # ###########################################################
    # # Konlpy 설치 및 4가지 형태소 분석기 실습
    # ###########################################################
    # # 1. Komoran
    # komoran = Komoran()
    
    # # 1) 명사 추출:nouns()
    # print('==== Komoran 명사추출 =====')
    # print(komoran.nouns(text_before_analysis)) # list type

    # komoran_nouns_count = len(komoran.nouns(text_before_analysis))
    # print("명사 : ", komoran_nouns_count)  


    # # 2) 형태소 추출:morphs()
    # print('==== Komoran 형태소추출 =====')
    # print(komoran.morphs(text_before_analysis))

    # komoran_morphs_count = len(komoran.morphs(text_before_analysis))
    # print("형태소 : ", komoran_morphs_count)  


    # # 3) 형태소와 태그 반환:pos()
    # print('==== Komoran 형태소, 태그 추출 =====')
    # print(komoran.pos(text_before_analysis))  # list type
    # komoran_pos_count = len(komoran.pos(text_before_analysis))
    # print("형태소 + 태그:", komoran_pos_count)


    # # -------------------------------------------------------
    # # 2. Hannanum
    # hannanum = Hannanum()

    # # 1) 명사 추출:nouns()
    # print('==== Hannanum 명사추출 =====')
    # print(hannanum.nouns(text_before_analysis)) # list type

    # hannanum_nouns_count = len(hannanum.nouns(text_before_analysis))
    # print("명사 : ", hannanum_nouns_count)  


    # # 2) 형태소 추출:morphs()
    # print('==== Hannanum 형태소추출 =====')
    # print(hannanum.morphs(text_before_analysis))

    # hannanum_morphs_count = len(hannanum.morphs(text_before_analysis))
    # print("형태소 : ", hannanum_morphs_count) 


    # # 3) 형태소와 태그 반환:pos()
    # print('==== Hannanum 형태소, 태그 추출 =====')
    # print(hannanum.pos(text_before_analysis))  # list type
    # hannanum_pos_count = len(hannanum.pos(text_before_analysis))
    # print("형태소 + 태그:", hannanum_pos_count) 


    # # 4) 형태소 후보 반환:analyze()
    # print('==== Hannanum 형태소 후보 반환 =====')
    # # print(hannanum.analyze(text_before_analysis)) 
    # hannanum_analyze_count = len(hannanum.analyze(text_before_analysis))
    # for i in hannanum.analyze(text_before_analysis):
    #     print(i)
    # print("형태소 후보:", hannanum_analyze_count) 



    # -------------------------------------------------------
    # 3. Kkma
    kkma = Kkma()

    # # 1) 명사 추출:nouns()
    # print('==== kkma 명사추출 =====')
    global kkma_nouns 
    kkma_nouns = kkma.nouns(text_before_analysis)
    # print(kkma_nouns) # list type

    # kkma_nouns_count = len(kkma_nouns)
    # print("명사 : ", kkma_nouns_count) 


    # # 2) 형태소 추출:morphs()
    # print('==== kkma 형태소추출 =====')
    global kkma_morphs 
    kkma_morphs = kkma.morphs(text_before_analysis)
    # print(kkma_morphs)

    # kkma_morphs_count = len(kkma_morphs)
    # print("형태소 : ", kkma_morphs_count)  


    # 3) 형태소와 태그 반환:pos()
    # print('==== kkma 형태소, 태그 추출 =====')
    global kkma_pos
    kkma_pos = kkma.pos(text_before_analysis)
    # print(kkma_pos)  # list type

    # kkma_pos_count = len(kkma_pos)
    # print("형태소 + 태그:", kkma_pos_count) 


    # # 4) 문장 반환:sentences()
    # print('==== kkma 문장 추출 =====')
    global kkma_sentences
    kkma_sentences = kkma.sentences(text_before_analysis)
    # print(kkma_sentences)  # list type

    # kkma_sentences_count = len(kkma_sentences)
    # print("형태소 + 태그:", kkma_sentences_count) 


    # # -------------------------------------------------------
    # # 4. Okt
    # okt = Okt()

    # # 1) 명사 추출:nouns()
    # print('==== okt 명사추출 =====')
    # print(okt.nouns(text_before_analysis)) # list type

    # okt_nouns_count = len(okt.nouns(text_before_analysis))
    # print("명사 : ", okt_nouns_count) 


    # # 2) 형태소 추출:morphs()
    # print('==== okt 형태소추출 =====')
    # print(okt.morphs(text_before_analysis))

    # okt_morphs_count = len(okt.morphs(text_before_analysis))
    # print("형태소 : ", okt_morphs_count)  


    # # 3) 형태소와 태그 반환:pos()
    # print('==== okt 형태소, 태그 추출 =====')
    # print(okt.pos(text_before_analysis))  # list type
    # okt_pos_count = len(okt.pos(text_before_analysis))
    # print("형태소 + 태그:", okt_pos_count) 


    # # 4) 구문별 반환:phrases()
    # print('==== okt 문장 추출 =====')
    # print(okt.phrases(text_before_analysis))  # list type
    # okt_phrases_count = len(okt.phrases(text_before_analysis))
    # print("형태소 + 태그:", okt_phrases_count) 

    # # -------------------------------------------------------
    # # 형태소 분석기 4가지 비교
    # print("==== 형태소 분석기 4가지 비교 ====")
    # print('%10s |%10s |%10s |%10s |%10s' % ('비교항목', 'Kpmpran', 'Hannanum', 'Kkma', 'Okt'))
    # print('-'*len('%10s |%10s |%10s |%10s |%10s' % ('비교항목', 'Kpmpran', 'Hannanum', 'Kkma', 'Okt')))
    # print('%10s|%10d |%10d |%10d |%10d' %('명사추출', komoran_nouns_count, hannanum_nouns_count, kkma_nouns_count, okt_nouns_count))
    # print('%10s|%10d |%10d |%10d |%10d' %('형태소추출', komoran_morphs_count, hannanum_morphs_count, kkma_morphs_count, okt_morphs_count))
    # print('%10s|%10d |%10d |%10d |%10d' %('형태소+태그', komoran_pos_count, hannanum_pos_count, kkma_pos_count,  okt_pos_count))
    # print('%10s|%10s |%10d |%10s |%10s' %('형태소후보반환', '-', hannanum_analyze_count, '-', '-'))
    # print('%10s|%10s |%10s |%10d |%10s' %('문장반환', '-', '-', kkma_sentences_count, '-'))
    # print('%10s|%10s |%10s |%10s |%10d' %('구문반환', '-', '-', '-', okt_phrases_count))

    # print(getTimeStr(), "OCR using Google API is Finished Successfully..")

    return  kkma_nouns, kkma_morphs, kkma_pos, kkma_sentences

def kkmaPreprocess(text, tokenizer):
    global kkma_pos_dic
    kkma_pos_dic = {}

    # print('===========KKMA POS==========')
    # 형태소에서 키와 값 추출 -> dict 타입으로 변환(key:형태소 태그, value:한글 텍스트)
    for hantxt, tags in kkma_pos:
        kkma_pos_dic[tags] = hantxt 

    # 불용어로 추가할 태그 추가
    tag_add_boollist = ['SF', 'JKO', 'ETD', 'EFN', 'VCP', 'VV', 'XSV', 'ETN', 'JX', 'VXV', 'EPT', 'ECS', 'ETD', 'ECE', ]
    bool_list = []
    for bool_tags in tag_add_boollist:
        bool_list += kkma_pos_dic[bool_tags].split()


    # 불용어 정의
    stopwords = ['ㅂ니다', '네요', '에', '아', '를','은', '과', '거든요', '에게', '있', '분', '아야', '아도', '던', '지만', '았', '한', 'ㄴ', 'ㄹ', '어요', '에서', '부터', '러', '는데', 'ㅂ시다', '어도', '것', '지', '라고요', '도', '고', '가', '으로', '죠', '아요', '다고','ㄴ다'] + bool_list
    # print("=====불용어 정의 리스트======")
    # print(stopwords)

    txt = re.sub('[^가-힣a-z]', ' ', text)
    token = tokenizer.morphs(txt) # 형태소 추출 토큰
    token = [t for t in token if t not in stopwords]

    return token

def loadResultSample(resultFile):
    res = ''
    with open(resultFile, 'r', encoding="utf-8") as result_file:
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

    tokenizer = Kkma()
    

kkma_pre = kkmaPreprocess(text_before_analysis, tokenizer)
print('==== kkma_pre ====== ')
print(kkma_pre)
# print('==== kkma_nouns ====== ')
# print(kkma_nouns)
# print("------kkma_pre.count------------")
kkma_pre_list = []
for e in kkma_pre:
    if e not in kkma_pre_list:
        kkma_pre_list.append(e)
print("----kkma_pre_list---------")
print(kkma_pre_list)
print("------kkma_pre.count------------")
for i in kkma_pre_list:
    print(f"{i}",kkma_pre.count(i))

kkma_pre_txt= " ".join(kkma_pre)
# print('==== kkma_pre_txt ====== ')
# print(kkma_pre_txt)

# # kkma nouns로 워드 클라우드 생성
# kkma_pre_txt= " ".join(kkma_nouns)


print("===워드 클라우드 생성")
wordcloud = WordCloud(font_path='font/NanumGothic.ttf', background_color='white').generate(kkma_pre_txt)
plt.figure(figsize=(10,10)) #이미지 사이즈 지정
plt.imshow(wordcloud, interpolation='lanczos') #이미지의 부드럽기 정도
plt.axis('off') #x y 축 숫자 제거
# plt.show() 
plt.savefig('../1.data/result/result.png')  # plt 파일로 저장
# 워드 클라우드의 단점
# 1) pos의 태그를 반영하여 카운트를 하지 않음
#    예: '나'가 2번 존재. '나'는 I를 의미하는 게 아니라 짜증난다의 '나', 화가난다의 '나'이다 
# 2) str의 맨 앞단에 있는 단어들이 크게 출력됨
# 3) nouns()함수는 unique한 단어만 뽑아냄. 중복 허용하지 않는다. 그래서 워드 클라우드에 쓸 수 없음.