from flask import render_template, request, redirect, url_for
from . import db
from .models import Todo
from flask import current_app as app

@app.route('/')
def index():
    todos = Todo.query.filter_by(completed=False).all()
    completed_todos = Todo.query.filter_by(completed=True).all()
    return render_template('index.html', todos=todos, completed_todos=completed_todos)

@app.route('/add', methods=['GET', 'POST'])
def add_todo():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_todo = Todo(title=title, description=description)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_todo.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_todo(id):
    todo = Todo.query.get_or_404(id)
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.description = request.form['description']
        todo.completed = 'completed' in request.form
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_todo.html', todo=todo)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))