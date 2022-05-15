'''
from db import db
import datetime


class UserDetailC(db.Model):
    __tablename__ = 'user_details_clint'

    id1 = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String, unique=True)
    FirstName = db.Column(db.String(512))
    LastName = db.Column(db.String(512))
    MiddleName = db.Column(db.String(512))
    Email = db.Column(db.String(1024), unique=True)
    UserPassword = db.Column(db.String(1024))
    Admin = db.Column(db.Boolean(), default=False)
    isActive = db.Column(db.Boolean(), default=True)
    RoleName = db.Column(db.String(128))
    CreatedD = db.Column(db.Date(), default=datetime.date.today())
    Created = db.Column(db.DateTime(), default=datetime.datetime.now())
    Avatar = db.Column(db.Text(), default='img-baseurl')
    UpdatedD = db.Column(db.Date())
    Updated = db.Column(db.DateTime())
    Spare1 = db.Column(db.Text())
    Spare2 = db.Column(db.Text())

    def __init__(self, id, FirstName, LastName, MiddleName, Email, UserPassword, Admin, isActive, RoleName, Avatar):
        self.id = id
        self.FirstName = FirstName
        self.LastName = LastName
        self.MiddleName = MiddleName
        self.Email = Email
        self.UserPassword = UserPassword
        self.Admin = Admin
        self.isActive = isActive
        self.RoleName = RoleName
        self.Avatar = Avatar

    @classmethod
    # Get All List of User
    def getAllUserC(cls):
        return cls.query.all()

    @classmethod
    # Get Specific User with ID
    def getIdUserC(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    # Get Specific User with Name
    def getNameUserC(cls, _name):
        return cls.query.filter_by(FirstName=_name).first()

    @classmethod
    # Get Specific User with Email
    def getEmailUserC(cls, _email):
        return cls.query.filter_by(Email=_email).first()

    def saveUserC(self):
        db.session.add(self)
        db.session.commit()
        print('User Added to Clint DB')

    def deleteUserC(self):
        db.session.delete(self)
        db.session.commit()
        print('User Deleted from Clint DB')

    def updateUserC(self):
        db.session.commit()
        print('User update from Clint DB!')
'''
