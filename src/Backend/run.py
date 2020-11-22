from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from resources.register import registerBp
    app.register_blueprint(registerBp)
    
    from resources.userPosts import postBp
    app.register_blueprint(postBp)
    
    from resources.login import loginBp
    app.register_blueprint(loginBp)

    #create database
    from models import db
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
    return app

if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True)