# 워드클라우드 테스트하기 위한 용도

# pip install wordcloud
# pip install matplotlib

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# text = "오늘은 운동도 공부도 휴무 ... 마침 비도 오고... "
text = "둘래 선버가  은늘부터 한달동안\
일기 써보라고 선버가 하셨는데 n. \
M야지 서야지 가다가 선버가 역시 그냥\
이루고 자버졌다. 습관을 선버가 한꺼 번에\
바꾸는 건 힘든 일or다 그T\
아이패드 두고와서  선버가 회사 다녀옹!\
"
# text = "선버가 선버가 선버가"
 
# wordcloud = WordCloud(font_path='font/NanumGothic.ttf', background_color='white').generate(text)

stopwords = set(STOPWORDS) 
stopwords.add('하게') 
stopwords.add('에') 
stopwords.add('할') 
stopwords.add('하지') 
stopwords.add('인지') 
stopwords.add('은') 
stopwords.add('을') 
 
wordcloud = WordCloud(font_path='font/NanumGothic.ttf',stopwords=stopwords,background_color='black').generate(text)



plt.figure(figsize=(20,20)) #이미지 사이즈 지정
plt.imshow(wordcloud, interpolation='lanczos') #이미지의 부드럽기 정도
plt.axis('off') #x y 축 숫자 제거
plt.show() 
plt.savefig()
