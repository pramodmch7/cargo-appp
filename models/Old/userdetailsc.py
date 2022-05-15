from db import db
import datetime


class UserDetailC(db.Model):
    __tablename__ = 'user_details_clint'

    id1 = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String, unique=True)

    HUsrUniqueNo = db.Column(db.String(256), unique=True)
    HUsrFirstName = db.Column(db.String(512))
    HUsrLastName = db.Column(db.String(512))
    HUsrMiddleName = db.Column(db.String(512))
    HUsrPhone = db.Column(db.String(128), unique=True)
    HUsrEmail = db.Column(db.String(256), unique=True)
    HUsrPassword = db.Column(db.String(512))
    HUsrAdmin = db.Column(db.Boolean())
    HUsrActive = db.Column(db.Boolean())
    HUsrRoleName = db.Column(db.String(128))
    HUsrAvatar = db.Column(db.Text())
    HUsrLocation = db.Column(db.String(512))
    HUsrCreatedDate = db.Column(db.Date())
    HUsrCreatedDateTime = db.Column(db.DateTime())
    HUsrLogPath = db.Column(db.Text())
    HUsrDeleted = db.Column(db.Boolean(), default=False)
    HUsrForceDeleted = db.Column(db.Boolean(), default=False)
    HUsrUpdatedDate = db.Column(db.Date())
    HUsrUpdatedDate = db.Column(db.DateTime())
    HUsrSpare1 = db.Column(db.Text())
    HUsrSpare2 = db.Column(db.Text())

    def __init__(self, id, HUsrUniqueNo, HUsrFirstName, HUsrLastName, HUsrMiddleName, HUsrPhone, HUsrEmail, HUsrPassword,
                 HUsrAdmin, HUsrActive, HUsrRoleName, HUsrAvatar, HUsrCreatedDate, HUsrCreatedDateTime,
                 ):
        self.id = id
        self.HUsrUniqueNo = HUsrUniqueNo
        self.HUsrFirstName = HUsrFirstName
        self.HUsrLastName = HUsrLastName
        self.HUsrMiddleName = HUsrMiddleName
        self.HUsrPhone = HUsrPhone
        self.HUsrEmail = HUsrEmail
        self.HUsrPassword = HUsrPassword
        self.HUsrAdmin = HUsrAdmin
        self.HUsrActive = HUsrActive
        self.HUsrRoleName = HUsrRoleName
        self.HUsrAvatar = HUsrAvatar
        self.HUsrCreatedDate = HUsrCreatedDate
        self.HUsrCreatedDateTime = HUsrCreatedDateTime

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
        return cls.query.filter_by(HUsrFirstName=_name).first()

    @classmethod
    # Get Specific User with Email
    def getEmailUserC(cls, _email):
        return cls.query.filter_by(HUsrEmail=_email).first()

    @classmethod
    # Get Specific User with Email
    def getUniqueUserC(cls, _uniqueno):
        return cls.query.filter_by(HUsrUniqueNo=_uniqueno).first()

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
