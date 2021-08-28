import datetime
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash
from flask_app.models import user


class TV_show:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.fan = []

    @classmethod
    def get_all_tv_shows(cls):

        query = 'SELECT * FROM tv_shows LEFT JOIN users on users.id = tv_shows.user_id;'

        results = connectToMySQL('tv_shows_schema').query_db(query)

        tv_shows = []

        for show in results:
            new_show = TV_show(show)
            fans_data = {
                'id': show['users.id'],
                'first_name': show['first_name'],
                'last_name': show['last_name'],
                'email': show['email'],
                'password': show['password'],
                'created_at': show['users.created_at'],
                'updated_at': show['users.updated_at']
            }
            fan = user.User(fans_data)
            new_show.fan = fan
            tv_shows.append(new_show)
        return tv_shows

    @classmethod
    def add_show(cls, data):

        query = 'INSERT INTO tv_shows (title, network, release_date, description, user_id) VALUES (%(title)s, %(network)s, %(release_date)s, %(description)s, %(user_id)s);'

        show_id = connectToMySQL('tv_shows_schema').query_db(query, data)

        return show_id

    @classmethod
    def get_one_show(cls, data):

        query = 'SELECT * FROM tv_shows LEFT JOIN users on users.id = tv_shows.user_id WHERE tv_shows.id = %(id)s;'

        results = connectToMySQL('tv_shows_schema').query_db(query, data)

        show = TV_show(results[0])

        fans_data = {
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at']
        }
        fan = user.User(fans_data)
        show.fan = fan

        return show

    @classmethod
    def get_liked_tv_shows(cls, data):

        query = 'SELECT * FROM tv_shows LEFT JOIN likes ON tv_shows.id = likes.tv_shows_id LEFT JOIN users ON users.id = likes.users_id WHERE users.id = %(id)s;'

        results = connectToMySQL('tv_shows_schema').query_db(query, data)
        liked_shows = []

        for show in results:
            new_show = TV_show(show)
            fans_data = {
                'id': show['users.id'],
                'first_name': show['first_name'],
                'last_name': show['last_name'],
                'email': show['email'],
                'password': show['password'],
                'created_at': show['users.created_at'],
                'updated_at': show['users.updated_at']
            }
            fan = user.User(fans_data)
            new_show.fan = fan
            liked_shows.append(new_show)
        return liked_shows

    @classmethod
    def get_unliked_shows(cls, data):

        query = 'SELECT * FROM tv_shows LEFT JOIN users ON users.id = tv_shows.user_id WHERE tv_shows.id NOT IN ( SELECT tv_shows_id FROM likes WHERE users_id = %(id)s);'

        results = connectToMySQL('tv_shows_schema').query_db(query, data)

        unliked_shows = []

        for show in results:
            new_show = TV_show(show)
            fans_data = {
                'id': show['user_id'],
                'first_name': show['first_name'],
                'last_name': show['last_name'],
                'email': show['email'],
                'password': show['password'],
                'created_at': show['users.created_at'],
                'updated_at': show['users.updated_at']
            }
            fan = user.User(fans_data)
            new_show.fan = fan
            unliked_shows.append(new_show)
        return unliked_shows

    @classmethod
    def edit_show(cls, data):

        query = 'UPDATE tv_shows SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s WHERE id = %(id)s;'

        connectToMySQL('tv_shows_schema').query_db(query, data)

    @classmethod
    def remove_show(cls, data):

        query = "DELETE FROM likes WHERE likes.tv_shows_id = %(id)s;"

        connectToMySQL('tv_shows_schema').query_db(query, data)

        query = "DELETE FROM tv_shows WHERE tv_shows.id = %(id)s;"

        connectToMySQL('tv_shows_schema').query_db(query, data)

    @classmethod
    def like_show(cls, data):

        query = 'INSERT INTO likes (users_id, tv_shows_id) VALUES (%(users_id)s, %(show_id)s);'

        connectToMySQL('tv_shows_schema').query_db(query, data)

    @classmethod
    def unlike_show(cls, data):

        query = 'DELETE FROM likes WHERE likes.users_id = %(user_id)s AND likes.tv_shows_id = %(show_id)s;'

        connectToMySQL('tv_shows_schema').query_db(query, data)

    @staticmethod
    def num_of_likes(data):

        query = 'SELECT COUNT(*) FROM likes WHERE tv_shows_id = %(id)s;'

        num_of_likes = connectToMySQL('tv_shows_schema').query_db(query, data)

        return num_of_likes[0]['COUNT(*)']

    # @staticmethod
    # def format_datetime(value, format="%B %d %Y"):
    #     if value is None:
    #         return ""
    #     return value.strftime(format)

    @staticmethod
    def validate_show(data):

        is_valid = True

        if len(data['title']) < 3:
            is_valid = False
            flash('The title must be at least 3 characters long.')

        if len(data['network']) < 3:
            is_valid = False
            flash('The network name must be at least 3 characters.')

        if len(data['release_date']) < 8:
            is_valid = False
            flash('You must select a valid release date')

        if len(data['description']) < 3:
            is_valid = False
            flash('Your description for the show must be at least 3 characters')

        return is_valid
