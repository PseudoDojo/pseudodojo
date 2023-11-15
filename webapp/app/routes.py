from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contribute')
def contribute():
    return render_template('contribute.html')

@app.route('/direct_table_test')
def direct_table_test():
    return render_template('direct_table_test.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/paperlist')
def paperlist():
    return render_template('paperlist.html')

@app.route('/papers')
def papers():
    return render_template('papers.html')

@app.route('/abinintsitepage')
def abinintsitepage():
    return render_template('abinintsitepage.html')