from datetime import datetime
import numpy as np


def start():
    
    dataFile = "./movieLens/ratings.csv"
    userSimFile = "./movieLens/ratings.csv"
    # Training for Recommendation
    # 1. 유사사용자 목록을 구한다
    #   1) 전체 rating 데이터를 로드한다(Utility Matrix 생성)
    #       - 데이터를 읽어서, 사용자 목록와 아이템 목록을 확인한다
    #       - 사용자 수와 아이템 수로 빈 Utility NMatrix를 만들어서, rating 값을 채운다
    #       - Utility Matrix 완성
    userList, itemList = loadUserAndItem(dataFile)
    # print(userList)
    # print(itemList)
    print(getTimeStr(), "{0} Users & {1} Items Loaded..".format(len(userList), len(itemList)))

    utilityMatrix, ratingCnt = getUtilityMatrix(dataFile, userList, itemList)
    print(getTimeStr(), "{0} Rating are Loaded to Utility Matrix..".format(ratingCnt))


    userSimilarityList = getUserSimilarity(utilityMatrix, userList )
    print(userSimilarityList)
    print(getTimeStr(), "{0} Similarity Computed from Utility Matrix.. ".format(len(userSimilarityList))


    # uIdx = userList.index("2")
    # iIdx = itemList.index("68157")
    # print(utilityMatrix[uIdx][iIdx])

    # uIdx = userList.index("423")
    # iIdx = itemList.index("1080")
    # print(utilityMatrix[uIdx][iIdx])



    # print(userList)
    # print(itemList)

    utilityMatrix = getUtilityMatrix(dataFile, userList, itemList)

    #     i1 i2 i3 i4
    # u1  1  3  2  5 
    # u2  0  1  0  1
    # u3  2  0  1  2
    # u4  3  1  3  1
    
    #   2) 각 사용자들의 유사도를 계산한다(피어슨 상관계수)

    #     u1 u2 u3 u4
    # u1  x  o  o  o
    # u2  x  x  o  o 
    # u3  x  x  x  x 
    # u4  x  x  x  x


    #   3) 계산된 유사도를 저장한다

    
    # 2. 목표 사용자의 목표 아이템에 대한 추천 값을 계산한다.
    #   1) 계산된 유사도로부터, 목표 사용자와 유사한 사용자들을 불러온다
    #   2) 목표 아이템에 대한 유사 사용자들의 점수를 불러온다.
    #   3) 불러온 유사 사용자들의 점수를 이용하여, 목표 사용자의 점수를 예측한다.

def getUserSimilarity(utilityMatrix, userList):
    userSimilarityList = []
    commonRatingLimit = 10

    for i in range(len(utilityMatrix)-1):
        userA = utilityMatrix[i]
        for j in range(i+1, len(utilityMatrix)):
            userB = utilityMatrix[j]
            pccAB = getPccVal(userA, userB, commonRatingLimit)

            if pccAB > 0:
                userSimilarityList.append(list(userList[i], userList[j], pccAB))

            cnt = cnt + 1
            if (cnt%5000==0):
                print(getTimeStr, "{0} Similarity computed".format(cnt))

    return userSimilarityList


def getPccVal(list_1, list_2, commonLimit):
    x_sum = 0
    y_sum = 0
    xy_sum = 0

    n = len(list_1)
    for i in range(n):
        commonCnt = 0
        if (list_1[i] > 0) and (list_2[i] > 0):
            x_sum =  x_sum + list_1[i] 








def getUtilityMatrix(dataFile, userList, itemList):
    utilityMatrix = np.full((len(userList), len(itemList)), 0, dtype=float)
    cnt = 0

    with open(dataFile, "r") as f:
        f.readline()
        rows = f.readlines()
        for row in rows:
            tokens= row.split(",")
            rating = float(tokens[2])
            
            userIndex = userList.index(tokens[0])
            itemIndex = itemList.index(tokens[1])
            utilityMatrix[userIndex][itemIndex] = rating


    #      1 10 100 10044
    #   1  1  3  2    5 
    #  10  0  1  0    1
    # 100  2  0  1    2
    # 101  3  1  3    1

    return utilityMatrix, cnt



def loadUserAndItem(dataFile):
    userSet = set()
    itemSet = set()

    with open(dataFile, "r") as f:
        f.readline()
        rows = f.readlines()
        for row in rows:
            tokens= row.split(",")

            userSet.add(tokens[0])
            itemSet.add(tokens[1])

    return sorted(list(userSet)), sorted(list(itemSet))

           
####################################################
# main execution
def getTimeStr():
    return "[" + str(datetime.now()) + "]"

if __name__ == "__main__":
    print(getTimeStr(), "CF Recommendation Start")
    start()
    print(getTimeStr(), "CF Recommendation Finish")