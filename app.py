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
isawbib_json = z.everything(z.top(sort="dateModified"))
cit = z.add_parameters(content='bib', style='mla', sort="dateModified")
isawbib_cit = z.everything(z.top())

# More elegant way to write this?
for i, item in enumerate(isawbib_cit):
    isawbib_json[i]['data']['citation'] = item

def _sort_zotero_date(zotero_items, reverse=True):
    return sorted(zotero_items, key=lambda k: k['data']['date'], reverse=reverse)

def get_zotero_data():
	z = zotero.Zotero(library_id, library_type, api_key)
	isawbib_json = z.everything(z.top(sort="dateModified"))
	cit = z.add_parameters(content='bib', style='mla', sort="dateModified")
	isawbib_cit = z.everything(z.top())

	# More elegant way to write this?
	for i, item in enumerate(isawbib_cit):
	    isawbib_json[i]['data']['citation'] = item
	items = isawbib_json
	count = len(items)
	items = _sort_zotero_date(items)
	return items, count

@app.route('/')
def homepage():
	items = isawbib_json
	from pprint import pprint
	pprint(items)
	count = len(items)
	items = _sort_zotero_date(items)
	return render_template('isaw-bibliography.html', title=None, items=items, count=count)


@app.route('/refresh')
def refresh():
	items, count = get_zotero_data()
	count = len(items)
	items = _sort_zotero_date(items)
	return render_template('isaw-bibliography.html', title=None, items=items, count=count)


@app.route('/year/<year>')
def bib_by_year(year):
    items = []
    for item in isawbib_json:
        if item['data']['date'] == year:
            items.append(item)
    count = len(items)
    items = _sort_zotero_date(items)
    return render_template('isaw-bibliography.html', title='Year: %s' % str(year), items=items, count=count)


@app.route('/author/<author>')
@app.route('/authors/<author>')
def bib_by_author(author):
    items = []
    for item in isawbib_json:
        for creator in item['data']['creators']:
            for authors in creator.values():
                if author.lower() in authors.lower():
                    items.append(item)
    count = len(items)
    items = _sort_zotero_date(items)
    return render_template('isaw-bibliography.html', title='Author: %s' % author, items=items, count=count)


@app.route('/tag/<tag>')
@app.route('/tags/<tag>')
def bib_by_tag(tag):
    items = []
    for item in isawbib_json:
        for tags in item['data']['tags']:
            if tag in tags.values():
                items.append(item)
    count = len(items)
    items = _sort_zotero_date(items)
    return render_template('isaw-bibliography.html', title='Tag: %s' % tag, items=items, count=count)


@app.route('/json')
def print_first_record():
    return render_template('isaw-json.html', item=isawbib_json[0])


if __name__ == '__main__':
    app.run()
