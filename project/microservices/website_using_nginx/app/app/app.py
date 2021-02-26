import os
from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ds_pipe.datasets.dataset_loader import Dataset_Collections

# Loading the basic datasets
dc = Dataset_Collections()
dc_full_dict = dc.get_full_dictionary()
datasets = dc.keel_datasets() + dc.chapelle_datasets()
dataset_meta_information = [(dataset_name,  len(dataset.data[0]), len(dataset.target)) for dataset, dataset_name in datasets]

# Setting the DB
db = SQLAlchemy()


def create_app():
    from app.models import User, Todo, ResultCatalog, UserResult
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    #if not os.path.isfile("db.sqlite"):
    db.create_all(app=app)


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    return app


if __name__=="__main__":
    app = create_app()
