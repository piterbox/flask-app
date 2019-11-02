from flask import Blueprint
from flask import render_template
from models import Post, Tag
from flask import request
from .forms import PostForm
from app import db
from flask import redirect
from flask import url_for
from flask_security import login_required

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/')
def index():
    search = request.args.get('search')
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    if search:
        posts = Post.query.filter(Post.title.contains(search) | Post.content.contains(search))
    else:
        posts = Post.query.order_by(Post.id.desc())

    pages = posts.paginate(page=page, per_page=3)
    print(pages.total)
    return render_template('posts/index.html', pages=pages)


@posts.route('/create', methods=['GET', 'POST'])
@login_required
def post_create():
    form = PostForm(request.form) if request.form else PostForm()
    if request.method == 'POST' and form.validate():
        title = request.form['title']
        content = request.form['content']

        try:
            if title:
                post = Post(title = title, content = content)
                db.session.add(post)
                db.session.commit()
            else:
                return redirect(url_for('posts.post_create'))
        except:
            print('Something wrong!')
        return redirect(url_for('posts.index'))

    return render_template('posts/form.html', form=form, mode='create')


@posts.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
def post_edit(slug):
    post = Post.query.filter(Post.slug == slug).first()
    form = PostForm(formdata=request.form, obj=post)if request.form else PostForm(obj=post)
    if request.method == 'POST' and form.validate():
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for('posts.post_view', slug=post.slug))
    return render_template('posts/form.html', post = post, form=form, mode='update')

@posts.route('/<slug>')
def post_view(slug):
    post = Post.query.filter(Post.slug == slug).first()
    return render_template('posts/view.html', post=post)

@posts.route('/tags/<slug>')
def tag_view(slug):
    tag = Tag.query.filter(Tag.slug == slug).first()
    return render_template('tags/view.html', tag=tag)