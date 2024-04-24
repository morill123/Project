from flask import Flask, jsonify, request
import psycopg2
import psycopg2.extras

app = Flask(__name__)

class LoginService:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(
            database="Database",
            user="postgres",
            password="20040510",
            host="localhost",
            port="5432")

    def validate_login(self, username, password):
        with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT * FROM manager WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            return user is not None


login_service = LoginService('Manager', 'postgres', 'Aa20030802', 'localhost', '5432')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if login_service.validate_login(username, password):
        return jsonify({'success': True, 'message': 'Login successful'})
    else:
        return jsonify({'success': False, 'message': 'Login failed'})


if __name__ == '__main__':
    app.run(port=5003, debug=True)
