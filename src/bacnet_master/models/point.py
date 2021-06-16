from sqlalchemy import and_

from src import db
from src.bacnet_master.interfaces.device import ObjType
from src.bacnet_master.models.model_base import ModelBase


class BacnetPointModel(ModelBase):
    __tablename__ = 'bacnet_points'
    point_name = db.Column(db.String(80), unique=False, nullable=False)
    point_enable = db.Column(db.Boolean())
    point_uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    point_object_id = db.Column(db.Integer(), unique=False, nullable=False)
    point_object_type = db.Column(db.Enum(ObjType), unique=False, nullable=False)
    point_writable = db.Column(db.Boolean())
    device_uuid = db.Column(db.String, db.ForeignKey('bacnet_devices.device_uuid'))


    def __repr__(self):
        return f"Device(point_uuid = {self.device_uuid})"

    @classmethod
    def delete_all_points_by_device(cls, device_uuid):
        try:
            cls.query.filter_by(device_uuid=device_uuid).delete()
            db.session.commit()
            return True

        except:
            db.session.rollback()
            return False

    @classmethod
    def find_by_point_uuid(cls, point_uuid):
        return cls.query.filter_by(point_uuid=point_uuid).first()

    @classmethod
    def find_by_point_name(cls, point_name):
        return cls.query.filter_by(point_name=point_name).first()

    @classmethod
    def existing_object_name(cls, point_name):
        return cls.query.filter(BacnetPointModel.point_name == point_name).all()

    @classmethod
    def existing_object_id(cls, point_object_id, point_object_type):
        return cls.query.filter(BacnetPointModel.point_object_id == point_object_id) \
            .filter((BacnetPointModel.point_object_type == point_object_type)).all()
