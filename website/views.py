from flask import Blueprint, render_template, request, redirect, url_for, Response
from flask_login import login_required, current_user
from . import db
from .models import User, Task, Img

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html' , user=current_user)

@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@views.route('/profile/edit-personal-data', methods=['GET', 'POST'])
@login_required
def edit_personal_data():
    if request.method == 'POST':
        current_user.fullname = request.form.get('name')
        current_user.bio = request.form.get('bio')
        current_user.city = request.form.get('city')
        current_user.country = request.form.get('country')
        current_user.url = request.form.get('url')

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
@login_required
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

@views.route('/user', methods=['POST', 'GET'])
def user():
    return redirect(url_for('views.profile'))