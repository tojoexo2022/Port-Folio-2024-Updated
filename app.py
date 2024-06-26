from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  # MySQL username (replace with your MySQL username)
    password="",  # MySQL password (replace with your MySQL password)
    database="my_database"
)
cursor = db.cursor()

# Helper function to handle database operations
def update_post_counts(post_id, field, increment=True):
    try:
        cursor.execute(f'SELECT {field} FROM posts WHERE id = %s', (post_id,))
        count = cursor.fetchone()[0]

        if count is not None:
            new_count = count + 1 if increment else max(count - 1, 0)
            cursor.execute(f'UPDATE posts SET {field} = %s WHERE id = %s', (new_count, post_id))
            db.commit()
            return jsonify({field: new_count}), 200
        else:
            return jsonify({'error': 'Post not found'}), 404
    except mysql.connector.Error as err:
        return jsonify({'error': f"MySQL Error: {err}"}), 500

# Routes
@app.route('/posts/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    return update_post_counts(post_id, 'likes_count', increment=True)

@app.route('/posts/<int:post_id>/dislike', methods=['POST'])
def dislike_post(post_id):
    return update_post_counts(post_id, 'dislikes_count', increment=True)

@app.route('/posts/<int:post_id>/unlike', methods=['POST'])
def unlike_post(post_id):
    return update_post_counts(post_id, 'likes_count', increment=False)

@app.route('/posts/<int:post_id>/undislike', methods=['POST'])
def undislike_post(post_id):
    return update_post_counts(post_id, 'dislikes_count', increment=False)

@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    try:
        cursor.execute('SELECT id, title, content, likes_count, dislikes_count FROM posts WHERE id = %s', (post_id,))
        result = cursor.fetchone()

        if result:
            post = {
                'id': result[0],
                'title': result[1],
                'content': result[2],
                'likes_count': result[3],
                'dislikes_count': result[4]
            }
            return jsonify(post), 200
        else:
            return jsonify({'error': 'Post not found'}), 404
    except mysql.connector.Error as err:
        return jsonify({'error': f"MySQL Error: {err}"}), 500

if __name__ == '__main__':
    app.run(debug=True)