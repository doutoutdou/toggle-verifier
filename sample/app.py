from flask import (
    Flask,
    render_template
)
import connexion
from flask_cors import CORS

# connexion
app = connexion.FlaskApp(__name__, specification_dir='./')

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')

# cors support
CORS(app.app)

# flask
app = app.app


@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/
    :return:        the rendered template 'home.html'
    """
    return render_template('home.html')


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
