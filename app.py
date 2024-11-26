from flask import Flask, render_template , request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

## Defining the schema in the database

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_time = db.Column(db.DateTime, default= datetime.datetime.utcnow)
    def __repr__(self) -> str:
        return f"{self.sno} {self.title}"
    
## Creating the databse and the tables
with app.app_context():
    db.create_all()

@app.route('/',methods = ['GET','POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()

    alltodo = Todo.query.all()
    return render_template('index.html', alltodo = alltodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.get(sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>',methods = ['GET','POST'])
def update(sno):
    todo = Todo.query.get(sno)
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    return render_template('update.html', todo = todo)
@app.route('/search',methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    if query:
        results = Todo.query.filter(Todo.title.ilike(f"%{query}%")).all()
    else:
        results = []
    return render_template('search.html', results=results, query=query)

if __name__ == '__main__':
    app.run(debug = True,port = 8000)