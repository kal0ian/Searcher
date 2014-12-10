from flask import Flask, render_template
from flask import request

from get_html_source import search_word


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('searcher.html')


@app.route('/searcher/')
def search():
    print(request.args)
    keyword = request.args['keyword']
    pages_searched = search_word(keyword)
    return render_template('result.html', keyword=keyword, pages_searched=pages_searched)


if __name__ == '__main__':
    app.run(debug=True)