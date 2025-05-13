from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///polls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    options = db.relationship('Option', backref='poll', lazy=True)

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    votes = db.Column(db.Integer, default=0)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)

# Home page - Displaying all polls
@app.route('/')
def index():
    polls = Poll.query.all()
    return render_template('index.html', polls=polls)

# Show a specific poll
@app.route('/poll/<int:poll_id>')
def show_poll(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    return render_template('poll.html', poll=poll)

# Handle voting
@app.route('/vote/<int:poll_id>', methods=['POST'])
def vote(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    selected_option_id = request.form.get('option')
    option = Option.query.filter_by(id=selected_option_id, poll_id=poll.id).first()
    if option:
        option.votes += 1
        db.session.commit()
        return redirect(url_for('results', poll_id=poll.id))
    return "Invalid vote", 400

# Show poll results
@app.route('/results/<int:poll_id>')
def results(poll_id):
    poll = Poll.query.get_or_404(poll_id)
    total_votes = sum(option.votes for option in poll.options)
    return render_template('results.html', poll=poll, total_votes=total_votes)

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Run this only once to create tables
        # Optional: Add some sample data if table is empty
        if not Poll.query.first():
            sample_poll = Poll(question="What is your favorite programming language?")
            db.session.add(sample_poll)
            db.session.commit()

            options = ["Python", "JavaScript", "Java", "C++"]
            for opt in options:
                db.session.add(Option(text=opt, poll_id=sample_poll.id))
            db.session.commit()

    app.run(debug=True, port=5002)
