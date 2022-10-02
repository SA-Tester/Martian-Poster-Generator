from flask import Flask, render_template, url_for, request
import PosterGenerator

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/create',  methods=["GET"])
def create():
    return render_template('create.html', title='Create')

@app.route('/poster')
def generate_poster():
    search = request.args.get("searchBar")
    PosterGenerator.getInput(str(search))

if __name__ == '__main__':
    app.run(debug=True)