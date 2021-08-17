from flaskapp import create_app
from .api import create_api

app = create_app()
create_api(app)

if __name__ == "__main__":
    app.run(debug=True)