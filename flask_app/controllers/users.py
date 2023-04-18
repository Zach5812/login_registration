from flask_app import app, render_template, redirect, request, session, flash, bcrypt
from flask_app.models.user import User


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route("/register", methods=['post'])
def register():
    print(request.form)
    if not User.validate_user(request.form):
        return redirect('/')
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])    
    temp_user = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hashed_pw
    }
    user = User.save(temp_user)
    session['user_id'] = user
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    
    
    return redirect('/dashboard')




@app.route('/login', methods=['post'])
def login():
    user = User.find_by_email(request.form['email'])
    if not user:
        flash("invalid credentials")
        return redirect('/')
    password_valid = bcrypt.check_password_hash(user.password, request.form['password'])
    if not password_valid:
        flash("invalid credentials")
        return redirect('/')
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')