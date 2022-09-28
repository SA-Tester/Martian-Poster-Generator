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
    #cameraSelection = request.args.getlist("cameraType")
    PosterGenerator.getInput(str(search)) #  + " " + str(cameraSelection)
    return render_template('create.html', title='Create')

if __name__ == '__main__':
    app.run(debug=True)
