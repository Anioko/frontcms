from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from app.models import PaymentSetting, TransactionFee
from .forms import PricingPlanForm, TransactionFeeForm
import commonmark
from app import db
from app.decorators import admin_required
from app.models import PricingPlan
from app.admin.views import admin
from wtforms import Flags
#from .forms import PostForm, CategoryForm, EditCategoryForm


@admin.route('/pricing/plan')
@login_required
@admin_required
def pricing_plan_index():
    """pricing plan dashboard page."""
    return render_template('admin/pricingplan/index.html')


@admin.route('/pricing/settings/free', methods=['GET', 'POST'])
@admin.route('/pricing/settings/free/', methods=['GET', 'POST'])
@login_required
@admin_required
def free_pricing_plan_settings():
    appt = db.session.query(PricingPlan).count()
    appts = db.session.query(PricingPlan).get(1)   
    if appt >= 1 :
        return redirect(url_for('admin.edit_pricing_plan_settings', id=appts.id))
        
    form = PricingPlanForm()
    if request.method == 'POST' and form.validate():
        appt = PricingPlan()
        form.populate_obj(appt)
        db.session.add(appt)
        db.session.commit()
        flash("Changes saved successfully", "success")
        return redirect(url_for('admin.edit_pricing_plan_settings', id=appt.id))
    return render_template('admin/pricingplan/pricingplan.html', form=form)

@admin.route('/pricing/settings/<int:id>/edit', methods=['GET', 'POST'])
@admin.route('/pricing/settings/<int:id>/edit/', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_pricing_plan_settings(id):
    appt = PricingPlan.query.get(id)
    form = PricingPlanForm(obj=appt)
    if request.method == 'POST' and form.validate():
        form.populate_obj(appt)
        db.session.add(appt)
        db.session.commit()
        flash("Changes saved successfully", "success")
        return redirect(url_for('admin.pricing_plan_index'))
    return render_template('admin/pricingplan/pricingplan.html', form=form)

@admin.route('/pricing/settings/basic', methods=['GET', 'POST'])
@admin.route('/pricing/settings/basic/', methods=['GET', 'POST'])
@login_required
@admin_required
def basic_pricing_plan_settings():

    appt = db.session.query(PricingPlan).filter_by(name='Basic').count()
    appts = db.session.query(PricingPlan).get(2)   
    if appt >= 1 :
        return redirect(url_for('admin.edit_pricing_plan_settings', id=appts.id))
    
    form = PricingPlanForm()
    if form.validate_on_submit():
        appt = PricingPlan(
            name=form.name.data,
            duration=form.duration.data,
            cost=form.cost.data,
           currency_symbol=form.currency_symbol.data)
        db.session.add(appt)
        db.session.commit()
        
        flash("Changes saved successfully", "success")
        return redirect(url_for('admin.edit_pricing_plan_settings', id=appt.id))
    return render_template('admin/pricingplan/pricingplan.html', form=form)


@admin.route('/pricing/settings/pro', methods=['GET', 'POST'])
@admin.route('/pricing/settings/pro/', methods=['GET', 'POST'])
@login_required
@admin_required
def pro_pricing_plan_settings():

    appt = db.session.query(PricingPlan).filter_by(name='Pro').count()
    appts = db.session.query(PricingPlan).get(3)   
    if appt >= 1 :
        return redirect(url_for('admin.edit_pricing_plan_settings', id=appts.id))
    form = PricingPlanForm()
    if form.validate_on_submit():
        appt = PricingPlan(
            name=form.name.data,
            duration=form.duration.data,
            cost=form.cost.data,
           currency_symbol=form.currency_symbol.data)
        db.session.add(appt)
        db.session.commit()
        
        flash("Changes saved successfully", "success")
        return redirect(url_for('admin.edit_pricing_plan_settings', id=appt.id))
    return render_template('admin/pricingplan/pricingplan.html', form=form)

@admin.route('/pricing/settings/gold', methods=['GET', 'POST'])
@admin.route('/pricing/settings/gold/', methods=['GET', 'POST'])
@login_required
@admin_required
def gold_pricing_plan_settings():
    appt = db.session.query(PricingPlan).filter_by(name='Gold').count()
    appts = db.session.query(PricingPlan).get(4)   
    if appt >= 1 :
        return redirect(url_for('admin.edit_pricing_plan_settings', id=appts.id))
    
    form = PricingPlanForm()
    if form.validate_on_submit():
        appt = PricingPlan(
            name=form.name.data,
            duration=form.duration.data,
            cost=form.cost.data,
           currency_symbol=form.currency_symbol.data)
        db.session.add(appt)
        db.session.commit()
        
        flash("Changes saved successfully", "success")
        return redirect(url_for('admin.edit_pricing_plan_settings', id=appt.id))
    return render_template('admin/pricingplan/pricingplan.html', form=form)


@admin.route('/transaction/settings/stripe', methods=['GET', 'POST'])
@admin.route('/transaction/settings/stripe/', methods=['GET', 'POST'])
@login_required
@admin_required
def stripe_transaction_fee_settings():
    appt = db.session.query(TransactionFee).count()
    appts = db.session.query(TransactionFee).get(1)   
    if appt >= 1 :
        return redirect(url_for('admin.edit_transaction_fee_settings', id=appts.id))
        
    form = TransactionFeeForm()
    if request.method == 'POST' and form.validate():
        appt = TransactionFee()
        form.populate_obj(appt)
        db.session.add(appt)
        db.session.commit()
        flash("Changes saved successfully", "success")
        return redirect(url_for('admin.edit_transaction_fee_settings', id=appt.id))
    return render_template('admin/pricingplan/transactionfee.html', form=form)

@admin.route('/transaction/settings/<int:id>/edit', methods=['GET', 'POST'])
@admin.route('/transaction/settings/<int:id>/edit/', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_transaction_fee_settings(id):
    appt = TransactionFee.query.get(id)
    form = TransactionFeeForm(obj=appt)
    if request.method == 'POST' and form.validate():
        form.populate_obj(appt)
        db.session.add(appt)
        db.session.commit()
        flash("Changes saved successfully", "success")
        return redirect(url_for('admin.pricing_plan_index'))
    return render_template('admin/pricingplan/transactionfee.html', form=form)

@admin.route('/transaction/settings/paystack', methods=['GET', 'POST'])
@admin.route('/transaction/settings/paystack/', methods=['GET', 'POST'])
@login_required
@admin_required
def paystack_transaction_fee_settings():
    appt = db.session.query(TransactionFee).filter_by(name='Paystack').count()
    appts = db.session.query(TransactionFee).get(2)   
    if appt >= 1 :
        return redirect(url_for('admin.edit_transaction_fee_settings', id=appts.id))
    
    form = TransactionFeeForm()
    if form.validate_on_submit():
        appt = TransactionFee(
            provider_name=form.provider_name.data,
            local_fee=form.local_fee.data,
            european_fee=form.european_fee.data,
            international_fee=form.international_fee.data,
            transfer_fee=form.transfer_fee.data,
            local_percentage=form.local_percentage.data,
            european_percentage=form.european_percentage.data,
            international_percentage=form.international_percentage.data,
            our_percentage=form.our_percentage.data,
            currency_symbol=form.currency_symbol.data,
           our_fee=form.our_fee.data)
        db.session.add(appt)
        db.session.commit()
        
        flash("Changes saved successfully", "success")
        return redirect(url_for('admin.edit_transaction_plan_settings', id=appt.id))
    return render_template('admin/pricingplan/transactionfee.html', form=form)
