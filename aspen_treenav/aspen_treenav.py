import os
import os.path

import aspen
import pymongo
import pymongo.uri_parser


def Database():
    connect = os.environ['MONGO']
    conn = pymongo.Connection(connect)

    # grab the dbname, because we can't get it via the Connection
    dbname = pymongo.uri_parser.parse_uri(connect)["database"]

    return conn[dbname]

class File(dict):
    def __getattr__(self, name):
        try:
            return dict.__getitem__
        except KeyError:
            raise AttributeError("No attribute named %s.")

db = None
def startup(website):
    return
    global db
    _db = Database()
    _db.drop_collection('tree')
    db = _db['tree']

    for path, dirs, files in os.walk(website.www_root):

        # Ignore hidden files.
        # ====================

        for seq in (dirs, files):
            for i in range(len(dirs)-1, -1, -1):
                name = dirs[i]
                if name.startswith('.'):
                    dirs.pop(i)

        # Index files.
        # ============

        parent = path[len(website.www_root):].replace(os.sep, '/')
        for name in files:
            if name == 'index.html':
                name = ''
            url_path = '/'.join([parent, name])
            aspen.log("indexing " + url_path)
            resource = website.load_simplate(url_path)
            doc = {"_id": url_path}
            if hasattr(resource, 'pages'):
                assert isinstance(resource.pages[0], dict) # sanity check
                for k, v in resource.pages[0].items():
                    if isinstance(v, (basestring,)):
                        doc[k] = v

            db.save(doc)

