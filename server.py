from flask import Flask, render_template
from flask import request
import requests

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/test", methods=['POST'])
def test():
    data1 = request.form['a1']+','+request.form['b1']+','+request.form['c1']+','+request.form['d1']+','+request.form['e1']+','+request.form['f1']+','+request.form['g1']+','+request.form['h1']+','+request.form['i1']+','+request.form['j1']+','
    data2 = request.form['a2']+','+request.form['b2']+','+request.form['c2']+','+request.form['d2']+','+request.form['e2']+','+request.form['f2']+','+request.form['g2']+','+request.form['h2']+','+request.form['i2']+','+request.form['j2']+','
    data3 = request.form['a3']+','+request.form['b3']+','+request.form['c3']+','+request.form['d3']+','+request.form['e3']+','+request.form['f3']+','+request.form['g3']+','+request.form['h3']+','+request.form['i3']+','+request.form['j3']
    data = data1+data2+data3
    data = data.split(',')
    data = [float(i) for i in data]
    content = {
        'data': data
    }
    res = requests.post('https://Kara.lyrenyx.repl.co/WDBC', json=content)
    print('response from server:',res)
    result = res.json()
    print(result)
    return render_template("result.html", result = result)

@app.route("/test2", methods=['POST'])
def test2():
    data = request.form['csv']
    data = data.split(',')
    data = [float(i) for i in data]
    content = {
        'data': data
    }
    res = requests.post('https://Kara.lyrenyx.repl.co/WDBC', json=content)
    print('response from server:',res)
    result = res.json()
    print(result)
    return render_template("result.html", result = result)
if __name__ == "__main__":
    app.run(debug=True)

