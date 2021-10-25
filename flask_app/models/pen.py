import datetime
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash
from flask_app.models import user


class Pen:
    def __init__(self, data):
        self.id = data['id']
        self.manufacturer = data['manufacturer']
        self.model = data['model']
        self.nib_size = data['nib_size']
        self.nib_type = data['nib_type']
        self.color = data['color']
        self.price = data['price']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.favorite = []

    @classmethod
    def get_all_pens(cls):

        query = 'SELECT * FROM pens LEFT JOIN users on users.id = pens.user_id;'

        results = connectToMySQL('pens_schema').query_db(query)

        pens = []

        for pen in results:
            new_pen = Pen(pen)
            favorites_data = {
                'id': pen['users.id'],
                'first_name': pen['first_name'],
                'last_name': pen['last_name'],
                'email': pen['email'],
                'password': pen['password'],
                'created_at': pen['users.created_at'],
                'updated_at': pen['users.updated_at']
            }
            favorite = user.User(favorites_data)
            new_pen.favorite = favorite
            pens.append(new_pen)
        return pens

    @classmethod
    def add_pen(cls, data):

        query = 'INSERT INTO pens (manufacturer, model, nib_size, nib_type, color, price, description, user_id) VALUES (%(manufacturer)s, %(model)s, %(nib_size)s, %(nib_type)s, %(color)s, %(price)s, %(description)s, %(user_id)s);'

        pen_id = connectToMySQL('pens_schema').query_db(query, data)

        return pen_id

    @classmethod
    def get_one_pen(cls, data):

        query = 'SELECT * FROM pens LEFT JOIN users on users.id = pens.user_id WHERE pens.id = %(id)s;'

        results = connectToMySQL('pens_schema').query_db(query, data)

        pen = Pen(results[0])

        favorites_data = {
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at']
        }
        favorite = user.User(favorites_data)
        pen.favorite = favorite

        return pen

    @classmethod
    def get_liked_pens(cls, data):

        query = 'SELECT * FROM pens LEFT JOIN favorites ON pens.id = favorites.pens_id LEFT JOIN users ON users.id = favorites.users_id WHERE users.id = %(id)s;'

        results = connectToMySQL('pens_schema').query_db(query, data)
        liked_pens = []

        for pen in results:
            new_pen = Pen(pen)
            favorites_data = {
                'id': pen['users.id'],
                'first_name': pen['first_name'],
                'last_name': pen['last_name'],
                'email': pen['email'],
                'password': pen['password'],
                'created_at': pen['users.created_at'],
                'updated_at': pen['users.updated_at']
            }
            favorite = user.User(favorites_data)
            new_pen.favorite = favorite
            liked_pens.append(new_pen)
        return liked_pens

    @classmethod
    def get_unliked_pens(cls, data):

        query = 'SELECT * FROM pens LEFT JOIN users ON users.id = pens.user_id WHERE pens.id NOT IN ( SELECT pens_id FROM favorites WHERE users_id = %(id)s);'

        results = connectToMySQL('pens_schema').query_db(query, data)

        unliked_pens = []

        for pen in results:
            new_pen = Pen(pen)
            favorites_data = {
                'id': pen['user_id'],
                'first_name': pen['first_name'],
                'last_name': pen['last_name'],
                'email': pen['email'],
                'password': pen['password'],
                'created_at': pen['users.created_at'],
                'updated_at': pen['users.updated_at']
            }
            favorite = user.User(favorites_data)
            new_pen.favorite = favorite
            unliked_pens.append(new_pen)
        return unliked_pens

    @classmethod
    def edit_pen(cls, data):

        query = 'UPDATE pens SET manufacturer = %(manufacturer)s, model = %(model)s, nib_size = %(nib_size)s, nib_type = %(nib_type)s, color = %(color)s, price = %(price)s, description = %(description)s WHERE id = %(id)s;'

        connectToMySQL('pens_schema').query_db(query, data)

    @classmethod
    def remove_pen(cls, data):

        query = "DELETE FROM favorites WHERE favorites.pens_id = %(id)s;"

        connectToMySQL('pens_schema').query_db(query, data)

        query = "DELETE FROM pens WHERE pens.id = %(id)s;"

        connectToMySQL('pens_schema').query_db(query, data)

    @classmethod
    def like_pen(cls, data):

        query = 'INSERT INTO favorites (users_id, pens_id) VALUES (%(users_id)s, %(pen_id)s);'

        connectToMySQL('pens_schema').query_db(query, data)

    @classmethod
    def unlike_pen(cls, data):

        query = 'DELETE FROM favorites WHERE favorites.users_id = %(user_id)s AND favorites.pens_id = %(pen_id)s;'

        connectToMySQL('pens_schema').query_db(query, data)

    @staticmethod
    def num_of_favorites(data):

        query = 'SELECT COUNT(*) FROM favorites WHERE pens_id = %(id)s;'

        num_of_favorites = connectToMySQL('pens_schema').query_db(query, data)

        return num_of_favorites[0]['COUNT(*)']

    # @staticmethod
    # def format_datetime(value, format="%B %d %Y"):
    #     if value is None:
    #         return ""
    #     return value.strftime(format)

    @staticmethod
    def validate_pen(data):

        is_valid = True

        if len(data['manufacturer']) < 3:
            is_valid = False
            flash('The manufacturer name must be at least 3 characters long.')

        if len(data['model']) < 3:
            is_valid = False
            flash('The model name must be at least 3 characters.')

        if len(data['nib_size']) < 1:
            is_valid = False
            flash('You must select a valid nib size')

        if len(data['nib_type']) < 1:
            is_valid = False
            flash('You must select a valid nib type')

        if len(data['color']) < 3:
            is_valid = False
            flash('The color name must be at least 3 characters')

        if len(data['price']) < 1:
            is_valid = False
            flash('The price must be at least $1')    

        # if int(data['price']) < 1:
        #     is_valid = False
        #     flash('The price must be at least $1')

        if len(data['description']) < 3:
            is_valid = False
            flash('Your description for the pen must be at least 3 characters')

        return is_valid
