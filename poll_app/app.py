 from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy poll data
poll = {
    "question": "What is your favorite programming language?",
    "options": ["Python", "JavaScript", "Java", "C++"],
    "votes": [0, 0, 0, 0]  # Initial vote count
}

@app.route('/')
def index():
    return render_template('poll.html', poll=poll)

@app.route('/vote', methods=['POST'])
def vote():
    selected_option = request.form.get('option')
    if selected_option is not None:
        index = int(selected_option)
        poll['votes'][index] += 1
    return redirect(url_for('results'))

@app.route('/results')
def results():
    total_votes = sum(poll['votes'])
    return render_template('results.html', poll=poll, total_votes=total_votes)

if __name__ == '__main__':
    app.run(debug=True)
