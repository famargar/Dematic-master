__author__ = 'fabriziomargaroli'

import bottle
import os

app = bottle.app()
DOC_ROOT = ''

# This is the not found error page
@bottle.error(404)
def error404(error):
    return bottle.template("not_found")

# This is the error page
@bottle.error(500)
def error500(error):
    return bottle.template("error")

# This route is the main page
@bottle.route('/')
def publication_index():
    return bottle.redirect('welcome')

# This route the static files
@bottle.route('/static/:filename#.*#')
def server_static(filename):

    path_static = './static'
    try:
        if not os.path.exists(path_static+"/"+filename):
            return bottle.template("not_found")
    except Exception as e:
        return bottle.redirect("/internal_error")

    return bottle.static_file(filename, root=path_static)

@bottle.get('/welcome')
def welcome():

    return bottle.template('welcome')


if __name__ == '__main__':
    # Start the webserver running and wait for requests

    bottle.run(host='localhost', port=8084, reloader=True)
