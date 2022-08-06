from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

from sqlalchemy import desc
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    content=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title} , {self.content}"

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title , content=desc)
        db.session.add(todo)
        db.session.commit()
    
    allTodo=Todo.query.all()
    return render_template('index.html',allTodo=allTodo)


@app.route('/show')
def products():
    #this returns all the records from db
    allTodo=Todo.query.all()
    print(allTodo)
    return 'this is products'

@app.route('/update/<int:sno>', methods=['POST','GET'])
def update(sno):
    #this returns all the records from db
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.content=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo=Todo.query.filter_by(sno=sno).first()
    print(todo)
    return render_template('update.html',todo=todo)
    #this returns all the records from db
    # if request.method=='POST':
    #     title=request.form['title']
    #     desc=request.form['desc']
    

@app.route('/delete/<int:sno>')
def delete(sno):
    #this returns the first record with serial num sno
    allTodo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(allTodo)
    db.session.commit()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True, port=8000)