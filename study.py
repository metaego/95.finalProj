from datetime import datetime
import numpy as np
import math

def pccStudy():

    list_1 = np.random.rand(10000000)
    list_2 = np.random.rand(10000000)
    list_3 =

    u1 = [4, 4, 0]   # 1번, 2번, 3번 영화
    u4 = [0, 2, 3]   # 1번, 2번, 3번 영화

    n = len(user)

    for i in range(0, n-1):
        for j in range(0, n):


    print(getTimeStr())
    pccVal_np = np.corrcoef(list_1, list_2)
    print(getTimeStr(), "Numpy PCC")
    print(getTimeStr(), pccVal_np)

    pccVal_my1 = getPccVal(list_1, list_2)
    print(getTimeStr(), "My PCC _ 1 iter")
    print(getTimeStr(), pccVal_my1)







def getPccVal(list_1, list_2):
    x_sum = 0
    y_sum = 0
    xy_sum = 0
    x2_sum = 0
    y2_sum = 0

    n = len(list_1)
    if len(list_2) < n:
        n = len(list_2)

    commonCnt = 0
    for i in range(n):
        if(list_1[i]>0) and (list_2[i]>0):
            commonCnt = commonCnt + 1
            x_sum = x_sum + list_1[i]
            y_sum = y_sum + list_2[i]
            xy_sum = xy_sum + (list_1[i] * list_2[i])
            x2_sum = x2_sum + (list_1[i] * list_1[i])
            y2_sum = y2_sum + (list_2[i] * list_2[i])

    if commonCnt < 10:
        pccVal = 0
    else:
        num = (n * xy_sum) - (x_sum * y_sum)
        denom = (math.sqrt((n * x2_sum) - (x_sum * x_sum)) * (math.sqrt((n * y2_sum) - (y_sum * y_sum))))

        if denom == 0:
            pccVal = 0
        else:
            pccVal = num / denom

    return pccVal


###########################################################
# main execution
def getTimeStr():
    return "[" + str(datetime.now()) + "]"

if __name__ == "__main__":
    print(getTimeStr(), "Study Start")

    pccStudy()

    print(getTimeStr(), "Study Finish")