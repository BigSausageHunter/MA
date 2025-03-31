from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aec4255d5d5032953ab8e01aad09e7f4c47a3d36d32d28b0f8bb825c52d7780c6072f2d79033979386cc21497fa7110f53e4b67d9b04bfd470c8d5c649de0c257d3a61c2328bd4a5df31c3e95c68634d1dff814d0f718b1ff5fc3242a9e330329d5a8f1367f268c1627c12f63c219fca3e10087e7c4dc74dda7d356f43c53fa4871bb689793727548728adf7aceadedc43a92e796325f1eac0b16731b1ae6987787ed38438a64afc6e523f912f0ae32b9febe65bcd8fcde03a78bb9462bb9bed080f7c5b3411545b1941620b57221071f6c44e19dc52779d27812d1aaefbfcae967e543552e98d086fa088948ff119f80b0e5cb70e0d2351510d02116e730ea8'

users = {}  

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username in users:
        return jsonify({"message": "Пользователь уже существует"}), 400
    users[username] = generate_password_hash(password)
    return jsonify({"message": "Пользователь зарегистрирован успешно"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username not in users or not check_password_hash(users[username], password):
        return jsonify({"message": "Неверные учетные данные"}), 401
    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'token': token})

@app.route('/validate', methods=['POST'])
def validate():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Токен отсутствует!"}), 403
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return jsonify({"username": data['username']})
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Срок действия токена истек!"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"message": "Недействительный токен!"}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)