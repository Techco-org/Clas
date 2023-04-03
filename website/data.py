from flask import Blueprint, Response
from .models import Img

data = Blueprint('data', __name__)

@data.route('/<user_id>/avatar')
def get_avatar_image(user_id):
    img = Img.query.filter_by(name=str(user_id)+'-avatar').first()
    if not img:
        return 'No image with this id', 404
    
    return Response(img.img, mimetype=img.mimetype)

@data.route('/<user_id>/background')
def get_background_image(user_id):
    img = Img.query.filter_by(name=str(user_id)+'-background').first()
    if not img:
        return 'No image with this id', 404
    
    return Response(img.img, mimetype=img.mimetype)
