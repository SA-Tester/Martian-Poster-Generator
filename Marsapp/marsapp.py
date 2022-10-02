from cgitb import text
from flask import Flask, render_template, url_for, request
import PosterGenerator

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/create',  methods=["GET"])
def create():
    search = request.args.get("searchBar")
    paths = []
    if(search != None):
        PosterGenerator.getInput(str(search))
        paths = PosterGenerator.getPathsToPosters()
    return render_template('create.html', title='Create', paths=paths)

@app.route('/template')
def template():
    return render_template('template.html')

if __name__ == '__main__':
    app.run(debug=True)