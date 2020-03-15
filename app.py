from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)


class Database:
    def __init__(self):
        host = "eu-cdbr-west-02.cleardb.net"
        user = "b97d9a4cdd963d"
        password = "7ac67734"
        db = "heroku_885d7750b5b3cac"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    def list_book(self, query=None):
        if query:
            self.cur.execute(query)
            return self.cur.fetchall()
        self.cur.execute("select * from all_data ")
        return self.cur.fetchall()

    def list_genre(self):
        self.cur.execute("select genre_name from all_data where genre_name is not null;")
        result = self.cur.fetchall()
        return result

    def list_books(self):
        self.cur.execute("select distinct book_name from all_data")
        result = self.cur.fetchall()
        return result

    def list_author(self):
        self.cur.execute("select distinct author_name from all_data")
        result = self.cur.fetchall()
        return result

    def list_type(self):
        self.cur.execute("select distinct type from all_data where type is not null;")
        result = self.cur.fetchall()
        return result

    def list_subtype(self):
        self.cur.execute("select book_subtype from all_data where book_subtype is not null;")
        result = self.cur.fetchall()
        return result


@app.route('/', methods=['GET', 'POST'])
def books():
    db = Database()
    if request.method == 'GET':
        return render_template('books.html', result=db.list_book(), genres=db.list_genre(), types=db.list_type(),
                               books=db.list_book(), authors=db.list_author(),
                               subtypes=db.list_subtype(),
                               content_type='application/json')

    form = request.form.to_dict()
    print(form)
    if form:
        query = 'select * from all_data where '
        if form['book']:
            query += 'and book_name = ' + "'" + form['book'] + "'"
        if form['author']:
            query += 'and author_name = ' + "'" + form['author'] + "'"
        if form['genre']:
            query += 'and genre_name = ' + "'" + form['genre'] + "'"
        if form['type']:
            query += 'and type = ' + "'" + form['type'] + "'"
        if form['subtype']:
            query += 'and book_subtype = ' + "'" + form['subtype'] + "'"
    return render_template('books.html', result=db.list_book(query.replace("and", "", 1)), genres=db.list_genre(),
                           types=db.list_type(),
                           subtypes=db.list_subtype(),
                           books=db.list_book(), authors=db.list_author(),
                           content_type='application/json')


if __name__ == '__main__':
    app.run()
