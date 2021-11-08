from flask import render_template, redirect, url_for, abort, flash, request
from . import main
from flask_login import login_required, current_user
 
from app.models import User, Post, Comment,Category
from .. import db, photos
from .forms import CategoryForm, PostForm
from slugify import slugify
 
 
 
@main.route('/')
def index():
   posts = Post.query.order_by(Post.date_posted.desc()).all()
   print(posts)
   return render_template('index.html', posts=posts)
 
@main.route('/category', methods=('GET', 'POST'))
 
def add_category():
   form = CategoryForm()
   if form.validate_on_submit():
       category = Category(name=form.name.data)
       db.session.add(category)
       db.session.commit()
       flash("Category added successfully.")
       return redirect(url_for('.index'))
   return render_template('category.html', form=form)
 
@main.route('/post', methods=('GET', 'POST'))
 
def post():
   form = PostForm()
   if form.validate_on_submit():
       post = Post(title=form.title.data, content = form.content.data, author = current_user)
       db.session.add(post)
       db.session.commit()
       flash('Your post has been created')
       return redirect(url_for('.index'))
   return render_template('post.html', form=form)