import datetime
from flask import Flask, render_template, request, url_for,redirect
from flask_sqlalchemy import SQLAlchemy

#app config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rihlwxzfygidkw:a09e10b3c7cf038b9a9463cfc78f4355fdb23a94f97a818756bd006ca5c2a8bd@ec2-54-225-113-7.compute-1.amazonaws.com:5432/detlkhh9n3dev0'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db= SQLAlchemy(app)

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.String(200))
  completed = db.Column(db.Boolean)


@app.route("/")
def index():
  cd = datetime.datetime.now()
  web_date = "%s,%s %s %s" % (cd.strftime(
      "%A"), cd.strftime("%d"), cd.strftime("%B"), cd.strftime("%Y"))
  cards = Todo.query.filter_by(completed=False).all()
  crushed= Todo.query.filter_by(completed=True).all()

  return(render_template('main.html', cards = cards, crushed= crushed,date= web_date))

@app.route("/add", methods=["POST"])
def add():
  todo =Todo(text = request.form.get("card"), completed=False)
  db.session.add(todo)
  db.session.commit()
  return (redirect(url_for('index')))

@app.route("/complete/<id>")
def complete(id):
  todo = Todo.query.filter_by(id=int(id)).first()
  todo.completed = True
  db.session.commit()
  return redirect(url_for('index'))

@app.route("/delete/<id>")
def delete(id):
  todo = Todo.query.filter_by(id=int(id)).first()
  db.session.delete(todo)
  db.session.commit()
  return redirect(url_for('index'))


#code written by wilfred