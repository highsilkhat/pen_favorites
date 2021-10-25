import datetime
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt

from flask_app.models.user import User
from flask_app.models.tv_show import TV_show
from flask_app.controllers import users


@app.route('/dashboard')
def all_pens():
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    
    data = {
        'id':session['user_id']
    }
    
    likes = TV_show.get_liked_tv_shows(data)
    unlikes = TV_show.get_unliked_shows(data)

    return render_template('tv_shows.html', unlikes = unlikes , likes = likes)

@app.route('/new')
def add_show():
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    
    return render_template('new_show.html')

@app.route("/shows/post", methods = ['POST'])
def post_show():
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')

    if not TV_show.validate_show(request.form):
        return redirect ('/new')

    
    data = {
        'title': request.form['title'],
        'network': request.form['network'],
        'release_date': request.form['release_date'],
        'description': request.form ['description'],
        'user_id': session['user_id']
    }

    show_id = TV_show.add_show(data)

    return redirect ('/dashboard')

@app.route('/show/<int:show_id>')
def tv_show_show(show_id):
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')

    data = {
        'id':show_id
    }

    num_of_likes = TV_show.num_of_likes(data)
    show = TV_show.get_one_show(data)

    return render_template ('show_tv_show.html', show = show, num_of_likes = num_of_likes)

@app.route('/edit/<int:show_id>')
def edit_show(show_id):
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')

    data = {
        'id':show_id
    }

    show = TV_show.get_one_show(data)

    return render_template ('edit_show.html', show =show )

@app.route('/edit/<int:show_id>/post', methods = ['POST'])
def post_edit_show(show_id):
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    
    if not TV_show.validate_show(request.form):
        return redirect (f'/edit/{show_id}')
    
    data = {
        'title': request.form['title'],
        'network': request.form['network'],
        'release_date': request.form['release_date'],
        'description': request.form ['description'],
        'id': show_id

    }

    TV_show.edit_show(data)

    return redirect ('/dashboard')

@app.route('/like/<int:show_id>')
def like_show(show_id):
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')

    data = {
        'users_id':session['user_id'],
        'show_id':show_id
    }

    TV_show.like_show(data)

    return redirect('/dashboard')

@app.route('/unlike/<int:show_id>')
def unlike_show(show_id):
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    
    data = {
        'user_id':session['user_id'],
        'show_id':show_id
    }

    TV_show.unlike_show(data)
    return redirect('/dashboard')

@app.route('/delete/<int:show_id>')
def remove_show(show_id):
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    
    data = {
        'id':show_id
    }

    TV_show.remove_show(data)

    return redirect ('/dashboard')