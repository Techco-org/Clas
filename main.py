from flask import render_template, url_for
from website import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='localhost', port='5000', debug=True)