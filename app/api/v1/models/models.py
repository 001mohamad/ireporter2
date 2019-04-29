from app import db

class Ireporter2(db.Model):
    """this class represents ireporter2 table"""


    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email =  db.Column(db.String(255))
    comment =  db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, name):
        """initialize with name."""
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Ireporter2.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Ireporter2: {}>".format(self.name)    

   
