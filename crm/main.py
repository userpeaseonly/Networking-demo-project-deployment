from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)


# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Task {self.name}>'


# Create the database and tables
with app.app_context():
    db.create_all()


@app.route('/')
def crm():
    tasks = Task.query.all()
    data = {
        'title': 'CRM',
        'message': 'Welcome to CRM!',
        'items': tasks
    }
    return render_template('index.html', data=data)


@app.route("/add_crm", methods=['POST'])
def add_task():
    task_name = request.form.get("task_name")
    if task_name:
        new_task = Task(name=task_name)
        db.session.add(new_task)
        db.session.commit()
    return redirect('/crm')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
