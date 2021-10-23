from datetime import datetime
import cv2
import copy
import dlib

faceDetectorOption = 'cv2' # cv2, dlib
imageOption = 'cam' # img, cam

opt_cv2Font = cv2.FONT_HERSHEY_SIMPLEX
opt_cv2FaceBoxColor = (0, 255, 0)   # Blue, Green, Red
detector_cv2_face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
detector_cv2_eye = cv2.CascadeClassifier('haarcascade_eye.xml')
detector_dlib_face = dlib.get_frontal_face_detector()


def detectFaceByDLib(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector_dlib_face(gray, 1)

    for f in faces:
        x1 = f.left()
        y1 = f.top()
        x2 = f.right()
        y2 = f.bottom()

        cv2.rectangle(frame, (x1, y1), (x2, y2), opt_cv2FaceBoxColor, 3, 4, 0)
        cv2.putText(frame, 'Detected Face', (x1 - 5, y1 - 5), opt_cv2Font, 0.9, (255, 255, 0), 2)

    return frame



def detectFaceByOpenCV(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector_cv2_face.detectMultiScale(gray, 1.02, 3, 0, (70, 70))

    filterFaces = []
    for (x, y, w, h) in faces:
        x1 = x
        y1 = y
        x2 = x+w
        y2 = y+h

        face_gray = gray[y1:y2, x1:x2]
        face_color = frame[y1:y2, x1:x2]

        existEye = False
        eyes = detector_cv2_eye.detectMultiScale(image=face_gray, scaleFactor=1.03, minNeighbors=7)
        for (ex, ey, ew, eh) in eyes:
            existEye = True
            cv2.rectangle(face_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)

        if existEye:
            filterFaces.append([x1, y1, x2, y2])

    finalFaces = getReducedFaces(filterFaces)


    for (x1, y1, x2, y2) in finalFaces:
        cv2.rectangle(frame, (x1, y1), (x2, y2), opt_cv2FaceBoxColor, 3, 4, 0)
        cv2.putText(frame, 'Detected Face', (x1 - 5, y1 - 5), opt_cv2Font, 0.5, (255, 255, 0), 2)

    return frame


def getReducedFaces(faces):
    filteredFaces = copy.deepcopy(faces)
    dupCnt = 0

    while True:
        i, j = existDuplicate(filteredFaces)
        if i==-1 and j==-1:
            break

        dupCnt = dupCnt + 1
        print("exist duplicate - {0}".format(dupCnt))

        filteredFaces = reduceFaces(copy.deepcopy(filteredFaces), i, j)

    return filteredFaces

def reduceFaces(faces, idx_1, idx_2):
    reducedFaces = []

    for i in range(len(faces)):
        if i==idx_1 or i==idx_2:
            continue

        reducedFaces.append(faces[i])


    new_x1 = min(faces[idx_1][0], faces[idx_2][0])
    new_y1 = min(faces[idx_1][1], faces[idx_2][1])
    new_x2 = max(faces[idx_1][2], faces[idx_2][2])
    new_y2 = max(faces[idx_1][3], faces[idx_2][3])
    reducedFaces.append([new_x1, new_y1, new_x2, new_y2])

    return copy.deepcopy(reducedFaces)

def existDuplicate(faces):
    ratioLimit = 0.4

    dupIdx_1 = -1
    dupIdx_2 = -1

    for i in range(len(faces)-1):
        for j in range(i + 1, len(faces)):
            x_diff1 = faces[i][2] - faces[j][0]
            x_diff2 = faces[j][2] - faces[i][0]
            y_diff1 = faces[i][3] - faces[j][1]
            y_diff2 = faces[j][3] - faces[i][1]

            if ((x_diff1 * x_diff2) > 0) and ((y_diff1 * y_diff2) > 0):
                dupArea = min(x_diff1, x_diff2) * min(y_diff1, y_diff2)
                i_area = (faces[i][2] - faces[i][0]) * (faces[i][3] - faces[i][1])
                j_area = (faces[j][2] - faces[j][0]) * (faces[j][3] - faces[j][1])

                if (dupArea / min(i_area, j_area)) > ratioLimit:
                    # print("exist duplicate", dupArea / min(i_area, j_area))
                    # print(min(faces[i][0], faces[j][0]), min(faces[i][1], faces[j][1]))
                    # print(min(faces[i][2], faces[j][2]), min(faces[i][3], faces[j][3]))
                    dupIdx_1 = i
                    dupIdx_2 = j
                    break

        if dupIdx_1 >= 0:
            break


    return dupIdx_1, dupIdx_2




def startImage():
    frame = cv2.imread("bts_sample_1.jpeg")

    if faceDetectorOption == 'cv2':
        processedFrame = detectFaceByOpenCV(frame)
    elif faceDetectorOption == 'dlib':
        processedFrame = detectFaceByDLib(frame)
    else:
        processedFrame = frame


    cv2.imshow("test", processedFrame)
    cv2.waitKey(0);


def startWebCam():

    webCam = cv2.VideoCapture(0)
    while True:

        # 1. 이미지를 받아 온다 (예. 웹캠으로부터, OpenCV)
        ret, frame = webCam.read()
        if not ret:
            return

        if faceDetectorOption == 'cv2':
            processedFrame = detectFaceByOpenCV(frame)
        elif faceDetectorOption == 'dlib':
            processedFrame = detectFaceByDLib(frame)
        else:
            processedFrame = frame



        # 4. 그려진 이미지를 보여준다.
        resizeFrame = cv2.resize(processedFrame, dsize=(0, 0), fx=0.7, fy=0.7, interpolation=cv2.INTER_AREA)
        cv2.imshow('Face Detection', resizeFrame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    webCam.release()
    cv2.destroyAllWindows()


###########################################################
# main execution
def getTimeStr():
    return "[" + str(datetime.now()) + "]"

if __name__ == "__main__":
    print(getTimeStr(), "Start - Face Recognition Example")

    if imageOption == 'img':
        startImage()
    elif imageOption == 'cam':
        startWebCam()

    print(getTimeStr(), "Finish - Face Recognition Example")