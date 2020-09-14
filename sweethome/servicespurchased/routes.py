from decimal import Decimal

from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from operator import attrgetter
from sweethome import db
from sweethome.models import ServicesPurchased, VendorServices
from sweethome.servicespurchased.forms import ServicesPurchasedForm


servicespurchased = Blueprint('servicespurchased', __name__, template_folder='servicespurchased_templates')


@servicespurchased.route("/servicespurchased/new", methods=['GET', 'POST'])
@login_required
def new():
    form = ServicesPurchasedForm()
    form.home_id.choices = list(map(attrgetter('id','address'),current_user.homes))
    form.service_id.choices = VendorServices.query.with_entities(VendorServices.id, VendorServices.name).all()
    if form.validate_on_submit():
        servicepurchased = ServicesPurchased(name=form.name.data,
                                             purchase_date=form.purchase_date.data,
                                             purchase_price = form.purchase_price.data,
                                             warranty_enddate=form.warranty_enddate.data,
                                             home_id=form.home_id.data,
                                             service_id=form.service_id.data,
                                             vendor_id=current_user.id)
        db.session.add(servicepurchased)
        db.session.commit()
        flash('Your Service Purchase has been recorded!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_servicepurchased.html', title='New Service Purchase',
                           form=form, legend='New Service Purchase')


@servicespurchased.route("/servicespurchased/<int:service_id>")
def servicepurchased(service_id):
    servicepurchased = ServicesPurchased.query.get_or_404(service_id)
    form = ServicesPurchasedForm()
    form.home_id.choices = list(map(attrgetter('id','address'),current_user.homes))
    form.service_id.choices = VendorServices.query.with_entities(VendorServices.id, VendorServices.name).all()
    form.name.data = servicepurchased.name
    form.purchase_date.data = servicepurchased.purchase_date
    form.purchase_price.data = servicepurchased.purchase_price
    form.warranty_enddate.data = servicepurchased.warranty_enddate
    form.home_id.data = servicepurchased.home_id
    form.service_id.data = servicepurchased.service_id
    form.submit.label.text = 'Close'
    return render_template('create_servicepurchased.html',
                           form=form,
                           servicepurchased=servicepurchased)


@servicespurchased.route("/servicespurchased/<int:servicepurchased_id>/update", methods=['GET', 'POST'])
@login_required
def update_servicepurchased(service_id):
    servicepurchased = ServicesPurchased.query.get_or_404(service_id)
    if servicepurchased.vendor_id != current_user.id:
        abort(403)
    form = ServicesPurchasedForm()
    if form.validate_on_submit():
        servicepurchased.name = form.name.data
        servicepurchased.purchase_date = form.purchase_date.data.strftime('%Y-%m-%d')
        servicepurchased.purchase_price = form.purchase_price.data
        servicepurchased.warranty_enddate = form.warranty_enddate.data.strftime('%Y-%m-%d')
        servicepurchased.home_id = form.home_id.data
        servicepurchased.service_id = form.service_id.data
        db.session.commit()
        flash('Your Service Purchase has been updated!', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.name.data = servicepurchased.name
        form.purchase_date.data = servicepurchased.purchase_date
        form.purchase_price.data = servicepurchased.purchase_price
        form.warranty_enddate.data = servicepurchased.warranty_enddate
        form.home_id.data = servicepurchased.home_id
        form.service_id.data = servicepurchased.service_id
        form.submit.label.text = 'Update Service'
        all_services = VendorServices.query.get()
    return render_template('create_servicepurchased.html', title='Update Service',
                           form=form,
                           homes=current_user.homes,
                           services=all_services,
                           legend='Update Service')


@servicespurchased.route("/servicespurchased/<int:service_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_servicepurchased(service_id):
    servicepurchased = ServicesPurchased.query.get_or_404(service_id)
    if servicepurchased.vendor_id != current_user.id:
        abort(403)
    db.session.delete(servicepurchased)
    db.session.commit()
    flash('Your service purchase has been deleted!', 'success')
    return redirect(url_for('main.home'))
