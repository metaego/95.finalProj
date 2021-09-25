from datetime import datetime
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import diaryOcrMain

app = Flask(__name__, template_folder='templates')
userImgPath = "./static/userImg/"


@app.after_request
def set_response_headers(r):
    r.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    r.headers['Pragma'] = 'no-cache'
    r.headers['Expires'] = '0'
    return r

@app.route('/')
def mainResponse():
    print("[" + str(datetime.now()) + "] Server Request Income: '/'")
    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
def searchResponse():
    print("[" + str(datetime.now()) + "] Server Request Income: '/search'")

    resultHtmlStr = ""
    if request.method == 'POST':


        f = request.files['imgFile']
        fileName = request.form['id'] + "_" + f.filename
        f.save(userImgPath + secure_filename(fileName))
        print(">>> ", os.path.basename(fileName))

        # mamT server exec.
        # diaryOcrMain.startMamT(request.form['id'], userImgPath + secure_filename(fileName))
        # img path, result path

        resultHtmlStr = getSearchResultHtml(request.form, fileName)

    return resultHtmlStr

def getSearchResultHtml(requestForm, imgFileName):

    htmlStr = "<html>"
    htmlStr = htmlStr + "\n" + "<head>"
    htmlStr = htmlStr + "\n" + "</head>"
    htmlStr = htmlStr + "\n" + "<body>"
    htmlStr = htmlStr + "\n" + "아이디: " + requestForm['id']
    htmlStr = htmlStr + "\n" + "<br>"
    htmlStr = htmlStr + "\n" + "이미지 경로: " + userImgPath + imgFileName
    htmlStr = htmlStr + "\n" + "</body>"
    htmlStr = htmlStr + "\n" + "</html>"

    print(htmlStr)

    return htmlStr

##########################################
# Main Method
##########################################
if __name__ == "__main__":
    print("[" + str(datetime.now()) + "] Web Server Prepare..")
    app.run(host="127.0.0.1", port="8080")
    print("[" + str(datetime.now()) + "] Web Server is Stopped..")





