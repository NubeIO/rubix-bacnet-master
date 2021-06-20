import logging

from flask import jsonify
from flask_restful import reqparse, fields, marshal_with
from rubix_http.exceptions.exception import NotFoundException, BadDataException
from rubix_http.resource import RubixResource

from src.bacnet_master.models.network import BacnetNetworkModel
from src.bacnet_master.resources.rest_schema.schema_network import network_all_attributes, network_all_fields, \
    network_extra_attributes
from src.bacnet_master.services.network import Network as NetworkService
from src.utils.functions import Functions

logger = logging.getLogger(__name__)


class NetworkBase(RubixResource):
    parser = reqparse.RequestParser()
    for attr in network_all_attributes:
        parser.add_argument(attr,
                            type=network_all_attributes[attr]['type'],
                            required=network_all_attributes[attr].get('required', None),
                            help=network_all_attributes[attr].get('help', None),
                            store_missing=False)

    post_parser = reqparse.RequestParser()
    all_attributes = {**network_extra_attributes, **network_all_attributes}
    for attr in all_attributes:
        post_parser.add_argument(attr,
                                 type=all_attributes[attr]['type'],
                                 required=all_attributes[attr].get('required', None),
                                 help=all_attributes[attr].get('help', None),
                                 store_missing=False)


class AddNetwork(NetworkBase):
    parser_patch = reqparse.RequestParser()
    for attr in network_all_attributes:
        parser_patch.add_argument(attr,
                                  type=network_all_attributes[attr]['type'],
                                  required=False,
                                  help=network_all_attributes[attr].get('help', None),
                                  store_missing=False)

    @classmethod
    @marshal_with(network_all_fields)
    def put(cls):
        network_uuid = Functions.make_uuid()
        data = Network.parser.parse_args()
        network = BacnetNetworkModel.find_by_network_uuid(network_uuid)
        if network is None:
            network = Network.create_network_model_obj(network_uuid, data)
            network.save_to_db()
        else:
            network.update(**data)
        NetworkService.get_instance().add_network(network)
        return network


class Network(NetworkBase):
    parser_patch = reqparse.RequestParser()
    for attr in network_all_attributes:
        parser_patch.add_argument(attr,
                                  type=network_all_attributes[attr]['type'],
                                  required=False,
                                  help=network_all_attributes[attr].get('help', None),
                                  store_missing=False)

    @classmethod
    @marshal_with(network_all_fields)
    def get(cls, network_uuid):
        network = BacnetNetworkModel.find_by_network_uuid(network_uuid)
        if not network:
            raise NotFoundException("Network not found")
        return network

    @classmethod
    @marshal_with(network_all_fields)
    def patch(cls, network_uuid):
        data = Network.parser_patch.parse_args()
        network: BacnetNetworkModel = BacnetNetworkModel.find_by_network_uuid(network_uuid)
        if network is None:
            raise NotFoundException("Network not found")
        network.update(**data)
        NetworkService.get_instance().add_network(network)
        return network

    @classmethod
    def delete(cls, network_uuid):
        network = BacnetNetworkModel.find_by_network_uuid(network_uuid)
        if network:
            network.delete_from_db()
            NetworkService.get_instance().delete_network(network)
        return '', 204

    @staticmethod
    def create_network_model_obj(network_uuid, data):
        return BacnetNetworkModel(network_uuid=network_uuid, **data)


class NetworkList(NetworkBase):
    @classmethod
    @marshal_with(network_all_fields, envelope="networks")
    def get(cls, with_children):
        with_children = Functions.to_bool(with_children)
        if not with_children:
            network = BacnetNetworkModel.find_all()
            network[0].devices = []
            return network
        else:
            return BacnetNetworkModel.find_all()


class NetworksIds(RubixResource):
    @classmethod
    @marshal_with({'network_uuid': fields.String}, envelope="networks")
    def get(cls):
        return BacnetNetworkModel.find_all()
