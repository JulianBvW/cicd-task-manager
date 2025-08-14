from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory task list
tasks = []
task_counter = 1


@app.route('/')
def hello():
    return 'Hello CI/CD'


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)


@app.route('/tasks', methods=['POST'])
def add_task():
    global task_counter
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400

    new_task = {
        'id': task_counter,
        'title': data['title'],
        'done': False
    }
    tasks.append(new_task)
    task_counter += 1
    return jsonify(new_task), 201


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    for task in tasks:
        if task['id'] == task_id:
            tasks = [t for t in tasks if t['id'] != task_id]
            return '', 204
    return jsonify({'error': 'Task not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
