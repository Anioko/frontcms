from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from app.models import PaymentSetting
from .forms import PricingPlanForm
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
    return render_template('admin/pricingplan/settings.html', form=form)

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
    return render_template('admin/pricingplan/settings.html', form=form)

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
    return render_template('admin/pricingplan/settings.html', form=form)


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
    return render_template('admin/pricingplan/settings.html', form=form)

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
    return render_template('admin/pricingplan/settings.html', form=form)
