from app import db , login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer , primary_key = True)
    time = db.Column(db.DateTime , default = datetime.now)
    fname = db.Column(db.String(30) , unique = False , nullable = False)
    lname = db.Column(db.String(30) , unique = False , nullable = True)
    email = db.Column(db.String(50) , unique = True , nullable = False)
    password = db.Column(db.String(60) , nullable = False)

    def get_id(self):
        try:
            return (self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    """Python __repr__() function returns the object representation. It could be any valid python expression such as tuple, dictionary, string etc.
    This method is called when repr() function is invoked on the object, in that case, __repr__() function must return a String otherwise error will be thrown."""
    def __repr__(self):
        return  'User(%s , %s , %s)' % (self.fname , self.lname, self.email)