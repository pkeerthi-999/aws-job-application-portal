from flask import Flask, render_template, request, redirect
import pymysql
import boto3
import uuid

app = Flask(__name__)

db = pymysql.connect(
    host="YOUR_RDS_ENDPOINT",
    user="YOUR_DB_USER",
    password="YOUR_DB_PASSWORD",
    database="jobportal"
)

cursor = db.cursor()

s3 = boto3.client(
    "s3",
    region_name="YOUR_REGION",
    aws_access_key_id="YOUR_ACCESS_KEY",
    aws_secret_access_key="YOUR_SECRET_KEY"
)

BUCKET_NAME = "your-bucket-name"

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']

        sql = "INSERT INTO users(fullname, email, mobile, password) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (fullname, email, mobile, password))
        db.commit()
        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        sql = "SELECT * FROM users WHERE email=%s AND password=%s"
        cursor.execute(sql, (email, password))
        user = cursor.fetchone()

        if user:
            return redirect('/home')
        return "Invalid credentials"

    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/apply', methods=['POST'])
def apply():
    fullname = request.form['fullname']
    email = request.form['email']
    mobile = request.form['mobile']
    qualification = request.form['qualification']
    skills = request.form['skills']
    experience = request.form['experience']

    resume = request.files['resume']
    file_name = str(uuid.uuid4()) + ".pdf"

    s3.upload_fileobj(resume, BUCKET_NAME, file_name)

    resume_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{file_name}"

    sql = """INSERT INTO job_applications(fullname,email,mobile,qualification,skills,experience,resume_url)
    VALUES (%s,%s,%s,%s,%s,%s,%s)"""

    cursor.execute(sql, (fullname,email,mobile,qualification,skills,experience,resume_url))
    db.commit()

    return "Application Submitted"

if __name__ == '__main__':
    app.run(debug=True)
