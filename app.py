import os
from flask import Flask, redirect, render_template, request, url_for, redirect
from random import randint
import sqlite3

entries = [0]
encouragements_entries = [0]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

triggers = ['kill', 'suicide', 'sh', 'self-harm', 'depressed', 'die']

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit(entries=entries, encouragements=encouragements_entries):
    if request.method == 'POST':
        message = request.form['message']
        contact = request.form['contact']
        type = request.form['type']

        if (contact == ''):
            contact = "No contact information provided"

        if type == 'encouragement':
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO encouragements(id, message, contact) VALUES (?, ?, ?)",
                            (encouragements_entries[0], message, contact))
                con.commit()
            encouragements_entries[0] += 1
        else:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO messages(id, message, contact) VALUES (?, ?, ?)", (entries[0], message, contact))
                con.commit()
            entries[0] += 1
        messages = message.split(' ')
        for word in messages:
            if word.lower() in triggers:
                return render_template('help.html')

        return redirect(url_for('index'))
    else:
        return render_template('submit.html')


@app.route('/view')
def view():
    entry = randint(0, entries[0] - 1)
    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM messages WHERE id = (?)", (entry,))
        rows = cur.fetchall()
        return render_template('view.html', contact=rows[0]['contact'], message=rows[0]['message'])


@app.route('/encouragements')
def encouragements():
    encouragement = randint(0, encouragements_entries[0] - 1)
    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM encouragements WHERE id = (?)", (encouragement,))
        rows = cur.fetchall()
        return render_template('encouragements.html', contact=rows[0]['contact'], message=rows[0]['message'])

@app.route('/support')
def support():
    return render_template('support.html')

if __name__ == '__main__':
    app.run(debug=True)
