from db import db
import datetime


class BranchDetails(db.Model):
    __tablename__ = 'branch_details'
    id1 = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String, unique=True)

    HBrUniqueNo = db.Column(db.String(256), unique=True)
    HBrName = db.Column(db.String(1024))
    HBrLocation = db.Column(db.String(1024))
    HBrAddress = db.Column(db.Text())
    HBrPhone = db.Column(db.String(128), unique=True)
    HBrLatitude = db.Column(db.Float())
    HBrLongitude = db.Column(db.Float())
    HBrAuthorisedUser = db.Column(db.String(512))
    HBrCreatedDate = db.Column(db.Date())
    HBrCreatedDateTime = db.Column(db.DateTime())
    HBrLogPath = db.Column(db.Text())
    HBrDeleted = db.Column(db.Boolean(), default=False)
    HBrForceDeleted = db.Column(db.Boolean(), default=False)
    HBrUpdatedDate = db.Column(db.Date())
    HBrUpdatedDate = db.Column(db.DateTime())
    HBrSpare1 = db.Column(db.Text())
    HBrSpare2 = db.Column(db.Text())

    # PacDet = db.relationship('PacBusDetails', backref=db.backref(
    #     'package'))

    def __init__(self, id, HBrUniqueNo, HBrName, HBrLocation, HBrAddress, HBrPhone, HBrLatitude, HBrLongitude, HBrAuthorisedUser,
                 HBrCreatedDate, HBrCreatedDateTime,
                 ):
        self.id = id
        self.HBrUniqueNo = HBrUniqueNo
        self.HBrName = HBrName
        self.HBrLocation = HBrLocation
        self.HBrAddress = HBrAddress
        self.HBrPhone = HBrPhone
        self.HBrLatitude = HBrLatitude
        self.HBrLongitude = HBrLongitude
        self.HBrAuthorisedUser = HBrAuthorisedUser
        self.HBrCreatedDate = HBrCreatedDate
        self.HBrCreatedDateTime = HBrCreatedDateTime

    @classmethod
    # Get All List of Bus
    def getAllBranch(cls):
        return cls.query.all()

    @classmethod
    # Get Specific Bus with Name
    def getNameBranch(cls, name):
        return cls.query.filter_by(HBrName=name).first()

    @classmethod
    # Get Specific Bus with id
    def getidBranch(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    # Get Specific Bus with id
    def getUniqueNoBranch(cls, uno):
        return cls.query.filter_by(HBrUniqueNo=uno).first()

    def saveBranch(self):
        db.session.add(self)
        db.session.commit()
        print(f'Branch Added')

    def deleteBranch(self):
        db.session.delete(self)
        db.session.commit()
        # print(self)
        print('Branch Deleted!')

    def updateBranch(self):
        db.session.commit()
        # print(f'{name} Updated')
