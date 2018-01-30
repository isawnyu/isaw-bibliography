import os
from flask import Flask, render_template
from pyzotero import zotero

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

library_id = os.getenv('LIBRARY_ID')
library_type = os.getenv('LIBRARY_TYPE')
api_key = os.getenv('API_KEY')

z = zotero.Zotero(library_id, library_type, api_key)

@app.route('/')
def homepage():
    isawbib = z.everything(z.top())
    count = len(isawbib)
    #tags = get_tags(isawbib)
    return render_template('isaw-bib.html', isawbib=isawbib, count=count)

if __name__ == '__main__':
    app.run()