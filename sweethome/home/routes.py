import os

from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, current_app)
from flask_login import current_user, login_required

from sweethome import db
from sweethome.home.forms import HomeForm, DocumnentUploadForm
from sweethome.models import Home, Documents
from werkzeug.utils import secure_filename

homes = Blueprint('home', __name__, template_folder='home_templates')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@homes.route("/home/new", methods=['GET', 'POST'])
@login_required
def new_home():
    form = HomeForm()
    if form.validate_on_submit():
        home = Home(address=form.address.data,
                    city=form.city.data,
                    home_owner=current_user.id,
                    state = form.state.data,
                    zipcode = form.zipcode.data,
                    year_built = form.year_built.data,
                    zillow_url = form.zillow_url.data,
                    date_posted = form.date_posted.data)
        new_home = home.query.filter_by(address = home.address, city = home.city,state = home.state, zipcode = home.zipcode).first()
        if new_home is None:
            db.session.add(home)
            db.session.commit()
            flash('Your Home has been created!', 'success')
            return redirect(url_for('main.home'))


        else:
            flash('This home already exists')
            return render_template('create_home.html', title='New Home',
                           form=form, legend='New Home', error = 'error')
    return render_template('create_home.html', title='New Home',
                           form=form, legend='New Home')


@homes.route("/home/<int:home_id>")
def home(home_id):
    thishome = Home.query.get_or_404(home_id)
    return render_template('home.html',
                           home=thishome)


@homes.route("/home/<int:home_id>/update", methods=['GET', 'POST'])
@login_required
def update_home(home_id):
    home = Home.query.get_or_404(home_id)
    if home.home_owner != current_user.id:
        abort(403)
    form = HomeForm()
    if form.validate_on_submit():
        home.address = form.address.data
        home.address2 = form.address2.data
        home.city = form.city.data
        home.state = form.state.data
        home.zipcode = form.zipcode.data
        home.year_built = form.year_built.data
        home.zillow_url = form.zillow_url.data
        db.session.commit()
        flash('Your home has been updated!', 'success')
        return redirect(url_for('home.home', home_id=home.id))
    elif request.method == 'GET':
        form.address.data = home.address
        form.address2.data = home.address2
        form.city.data = home.city
        form.state.data = home.state
        form.zipcode.data = home.zipcode
        form.year_built.data = home.year_built
        form.zillow_url.data = home.zillow_url
        form.date_posted.data = home.date_posted
        form.submit.label.text = 'Update Home'
    return render_template('create_home.html', title='Update Home',
                           form=form, legend='Update Home')


@homes.route("/home/<int:home_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_home(home_id):
    home = Home.query.get_or_404(home_id)
    if home.home_owner != current_user.id:
        abort(403)
    db.session.delete(home)
    db.session.commit()
    flash('Your home has been deleted!', 'success')
    return redirect(url_for('main.home'))


@homes.route("/home/<int:home_id>/upload", methods=['GET', 'POST'])
@login_required
def upload_docs(home_id):
    home = Home.query.get_or_404(home_id)
    if home.home_owner != current_user.id:
        abort(403)
    form = DocumnentUploadForm()
    if form.validate_on_submit():
        if form.file.data:
            filepath = os.path.join(current_app.root_path, 'static', current_user.username, form.filename.data)
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(filepath)
            document = Documents(location=filename, home_id=home.id)
            db.session.save(document)
            db.session.commit()
        flash('Your Document uploaded!', 'success')
        return redirect(url_for('home.home',home_id=home.id))
    flash('Your Document upload failed!', 'failure')
    return redirect(request.url)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
