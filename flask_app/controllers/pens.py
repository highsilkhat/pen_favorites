import datetime
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt

from flask_app.models.user import User
from flask_app.models.pen import Pen
from flask_app.controllers import users


@app.route('/dashboard')
def all_pens():
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    
    data = {
        'id':session['user_id']
    }
    
    likes = Pen.get_liked_pens(data)
    unlikes = Pen.get_unliked_pens(data)

    return render_template('all_pens.html', unlikes = unlikes , likes = likes)

@app.route('/new')
def add_pen():
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    
    return render_template('new_pen.html')

@app.route("/pens/post", methods = ['POST'])
def post_pen():
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')

    if not Pen.validate_pen(request.form):
        return redirect ('/new')

    
    data = {
        'manufacturer': request.form['manufacturer'],
        'model': request.form['model'],
        'nib_size': request.form['nib_size'],
        'nib_type': request.form ['nib_type'],
        'color': request.form['color'],
        'price': request.form ['price'],
        'description': request.form ['description'],
        'user_id': session['user_id']
    }

    pen_id = Pen.add_pen(data)

    return redirect ('/dashboard')

@app.route('/pen/<int:pen_id>')
def pen_pen(pen_id):
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')

    data = {
        'id':pen_id
    }

    num_of_favorites = Pen.num_of_favorites(data)
    pen = Pen.get_one_pen(data)

    return render_template ('show_pen.html', pen = pen, num_of_favorites = num_of_favorites)

@app.route('/edit/<int:pen_id>')
def edit_pen(pen_id):
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')

    data = {
        'id':pen_id
    }

    pen = Pen.get_one_pen(data)

    return render_template ('edit_pen.html', pen =pen )

@app.route('/edit/<int:pen_id>/post', methods = ['POST'])
def post_edit_pen(pen_id):
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    
    if not Pen.validate_pen(request.form):
        return redirect (f'/edit/{pen_id}')
    
    data = {
        'manufacturer': request.form['manufacturer'],
        'model': request.form['model'],
        'nib_size': request.form['nib_size'],
        'nib_type': request.form ['nib_type'],
        'color': request.form['color'],
        'price': request.form ['price'],
        'description': request.form ['description'],
        'id': pen_id

    }

    Pen.edit_pen(data)

    return redirect ('/dashboard')

@app.route('/like/<int:pen_id>')
def like_pen(pen_id):
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')

    data = {
        'users_id':session['user_id'],
        'pen_id':pen_id
    }

    Pen.like_pen(data)

    return redirect('/dashboard')

@app.route('/unlike/<int:pen_id>')
def unlike_pen(pen_id):
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    
    data = {
        'user_id':session['user_id'],
        'pen_id':pen_id
    }

    Pen.unlike_pen(data)
    return redirect('/dashboard')

@app.route('/delete/<int:pen_id>')
def remove_pen(pen_id):
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    
    data = {
        'id':pen_id
    }

    Pen.remove_pen(data)

    return redirect ('/dashboard')