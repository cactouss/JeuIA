from flask_sqlalchemy import SQLAlchemy
from .views import app
import logging as lg

db = SQLAlchemy(app)

def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    lg.warning('Database initialized!')
    # definition des modèles
    #region 11/11
    p1 = Player("Admin")

    #endregion
    db.session.add(p1)
    db.session.commit()

	# définition des modèles
class Player(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_name = db.Column(db.String(200),primary_key=True)

    def __init__(self,user_name):
        self.user_name = user_name