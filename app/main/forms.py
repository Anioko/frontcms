from flask import url_for
from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.fields import (
    BooleanField,
    StringField,
    SubmitField,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length
from wtforms import StringField, SelectField, DateTimeField, IntegerField
#from app.wtform_widgets import MarkdownField
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired, Length
from app.models import BlogCategory
from app.models import BlogPostStatus
from app.models import Page
from app.models import BlogPost
from app.models import Menu
from app.models import MenuItem
from flask_wtf import Form

#from app.models import User


class SiteSettingForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), \
                        Length(min=1, max=128)])
    value = StringField("Value", validators=[InputRequired()])
    submit = SubmitField('Submit')
    

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 128)])
    slug = StringField('Slug/Url', validators=[DataRequired(), Length(1, 256)])
    content = PageDownField('Content')
    published_on = DateTimeField('Published On', validators=[DataRequired()])
    category = SelectField('Category', coerce=int)
    status = SelectField('Status', coerce=int)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        self.category.choices = [(category.id, category.name)
                                 for category in BlogCategory.query.order_by(BlogCategory.name)]
        self.status.choices = [(status.id, status.name)
                               for status in BlogPostStatus.query.order_by(BlogPostStatus.name)]


class CategoryForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(1, 64)])
    slug = StringField('Slug/Url', validators=[DataRequired(), Length(1, 256)])
    description = StringField("Description", validators=[Length(1, 512)])
    submit = SubmitField('Submit')

class EditCategoryForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(1, 64)])
    slug = StringField('Slug/Url', validators=[DataRequired(), Length(1, 256)])
    description = StringField("Description", validators=[Length(1, 512)])
    submit = SubmitField('Submit')
    
class StatusForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), \
                        Length(min=1, max=128)])
    #value = StringField("Value", validators=[InputRequired()])
    submit = SubmitField('Submit')
    
  
class EditMenuForm(Form):
    name = StringField('Menu Name', validators=[DataRequired(), Length(1, 32)])
    submit = SubmitField('Submit')
    
    def validate_name(self, field):
        if MenuItem.query.filter_by(name=field.data).first():
            raise ValidationError('Menu Name is already in use')


class EditMenuItemForm(Form):
    name = StringField('Menu Item Name', validators=[DataRequired(), Length(1, 32)])
    menu = SelectField('Menu', coerce=int)
    slug = SelectField('Url')
    weight = IntegerField('Item Weight')
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(EditMenuItemForm, self).__init__(*args, **kwargs)

        self.menu.choices = [(menu.id, menu.name)
                             for menu in Menu.query.order_by(Menu.name)]

        pageslugs = [("/{0}".format(page.slug)) for page in Page.query.filter_by(is_homepage=False).order_by(Page.slug)]
        blogslugs = [("/blog/post/{0}".format(post.slug)) for post in BlogPost.query.order_by(BlogPost.slug)]
        slugs = ["/"] + pageslugs + ["/blog"] + blogslugs
        self.slug.choices = [(slug, slug) for slug in slugs]