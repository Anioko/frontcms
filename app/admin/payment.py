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

@admin.route('/stripe', methods=['GET', 'POST'])
@login_required
@admin_required
def add_stripe_keys():
    """Add a new payment api key for a specific provider."""
    ''' check if key already exist, if it does, send to homepage. Avoid duplicate here'''
    check_key_exist = db.session.query(PaymentSetting).filter(PaymentSetting.name == 'stripe_public').count()
    key = PaymentSetting.query.get(1)
    if check_key_exist >= 1:
        return redirect(url_for('admin.edit_stripe_secret_keys'))
    
    form = PaymentSettingForm()
    if form.validate_on_submit():
        settings = PaymentSetting(
            name=form.name.data,
            display_name=form.display_name.data,
            value=form.value.data)
        db.session.add(settings)
        db.session.commit()
        flash('Key {} successfully created'.format(settings.name),
              'form-success')
        return redirect(url_for('admin.edit_stripe_secret_keys'))
    return render_template('payment/payment_keys.html', form=form)

@admin.route('/stripe/<id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_stripe_public_keys(id=None):
    """Add a new payment api key for a specific provider."""
    ''' check if key already exist, if it does, send to homepage. Avoid duplicate '''
    if id==None:
        key = PaymentSetting.query.get(1)
    else:
        key = PaymentSetting()
    form = PaymentSettingForm(request.form, obj=key)
    if form.validate_on_submit():
        form.populate_obj(key)
        db.session.add(key)
        db.session.commit()
        flash('Key {} successfully updated'.format(settings.name),
              'form-success')
    return render_template('admin/payment/settings.html', form=form, key=key)


@admin.route('/stripe/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_stripe_secret_keys():
    """Add a new payment api key for a specific provider."""
    ''' check if key already exist, if it does, send to homepage. Avoid duplicate '''
    key = PaymentSetting.query.filter_by(name='stripe_secret').all()
    form = PaymentSettingForm(request.form, obj=key)
    if form.validate_on_submit():
        form.populate_obj(key)
        db.session.add(key)
        db.session.commit()
        flash('Key {} successfully updated'.format(settings.name),
              'form-success')
    return render_template('payment/payment_keys.html', form=form)

@admin.route('/paystack', methods=['GET', 'POST'])
@login_required
@admin_required
def add_paystack_keys():
    ''' check if key already exist, if it does, send to homepage. Avoid duplicate here'''
    check_key_exist = db.session.query(PaymentSetting).filter(PaymentSetting.name == 'paystack_public').count()
    key = PaymentSetting.query.get(1)
    if check_key_exist >= 1:
        return redirect(url_for('admin.edit_paystack_keys', key_id = key.id))
    form = PaymentSettingForm()
    if form.validate_on_submit():
        settings = PaymentSetting(
            name=form.name.data,
            display_name=form.display_name.data,
            value=form.value.data)
        db.session.add(settings)
        db.session.commit()
        flash('Key {} successfully created'.format(settings.name),
              'form-success')
        return redirect(url_for('admin.edit_paystack_keys', key_id=key.id))
    return render_template('payment/payment_keys.html', form=form)

@admin.route('/paystack/<int:key_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_paystack_keys(key_id):
    """Add a new payment api key for a specific provider."""
    ''' check if photo already exist, if it does, send to homepage. Avoid duplicate upload here'''
    key = PaymentSetting.query.get(key_id)
    form = PaymentSettingForm(request.form, obj=key)
    if form.validate_on_submit():
        form.populate_obj(key)
        db.session.add(key)
        db.session.commit()
        flash('Key {} successfully updated'.format(settings.name),
              'form-success')
    return render_template('payment/payment_keys.html', form=form)


