from flask import Flask, render_template, request, redirect, session, flash, url_for
import database

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Initialize database on startup
with app.app_context():
    database.init_db()

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not username or not email or not password:
            flash('All fields are required')
            return redirect('/signup')
        
        user_id = database.create_user(username, email, password)
        
        if user_id:
            session['user_id'] = user_id
            session['username'] = username
            return redirect('/dashboard')
        else:
            flash('Username or email already exists')
            return redirect('/signup')
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = database.get_user_by_username(username)
        
        if user and database.verify_password(user, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect('/dashboard')
        else:
            flash('Invalid username or password')
            return redirect('/login')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    
    jobs = database.get_jobs_by_user(session['user_id'])
    return render_template('dashboard.html', jobs=jobs, username=session['username'])

@app.route('/add_job', methods=['POST'])
def add_job():
    if 'user_id' not in session:
        return redirect('/login')
    
    company = request.form.get('company')
    position = request.form.get('position')
    date_applied = request.form.get('date_applied')
    status = request.form.get('status')
    notes = request.form.get('notes', '')
    url = request.form.get('url', '')
    
    database.create_job(session['user_id'], company, position, date_applied, status, notes, url)
    
    return redirect('/dashboard')

@app.route('/edit_job/<int:job_id>', methods=['POST'])
def edit_job(job_id):
    if 'user_id' not in session:
        return redirect('/login')
    
    company = request.form.get('company')
    position = request.form.get('position')
    date_applied = request.form.get('date_applied')
    status = request.form.get('status')
    notes = request.form.get('notes', '')
    url = request.form.get('url', '')
    
    database.update_job(job_id, company, position, date_applied, status, notes, url)
    
    return redirect('/dashboard')

@app.route('/delete_job/<int:job_id>')
def delete_job(job_id):
    if 'user_id' not in session:
        return redirect('/login')
    
    database.delete_job(job_id)
    
    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(debug=True)
