import sys
import os
from pyzotero import zotero

library_id = os.getenv('LIBRARY_ID')
library_type = os.getenv('LIBRARY_TYPE')
api_key = os.getenv('API_KEY')
z = zotero.Zotero(library_id, library_type, api_key)

def main(tag):
    if tag in z.tags():
        # Get number of items with tag and report in next print statement
        tag_item_count = len(z.everything(z.items(tag=tag)))
        print(f'Removing tag \'{tag}\'...')
        z.delete_tags(tag)
        print(f'Removed tag \'{tag}\' from {tag_item_count} items...')
    else:
        print(f'Error: tag \'{tag}\' not in the tags for this collection.')
    return None

if __name__ == '__main__':
    if len(sys.argv) > 1:
        tag = sys.argv[1]
        main(tag)
    else:
        print('Error: script requires the tag to be removed;\ne.g. python remove-tags.py oldtag')
