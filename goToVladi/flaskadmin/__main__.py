from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from goToVladi.core.data.db.models import User
from dishka.integrations.flask import setup_dishka
from dishka import make_container
engine = create_engine(
    "postgresql+psycopg2://pguser:pgpassword@localhost:1001/goToVladi"
)
session_pool = sessionmaker(bind=engine)
current_session = scoped_session(session_pool)

if __name__ == '__main__':
    app = Flask(__name__)
    di_container = make_container()

    app.secret_key = 'kek'

    admin = Admin(app, name='goToVladi', template_mode='bootstrap4')

    admin.add_view(ModelView(User, current_session))
    # admin.add_view(RestaurantView(Restaurant, current_session))

    app.run(host='0.0.0.0', port=5000, debug=True)
