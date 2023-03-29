from flask import Blueprint, render_template, request, redirect, url_for, Response
from flask_login import login_required, current_user

from datetime import datetime

from . import db
from .models import User, Task, Img, Grade, Licer

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return redirect(url_for('views.profile'))

@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@views.route('/profile/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.fullname = request.form.get('name')
        current_user.bio = request.form.get('bio')
        current_user.city = request.form.get('city')
        current_user.country = request.form.get('country')
        current_user.url = request.form.get('url')

        db.session.commit()
        return redirect(url_for('views.profile'))
    
@views.route('/profile/edit-basic-info', methods=['GET', 'POST'])
@login_required
def edit_basic_info():
    if request.method == 'POST':
        current_user.home_address = request.form.get('home-address')
        date_of_birth = request.form.get('date-of-birth')
        if date_of_birth:
            current_user.date_of_birth =  datetime.strptime(str(date_of_birth), '%Y-%m-%d')
        current_user.current_grade = request.form.get('current_grade')
        current_user.highschool = request.form.get('highschool')

        db.session.commit()
        return redirect(url_for('views.profile'))

@views.route('/profile/grade/new', methods=['GET', 'POST'])
@login_required
@login_required
def add_grading():
    if request.method == 'POST':
        subject = request.form.get('subject')
        overall = request.form.get('overall')
        grade = request.form.get('grade')
        new_grade = Grade(subject=subject, overall=overall, grade=grade, user_id=current_user.id)
        db.session.add(new_grade)
        db.session.commit()
        return redirect(url_for('views.profile'))

@views.route('/grade/delete/<grade_id>')
@login_required
def delete_grade(grade_id):
    grade = Grade.query.filter_by(id=grade_id).first()
    db.session.delete(grade)
    db.session.commit()
    return redirect(url_for('views.profile'))
 
@views.route('/license-certification/new', methods=['GET', 'POST'])
@login_required
def add_licer():
    if request.method == 'POST':
        licer_name = request.form.get('licer-name')
        organization = request.form.get('organization')
        issue_date = datetime.strptime(str(request.form.get('issue-date')), '%Y-%m-%d')
        expiration_date = request.form.get('expiration-date')
        credential_id = request.form.get('credential-id')
        credential_url = request.form.get('credential-url')
        if expiration_date:
            expiration_date = datetime.strptime(str(expiration_date), '%Y-%m-%d')
        else:
            expiration_date = None
        print(issue_date, expiration_date)
        new_licer = Licer(licer_name=licer_name, organization=organization, issue_date=issue_date, expiration_date=expiration_date, credential_id=credential_id, credential_url=credential_url, user_id=current_user.id)
        db.session.add(new_licer)
        db.session.commit()
        return redirect(url_for('views.profile'))


@views.route('/license-certification/delete/<licer_id>')
@login_required
def delete_licer(licer_id):
    licer = Licer.query.filter_by(id=licer_id).first()
    db.session.delete(licer)
    db.session.commit()
    return redirect(url_for('views.profile'))

@views.route('/profile/upload-personal-image', methods=['GET', 'POST'])
@login_required
def edit_personal_image():
    if request.method == 'POST':
        avt_img = request.files['avatar-image-input']
        bg_img = request.files['background-image-input']
        if avt_img:
            exist_avt = Img.query.filter_by(name=str(current_user.id)+'-avatar').first()
            if not exist_avt:
                avt_filename = str(current_user.id)+"-avatar"
                avt_minetype = avt_img.mimetype
                avt_img = Img(img=avt_img.read(), mimetype=avt_minetype, name=avt_filename)
                db.session.add(avt_img)
                db.session.commit()
            else:
                exist_avt.img = avt_img.read()
                db.session.commit()
        if bg_img:
            exist_bg = Img.query.filter_by(name=str(current_user.id)+'-background').first()
            if not exist_bg:
                bg_filename = str(current_user.id)+"-background"
                bg_minetype = bg_img.mimetype
                bg_img = Img(img=bg_img.read(), mimetype=bg_minetype, name=bg_filename)
                db.session.add(bg_img)
                db.session.commit()
            else:
                exist_bg.img = bg_img.read()
                db.session.commit()
        return redirect(url_for('views.profile'))
    
@views.route('/<user_id>_avatar')
def get_avatar_image(user_id):
    img = Img.query.filter_by(name=str(user_id)+'-avatar').first()
    if not img:
        return 'No image with this id', 404
    
    return Response(img.img, mimetype=img.mimetype)

@views.route('/<user_id>_background')
def get_background_image(user_id):
    img = Img.query.filter_by(name=str(user_id)+'-background').first()
    if not img:
        return 'No image with this id', 404
    
    return Response(img.img, mimetype=img.mimetype)

@views.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search')
    return redirect(url_for('views.search_result', query=search_query))

@views.route('/search-result/<query>')
def search_result(query):
    results = User.query.msearch(query).all()
    for user in results:
        print(user.fullname)
    return render_template('search.html', results=results)

@views.route('/user/<user_id>')
def user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return 'No user with this id', 404
    return render_template('user.html', user=user) 
