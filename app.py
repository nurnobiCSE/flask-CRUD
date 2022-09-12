from flask import Flask,render_template, request, redirect, url_for, flash
import psycopg2
import psycopg2.extras

app = Flask(__name__)

db_host = "localhost" 
db_name = "flaskWeb"
db_user = "postgres"
db_pass = "admin"
conn = psycopg2.connect(dbname=db_name,user=db_user,password=db_pass,host=db_host)
@app.route("/")
def home():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    qry = "SELECT * FROM students"
    cur.execute(qry)
    all_data = cur.fetchall()
    return render_template('home.html',datas=all_data)
    
@app.route('/add_student', methods=['POST'])
def add_student():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        cur.execute("INSERT INTO students (fname, lname, email) VALUES (%s,%s,%s)", (fname, lname, email))
        conn.commit()
         
        return redirect(url_for('home'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_employee(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('SELECT * FROM students WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', student = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_student(id):
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
         
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE students
            SET fname = %s,
                lname = %s,
                email = %s
            WHERE id = %s
        """, (fname, lname, email, id))
         
        conn.commit()
        return redirect(url_for('home'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_student(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('DELETE FROM students WHERE id = {0}'.format(id))
    conn.commit()
    flash('Student Removed Successfully')
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run()