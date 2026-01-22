
import json

from flask import Flask, redirect, render_template, request, url_for

from test import Initiate, getDocs

app = Flask(__name__)
corpus_embeddings, K, raw_data, embedder =  Initiate()

file=open("templates/data.json")
data=file.read()
data=json.loads(data)

@app.route('/success/<query>')
def success(query):

    print("QUERY is : ",query)

    query_embedding = embedder.encode(query)
    df = getDocs(corpus_embeddings, query_embedding,raw_data,K)

    return render_template('index3.html',data=df)

@app.route('/UserQuery',methods = ['POST', 'GET'])
def UserQuery():

   if request.method == 'POST':

      userQ = request.form['qry']
      print(userQ)
      return redirect(url_for('success',query = userQ))

   else:

      userQ = request.args.get('qry')
      print(userQ)
      return redirect(url_for('success',query = userQ))


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
  app.run(debug=True)
