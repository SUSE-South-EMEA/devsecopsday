from flask import Flask
from flaskext.mysql import MySQL
import requests

app = Flask(__name__)

# MySQL configurations
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mypassword'
app.config['MYSQL_DATABASE_DB'] = 'mydb'
app.config['MYSQL_DATABASE_HOST'] = 'mysql'
mysql.init_app(app)

con = mysql.connect()
cur = con.cursor()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/db')
def db_query():
    cur.execute('''SELECT data FROM mytable''')
    rv = cur.fetchone()
    return str(rv)

@app.route('/forbidden')
def forbidden_url():
    try:
        response = requests.get('http://www.example.com')
        return response.text
    except Exception as e:
        return str(e)

def init_db():
    cur.execute('CREATE TABLE IF NOT EXISTS mytable (id INT AUTO_INCREMENT PRIMARY KEY, data VARCHAR(255) NOT NULL)')
    cur.execute('SELECT * FROM mytable')
    data = cur.fetchall()
    if len(data) == 0:
        for i in range(1, 4):
            cur.execute(f"INSERT INTO mytable (data) VALUES ('DB data {i}')")
        con.commit()

init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
