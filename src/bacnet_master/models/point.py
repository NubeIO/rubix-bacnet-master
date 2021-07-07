from src import db
from src.bacnet_master.interfaces.device import ObjType
from src.bacnet_master.models.model_base import ModelBase
from src.bacnet_master.models.model_point_store import BACnetPointStoreModel
from src.bacnet_master.models.model_priority_array import PriorityArrayModel


class BacnetPointModel(ModelBase):
    __tablename__ = 'bacnet_points'
    point_name = db.Column(db.String(100), unique=False, nullable=False)
    point_enable = db.Column(db.Boolean())
    point_uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    point_object_id = db.Column(db.Integer(), unique=False, nullable=False)
    point_object_type = db.Column(db.Enum(ObjType), unique=False, nullable=False)
    point_writable = db.Column(db.Boolean(), unique=False, nullable=True)
    fault = db.Column(db.Boolean(), unique=False, nullable=True)
    cov = db.Column(db.Float(), unique=False, nullable=True)
    timeout = db.Column(db.Float(), unique=False, nullable=True)
    enable_polling = db.Column(db.Boolean(), unique=False, nullable=True)
    device_uuid = db.Column(db.String, db.ForeignKey('bacnet_devices.device_uuid'))
    priority_array_write = db.relationship('PriorityArrayModel', backref='point', lazy=False, uselist=False,
                                           cascade="all,delete")
    point_store = db.relationship('BACnetPointStoreModel', backref='point', lazy=False, uselist=False,
                                  cascade="all,delete")

    def __repr__(self):
        return f"Device(device_uuid = {self.device_uuid})"

    def save_to_db(self, priority_array_write: dict):
        self.priority_array_write = PriorityArrayModel(point_uuid=self.point_uuid, **priority_array_write)
        self.point_store = BACnetPointStoreModel.create_new_point_store_model(self.point_uuid)
        db.session.add(self)
        db.session.commit()

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
    def existing_name_on_patch(cls, point_name):
        return cls.query.filter(BacnetPointModel.point_name == point_name).all()

    @classmethod
    def existing_name_on_add(cls, device_uuid, point_name):
        return cls.query.filter(BacnetPointModel.device_uuid == device_uuid) \
            .filter((BacnetPointModel.point_name == point_name)).all()

    @classmethod
    def existing_object_id(cls, device_uuid, point_object_id, point_object_type):
        return cls.query.filter(BacnetPointModel.device_uuid == device_uuid) \
            .filter((BacnetPointModel.point_object_id == point_object_id)) \
            .filter((BacnetPointModel.point_object_type == point_object_type)).all()

