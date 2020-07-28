from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from app.models import Profile
from .forms import ProfileForm
import commonmark
from app import db
from app.decorators import admin_required
from app.models import User
from app.account.views import admin
from wtforms import Flags




@account.route('/profile/<int:user_id>/<full_name>/)
def profile(user_id, full_name):
    """Provide HTML page with all details on a given user """
    user_id = Photo.user_id
    photo = Photo.query.filter_by(id=user_id, full_name=full_name).limit(1).all()
    return render_template('account/profile.html', user=user, current_user=current_user, photo=photo, id=User.id)


@account.route('/manage/update-profile', methods=['GET', 'POST'])
@login_required
def change_profile_details():
    """Respond to existing user's request to change their profile details."""
    user_instance = current_user
    form = ChangeProfileForm(obj=user_instance)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(user_instance)
            db.session.add(user_instance)
            if request.files['photo']:
                image_filename = images.save(request.files['photo'])
                image_url = images.url(image_filename)
                picture_photo = Photo.query.filter_by(user_id=current_user.id).first()
                if not picture_photo:
                    picture_photo = Photo(
                        image_filename=image_filename,
                        image_url=image_url,
                        user_id=current_user.id,
                    )
                else:
                    picture_photo.image_filename = image_filename
                    picture_photo.image_url = image_url
                db.session.add(picture_photo)
            db.session.commit()
            flash('You have successfully updated your profile',
                  'success')
            return redirect(url_for('account.change_profile_details'))
        else:
            flash('Unsuccessful.', 'warning')
    return render_template('account/manage.html', form=form)
