import os
from flask import Flask, render_template
from pyzotero import zotero

from pprint import pprint

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

library_id = os.getenv('LIBRARY_ID')
library_type = os.getenv('LIBRARY_TYPE')
api_key = os.getenv('API_KEY')

z = zotero.Zotero(library_id, library_type, api_key)
isawbib_json = z.everything(z.top())
cit = z.add_parameters(content='bib', style='mla')
isawbib_cit = z.everything(z.top())

@app.route('/')
def homepage():
    count = len(isawbib_json)
    #tags = get_tags(isawbib)
    return render_template('isaw-bibliography.html', isawbib=isawbib_json, count=count)


@app.route('/bib')
def bib():
    count = len(isawbib_cit)
    #tags = get_tags(isawbib)
    return render_template('isaw-citations.html', isawbib=isawbib_cit, count=count)


if __name__ == '__main__':
    app.run()