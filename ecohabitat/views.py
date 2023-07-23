from ecohabitat import app,db, bcrypt
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, current_user, logout_user, login_required
from ecohabitat.form import NewChallenge , Registration, Login
from ecohabitat.models import Challenge,UserProgress,User


@app.route('/')
@app.route('/home')
def home():
    title = "Home"
    # challenge = Challenge.query.
    return render_template('home.html' , title = title, challenge = challenge)

@app.route('/account')
def account():
    title = "Account"
    challenges= Challenge.query.all()
    return render_template('account.html',title=title,challenges = challenges)

@app.route('/challenge/<int:challenge_id>',methods = ['GET','POST'])
def challenge(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    return render_template('challenge.html',title = challenge.name , challenge=challenge)


@app.route('/create-challenge', methods = ['GET','POST'])
def new_challenge():
    form  =NewChallenge()
    if form.validate_on_submit():
        challenge = Challenge(name = form.name.data , description = form.description.data , duration = form.duration.data , points = form.points.data)
        db.session.add(challenge)
        db.session.commit()
        flash('New Challenge has been created ' , category='success')
        return redirect(url_for('adminDashboard'))
    return render_template('newChallenge.html', form = form , legend = 'Add Challenge')

@app.route('/delete-challenge/<int:challenge_id>' , methods = ['GET','POST'])
def delete_challenge(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    db.session.delete(challenge)
    db.session.commit()
    print('Successfully deleted')
    flash('Challenge has been deleted successfully!', 'success')

    return redirect(url_for('adminDashboard'))

@app.route('/edit-challenge/<int:challenge_id>' , methods = ['GET','POST'])
def edit_challenge(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    form = NewChallenge()
    if form.validate_on_submit():
        challenge.name = form.name.data
        challenge.description = form.description.data
        challenge.points = form.points.data
        challenge.duration = form.duration.data
        db.session.commit()
        flash('Your Challenge has been updated' , category='success')
        return redirect(url_for('adminDashboard'))
    elif request.method == 'GET':
        form.name.data = challenge.name
        form.description.data = challenge.description
        form.points.data = challenge.points
        form.duration.data = challenge.duration
    return render_template('newchallenge.html',title = 'Edit Challenge', form = form , legend = 'Edit Challenge')

    

@app.route('/AdminDashboard')
def adminDashboard():
    challenges = Challenge.query.all()
    return  render_template('adminDashboard.html', challenges = challenges)

@app.route('/UserDashboard')
def userDashboard():
    challenges = Challenge.query.all()
    return render_template('userDashboard.html', challenges = challenges)

@app.route('/register', methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Registration()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            flash('User Already Exist !!' , category='danger')
            return redirect(url_for('login'))
        else:
            hashed_password =bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user= User(username = form.username.data, email = form.email.data , password = hashed_password) 
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been successfully created', category='success')
            return redirect(url_for('login'))

    return render_template('register.html', form = form)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else (url_for('home'))
            else:
                flash('Incorrect Password',category='danger')
        else:
            flash("User doesn't exist",category="danger")
            return redirect(url_for('register'))
    return render_template('login.html',form = form , title = "Login")

@app.route('/logout', methods= ['GET','POST'])
@login_required
def logout():
    logout_user()
    flash('You are successfully logged out', category="success")
    return redirect(url_for('home'))


