from flask_restful import reqparse, marshal_with
from rubix_http.exceptions.exception import NotFoundException, BadDataException, InternalServerErrorException
from rubix_http.resource import RubixResource

from src.bacnet_master.models.point import BacnetPointModel
from src.bacnet_master.resources.rest_schema.schema_point import point_all_attributes, point_all_fields, \
    point_extra_attributes
from src.bacnet_master.services.device import Device as DeviceService
from src.bacnet_master.utils.functions import to_bool


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
    def put(cls, point_uuid):
        data = Point.parser.parse_args()
        point: BacnetPointModel = BacnetPointModel.find_by_point_uuid(point_uuid)
        if point is None:
            point = Point.create_model(point_uuid, data)
            point.save_to_db()
        else:
            point.update(**data)
        return point

    @classmethod
    @marshal_with(point_all_fields)
    def patch(cls, point_uuid):
        data = Point.parser_patch.parse_args()
        point: BacnetPointModel = BacnetPointModel.find_by_point_uuid(point_uuid)
        if point is None:
            raise NotFoundException("Point not found")
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


class PointBACnetRead(RubixResource):
    @classmethod
    def get(cls, pnt_uuid, get_priority):
        point = BacnetPointModel.find_by_point_uuid(pnt_uuid)
        get_priority = to_bool(get_priority)
        if not point:
            raise NotFoundException('Points not found')
        read = DeviceService.get_instance().get_point_pv(point)
        if not isinstance(read, (int, float)):
            raise InternalServerErrorException(f"Error: {read}")
        if get_priority:
            priority = DeviceService.get_instance().get_point_priority(point)
            return {
                "point_name": point.point_name,
                "point_value": read,
                "priority": priority
            }
        else:
            return {
                "point_name": point.point_name,
                "point_value": read
            }


class PointBACnetWrite(RubixResource):
    @classmethod
    def post(cls, pnt_uuid, value, priority):
        point = BacnetPointModel.find_by_point_uuid(pnt_uuid)
        if not point:
            raise NotFoundException('Points not found')
        read = DeviceService.get_instance().write_point_pv(point, value, priority)
        if read:
            raise InternalServerErrorException('Error on point write')
        return {
            "point_name": point.point_name,
            "point_value": value,
            "priority": priority
        }


class PointRelease(RubixResource):
    @classmethod
    def post(cls, pnt_uuid, priority, feedback):
        point = BacnetPointModel.find_by_point_uuid(pnt_uuid)
        value = 'null'
        feedback = to_bool(feedback)
        if not point:
            raise NotFoundException('Points not found')
        write = DeviceService.get_instance().write_point_pv(point, value, priority)
        if write:
            raise InternalServerErrorException('Error on point write')
        if feedback:
            read = DeviceService.get_instance().get_point_pv(point)
            if not isinstance(read, (int, float)):
                raise BadDataException('release: False')
            else:
                return {
                    "release": True,
                    "value": read,
                    "priority": read
                }
        else:
            return {"release": True}
