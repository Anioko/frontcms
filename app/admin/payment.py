from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from app.models import PaymentSetting
from .forms import PaymentSettingForm
import commonmark
from app import db
from app.decorators import admin_required
from app.models import PaymentSetting
from app.admin.views import admin
from wtforms import Flags
#from .forms import PostForm, CategoryForm, EditCategoryForm




@admin.route('/payment_index')
def payment_index():
    return render_template("payment/index.html")

@admin.route('/payment/settings', methods=['GET', 'POST'])
@admin.route('/payment/settings/', methods=['GET', 'POST'])
@login_required
@admin_required
def payment_settings():
    if request.method == 'POST':
        for i in request.form.lists():
            s = PaymentSetting.query.filter_by(name=i[0]).first()
            if s:
                s.value = request.form.get(i[0])
                db.session.add(s)
                db.session.commit()
        flash("Changes saved successfully", "success")
        return redirect(url_for('admin.payment_settings'))
    c = PaymentSetting.query.count()
    if c == 0:
        PaymentSetting.insert_stripe()
    settings = PaymentSetting.query.order_by(PaymentSetting.id.asc()).all()
    return render_template('admin/payment/settings.html', settings=settings)



@admin.route('/payment/settings/stripe')
def insert_stripe():
    ''' The belowe insertions were used to insert some data '''
    stripe_settings = [
            ['stripe_public', 'Stripe Public Key'],
            ['stripe_secret', 'Stripe Secret Key']
        ]
    for s in stripe_settings:
        setting = PaymentSetting.query.filter_by(name=s[0]).first()
        if setting is None:
            setting = PaymentSetting(name=s[0], display_name=s[1])
            db.session.add(setting)
        db.session.commit()
    return redirect(url_for('admin.payment_settings'))

@admin.route('/payment/settings/paystack')
def insert_paystack():
    ''' The belowe insertions were used to insert some data '''
    paystack_settings = [
            ['paystack_public', 'Paystack Public Key'],
            ['paystack_secret', 'Paystack Secret Key']
        ]
    for s in paystack_settings:
        setting = PaymentSetting.query.filter_by(name=s[0]).first()
        if setting is None:
            setting = PaymentSetting(name=s[0], display_name=s[1])
            db.session.add(setting)
        db.session.commit()
    return redirect(url_for('admin.payment_settings'))




