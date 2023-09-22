from flask import Flask,render_template, url_for,request,redirect,flash
from flask_mysqldb import MySQL
app = Flask(__name__)
app.secret_key = "flash message"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'gbro7738'
app.config['MYSQL_DB'] = 'crud'

mysql = MySQL(app)

@app.route('/')
def home():
    
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    data =cur.fetchall()
    cur.close()
    
    return render_template('index.html', tasks = data)

@app.route('/insert', methods= ['POST'])
def insert():
    if request.method == "POST":
        name = request.form['tskname']
        description = request.form['dscr']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tasks (task_name,description) VALUES (%s,%s)", (name,description))
        mysql.connection.commit()
        return render_template('index.html')

@app.route('/crts')
def crts():
    return render_template('crts.html')


@app.route('/delete/<string:num_data>', methods = ['GET'])
def delete(num_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE num=%s", (num_data,))
    mysql.connection.commit()
    return render_template('index.html')



@app.route('/update/<string:num_data>',methods=['POST','GET'])
def update(num_data):

    if request.method == 'POST':
        name = request.form['tskname']
        description = request.form['dscr']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE tasks
               SET name=%s, description=%s, 
               WHERE num=%s
            """, (name,description, num_data))
        mysql.connection.commit()
        return render_template('index.html')
    

if __name__ == '__main__':
    app.run()