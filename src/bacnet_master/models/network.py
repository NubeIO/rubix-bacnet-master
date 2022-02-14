from sqlalchemy.orm import validates

from src import db
from src.bacnet_master.models.model_base import ModelBase
from src.bacnet_master.utils.functions import BACnetFunctions
from src.utils.functions import Functions


class BacnetNetworkModel(ModelBase):
    __tablename__ = 'bacnet_networks'
    network_name = db.Column(db.String(100), unique=True, nullable=False)
    network_enable = db.Column(db.Boolean())
    network_uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    network_ip = db.Column(db.String(20), unique=False, nullable=False)
    network_mask = db.Column(db.Integer(), nullable=False)
    network_port = db.Column(db.Integer(), unique=False, nullable=True)
    network_device_object_id = db.Column(db.Integer(), nullable=False)
    network_device_name = db.Column(db.String(80), nullable=False)
    enable_polling = db.Column(db.Boolean(), unique=False, nullable=True)
    fault = db.Column(db.Boolean(), unique=False, nullable=True)
    devices = db.relationship('BacnetDeviceModel', cascade="all,delete", backref='network', lazy=True)

    def __repr__(self):
        return f"Network(network_uuid = {self.network_uuid})"

    @classmethod
    def find_by_network_uuid(cls, network_uuid):
        return cls.query.filter_by(network_uuid=network_uuid).first()

    @validates('device_ip')
    def validate_ip(self, _, value):
        """
        """
        if not Functions.is_valid_ip(value):
            raise ValueError(f"IP Address: {value} is not not valid")
        return value

    @validates('device_mask')
    def validate_mask(self, _, value):
        """
        """
        if not Functions.cidr_is_in_range(value):
            raise ValueError(f"Subnet Address: {value} is not not valid, a valid rang is between 0 and 32")
        return value

    @validates('network_port')
    def validate_network_port(self, _, value):
        """
        """
        if not BACnetFunctions.validate_network_number(value):
            raise ValueError(f"Device port number: {value} is not not valid, a valid rang is between 0 and 65534")
        return value

    @validates('network_number')
    def validate_network_number(self, _, value):
        """
        """
        if not BACnetFunctions.validate_network_number(value):
            raise ValueError(f"BACnet network number: {value} is not not valid, a valid rang is between 0 and 65534")
        return value
