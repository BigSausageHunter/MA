from database import app, db
from database.models import User
@app.route('/add_user')
def add_user():
    user = User(name="Test User")
    db.session.add(user)
    db.session.commit()
    return "User added!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)