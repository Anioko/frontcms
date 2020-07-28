import operator

from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_ckeditor import upload_success
from flask_login import current_user, login_required
from flask_sqlalchemy import Pagination
from sqlalchemy import desc, func
from app.email import send_email
from .forms import *
from ..utils import Struct

invite = Blueprint('invite', __name__)



@invite.route('/invite-colleague', methods=['GET', 'POST'])
@login_required
def invite_user():
    """Invites a new user to create an account and set their own password."""

    form = InviteUserForm()
    if form.validate_on_submit():
        invited_by = db.session.query(User).filter_by(id=current_user.id).first()
        user = User(
            invited_by=invited_by.full_name,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        invite_link = url_for(
            'account.join_from_invite',
            user_id=user.id,
            token=token,
            _external=True)

        get_queue().enqueue(
            send_email,
            recipient=user.email,
            subject='You Are Invited To Join',
            template='account/email/invite',
            user=user.id,
            invited_by=invited_by,
            invite_link=invite_link,
            invite_by=invited_by
        )
        flash('User {} successfully invited'.format(user.full_name),
              'form-success')
        return redirect(url_for('invite.index'))
    return render_template('invite/new_user.html', form=form)












