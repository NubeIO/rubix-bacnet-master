from flask import Blueprint
from flask_restful import Api

from src.bacnet_master.resources.device import Device, DeviceList, \
    DeviceObjectList, BuildPointsList
from src.bacnet_master.resources.network import Network, NetworkList, NetworksIds
from src.bacnet_master.resources.network_whois import Whois, UnknownDeviceObjects, \
    UnknownReadPointPv
from src.bacnet_master.resources.point import Point, PointList, PointBACnetRead, PointBACnetWrite, PointRelease

from src.system.resources.ping import Ping

bp_bacnet_master = Blueprint('bacnet_master', __name__, url_prefix='/api/bm')
api_bacnet_master = Api(bp_bacnet_master)

# master
api_bacnet_master.add_resource(Device, '/device/<string:uuid>')
api_bacnet_master.add_resource(DeviceList, '/devices')
api_bacnet_master.add_resource(Network, '/network/<string:uuid>')
api_bacnet_master.add_resource(NetworkList, '/networks')
api_bacnet_master.add_resource(NetworksIds, '/networks/ids')
api_bacnet_master.add_resource(Point, '/point/<string:uuid>')
api_bacnet_master.add_resource(PointList, '/points')

# bacnet network calls
api_bacnet_master.add_resource(Whois, '/b/network/whois/<string:net_uuid>')
api_bacnet_master.add_resource(PointBACnetRead, '/b/points/read/pv/<string:pnt_uuid>')  # read point pv
api_bacnet_master.add_resource(PointBACnetWrite,
                               '/b/points/write/pv/<string:pnt_uuid>/<string:value>/<string:priority>')  # write point pv
api_bacnet_master.add_resource(PointRelease,
                               '/b/points/write/release/<string:pnt_uuid>/<string:priority>/<string:feedback>')  # release point pv

api_bacnet_master.add_resource(BuildPointsList, '/b/points/point_list/<string:dev_uuid>')  # build points list
api_bacnet_master.add_resource(DeviceObjectList, '/b/device/objects/<string:dev_uuid>')
api_bacnet_master.add_resource(UnknownDeviceObjects, '/b/device/unknown/objects/<string:net_uuid>')
api_bacnet_master.add_resource(UnknownReadPointPv, '/b/point/unknown/point_pv/<string:net_uuid>')

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
api_system = Api(bp_system)
api_system.add_resource(Ping, '/ping')
