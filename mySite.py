from flask import Flask, render_template, redirect, url_for, request,session,Response
from werkzeug import secure_filename
import os
import cv2
from detect import *
import pandas as pd
from datetime import datetime
import sqlite3

login_status = 0 

app = Flask(__name__)

app.secret_key = '1234'
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/home', methods=['GET', 'POST'])
def home():
	return redirect(url_for('input'))

@app.route('/input', methods=['GET', 'POST'])
def input():
	
	if request.method == 'POST':
		if request.form['sub']=='Submit':
			num = request.form['num']
			
			users = {'Name':request.form['name'],'Email':request.form['email'],'Contact':request.form['num']}
			df = pd.DataFrame(users,index=[0])
			df.to_csv('users.csv',mode='a',header=False)

			sec = {'num':num}
			df = pd.DataFrame(sec,index=[0])
			df.to_csv('secrets.csv')

			name = request.form['name']
			num = request.form['num']
			email = request.form['email']
			password = request.form['password']
			age = request.form['age']
			gender = request.form['gender']

			now = datetime.now()
			dt_string = now.strftime("%d/%m/%Y %H:%M:%S")			
			con = sqlite3.connect('mydatabase.db')
			cursorObj = con.cursor()
			cursorObj.execute("CREATE TABLE IF NOT EXISTS Users (Date text,Name text,Contact text,Email text,password text,age text,gender text)")
			cursorObj.execute("INSERT INTO Users VALUES(?,?,?,?,?,?,?)",(dt_string,name,num,email,password,age,gender))
			con.commit()

			return redirect(url_for('login'))

	return render_template('input.html')


@app.route('/', methods=['GET', 'POST'])
def login():
	error = None
	global video
	global name
	if request.method == 'POST':
		name = request.form['name']
		password = request.form['password']
		con = sqlite3.connect('mydatabase.db')
		cursorObj = con.cursor()
		cursorObj.execute(f"SELECT Name from Users WHERE Name='{name}' AND password = '{password}';")

	
		if(cursorObj.fetchone()):
			return redirect(url_for('image'))
		else:
			error = "Invalid Credentials Please try again..!!!"
	return render_template('login.html',error=error)

@app.route('/image', methods=['GET', 'POST'])
def image():
    global save_path
    upload_message = None  
    if request.method == 'POST':
        if request.form['sub'] == 'Upload':
            savepath = r'upload/'
            photo = request.files['photo']
            if photo.filename == '':
                upload_message = "Upload the image first"  
                return render_template('image.html', upload_message=upload_message)
            else:
                photo.save(os.path.join(savepath, (secure_filename(photo.filename))))
                image = cv2.imread(os.path.join(savepath, secure_filename(photo.filename)))
                cv2.imwrite(os.path.join("static/images/", "test.jpg"), image)
                return render_template('image.html')
        elif request.form['sub'] == 'Test':
            save_path= run(**vars(opt))
            return redirect(url_for('result'))
    return render_template('image.html', upload_message=upload_message)  

@app.route('/result', methods=['GET', 'POST'])
def result():
	return render_template('result.html', save_path=save_path)

@app.route('/results', methods=['GET'])
def resultset():
	result_files = get_sorted_results()
	return render_template('resultset.html', result_files=result_files)

def get_sorted_results():
    result_dir = 'static/runs/detect'
    folders = os.listdir(result_dir)
    sorted_results = []
    for folder in folders:
        folder_path = os.path.join(result_dir, folder)
        if os.path.isdir(folder_path):
            images = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
            images.sort()  # Sort images alphabetically
            # Take the first 25 images if there are more than 25
            images = images[:25]
            sorted_results.append({'folder': folder, 'images': images})
    return sorted_results

@app.after_request
def add_header(response):
	response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
	response.headers['Pragma'] = 'no-cache'
	response.headers['Expires'] = '-1'
	return response


if __name__ == '__main__' and run:
	app.run(host='0.0.0.0', debug=True, threaded=True)