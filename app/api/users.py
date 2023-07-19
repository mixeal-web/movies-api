# app/api/movies.py

from flask import Blueprint, jsonify, request
from app.db import get_db_connection
from flask_jwt_extended import create_access_token, jwt_required
from app.main import bcrypt

users = Blueprint('users', __name__)


@users.route('/register', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data['name']
    password = data['password']
    try:
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute('SELECT * FROM user WHERE user_name=%s', [name])
        results = cur.fetchall()
        row_count = cur.rowcount
        if row_count != 0:
            return jsonify({'message': 'User already exists'}), 500
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        cur.execute('INSERT INTO user VALUES (%s, %s)', (name, hashed_password))
        connection.commit()

        return jsonify({'message': 'success'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': e}), 500


@users.route('/login', methods=['POST'])
def user_login():
    username = request.json['username']
    password = request.json['password']

    # Check if the user exists in the database
    connect = get_db_connection()
    cur = connect.cursor()
    cur.execute('SELECT * FROM user WHERE user_name=%s', [username])
    data = cur.fetchone()
    row_count = cur.rowcount
    if row_count == 0 or not bcrypt.check_password_hash(data[1], password):
        return jsonify({'message': 'Invalid username or password'}), 401
    # Generate the access token
    access_token = create_access_token(identity=data[0])

    return jsonify({'token': access_token, 'user': username}), 200


@users.route('/comment', methods=['POST'])
def comment():
    data = request.get_json()
    name = data['name']
    movie_id = data['movie_id']
    comment = data['comment']
    print(comment)
    try:
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute('SELECT MAX(comment_id) FROM comment')
        data = cur.fetchone()
        if data[0] is None:
            comment_id = 0
        else:
            comment_id = data[0] + 1
        cur.execute('INSERT INTO comment VALUES (%s, %s, %s, %s)', (comment_id, name, movie_id, comment))
        comment_id += 1
        connection.commit()
        return jsonify({'message': 'Success'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@users.route('/comment_display/<movie_id>/<int:num>')
def comment_display(movie_id, num):
    try:
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute('SELECT * FROM comment WHERE movie_id = %s ORDER BY comment_id DESC LIMIT %s', [movie_id, num])
        data = cur.fetchall()
        json_data = []
        for row in data:
            json_data.append({'username': row[1], 'comment': row[3]})
        return jsonify(json_data)
    except Exception as e:
        return f'Failed to connect to the database: {str(e)}'


@users.route('/rating', methods=['POST'])
def rating():
    data = request.get_json()
    user_name = data['user_name']
    movie_id = data['movie_id']
    rating = data['rating']
    try:
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute('INSERT INTO user_rating (user_name, movie_id, rating) VALUES ( %s, %s, %s) ON DUPLICATE KEY UPDATE'
                    ' rating = %s;',
                    (user_name, movie_id, rating, rating))
        connection.commit()
        return jsonify({'message': 'Success'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@users.route('/user-rating/<user>/<int:movie_id>', methods=['GET'])
def get_user_rating(user, movie_id):
    try:
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute('SELECT rating FROM user_rating WHERE movie_id = %s AND user_name = %s', [movie_id, user])
        data = cur.fetchone()
        print(data[0])
        return jsonify({'userRating': data[0]}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
