from flask import Flask, render_template, request, redirect, url_for
from chat_with_pdf import data

app = Flask(__name__)



from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form["search_query"].lower()
        results = data()
    else:
        results = []

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True,port='8080')