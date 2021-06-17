from flask import Blueprint
from flask_restful import Api

from src.bacnet_master.resources.device import Device, DeviceList, \
    AddDevice, DeleteDevices, DeviceObjectList
from src.bacnet_master.resources.network import Network, NetworkList, NetworksIds, AddNetwork
from src.bacnet_master.resources.network_whois import Whois, NetworkAllPoints, DeviceAllPoints, DevicePollAllPoints
from src.bacnet_master.resources.point import Point, PointList, PointBACnetRead, PointBACnetWrite, PointRelease, \
    AddPoint, DeletePointList

from src.system.resources.ping import Ping

bp_bacnet_master = Blueprint('bacnet_master', __name__, url_prefix='/api/bm')
api_bacnet_master = Api(bp_bacnet_master)

# master
api_bacnet_master.add_resource(AddNetwork, '/network')
api_bacnet_master.add_resource(Network, '/network/<string:network_uuid>')
api_bacnet_master.add_resource(NetworkList, '/networks/<string:with_children>')
api_bacnet_master.add_resource(NetworksIds, '/networks/ids')
api_bacnet_master.add_resource(DeleteDevices, '/network/devices/drop/<string:network_uuid>')
api_bacnet_master.add_resource(AddDevice, '/device')
api_bacnet_master.add_resource(Device, '/device/<string:device_uuid>')
api_bacnet_master.add_resource(DeviceList, '/devices/<string:with_children>')
api_bacnet_master.add_resource(DeletePointList, '/device/points/drop/<string:device_uuid>')
api_bacnet_master.add_resource(AddPoint, '/point')
api_bacnet_master.add_resource(Point, '/point/<string:point_uuid>')
api_bacnet_master.add_resource(PointList, '/points')


# bacnet network calls
api_bacnet_master.add_resource(Whois, '/b/network/whois/<string:network_uuid>')
api_bacnet_master.add_resource(NetworkAllPoints, '/b/network/discover/points/<string:network_uuid>')
api_bacnet_master.add_resource(DeviceAllPoints, '/b/device/discover/points/<string:device_uuid>')
api_bacnet_master.add_resource(DevicePollAllPoints, '/b/device/poll/points/<string:device_uuid>')
api_bacnet_master.add_resource(DeviceObjectList, '/b/device/objects/<string:device_uuid>')
api_bacnet_master.add_resource(PointBACnetRead, '/b/points/read/pv/<string:point_uuid>')
api_bacnet_master.add_resource(PointBACnetWrite, '/b/points/write/pv/<string:point_uuid>')
api_bacnet_master.add_resource(PointRelease, '/b/points/write/release/<string:point_uuid>')


# api_bacnet_master.add_resource(DiscoverPoints,
# '/b/points/discover_points/<string:device_uuid>/<string:add_points>/<string:get_pv>')
# api_bacnet_master.add_resource(AddAllPoints,
# '/b/network/network_point_list/add/<string:network_uuid>/<string:add_points>') api_bacnet_master.add_resource(
# AddAllPointsNew, '/b/points/network_point_list/poll/<string:network_uuid>') api_bacnet_master.add_resource(
# GetAllPoints, '/b/points/network_point_list/<string:network_uuid>/<string:timeout>')
# api_bacnet_master.add_resource(UnknownDeviceObjects, '/b/device/unknown/objects/<string:network_uuid>')
# api_bacnet_master.add_resource(UnknownReadPointPv, '/b/point/unknown/point_pv/<string:network_uuid>')

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
api_system = Api(bp_system)
api_system.add_resource(Ping, '/ping')
