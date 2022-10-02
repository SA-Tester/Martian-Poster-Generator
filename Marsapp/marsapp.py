from flask import Flask, render_template, url_for, request
import PosterGenerator

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/create', methods=["GET"])
def create():
    search = request.args.get("searchBar")
    if(search != None):
        PosterGenerator.getInput(str(search))
    return render_template('create.html', title='Create')

@app.route('/template')
def template():
    return render_template('template.html')
	
if __name__ == '__main__':
    app.run(debug=True)