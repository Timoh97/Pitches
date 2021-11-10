from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from ..models import User,Post, Comment, Upvote, Downvote
from flask_login import login_required,current_user
from .. import db
from .forms import PostForm, UpdateProfile, CommentForm


#views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data.
    '''
    post_form = PostForm()
    all_posts = Post.query.order_by(Post.date_posted).all()
    return render_template('index.html', posts = all_posts)



@main.route('/post', methods=['GET', 'POST'])
@login_required
def new_post():
    post_form = PostForm()
    if post_form.validate_on_submit():
        title = post_form.post_title.data
        category = post_form.category.data
        content = post_form.content.data
        new_post = Post(title=title, user=current_user, category=category, content=content)
        new_post.save_post()
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main.index'))

    else:
        all_posts = Post.query.order_by(Post.date_posted).all()

    return render_template('pitches.html', posts=all_posts,post_form = post_form)

@main.route('/post/<id>', methods=['GET', 'POST'])
@login_required
def post_details(id):
    
    comments = Comment.query.filter_by(post_id=id).all()
    posts = Post.query.get(id)
    if posts is None:
        abort(404)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            post_id=id,
            user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        form.content.data = ''
        flash('Your comment has been posted successfully!')
    return render_template('comments.html',post= posts, comment=comments, comment_form = form)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    return render_template("profile/profile.html", user = user)
@main.route('/user/<uname>/update',methods = ['GET','POST'])


@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile',uname=user.username))
    return render_template('profile/update.html',form =form)


# @main.route('/user/<uname>/update/pic',methods= ['POST'])
# @login_required
# def update_pic(uname):
#     user = User.query.filter_by(username = uname).first()
#     if 'photo' in request.files:
#         filename = photos.save(request.files['photo'])
#         path = f'photos/{filename}'
#         user.profile_pic_path = path
#         db.session.commit()
#     return redirect(url_for('main.profile',uname=uname))


@main.route('/like/<int:id>', methods=['GET', 'POST'])
@login_required
def like(id):
    posts = Post.query.get(id)
    if posts is None:
        abort(404)
   
    like = Upvote.query.filter_by(user_id=current_user.id, post_id=id).first()
    if like is not None:
        db.session.delete(like)
        db.session.commit()
        flash('You have successfully unlike the pitch!')
        return redirect(url_for('.index'))

    new_like = Upvote(
        user_id=current_user.id,
        post_id=id
    )
    db.session.add(new_like)
    db.session.commit()
    flash('You have successfully liked the pitch!')
    return redirect(url_for('.index'))


@main.route('/dislike/<int:id>', methods=['GET', 'POST'])
@login_required
def dislike(id):
    posts = Post.query.get(id)
    if posts is None:
        abort(404)
    dislike = Downvote.query.filter_by(
        user_id=current_user.id, post_id=id).first()
    if dislike is not None:
        db.session.delete(dislike)
        db.session.commit()
        flash('You have successfully undisliked the pitch!')
        return redirect(url_for('.index'))
    new_dislike = Downvote(
        user_id=current_user.id,
        post_id=id
    )
    db.session.add(new_dislike)
    db.session.commit()
    flash('You have successfully disliked the pitch!')
    return redirect(url_for('.index'))
