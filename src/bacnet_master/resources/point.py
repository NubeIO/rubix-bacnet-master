from flask_restful import reqparse, marshal_with
from rubix_http.exceptions.exception import NotFoundException, BadDataException
from rubix_http.resource import RubixResource

from src.bacnet_master.models.point import BacnetPointModel
from src.bacnet_master.resources.rest_schema.schema_point import point_all_attributes, point_all_fields, \
    point_extra_attributes
from src.bacnet_master.services.device import Device as DeviceService
from src.bacnet_master.utils.functions import BACnetFunctions
from src.utils.functions import Functions


class PointBase(RubixResource):
    parser = reqparse.RequestParser()
    for attr in point_all_attributes:
        parser.add_argument(attr,
                            type=point_all_attributes[attr]['type'],
                            required=point_all_attributes[attr].get('required', None),
                            help=point_all_attributes[attr].get('help', None),
                            store_missing=False)
    post_parser = reqparse.RequestParser()
    all_attributes = {**point_extra_attributes, **point_all_attributes}
    for attr in all_attributes:
        post_parser.add_argument(attr,
                                 type=all_attributes[attr]['type'],
                                 required=all_attributes[attr].get('required', None),
                                 help=all_attributes[attr].get('help', None),
                                 store_missing=False)


class AddPoint(PointBase):
    parser_patch = reqparse.RequestParser()
    for attr in point_all_attributes:
        parser_patch.add_argument(attr,
                                  type=point_all_attributes[attr]['type'],
                                  required=False,
                                  help=point_all_attributes[attr].get('help', None),
                                  store_missing=False)

    @classmethod
    def add_point(cls, data):
        print(data)
        point_uuid = Functions.make_uuid()
        point_name = data.get("point_name")
        point_object_id = data.get("point_object_id")
        point_object_type = data.get("point_object_type")
        device_uuid = data.get("device_uuid")
        check_object_id: BacnetPointModel = BacnetPointModel.existing_object_id(device_uuid, point_object_id,
                                                                                point_object_type)
        if check_object_id:
            raise NotFoundException(f"Point same Object Type and Object id exists id:{point_object_id}")
        check_name: BacnetPointModel = BacnetPointModel.existing_object_name(point_name)
        if check_name:
            raise NotFoundException(f"Point name with that device exists point_name:{point_name}")
        point: BacnetPointModel = BacnetPointModel.find_by_point_uuid(point_uuid)
        if point is None:
            point = Point.create_model(point_uuid, data)
            point.save_to_db()
        else:
            point.update(**data)
        return point

    @classmethod
    @marshal_with(point_all_fields)
    def put(cls):
        data = Point.parser.parse_args()
        return cls.add_point(data)


class Point(PointBase):
    parser_patch = reqparse.RequestParser()
    for attr in point_all_attributes:
        parser_patch.add_argument(attr,
                                  type=point_all_attributes[attr]['type'],
                                  required=False,
                                  help=point_all_attributes[attr].get('help', None),
                                  store_missing=False)

    @classmethod
    @marshal_with(point_all_fields)
    def get(cls, point_uuid):
        point = BacnetPointModel.find_by_point_uuid(point_uuid)
        if not point:
            raise NotFoundException('Point not found.')
        return point

    @classmethod
    @marshal_with(point_all_fields)
    def patch(cls, point_uuid):
        point: BacnetPointModel = BacnetPointModel.find_by_point_uuid(point_uuid)
        if point is None:
            raise NotFoundException(f"Point not found {point_uuid}")
        data = Point.parser_patch.parse_args()
        point_name = data.get("point_name")
        point_object_id = data.get("point_object_id")
        point_object_type = data.get("point_object_type")
        device_uuid = data.get("device_uuid")
        check_object_id: BacnetPointModel = BacnetPointModel.existing_object_id(device_uuid,
                                                                                point_object_id,
                                                                                point_object_type)
        if isinstance(check_object_id, list):
            for i in check_object_id:
                if not point_uuid == i.point_uuid:
                    raise NotFoundException(f"Point same Object Type and Object id exists id:{point_object_id}")

        check_name: BacnetPointModel = BacnetPointModel.existing_object_name(point_name)
        if check_name:
            if isinstance(check_name, list):
                for i in check_name:
                    if not point_uuid == i.point_uuid:
                        raise NotFoundException(f"Point name with that device exists point_name:{point_name}")

        point.update(**data)
        return point

    @classmethod
    def delete(cls, point_uuid):
        point = BacnetPointModel.find_by_point_uuid(point_uuid)
        if point:
            point.delete_from_db()
        return '', 204

    @staticmethod
    def create_model(uuid, data):
        return BacnetPointModel(point_uuid=uuid, **data)


class PointList(PointBase):
    @classmethod
    @marshal_with(point_all_fields)
    def get(cls):
        return BacnetPointModel.find_all()

    @classmethod
    @marshal_with(point_all_fields)
    def post(cls):
        data = Point.post_parser.parse_args()
        point_uuid = data.pop('point_uuid')
        if BacnetPointModel.find_by_point_uuid(point_uuid) is not None:
            raise BadDataException(f"Point with point_uuid '{point_uuid}' already exists.")
        point = Point.create_model(point_uuid, data)
        point.save_to_db()
        return point


