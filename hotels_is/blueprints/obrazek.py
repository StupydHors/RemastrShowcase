import os

from flask import Blueprint, render_template, flash, url_for
from werkzeug.utils import redirect
from flask_login import current_user

from hotels_is import app
from hotels_is.blueprints.create import create_obrazek
from hotels_is.queries import *
from werkzeug.utils import secure_filename

obrazek = Blueprint('obrazek', __name__, template_folder='templates')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# show obrazek
@obrazek.route('/', methods=['GET'])
def obrazek_base():
    if not current_user.is_anonymous and (current_user.role == "Admin" or current_user.role == "Vlastník"):
        obrazky = []
        obrazky_db = Obrazek.query.all()
        for filename in os.listdir(os.path.join(app.root_path, 'static', 'uploads')):
            obrazky.append(filename)
        return render_template('obrazek/obrazek.html', obrazky=obrazky, obrazky_db=obrazky_db)
    else:
        return render_template('error.html', error_code=401, error_message="Neoprávněný přístup ke správě obrázků!")


@obrazek.route('/', methods=['POST'])
def upload_image():
    if not current_user.is_anonymous and (current_user.role == "Admin" or current_user.role == "Vlastník"):
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.root_path, 'static', 'uploads', filename))
            create_obrazek(filename)
            obrazky_db = Obrazek.query.all()
            return render_template('obrazek/obrazek.html', filename=filename, obrazky_db=obrazky_db)
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)
    
    else:
        return render_template('error.html', error_code=401, error_message="Nemáte oprávnění přídavat obrázky!")


@obrazek.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
