from datetime import datetime
import numpy as np
import math

def pccStudy():

    list_1 = np.random.rand(10)
    list_2 = np.random.rand(10)

    pccVal_np = np.corrcoef(list_1, list_2)
    print(getTimeStr(), "Numpy PCC")
    print(getTimeStr(), pccVal_np)

    pccVal_my1 = getPccVal(list_1, list_2)
    print(getTimeStr(), "My Pcc_1 iter")
    print(getTimeStr(), pccVal_my1)

    pccVal_my2 = getPccVal_Avg(list_1, list_2)
    print(getTimeStr(), "My Pcc_1 iter")
    print(getTimeStr(), pccVal_my2)




def getPccVal(list_1, list_2):
    x_sum = 0
    y_sum = 0
    xy_sum = 0
    x2_sum = 0
    y2_sum = 0
    n = len(list_1)

    for i in range(len(list_1)):
        x_sum += list_1[i]
        y_sum += list_1[i]
        xy_sum += list_1[i] * list_2[i]
        x2_sum += list_1[i] * list_1[i]
        y2_sum += list_2[i] * list_2[i]

    num = (n*xy_sum) - (x_sum*y_sum)
    denom = (math.sqrt((n * x2_sum) - (x_sum * x_sum)))*(math.sqrt(((n * y2_sum) - (y_sum * y_sum))))
    pccVal_my = num/denom

    return pccVal_my


def getPccVal_Avg(list_1, list_2):
    x_avg = 0
    y_avg = 0

    x_sum = 0
    y_sum = 0
    n = len(list_1)

    for i in range(len(list_1)):
        x_sum += list_1[i]
        y_sum += list_1[i]

    x_avg = x_sum / n
    y_avg = y_sum / n

    xy_sum = 0
    x2_sum = 0
    y2_sum = 0

    for i in range(n):
        xy_sum += ((list_1[i] - x_avg) * (list_2[i] - y_avg))
        x2_sum += ((list_1[i] - x_avg) * (list_1[i] - y_avg))
        y2_sum += ((list_2[i] - x_avg) * (list_2[i] - y_avg))


    num = (n*xy_sum) - (x_sum*y_sum)
    denom = (math.sqrt((n * x2_sum) - (x_sum * x_sum)))*(math.sqrt(((n * y2_sum) - (y_sum * y_sum))))
    pccVal_my = num/denom

    return pccVal_my


#############################################
def getTimeStr():
    return "[" + str(datetime.now()) + "]"


if __name__ == "__main__":
    print(getTimeStr(), "Study Start")

    pccStudy()
    print(getTimeStr, "Study Finish")