class DeletePointList(PointBase):
    @classmethod
    def delete(cls, device_uuid):
        point = BacnetPointModel.delete_all_points_by_device(device_uuid)
        if point:
            return '', 204
        else:
            return '', 404


class PointBACnetRead(RubixResource):

    @classmethod
    @marshal_with(point_all_fields)
    def post(cls, point_uuid):
        data = Point.post_parser.parse_args()
        point = BacnetPointModel.find_by_point_uuid(point_uuid)
        get_priority = data.get('get_priority')
        timeout = data.get('timeout')
        if timeout:
            timeout = Functions.to_int(timeout)
            if not isinstance(timeout, int):
                raise BadDataException(f"Error: timeout must be an int {timeout}")
        if not point:
            raise NotFoundException('Points not found')
        read = DeviceService.get_instance().get_point_pv(point)
        if not isinstance(read, (int, float)):
            raise BadDataException(f"Error on point read: {read}")
        if get_priority:
            priority = DeviceService.get_instance().get_point_priority_errors(point)
            print(1111)
            print(priority.get("value"))
            print(priority.get("error"))
            print(priority.get("error"))
            print(1111)
            if not priority.get("value"):
                raise BadDataException(f"Error on point read: {priority}")
            print(priority)
            return {
                "point_name": point.point_name,
                "point_object_id": point.point_object_id,
                "point_object_type": point.point_object_type,
                "point_uuid": point_uuid,
                "device_uuid": point.device_uuid,
                "point_enable": point.point_enable,
                "point_writable": point.point_writable,
                "get_priority": get_priority,
                "point_value": read,
                "priority_array": priority.get("value")
            }
        else:
            return {
                "point_name": point.point_name,
                "point_object_id": point.point_object_id,
                "point_object_type": point.point_object_type,
                "point_uuid": point_uuid,
                "device_uuid": point.device_uuid,
                "point_enable": point.point_enable,
                "point_writable": point.point_writable,
                "get_priority": get_priority,
                "point_value": read,
                "priority_array": {},
            }


class PointBACnetWrite(RubixResource):
    @classmethod
    @marshal_with(point_all_fields)
    def post(cls, point_uuid):
        point = BacnetPointModel.find_by_point_uuid(point_uuid)
        data = Point.post_parser.parse_args()
        point_write_value = data.get('point_write_value')
        point_write_value = Functions.to_float(point_write_value)
        priority = data.get('priority')
        priority = int(priority)
        feedback = data.get('feedback')
        timeout = data.get('timeout')
        if not isinstance(point_write_value, (int, float)):
            raise BadDataException(f"Error on point write: value must be a number {point_write_value}")
        if timeout:
            timeout = Functions.to_int(timeout)
            if not isinstance(timeout, int):
                raise BadDataException(f"Error: timeout must be an int {timeout}")
        if not point:
            raise NotFoundException(f"Point {point_uuid} not found")
        if not BACnetFunctions.check_priority(priority):
            raise NotFoundException('priority must be between 1 and 16')
        write = DeviceService.get_instance().write_point_pv(point, point_write_value, priority)
        if isinstance(write, str):
            raise BadDataException(f"Error on point write: {write}")
        if feedback:
            read = DeviceService.get_instance().get_point_pv(point)
            priority = DeviceService.get_instance().get_point_priority(point)
            if not isinstance(read, (int, float)):
                raise BadDataException('release: False')
            else:
                return {
                    "point_name": point.point_name,
                    "point_object_id": point.point_object_id,
                    "point_object_type": point.point_object_type,
                    "point_uuid": point_uuid,
                    "device_uuid": point.device_uuid,
                    "point_enable": point.point_enable,
                    "point_writable": point.point_writable,
                    "point_value": read,
                    "priority_array": priority
                }
        else:
            return {
                "point_name": point.point_name,
                "point_object_id": point.point_object_id,
                "point_object_type": point.point_object_type,
                "point_uuid": point_uuid,
                "device_uuid": point.device_uuid,
                "point_enable": point.point_enable,
                "point_writable": point.point_writable,
            }


class PointRelease(RubixResource):
    @classmethod
    @marshal_with(point_all_fields)
    def post(cls, point_uuid):
        point = BacnetPointModel.find_by_point_uuid(point_uuid)
        if not point:
            raise NotFoundException('Points not found')
        data = Point.post_parser.parse_args()
        priority = data.get('priority')
        priority = int(priority)
        feedback = data.get('feedback')
        timeout = data.get('timeout')
        value = 'null'

        if not BACnetFunctions.check_priority(priority):
            raise NotFoundException('priority must be between 1 and 16')
        write = DeviceService.get_instance().write_point_pv(point, value, priority)
        if isinstance(write, str):
            raise BadDataException(f"Error on point write: {write}")
        if feedback:
            read = DeviceService.get_instance().get_point_pv(point)
            priority = DeviceService.get_instance().get_point_priority(point)
            if not isinstance(read, (int, float)):
                raise BadDataException('release: False')
            else:
                return {
                    "point_value": read,
                    "point_name": point.point_name,
                    "point_object_id": point.point_object_id,
                    "point_object_type": point.point_object_type,
                    "point_uuid": point_uuid,
                    "priority_array": priority,

                }
        else:
            return {
                "point_name": point.point_name,
                "point_object_id": point.point_object_id,
                "point_object_type": point.point_object_type,
                "point_uuid": point_uuid,
                "priority_array": {},
            }
