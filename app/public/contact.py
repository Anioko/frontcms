from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from validate_email import validate_email

from app import db, recaptcha
from app.blueprints.account.forms import ContactForm
from app.libs.spam_detector import SpamDetector
from app.models import EditableHTML, ContactMessage
from app.blueprints.public.forms import PublicContactForm



@public.route('/contact', methods=['GET', 'POST'])
def contact():
    if current_user.is_authenticated:
        form = ContactForm()
    else:
        form = PublicContactForm()
    editable_html_obj = EditableHTML.get_editable_html('contact')
    if request.method == 'POST':
        if form.validate_on_submit():
            if not recaptcha.verify():
                flash("Wrong Captcha, pls try again", 'error')
                return redirect(url_for("public.contact"))
            spam_detect = SpamDetector()

            if current_user.is_authenticated:
                spam_detect.setMessage(form.text.data)
                text_spam = spam_detect.predict()
                spam = False
                if 1 in text_spam:
                    spam = True
                contact_message = ContactMessage(
                    user_id=current_user.id,
                    text=form.text.data,
                    spam=spam
                )
            else:
                spam_detect.setMessage(form.name.data)
                name_spam = spam_detect.predict()
                spam_detect.setMessage(form.text.data)
                text_spam = spam_detect.predict()
                spam = False
                if 1 in name_spam or 1 in text_spam:
                    spam = True
                email = form.email.data
                is_valid = validate_email(email, check_mx=False)
                if not is_valid:
                    flash("The email you entered doesn't exist, pls insert a valid email", 'error')
                    return redirect(url_for("public.contact"))
                contact_message = ContactMessage(
                    name=form.name.data,
                    email=email,
                    text=form.text.data,
                    spam=spam
                )
            db.session.add(contact_message)
            db.session.commit()
            flash('Successfully sent contact message.', 'success')
            return redirect(url_for('public.contact'))
    return render_template('public/contact.html', editable_html_obj=editable_html_obj, form=form)

