from flask import *
from functools import wraps
import sqlite3

DATABASE = 'flasktask.db'

app = Flask(__name__)
app.config.from_object(__name__)

app.secret_key = 'my precious'

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('log'))
    return wrap

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect (url_for('log'))

@app.route('/tasks')
@login_required
def tasks():
    g.db  = connect_db()
    g.db.close()
    return render_template('tasks.html')

@app.route('/', methods=['GET', 'POST'])
def log():
    error = None
if request.method == 'POST':
    if request.form['username'] != 'admin' or request.form['password'] != 'admin':
        error = 'Invalid Credentials. Please try again.'
    else:
        session['logged_in'] = True
        return redirect(url_for('tasks'))
return render_template('log.html', error=error)

@app.before_request
def before_request():
    g.db = connect_db()

if __name__ == '__main__':
    app.run(debug=True)