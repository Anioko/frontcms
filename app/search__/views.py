import operator

from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_ckeditor import upload_success
from flask_login import current_user, login_required
from flask_sqlalchemy import Pagination
from sqlalchemy import desc, func
from app.email import send_email
#from .forms import *
from ..utils import Struct

search = Blueprint('search', __name__)




@search.route('/search')
@login_required
def search():
    query = request.args.get('query')
    page = request.args.get('page')
    search_type = request.args.get('type')
    sort_by = request.args.get('sort_by')
    sort_dir = request.args.get('sort_dir')

    query = query if query is not None else ''
    page = page if page is not None else 1
    try:
        page = int(page)
    except:
        page = 1
    search_type = search_type if search_type is not None else ''
    sort_by = sort_by if sort_by is not None else ''
    sort_dir = sort_dir if sort_dir is not None else ''
    if len(query) < 3:
        flash("Search Query must be at least 3 characters", "error")
        return render_template("search/search_results.html", query=query, search_type=search_type, sort_by=sort_by,
                               sort_dir=sort_dir, results=[])
    results = []
    if search_type == '':
        
        user_results = User.query.whooshee_search(query, order_by_relevance=0).all()
        products_results = MProduct.query.whooshee_search(query, order_by_relevance=0).all()

        user_results_count = User.query.whooshee_search(query, order_by_relevance=0).count()
        products_results_count = MProduct.query.whooshee_search(query, order_by_relevance=0).count()

        all_results = user_results + products_results
        all_count = user_results_count + products_results_count
        results = sorted(all_results, key=operator.attrgetter("score"))
        results.reverse()
        results = results[(page-1)*40:page*40]
        paginator = Pagination(items=results, page=page, per_page=40, query=None, total=all_count)
        results = paginator

    elif search_type == 'people':
        results = User.query.whooshee_search(query, order_by_relevance=-1).paginate(page, per_page=40)
        # results = sorted(user_results, key=operator.attrgetter("score"))
    elif search_type == 'products':
        results = MProduct.query.whooshee_search(query, order_by_relevance=10).paginate(page, per_page=10)
        # results = sorted(products_results, key=operator.attrgetter("score"))

    return render_template("search/search_results.html", query=query, search_type=search_type, sort_by=sort_by,
                           sort_dir=sort_dir, results=results)








