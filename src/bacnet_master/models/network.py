from src import db
from src.bacnet_master.models.model_base import ModelBase


class BacnetNetworkModel(ModelBase):
    __tablename__ = 'bacnet_networks'
    network_name = db.Column(db.String(80), unique=False, nullable=False)
    network_enable = db.Column(db.Boolean())
    network_uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    network_ip = db.Column(db.String(20), unique=False, nullable=False)
    network_mask = db.Column(db.Integer(), nullable=False)
    network_port = db.Column(db.Integer(), nullable=False)
    network_device_id = db.Column(db.Integer(), nullable=False)
    network_device_name = db.Column(db.String(80), nullable=False)
    devices = db.relationship('BacnetDeviceModel', cascade="all,delete", backref='network', lazy=True)

    def __repr__(self):
        return f"Network(network_uuid = {self.network_uuid})"

    @classmethod
    def find_by_network_uuid(cls, network_uuid):
        return cls.query.filter_by(network_uuid=network_uuid).first()
