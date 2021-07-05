import logging

from sqlalchemy.orm import validates

from src import db
from src.bacnet_master.models.model_base import ModelBase
from src.bacnet_master.utils.functions import BACnetFunctions
from src.utils.functions import Functions

logger = logging.getLogger(__name__)


class BacnetDeviceModel(ModelBase):
    __tablename__ = 'bacnet_devices'
    device_name = db.Column(db.String(100), unique=False, nullable=False)
    device_enable = db.Column(db.Boolean())
    device_uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    device_mac = db.Column(db.Integer(), unique=False, nullable=False)
    ethernet_mac_address = db.Column(db.String(120), unique=False, nullable=True)
    manufacture = db.Column(db.String(200), unique=False, nullable=True)
    device_object_id = db.Column(db.Integer(), unique=False, nullable=False)
    device_ip = db.Column(db.String(100), unique=False, nullable=False)
    device_mask = db.Column(db.Integer(), nullable=False)
    device_port = db.Column(db.Integer(), nullable=False)
    type_mstp = db.Column(db.Boolean())
    supports_rpm = db.Column(db.Boolean())
    supports_wpm = db.Column(db.Boolean())
    network_number = db.Column(db.Integer())
    network_uuid = db.Column(db.String, db.ForeignKey('bacnet_networks.network_uuid'))
    points = db.relationship('BacnetPointModel', cascade="all,delete", backref='points', lazy=True)

    def __repr__(self):
        return f"Device(network_uuid = {self.network_uuid})"

    @classmethod
    def delete_all_device_by_network(cls, network_uuid):
        try:
            devices = cls.query.filter_by(network_uuid=network_uuid).all()
            for device in devices:
                if device:
                    device.delete_from_db()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"DROP/DELETE DEVICE on network: {network_uuid} message: {e}")
            return False

    @classmethod
    def find_by_device_uuid(cls, device_uuid):
        return cls.query.filter_by(device_uuid=device_uuid).first()

    @classmethod
    def existing_device_id_to_net(cls, network_number, device_object_id):
        return cls.query.filter(BacnetDeviceModel.network_number == network_number) \
            .filter((BacnetDeviceModel.device_object_id == device_object_id)).all()

    @classmethod
    def existing_net_to_mac(cls, network_number, device_mac):
        return cls.query.filter(BacnetDeviceModel.network_number == network_number) \
            .filter((BacnetDeviceModel.device_mac == device_mac)).all()

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

    @validates('device_port')
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

    @validates('device_mac')
    def bacnet_mac_address(self, _, value):
        """
        """
        if not BACnetFunctions.validate_network_number(value):
            raise ValueError(f"BACnet mac address number: {value} is not not valid, a valid rang is between 0 and 254")
        return value
