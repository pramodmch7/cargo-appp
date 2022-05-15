from enum import unique
from db import db
import datetime


class PackageDetails(db.Model):
    __tablename__ = 'package_details'

    id1 = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String, unique=True)
    HPkgUniqueNo = db.Column(db.String(256), unique=True)
    HPkgCreatedDateTime = db.Column(db.DateTime())
    HPkgApproximateDeliveryDate = db.Column(db.Date())
    HPkgAllStatus = db.Column(db.Text())
    HPkgName = db.Column(db.String(512))
    HPkgDistance = db.Column(db.String(128))
    HPkgWeight = db.Column(db.String(128))
    HPkgQrCode = db.Column(db.Text())
    HPkgFromLocation = db.Column(db.String(512))
    HPkgCustomerName = db.Column(db.String(256))
    HPkgCustomerMobile = db.Column(db.String(128))
    HPkgToLocation = db.Column(db.String(512))
    HPkgCustomerToName = db.Column(db.String(256))
    HPkgCustomerToMobile = db.Column(db.String(158))
    HPkgCreatedDate = db.Column(db.Date())
    HPkgCreatedBy = db.Column(db.String(512))
    HPkgStatusFromCreted = db.Column(db.String(128))
    HPkgStatusCodeFromCreted = db.Column(db.Integer())
    HPkgTotalAmount = db.Column(db.Float())
    HPkgAdvanceAmount = db.Column(db.Float())
    HPkgBalanceAmount = db.Column(db.Float())
    HPkgGST = db.Column(db.Float())
    HPkgGSTAmount = db.Column(db.Float())
    HPkgFinalAmount = db.Column(db.Float())

    HPkgCustomerEmail = db.Column(db.String(512))
    HPkgCustomerToEmail = db.Column(db.String(512))
    HPkgActualDeliveryDate = db.Column(db.DateTime())
    HPkgDispatchDate = db.Column(db.DateTime())
    HPkgArrivingDate = db.Column(db.DateTime())
    HPkgLogPath = db.Column(db.Text())
    HPkgDeleted = db.Column(db.Boolean(), default=False)
    HPkgForceDeleted = db.Column(db.Boolean(), default=False)
    HPkgUpdatedDate = db.Column(db.Date())
    HPkgUpdatedDateTime = db.Column(db.DateTime())
    HPkgUpdatedBy = db.Column(db.String(512))
    HPkgSpare1 = db.Column(db.Text())
    HPkgSpare2 = db.Column(db.Text())
    HPkgDispatchBy = db.Column(db.String(512))
    HPkgStatusFromDispatch = db.Column(db.String(128))
    HPkgStatusCodeFromDispatch = db.Column(db.Integer())
    HPkgActualDeliveryDate = db.Column(db.Date())
    HPkgDeliveredBy = db.Column(db.String(512))
    HPkgStatusToDeliver = db.Column(db.String(128))
    HPkgStatusCodeToDeliver = db.Column(db.Integer())
    HPkgArrivingDate = db.Column(db.Date())
    HPkgArrivingBy = db.Column(db.String(512))
    HPkgStatusToArrive = db.Column(db.String(128))
    HPkgStatusCodeToArrive = db.Column(db.Integer())

    # BusDet = db.relationship('PacBusDetails', backref=db.backref(
    #     'bus'))
    # RawMaterials = db.relationship(
    #     'SPARawModel', secondary=R_FProducts, backref=db.backref('rawMaterials', lazy='dynamic'))

    def __init__(self, id, HPkgUniqueNo, HPkgCreatedDateTime, HPkgApproximateDeliveryDate, HPkgAllStatus, HPkgName, HPkgDistance, HPkgWeight, HPkgQrCode,
                 HPkgFromLocation, HPkgCustomerName, HPkgCustomerMobile, HPkgToLocation, HPkgCustomerToName, HPkgCustomerToMobile, HPkgCreatedDate, HPkgCreatedBy,
                 HPkgStatusFromCreted, HPkgStatusCodeFromCreted, HPkgTotalAmount, HPkgAdvanceAmount, HPkgBalanceAmount, HPkgGST, HPkgGSTAmount, HPkgFinalAmount,
                 ):
        self.id = id
        self.HPkgUniqueNo = HPkgUniqueNo
        self.HPkgCreatedDateTime = HPkgCreatedDateTime
        self.HPkgApproximateDeliveryDate = HPkgApproximateDeliveryDate
        self.HPkgAllStatus = HPkgAllStatus
        self.HPkgName = HPkgName
        self.HPkgDistance = HPkgDistance
        self.HPkgWeight = HPkgWeight
        self.HPkgQrCode = HPkgQrCode
        self.HPkgFromLocation = HPkgFromLocation
        self.HPkgCustomerName = HPkgCustomerName
        self.HPkgCustomerMobile = HPkgCustomerMobile
        self.HPkgToLocation = HPkgToLocation
        self.HPkgCustomerToName = HPkgCustomerToName
        self.HPkgCustomerToMobile = HPkgCustomerToMobile
        self.HPkgCreatedDate = HPkgCreatedDate
        self.HPkgCreatedBy = HPkgCreatedBy
        self.HPkgStatusFromCreted = HPkgStatusFromCreted
        self.HPkgStatusCodeFromCreted = HPkgStatusCodeFromCreted
        self.HPkgTotalAmount = HPkgTotalAmount
        self.HPkgAdvanceAmount = HPkgAdvanceAmount
        self.HPkgBalanceAmount = HPkgBalanceAmount
        self.HPkgGST = HPkgGST
        self.HPkgGSTAmount = HPkgGSTAmount
        self.HPkgFinalAmount = HPkgFinalAmount

    @classmethod
    # Get All List of Package
    def getAllP(cls):
        return cls.query.all()

    @classmethod
    # Get Specific Package with ID
    def getidP(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    # Get Specific Package with ID
    def getUniqueNoP(cls, _Uid):
        return cls.query.filter_by(HPkgUniqueNo=_Uid).first()

    @classmethod
    # Get Specific Package with Name
    def getnameP(cls, _name):
        return cls.query.filter_by(HPkgName=_name).first()

    @classmethod
    # Get Specific Package with Based on From Location
    def getLocFP(cls, _loc):
        return cls.query.filter_by(HPkgFromLocation=_loc)

    @classmethod
    # Get Specific Package with Based on From Location
    def getLocTP(cls, _loc):
        return cls.query.filter_by(HPkgToLocation=_loc)

    @classmethod
    # Get Specific Package with Based on Status Code
    def getStatusCodeP(cls, _status):
        return cls.query.filter_by(HPkgStatusCodeFromCreted=_status)

    def saveP(self):
        db.session.add(self)
        db.session.commit()
        print('Package Added')

    def deleteP(self):
        db.session.delete(self)
        db.session.commit()
        print('Package Deleted')

    def updateP(self):
        db.session.commit()
        print('Package Updated!')
