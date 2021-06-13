from src import db
from src.bacnet_master.models.model_base import ModelBase


class BacnetDeviceModel(ModelBase):
    __tablename__ = 'bacnet_devices'
    device_name = db.Column(db.String(80), unique=False, nullable=False)
    device_enable = db.Column(db.Boolean())
    device_uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    device_mac = db.Column(db.Integer(), unique=False, nullable=False)
    device_object_id = db.Column(db.Integer(), unique=False, nullable=False)
    device_ip = db.Column(db.String(80), unique=False, nullable=False)
    device_mask = db.Column(db.Integer(), nullable=False)
    device_port = db.Column(db.Integer(), nullable=False)
    type_mstp = db.Column(db.Boolean())
    supports_rpm = db.Column(db.Boolean())
    supports_wpm = db.Column(db.Boolean())
    network_number = db.Column(db.Integer())
    network_uuid = db.Column(db.String, db.ForeignKey('bacnet_networks.network_uuid'))
    points = db.relationship('BacnetPointModel', cascade="all,delete", backref='points', lazy=True)

    def __repr__(self):
        return f"Device(device_uuid = {self.network_uuid})"

    @classmethod
    def delete_all_device_by_network(cls, network_uuid):
        try:
            cls.query.filter_by(network_uuid=network_uuid).delete()
            db.session.commit()
            return True

        except:
            db.session.rollback()
            return False

    @classmethod
    def find_by_device_uuid(cls, device_uuid):
        return cls.query.filter_by(device_uuid=device_uuid).first()
