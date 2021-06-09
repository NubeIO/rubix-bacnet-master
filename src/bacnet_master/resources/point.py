from flask_restful import Resource, reqparse, abort, marshal_with
from src.bacnet_master.models.point import BacnetPointModel
from src.bacnet_master.resources.fields import point_fields
from src.bacnet_master.services.device import Device as DeviceService
from src.bacnet_master.utils.functions import to_bool


class Point(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('point_name',
                        type=str,
                        required=False,
                        help='True if device is type MSTP'
                        )
    parser.add_argument('point_obj_id',
                        type=int,
                        required=True,
                        help='Every device needs a network device_uuid'
                        )
    parser.add_argument('point_obj_type',
                        type=str,
                        required=False,
                        help='True if device is type MSTP'
                        )
    parser.add_argument('device_uuid',
                        type=str,
                        required=False,
                        help='Used for discovering networking (set to 0 to disable)'
                        )

    @marshal_with(point_fields)
    def get(self, uuid):
        p = BacnetPointModel.find_by_uuid(uuid)
        if not p:
            abort(404, message='Point not found.')
        return p

    @marshal_with(point_fields)
    def post(self, uuid):
        data = Point.parser.parse_args()
        p = Point.create_model(uuid, data)
        if p.find_by_uuid(uuid) is not None:
            abort(409, message="Already exist this value")
        p.save_to_db()
        return p, 201

    @marshal_with(point_fields)
    def put(self, uuid):
        data = Point.parser.parse_args()
        p = BacnetPointModel.find_by_uuid(uuid)
        if p is None:
            p = Point.create_model(uuid, data)
        else:
            p.point_name = data['point_name']
            p.point_obj_id = data['point_obj_id']
            p.point_obj_type = data['point_obj_type']
            p.device_uuid = data['device_uuid']
        p.save_to_db()
        return p

    def delete(self, uuid):
        p = BacnetPointModel.find_by_uuid(uuid)
        if p:
            p.delete_from_db()
        return '', 204

    @staticmethod
    def create_model(uuid, data):
        return BacnetPointModel(point_uuid=uuid, point_name=data['point_name'], point_obj_id=data['point_obj_id'],
                                point_obj_type=data['point_obj_type'], device_uuid=data['device_uuid'])


class PointList(Resource):
    @marshal_with(point_fields)
    def get(self):
        p = BacnetPointModel.query.all()
        if not p:
            abort(404, message='Points not found.')
        return p


class PointBACnetRead(Resource):
    def get(self, pnt_uuid):
        point = BacnetPointModel.find_by_uuid(pnt_uuid)
        if not point:
            abort(404, message='Points not found')
        read = DeviceService.get_instance().get_point_pv(point)
        if not isinstance(read, (int, float)):
            abort(404, message='Failed to read point value')
        return {
            "point_name": point.point_name,
            "point_value": read
        }


class PointBACnetWrite(Resource):
    def post(self, pnt_uuid, value, priority):
        point = BacnetPointModel.find_by_uuid(pnt_uuid)
        if not point:
            abort(404, message='Points not found')
        read = DeviceService.get_instance().write_point_pv(point, value, priority)
        if read:
            read(404, message={"error": "on point write"})
        return {
            "point_name": point.point_name,
            "point_value": value,
            "priority": priority
        }


class PointRelease(Resource):
    def post(self, pnt_uuid, priority, feedback):
        point = BacnetPointModel.find_by_uuid(pnt_uuid)
        value = 'null'
        feedback = to_bool(feedback)
        if not point:
            abort(404, message='Points not found')
        write = DeviceService.get_instance().write_point_pv(point, value, priority)
        if write:
            abort(404, message={"error": "on point write"})
        if feedback:
            read = DeviceService.get_instance().get_point_pv(point)
            if not isinstance(read, (int, float)):
                abort(404, message={"release": False})
            else:
                return {
                    "release": True,
                    "value": read,
                    "priority": read
                }
        else:
            return {"release": True}
