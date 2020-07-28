import operator

from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_ckeditor import upload_success
from flask_login import current_user, login_required
from flask_sqlalchemy import Pagination
from sqlalchemy import desc, func
from app.email import send_email
from .forms import *
from app.utils import Struct

notification = Blueprint('notification', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@notification.route('/notification/read/<notification_id>')
@login_required
def read_notification(notification_id):
    notification = current_user.notifications.filter_by(id=notification_id).first_or_404()
    notification.read = True
    db.session.add(notification)
    db.session.commit()
    if 'unread_message' in notification.name:
        user = User.query.filter_by(id=notification.related_id).first_or_404()
        link = url_for('notification.send_message', recipient=user.id, full_name=user.full_name)
##    elif 'post_likes' in notification.name:
##        user = User.query.filter_by(id=notification.related_id).first_or_404()
##        post = Post.query.filter_by(id=json.loads(notification.payload_json)['post']).first_or_404()
##        link = url_for('post.view_post', post_id=post.id)
##    elif 'post_replies' in notification.name:
##        user = User.query.filter_by(id=notification.related_id).first_or_404()
##        post = Post.query.filter_by(id=json.loads(notification.payload_json)['post']).first_or_404()
##        link = url_for('post.view_post', post_id=post.id)
##    elif 'answer' in notification.name:
##        user = User.query.filter_by(id=notification.related_id).first_or_404()
##        question = Question.query.filter_by(id=json.loads(notification.payload_json)['question']).first_or_404()
##        link = url_for('notification.question_details', question_id=question.id, title=question.title)
##    elif 'new_follower' in notification.name:
##        user = User.query.filter_by(id=notification.related_id).first_or_404()
##        link = url_for('notification.user', id=user.id, full_name=user.full_name)
##    elif 'new_post_of_followers' in notification.name:
##        post = Post.query.filter_by(id=json.loads(notification.payload_json)['post']).first()
##        link = url_for('post.view_post', post_id=post.id)
##    elif 'new_job' in notification.name:
##        job = Job.query.filter_by(id=json.loads(notification.payload_json)['job']).first()
##        link = url_for('jobs.job_details', position_id=job.id, position_title=job.position_title,
##                       position_city=job.position_city, position_state=job.position_state,
##                       position_country=job.position_country)

    return redirect(link)


@notification.route('/notifications/count')
@login_required
def notifications_count():
    notifications = Notification.query.filter_by(read=False).filter_by(user_id=current_user.id).count()
    messages = current_user.new_messages()

    return jsonify({
        'status': 1,
        'notifications': notifications,
        'messages': messages
    })


@notification.route('/notifications')
@login_required
def notifications():
    follow_lists = User.query.filter(User.id != current_user.id).order_by(func.random()).limit(10).all()
    jobs = Job.query.filter(Job.organisation != None).filter(Job.end_date >= datetime.now()).order_by(
        Job.pub_date.asc()).all()
    users = User.query.order_by(User.full_name).all()
    notifications = current_user.notifications.all()
    parsed_notifications = []
    for notification in notifications:
        parsed_notifications.append(notification.parsed())
    parsed_notifications = sorted(parsed_notifications, key=lambda i: i['time'])
    parsed_notifications.reverse()
    parsed_notifications = parsed_notifications[0:15]
    return render_template('notification/notifications.html', follow_lists=follow_lists, users=users, jobs=jobs,
                           notifications=parsed_notifications)


@notification.route('/notifications/more/<int:count>')
@login_required
def more_notifications(count):
    # follow_lists = User.query.filter(User.id != current_user.id).order_by(func.random()).limit(10).all()
    # jobs = Job.query.filter(Job.organisation != None).filter(Job.end_date >= datetime.now()).order_by(Job.pub_date.asc()).all()
    # users = User.query.order_by(User.full_name).all()
    notifications = current_user.notifications.all()
    print(len(notifications))
    parsed_notifications = []
    for notification in notifications:
        parsed_notifications.append(notification.parsed())
    parsed_notifications = sorted(parsed_notifications, key=lambda i: i['time'])
    parsed_notifications.reverse()
    if count == 0:
        parsed_notifications = parsed_notifications[0:15]
    elif count >= len(parsed_notifications):
        return "<br><br><h2>No more Notifications</h2>"
    else:
        parsed_notifications = parsed_notifications[count:count + 15]
    return render_template('notification/more_notifications.html', notifications=parsed_notifications)


@notification.route('/notification_test')
@login_required
def notification_test():
    n = Notification.query.get(379)
    related = User.query.get(32)
    extra = Job.query.get(17)
    extraextra = Answer.query.get(25)
    return render_template('account/email/notification.html', user=current_user, link="http://www.google.com",
                           notification=n, related=related, extra=extra,
                           extraextra=extraextra)


