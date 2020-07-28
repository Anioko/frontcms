from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from validate_email import validate_email

from app.models import BlogPost, BlogCategory, BlogTag, BlogComment, db, BlogNewsLetter
from app.utils import redirect_url

blog = Blueprint('blog', __name__)


@blog.route("/<int:page>", methods=['GET'])
@blog.route("/", defaults={'page': 1}, methods=['GET'])
def index(page):
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).paginate(page, per_page=10)
    categories = BlogCategory.query.order_by(BlogCategory.is_featured.desc()).order_by(BlogCategory.order.desc()).limit(10).all()
    tags = BlogTag.query.order_by(BlogTag.created_at.desc()).limit(10).all()
    return render_template("blog/index.html", posts=posts, categories=categories, tags=tags)


@blog.route('/categories/<int:page>', methods=['GET'])
@blog.route('/categories', defaults={'page': 1}, methods=['GET'])
def blog_categories(page):
    categories = BlogCategory.query.order_by(BlogCategory.is_featured.desc()).order_by(BlogCategory.order.desc()).paginate(page, per_page=40)
    return render_template("blog/categories/index.html", categories=categories)


@blog.route('/category/<int:category_id>/<int:page>', methods=['GET'])
@blog.route('/category/<int:category_id>', defaults={'page': 1}, methods=['GET'])
def blog_category(category_id, page):
    category = BlogCategory.query.get_or_404(category_id)
    posts = BlogPost.query.filter(BlogPost.categories.any(id=category.id)).order_by(BlogPost.created_at.desc()).paginate(page, per_page=40)
    return render_template("blog/categories/category.html", posts=posts, category=category)


@blog.route('/tag/<int:tag_id>/<int:page>', methods=['GET'])
@blog.route('/tag/<int:tag_id>', defaults={'page': 1}, methods=['GET'])
def blog_tag(tag_id, page):
    tag = BlogTag.query.get_or_404(tag_id)
    posts = BlogPost.query.filter(BlogPost.tags.any(id=tag.id)).order_by(BlogPost.created_at.desc()).paginate(page, per_page=40)
    return render_template("blog/categories/tag.html", posts=posts, tag=tag)


@blog.route('/article/<int:article_id>', methods=['GET'])
def blog_article(article_id):
    post = BlogPost.query.get_or_404(article_id)
    categories = post.categories
    tags = post.tags
    return render_template("blog/article.html", post=post, tags=tags, categories=categories)


@blog.route('/article/<int:article_id>/comment', methods=['POST'])
def add_comment(article_id):
    post = BlogPost.query.get_or_404(article_id)
    text = request.form['text']
    if not text:
        flash("Please insert comment text", 'danger')
        return redirect(url_for('blog.blog_article', article_id=article_id))
    parent_id = request.form['parent_id']
    if parent_id and parent_id != '0' and parent_id != 0:
        comment = BlogComment(
            post_id=post.id,
            text=text,
            user_id=current_user.id,
            parent_id=parent_id
        )
    else:
        comment = BlogComment(
            post_id=post.id,
            text=text,
            user_id=current_user.id,
        )
    db.session.add(comment)
    db.session.commit()
    flash("Comment added successfully", 'success')
    return redirect(url_for('blog.blog_article', article_id=article_id))


@blog.route('/sub', methods=['POST'])
def subscribe():
    email = request.form['email']
    if not email or not validate_email(email, check_mx=False):
        flash("Please enter a valid email", 'danger')
        return redirect(redirect_url())
    if BlogNewsLetter.query.filter_by(email=email).first():
        flash("You are already subscribed", 'danger')
        return redirect(redirect_url())

    sub = BlogNewsLetter(
        email=email,
    )
    db.session.add(sub)
    db.session.commit()
    flash('Subscription {} successfully added'.format(sub.email), 'success')
    return redirect(redirect_url())

