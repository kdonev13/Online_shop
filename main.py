from datetime import date
from functools import wraps

from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify
import json

from user import User
from post import Post

app = Flask(__name__)


@app.route('/')
def list_posts():
    return render_template('index.html', User = None, posts=Post.all())


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('registration_form.html')
    elif request.method == 'POST':
        email = request.form['email']
        values = (
            None,
            request.form['username'],
            User.hash_password(request.form['password']),
            email,
            request.form['address'],
            request.form['telephone_number']
        )
        User(*values).add_user()

        return redirect("/{}/".format(User.find_by_email(email)))


@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login_form.html')
    elif request.method == 'POST':
        return redirect("/{}/".format(User.find_by_email(request.form['email'])))


@app.route('/<int:id>/')
def after_reg_log(id):
    return render_template('index.html', User = User.find_by_id(id), posts=Post.all())


@app.route('/<int:id>/add_post/', methods=['GET', 'POST'])
def new_post(id):
    if request.method == 'GET':
        return render_template('add_post.html', User = User.find_by_id(id))
    elif request.method == 'POST':
        values = (
            None,
            request.form['title'],
            request.form['description'],
            request.form['price'],
            id,
        )
        Post(*values).create()

        return redirect('/{}/'.format(id))


@app.route('/<int:id>/my_posts/', methods=['GET'])
def my_posts(id):
    return render_template('my_posts.html', User = User.find_by_id(id), posts = Post.all())


@app.route('/<int:id>/delete/', methods=['POST'])
def delete(id):
    post = Post.find(id)
    username = User.find_by_id(post.owner)
    post.delete()
    return render_template("my_posts.html", User=username, posts = Post.all())


@app.route('/<int:post_id>/edit_post/<int:id>/', methods=['GET', 'POST'])
def edit_post(post_id, id):
    if request.method == 'GET':
        return render_template('edit_post.html', User = User.find_by_id(id), Post = Post.find(post_id))
    elif request.method == 'POST':
        values = (
            post_id,
            request.form['title'],
            request.form['description'],
            request.form['price'],
            id
        )
        Post(*values).edit()
        return redirect('/{}/'.format(id))


@app.route("/<int:id>/")
def print_hello(id):
    username = User.find_by_id(id)
    print(username)
    return render_template("index.html", User = username, Post = Post.all())


if __name__ == '__main__':
    app.run(debug=True)