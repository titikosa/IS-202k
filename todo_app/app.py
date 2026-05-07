from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

FILE_NAME = 'tasks.json'


def load_tasks():

    if os.path.exists(FILE_NAME):

        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            return json.load(f)

    return []


def save_tasks(tasks):

    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


tasks = load_tasks()


@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():

    new_task = request.form['task']

    if new_task:

        tasks.append({
            'text': new_task,
            'done': False
        })

        save_tasks(tasks)

    return redirect('/')


@app.route('/delete/<int:task_id>')
def delete_task(task_id):

    if 0 <= task_id < len(tasks):

        tasks.pop(task_id)

        save_tasks(tasks)

    return redirect('/')


@app.route('/done/<int:task_id>')
def done_task(task_id):

    if 0 <= task_id < len(tasks):

        tasks[task_id]['done'] = not tasks[task_id]['done']

        save_tasks(tasks)

    return redirect('/')


@app.route('/edit/<int:task_id>', methods=['POST'])
def edit_task(task_id):

    if 0 <= task_id < len(tasks):

        new_text = request.form['new_text']

        tasks[task_id]['text'] = new_text

        save_tasks(tasks)

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)