from flask import Flask,redirect,url_for,render_template

app=Flask(__name__)
def test():
    return 1

@app.route("/")
def home():
    testcontent=test()
    return render_template("index.html",content=testcontent)

if __name__=="__main__":
    app.run(debug=True)