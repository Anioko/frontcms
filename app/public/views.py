from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models import EditableHTML, SiteSetting
from .forms import SiteSettingForm, PostForm, CategoryForm, EditCategoryForm, StatusForm
import commonmark
from app import db
from app.decorators import admin_required
from app.models import BlogPost, BlogPostStatus
from app.models import BlogCategory
from app.models import Menu
from app.models import MenuItem
from .forms import EditMenuForm, EditMenuItemForm
#from .forms import PostForm, CategoryForm, EditCategoryForm
public = Blueprint('public', __name__)


@public.route('/')
def index():
    
    public = SiteSetting.query.limit(1).all()
    return render_template("public/public.html",public=public)

@public.route('/about')
def about():
    public = SiteSetting.find_all()
    return render_template("public/about.html",public=public)

@public.route('/all')
@login_required
@admin_required
def site_public():
    all_public = SiteSetting.query.all()
    return render_template("public/index.html",
                           public=all_public)


@public.route('/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_site_setting(id):
    form = SiteSettingForm()

    site_setting = db.session.query(SiteSetting).filter(SiteSetting.id==id).first()

    if(site_setting is None):
        abort(404)

    if form.validate_on_submit():
        site_setting.site_title = form.site_title.data
        site_setting.siteaddress= form.siteaddress.data
        site_setting.administration_user_address=form.administration_user_address.data
        site_setting.site_Language = form.site_Language.data

        db.session.add(site_setting)
        flash('"{0}" has been saved'.format(site_setting.site_title))

        return redirect(url_for('public.site_public'))

    form.site_title.data = site_setting.site_title
    form.siteaddress.data = site_setting.siteaddress
    form.administration_user_address.data= site_setting.administration_user_address
    form.site_Language.data=site_setting.site_Language

    return render_template("public/edit.html", form=form,
                           setting=site_setting)


@public.route('/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_site_setting():
    check_data_exists = SiteSetting.query.get(1)

    #if check_data_exists is  None :
       #return redirect(url_for('public.edit_site_setting',id=id))
    form = SiteSettingForm()

    if form.validate_on_submit():
        site_setting = SiteSetting()
        site_setting.site_title = form.site_title.data
        site_setting.siteaddress = form.siteaddress.data
        site_setting.administration_user_address =form.administration_user_address.data
        site_setting.site_Language = form.site_Language.data

        db.session.add(site_setting)
        flash('"{0}" has been saved'.format(site_setting.site_title))

        return redirect(url_for('public.site_public'))

    return render_template("public/new.html", form=form)


@public.route('/status/new', methods=['GET', 'POST'])
@login_required
@admin_required
def add_blog_status():
    form = StatusForm()

    if form.validate_on_submit():
        blog_post_status = BlogPostStatus()
        blog_post_status.name = form.name.data
        #blog_post_status.value = form.value.data

        db.session.add(blog_post_status)
        flash('"{0}" has been saved'.format(blog_post_status.name))

        return redirect(url_for('public.add_blog_post'))

    return render_template("public/add_blog_status.html", form=form)

@public.route('/delete/<int:id>')
@login_required
@admin_required
def delete_site_setting(id):
    setting = SiteSetting.query.filter_by(id=id).first()

    if(setting is not None):
        db.session.delete(setting)

        flash('"{0}" has been deleted.'.format(setting.site_title))
        return redirect(url_for('public.site_public'))

    flash('Setting does not exist')
    return redirect(url_for('public.site_public'))
    
@public.route('/posts', defaults={'page': 1})
@public.route('/posts/<int:page>')
@login_required
def blog_posts(page):
    the_posts = BlogPost.query.order_by(
        BlogPost.published_on.desc()).paginate(page, 5)
    return render_template('blog/posts/posts.html', js='posts/index', posts=the_posts)


@public.route('/posts/<post_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_blog_post(post_id):
    form = PostForm()
    post = BlogPost.query.filter_by(id=post_id).first()

    if post is None:
        abort(404)

    if form.validate_on_submit():
        post.slug = form.slug.data
        post.title = form.title.data
        post.content = form.content.data
        post.published_on = form.published_on.data
        post.blogcategory_id = form.category.data
        post.blogpoststatus_id = form.status.data

        db.session.add(post)
        flash('"{0}" has been saved'.format(post.title))

        return redirect(url_for('.blog_posts'))

    form.slug.data = post.slug
    form.title.data = post.title
    form.content.data = post.content
    form.published_on.data = post.published_on
    form.category.data = post.blogcategory_id
    form.status.data = post.blogpoststatus_id

    return render_template('blog/posts/edit_post.html', js='posts/edit_post', form=form, post=post)


@public.route('/posts/new', methods=['GET', 'POST'])
@login_required
@admin_required
def add_blog_post():
    form = PostForm()

    if form.validate_on_submit():
        post = BlogPost()

        post.slug = form.slug.data
        post.title = form.title.data
        post.content = form.content.data
        post.published_on = form.published_on.data
        post.user_id = current_user.id
        post.created_on = datetime.utcnow()
        post.blogcategory_id = form.category.data
        post.blogpoststatus_id = form.status.data

        db.session.add(post)
        flash('"{0}" has been saved'.format(post.title))

        return redirect(url_for('public.blog_posts'))

    return render_template('blog/posts/add_post.html', js='posts/add_post', form=form)


@public.route('/posts/delete/<post_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_blog_post(post_id):
    post = BlogPost.query.filter_by(id=post_id).first()

    if post is not None:
        db.session.delete(post)

        flash('"{0}" has been deleted.'.format(post.title))
        return redirect(url_for('.blog_posts'))

    flash('Post does not exist')
    return redirect(url_for('public.blog_posts'))


@public.route('/categories', defaults={'page': 1})
@public.route('/categories/<int:page>')
@login_required
@admin_required
def blog_categories(page):
    the_categories = BlogCategory.query.order_by(
        BlogCategory.name).paginate(page, 5)
    return render_template('blog/categories/categories.html', categories=the_categories)


@public.route('/categories/<int:category_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_blog_category(category_id):
    form = EditCategoryForm()
    category = BlogCategory.query.filter_by(id=category_id).first()

    if category is None:
        abort(404)

    if form.validate_on_submit():
        category.name = form.name.data
        category.slug = form.slug.data
        category.description = form.description.data

        db.session.add(category)
        flash('"{0}" has been saved'.format(category.name))

        return redirect(url_for('public.blog_categories'))

    form.name.data = category.name
    form.slug.data = category.slug
    form.description.data = category.description

    return render_template('blog/categories/edit_category.html',
                           js='posts/add_edit_category', form=form,
                           category=category)


@public.route('/categories/new', methods=['GET', 'POST'])
@login_required
@admin_required
def add_blog_category():
    form = EditCategoryForm()

    if form.validate_on_submit():
        category = BlogCategory()

        category.name = form.name.data
        category.slug = form.slug.data
        category.description = form.description.data
        category.created_on = datetime.utcnow()

        db.session.add(category)
        flash('"{0}" has been saved'.format(category.name))

        return redirect(url_for('public.blog_categories'))

    return render_template('blog/categories/add_category.html', js='posts/add_edit_category', form=form)


@public.route('/categories/delete/<int:category_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_blog_category(category_id):
    category = BlogCategory.query.filter_by(id=category_id).first()

    if category is not None:
        db.session.delete(category)

        flash('"{0}" has been deleted'.format(category.name))
        return redirect(url_for('public.blog_categories'))

    flash('Category does not exist')
    return redirect('public.blog_categories')
  
@public.route('/menu/')
@public.route('/menu')
@login_required
def menus():
    all_menus = Menu.query.all()
    return render_template('public/menus/menus.html', js='menus/menus', menus=all_menus)


@public.route('/menu/<int:menu_id>', methods=['GET', 'POST'])
@login_required
def menu(menu_id):
    the_menu = Menu.query.filter_by(id=menu_id).first()
    form = EditMenuForm()

    if the_menu is None:
        abort(404)

    if form.validate_on_submit():
        the_menu.name = form.name.data

        db.session.add(the_menu)
        flash("{0} has been saved".format(the_menu.name))

        return redirect(url_for('public.menus'))

    form.name.data = the_menu.name

    menu_items = the_menu.menu_items.order_by(MenuItem.weight)

    return render_template('public/menus/menu.html', js='menus/menu', form=form, menu=the_menu, menu_items=menu_items)

@public.route('/menu/new', methods=['GET', 'POST'])
@login_required
def add_menu():
    form = EditMenuForm()

    if form.validate_on_submit():
        the_menu = Menu()

        the_menu.name = form.name.data
        the_menu.created_on = datetime.utcnow()

        db.session.add(the_menu)
        flash("{0} has been created".format(the_menu.name))

        return redirect(url_for('public.menus'))

    return render_template("public/menus/new.html", js='menus/new', form=form)


@public.route('/menu/<int:menu_id>/delete')
@login_required
def delete_menu(menu_id):
    the_menu = Menu.query.filter_by(id=menu_id).first()

    if the_menu is not None:
        # Delete all menu items within this menu
        for item in the_menu.menu_items.all():
            db.session.delete(item)

        db.session.delete(the_menu)

        flash("{0} has been deleted".format(the_menu.name))
        return redirect(url_for("public.menus"))

    flash("That menu does not exist")
    return redirect(url_for("public.menus"))


@public.route('/menu/<int:menu_id>/item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def menu_item(menu_id, item_id):
    the_menu_item = MenuItem.query.filter_by(
        menu_id=menu_id, id=item_id).first()
    form = EditMenuItemForm()

    if form.validate_on_submit():
        the_menu_item.name = form.name.data
        the_menu_item.slug = form.slug.data
        the_menu_item.menu_id = form.menu.data
        the_menu_item.weight = form.weight.data

        items = MenuItem.query.filter_by(
            menu_id=menu_id, name=the_menu_item.name).all()
        for item in items:
            if item.id != the_menu_item.id:
                flash(
                    "Menu Item can't use the same name as another item in the same menu")
                return render_template("public/menus/menu-item/menu-item.html", form=form, menu_item=the_menu_item)

        db.session.add(the_menu_item)
        flash("{0} has been saved".format(the_menu_item.name))

        return redirect(url_for("public.menu", menu_id=the_menu_item.menu_id))

    form.name.data = the_menu_item.name
    form.slug.data = the_menu_item.slug
    form.menu.data = the_menu_item.menu_id
    form.weight.data = the_menu_item.weight

    return render_template("public/menus/menu-item/menu-item.html", js='menus/menu-item/menu-item', form=form,
                           menu_item=the_menu_item)


@public.route('/menu/<int:menu_id>/item/new', methods=['GET', 'POST'])
@login_required
def add_menu_item(menu_id):
    form = EditMenuItemForm()
    the_menu = Menu.query.filter_by(id=menu_id).first()

    if form.validate_on_submit():
        the_menu_item = MenuItem()

        the_menu_item.name = form.name.data
        the_menu_item.slug = form.slug.data
        the_menu_item.weight = form.weight.data
        the_menu_item.menu_id = form.menu.data
        the_menu_item.created_on = datetime.utcnow()

        items = MenuItem.query.filter_by(
            menu_id=menu_id, name=the_menu_item.name).all()
        if len(items) > 0:
            flash("Menu Item can't use the same name as another item in the same menu")
            return render_template("public/menus/menu-item/menu-item.html", form=form, menu_item=the_menu_item)

        db.session.add(the_menu_item)
        flash("{0} has been created".format(the_menu_item.name))

        return redirect(url_for("public.menu", menu_id=the_menu_item.menu_id))

    form.menu.data = menu_id

    return render_template("public/menus/menu-item/new.html", js='menus/menu-item/new', form=form, menu=the_menu)


@public.route('/menu/<int:menu_id>/item/<int:item_id>/delete')
@login_required
def delete_menu_item(menu_id, item_id):
    the_menu_item = MenuItem.query.filter_by(
        menu_id=menu_id, id=item_id).first()

    if the_menu_item is not None:
        db.session.delete(the_menu_item)

        flash("{0} has been deleted".format(the_menu_item.name))
        return redirect(url_for("public.menu", menu_id=menu_id))

    flash("That menu item doesn't exist")
    return redirect(url_for("public.menu", menu_id=menu_id))