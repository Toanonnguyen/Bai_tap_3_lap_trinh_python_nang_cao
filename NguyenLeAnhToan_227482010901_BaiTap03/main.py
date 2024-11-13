from flask import Flask, render_template, request, redirect, url_for, flash, session
from login import connect_to_db, authenticate
from studentmanagement import create_table, get_students, add_student, update_student, delete_student, get_student_by_id, search_students

app = Flask(__name__)
app.secret_key = 'your_secret_key'

conn = connect_to_db()
if conn is None:
    print("Không kết nói được dữ liệu. Sẽ thoát sau 3s")
    exit()

create_table(conn)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate(username, password):
            session['logged_in'] = True
            flash('Bạn đã đăng nhập thành công.')
            return redirect(url_for('index'))
        else:
            flash('Tài khoản hoặc mật khẩu không chính xác! Vui long nhập lại.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Bạn đã đăng xuất thành công.')
    return redirect(url_for('login'))

@app.route('/index')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    students = get_students(conn)
    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    major = request.form['major']
    if name and age and gender and major:
        add_student(conn, name, age, gender, major)
        flash('Thêm học sinh thành công')
    else:
        flash('Vui lòng nhập đầy đủ thông tin.')
    return redirect(url_for('index'))

@app.route('/update/<int:student_id>', methods=['GET', 'POST'])
def update(student_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        major = request.form['major']
        if name and age and gender and major:
            update_student(conn, student_id, name, age, gender, major)
            flash('Cập nhật thành công')
        else:
            flash('Vui lòng nhập đầy đủ thông tin.')
        return redirect(url_for('index'))
    else:
        student = get_student_by_id(conn, student_id)
        return render_template('update.html', student=student)

@app.route('/delete/<int:student_id>')
def delete(student_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    delete_student(conn, student_id)
    flash('Xóa thành công')
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        search_term = request.form['search_term']
        students = search_students(conn, search_term)
        return render_template('index.html', students=students)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
