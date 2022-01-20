from flask import Flask, render_template, request
from app import *

#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db=SQLAlchemy(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()