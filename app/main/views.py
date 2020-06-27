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
main = Blueprint('main', __name__)



@main.route('/about')
def about():
    public = SiteSetting.find_all()
    return render_template("public/public.html",public=public)

@main.route('/')
def index():
    return render_template("main/index.html")