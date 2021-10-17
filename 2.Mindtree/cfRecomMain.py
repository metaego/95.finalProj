from datetime import datetime
import numpy as np
import math

def start():

    dataFile = "./movielens/ratings.csv"
    userSimFile = "./movielens/userSim.csv"
    # Training for Recommendation
    # 1. 모든 사용자들의 유사사용자 목록을 구한다.
    #   1.1) 전체 rating 데이터를 로드 한다. (Utility Matrix 생성)
    userList, itemList = loadUserAndItem(dataFile)
    # print(userList)
    # print(itemList)
    print(getTimeStr(), "{0} Users & {1} Items Loaded..".format(len(userList), len(itemList)))

    utilityMatrix, ratingCnt = getUtilityMatrix(dataFile, userList, itemList)
    # print(utilityMatrix)
    print(getTimeStr(), "{0} Ratings are Loaded to Utility Matrix..".format(ratingCnt))

    #   1.2) 각 사용자들의 유사도를 계산한다 (피어슨 상관계수)
    # userSimilarityList = getUserSimilarity(utilityMatrix, userList)
    # print(userSimilarityList)
    # print(getTimeStr(), "{0} Similarity Computed from Utility Matrix..".format(len(userSimilarityList)))
    #
    # saveUserSimilarity(userSimilarityList, userSimFile)
    # print(getTimeStr(), "{0} Similarity File is Written..".format(userSimFile))



    # 계산된 유사도를 불러 온다.
    userSimilarityList = loadUserSimilarity(userSimFile)
    print(getTimeStr(), "{0} Similarities are loaded..".format(len(userSimilarityList)))
    # print(userSimilarityList)

    # 445, 2324, 4.5
    # 140, 1252, 3.5

    targetUID = "445"
    targetIID = "2324"
    targetRating = utilityMatrix[userList.index(targetUID)][itemList.index(targetIID)]
    print(getTimeStr(), "Test - UserID={0}, ItemID={1}, Rating={2}".format(targetUID, targetIID, targetRating))

    # 1. TargetUser와 유사한 사용자들을 불러온다 (n명, 유사도 n 이상)
    simLimit = 0.5
    similarUserList = getSimilarUserList(targetUID, simLimit, userSimilarityList)
    print(getTimeStr(), "Similar User List of {0}: {1} (Similarity Limit={2})".format(targetUID, len(similarUserList), simLimit))
    print(similarUserList)

    # 2. n명의 TargetItem 정수를 가져온다
    predictionDataList = getSImilarUserRating(utilityMatrix, similarUserList, targetIID, userList, itemList)
    print(getTimeStr(), "{0} ratings of Similar Users are extracted.".format(len(predictionDataList)))
    print(predictionDataList)

    # 3. 가져온 n개의 점수를 가지고, TaergetUser의 점수를 예측한다
    predictedRating = 0
    if len(predictionDataList) > 0:
        for r in predictionDataList:
            predictedRating = predictedRating + r
        predictedRating = predictedRating / len(predictionDataList)
        print(getTimeStr(), "Prediction for Item-{0} of User-{1}: {2}".format(targetIID, targetUID, predictedRating))
    else:
        print(getTimeStr(), "Can Not Predict - No Ratings of Similar Users")



def getSImilarUserRating(utilityMatrix, similarUserList, targetIID, userList, itemList):
    predictionDataList = []
    itemIdx = itemList.index(targetIID)

    for simUser in similarUserList:
        userIdx = userList.index(simUser)
        simUserRating = utilityMatrix[userIdx][itemIdx]

        if simUserRating > 0:
            predictionDataList.append(simUserRating)

    return predictionDataList

def getSimilarUserList(targetUID, similarityLimit, userSimilarityList):
    similarUserList = []

    for simInfo in userSimilarityList:
        simIdx = -1
        if simInfo[0] == targetUID:
            simIdx = 1
        elif simInfo[1] == targetUID:
            simIdx = 0

        if simIdx > -1 and simInfo[2] >= similarityLimit:
            similarUserList.append(simInfo[simIdx])

    return similarUserList







def loadUserSimilarity(userSimFile):
    userSimList = []

    with open(userSimFile, "r") as f:
        rows = f.readlines()
        for row in rows:
            tokens = row.split(",")
            userSimList.append([tokens[0], tokens[1], float(tokens[2])])

    return userSimList



def saveUserSimilarity(userSimilarityList, userSimFile):
    f = open(userSimFile, "w")
    for userSim in userSimilarityList:
        f.write("{0},{1},{2}\n".format(userSim[0], userSim[1], userSim[2]))
    f.close()


def getUserSimilarity(utilityMatrix, userList):
    userSimilarityList = []
    commonRatingLimit = 10

    cnt = 0
    for i in range(len(utilityMatrix)-1):
        userA = utilityMatrix[i]
        for j in range(i+1, len(utilityMatrix)):
            userB = utilityMatrix[j]
            pccAB = getPccVal(userA, userB, commonRatingLimit)

            if pccAB > 0:
                userSimilarityList.append([userList[i], userList[j], pccAB])

            cnt = cnt + 1
            if(cnt%5000==0):
                print(getTimeStr(), "{0} Similarity computed".format(cnt))

    return userSimilarityList

def getPccVal(list_1, list_2, commonLimit):
    x_sum = 0
    y_sum = 0
    xy_sum = 0
    x2_sum = 0
    y2_sum = 0

    n = len(list_1)
    commonCnt = 0
    for i in range(n):
        x = list_1[i]
        y = list_2[i]
        if(x > 0) and (y > 0):
            commonCnt = commonCnt + 1
            x_sum = x_sum + x
            y_sum = y_sum + y
            xy_sum = xy_sum + (x * y)
            x2_sum = x2_sum + (x * x)
            y2_sum = y2_sum + (y * y)

    if commonCnt < commonLimit:
        pccVal = 0
    else:
        num = (commonCnt * xy_sum) - (x_sum * y_sum)
        denom = (math.sqrt((commonCnt * x2_sum) - (x_sum * x_sum)) * (math.sqrt((commonCnt * y2_sum) - (y_sum * y_sum))))

        if denom == 0:
            pccVal = 0
        else:
            pccVal = num / denom

    return pccVal

def getUtilityMatrix(dataFile, userList, itemList):
    utilityMatrix = np.full((len(userList), len(itemList)), 0, dtype=float)
    cnt = 0
    with open(dataFile, "r") as f:
        f.readline()
        rows = f.readlines()
        for row in rows:
            cnt = cnt + 1
            tokens = row.split(",")
            rating = float(tokens[2])

            userIndex = userList.index(tokens[0])
            itemIndex = itemList.index(tokens[1])
            utilityMatrix[userIndex][itemIndex] = rating

    return utilityMatrix, cnt

def loadUserAndItem(dataFile):
    userSet = set()
    itemSet = set()

    with open(dataFile, "r") as f:
        f.readline()
        rows = f.readlines()
        for row in rows:
            tokens = row.split(",")
            userSet.add(tokens[0])
            itemSet.add(tokens[1])

    return sorted(list(userSet)), sorted(list(itemSet))






###########################################################
# main execution
def getTimeStr():
    return "[" + str(datetime.now()) + "]"

if __name__ == "__main__":
    print(getTimeStr(), "CF Recommendation Start")
    start()
    print(getTimeStr(), "CF Recommendation Finish")