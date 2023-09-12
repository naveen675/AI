from flask import Flask, render_template, request, redirect, url_for
from AI_search_engine import get_response

app = Flask(__name__)



from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form["search_query"].lower()
        results = get_response(query)
    else:
        results = []

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True,port='8080')

# @app.route("/search_results",methods=["POST"])
# def search_results():

#     if request.method == "POST":
#         query = request.form["search_query"].lower()
#         msg = get_response(query)
#     return msg

# if __name__ == "__main__":
#     app.run(debug=True)