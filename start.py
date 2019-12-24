from flask import Flask
from flask import render_template, request, jsonify
from preprocess_data import Question

que=Question()
print("Create question REmains todo!")

app = Flask(__name__)


@app.route("/")
def startpage():
    return render_template('index.html')


@app.route("/dealquestion1", methods=['POST'])
def dealquestion():
    #question = request.args.get('query')
    question = request.json['query']
    answer = que.question_process(question)
    print("question is " , question)
    #answer = request.args.get('query')
    #answer = question
    return jsonify(ans=answer)


if __name__ == "__main__":
    app.run()
