from flask import Flask, render_template, url_for, request
import MapRouting

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/result',methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    MapRouting.queryPath(output['source'],output['sink'])
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)