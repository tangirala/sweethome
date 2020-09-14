from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required

from sweethome import db
from sweethome.models import VendorServices
from sweethome.vendorservices.forms import VendorServicesForm

vendorservices = Blueprint('vendorservices', __name__, template_folder='vendorservices_templates')

@vendorservices.route("/vendorservices/new", methods=['GET', 'POST'])
@login_required
def new_vendorservice():
    form = VendorServicesForm()
    if form.validate_on_submit():
        vendorservice = VendorServices(name=form.name.data, description=form.description.data, vendor_id=current_user.id)
        db.session.add(vendorservice)
        db.session.commit()
        flash('Your Service has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_vendorservice.html', title='New Service',
                           form=form, legend='New Service')


@vendorservices.route("/vendorservices/<int:service_id>")
def vendorservice(service_id):
    vendorservice = VendorServices.query.get_or_404(service_id)
    return render_template('vendorservice.html',
                           vendorserice=vendorservice)


@vendorservices.route("/vendorservices/<int:service_id>/update", methods=['GET', 'POST'])
@login_required
def update_vendorservice(service_id):
    vendorservice = VendorServices.query.get_or_404(service_id)
    if vendorservice.vendor_id != current_user.id:
        abort(403)
    form = VendorServicesForm()
    if form.validate_on_submit():
        vendorservice.name = form.name.data
        vendorservice.description = form.description.data
        db.session.commit()
        flash('Your Service has been updated!', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.name.data = vendorservice.name
        form.description.data = vendorservice.description
        form.submit.label.text = 'Update Service'
    return render_template('create_vendorservice.html', title='Update Service',
                           form=form, legend='Update Service')


@vendorservices.route("/vendorservices/<int:service_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_vendorservice(service_id):
    vendorservice = VendorServices.query.get_or_404(service_id)
    if vendorservice.vendor_id != current_user.id:
        abort(403)
    db.session.delete(vendorservice)
    db.session.commit()
    flash('Your service has been deleted!', 'success')
    return redirect(url_for('main.home'))
