from flask import Flask, request, abort
import datetime
import time
import sqlite3

def AdmInLogIn(Username, Password):
    print('хых, я тут')
    con = sqlite3.connect('BulbaDb.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS All_Users(username TEXT,'
                'password TEXT)')
    cur.execute("SELECT * FROM All_Users WHERE username=?", (Username,))
    Nams = cur.fetchall()
    i = 0
    for nam in Nams:
        i += 1
        print(nam)
        print(nam[1])
    print(i)
    info = [Username, Password]
    if i == 0:
        cur.execute('INSERT INTO All_Users VALUES(?, ?)', info)
        con.commit()
        cur.close()
        con.close()
        return True
    else:
        if Password != nam[1]:
            return abort(401)
        else:
            con.commit()
            cur.close()
            con.close()
            return True


def ImWatchingYou(username, text, current_time):
    con = sqlite3.connect('BulbaDb.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS All_Mess(username TEXT,'
                'text TEXT, '
                'time FLOAT)')
    info = [username, text, current_time]
    cur.execute('INSERT INTO All_Mess VALUES(?, ?, ?)', info)
    con.commit()
    cur.close()
    con.close()


messages = [
    {'username': 'shura', 'text': 'Good evening', 'time': 0.0}
]

users = {
    'shura': '12345'
}

print('F')
AdmInLogIn('shura', '12345')

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/about")
def about():
    return {
        "status": True
    }

@app.route('/status')
def shura():
    return {
        'status': True,
        'Name': 'Shurec',
        'time': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
        'n_messages': len(messages) - 1,
        'n_users': len(users)
    }

@app.route('/send', methods=['POST'])
def send():
    """
    принимаем JSON
    {
        "username": str,
        "password": str,
        "text": str
    }
    :return: JSON {'OK': true}
    """
    username = request.json['username']
    password = request.json['password']

    AdmInLogIn(username, password)

    text = request.json['text']
    current_time = time.time()
    message = {'username': username, 'text': text, 'time': current_time}
    messages.append(message)
    ImWatchingYou(username, text, current_time)
    print(messages)
    print(users)
    return {
        'OK': True
    }

@app.route('/messages')
def messages_view():
    """
    принимаем ?after = float
    :return: JSON
    {
        "messages": [
            {"username": str, "text": str, "time": float}
        ]
    }
    """
    after = float(request.args.get('after'))
    # 
    # filtered_messages = []
    # for message in messages:
    # if message['time'] > after:
    # filtered_messages.append(message)

    filtered_messages = [message for message in messages if message['time'] > after]

    return {
        'messages': filtered_messages
    }


app.run()
