from flask import render_template, request, Blueprint
from flask_login import current_user, login_required

from sweethome.models import Home, VendorServices

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    if current_user.user_type == 1:  # USER
        homes = Home.query.filter(Home.home_owner == current_user.id).order_by(
            Home.date_posted.desc())  # .paginate(page=page, per_page=5)
        return render_template('homes.html', homes=homes)
    else:
        services = VendorServices.query.filter(VendorServices.vendor_id == current_user.id)
        return render_template('vendorservices.html', vendorservices=services)


@main.route("/lists")
def lists():
    return render_template('lists.html', title='Lists')
