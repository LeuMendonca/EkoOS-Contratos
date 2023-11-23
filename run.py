from waitress import serve

from control.wsgi import application
# documentation: https://docs.pylonsproject.org/projects/waitress/en/stable/api.html

if __name__ == '__main__':
    serve(application, host = '192.168.0.7', port='9091')
