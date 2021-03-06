import logging
import time
import polling2

from src.bacnet_master.resources.network import Network
from src.bacnet_master.resources.network_whois import poll_points_rpm

logger = logging.getLogger(__name__)


class Polling:

    @staticmethod
    def loop(enable_point_store):
        from src.mqtt import MqttClient
        discovery = False
        add_points = False
        timeout = 1
        networks = Network.get_networks()
        logger.info(f"POLLING LOOP ----------- POLLING----START------- ")
        from flask import current_app
        from src import AppSetting
        setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        mqtt_client = MqttClient()
        _delay = setting.bacnet.polling_time_between_devices
        _delay_points = setting.bacnet.polling_time_between_points
        for network in networks:
            logger.info(f"POLLING LOOP ----------- POLLING----NETWORKS------- ")
            devices = network.devices
            network_name = network.network_name
            network_uuid = network.network_uuid
            if devices:
                for device in devices:
                    time.sleep(_delay)
                    points_list = {}
                    if device.points:
                        logger.info(
                            f"POLLING LOOP ----- device_name:{device.device_name}---- POLLING----DEVICES------- ")
                        device_uuid = device.device_uuid
                        device_name = device.device_name
                        point_values = poll_points_rpm(device_uuid=device_uuid,
                                                       discovery=discovery,
                                                       add_points=add_points,
                                                       timeout=timeout
                                                       )

                        if not enable_point_store:
                            topic = f"{network_name}/{device_uuid}/{device_name}"
                            points_list["device"] = {"device_name": device_name, "points": point_values}
                            mqtt_client.publish_value(('poll', topic), points_list)
                            logger.info(f"POLLING LOOP device_name:{device_name} ")
                        else:
                            if point_values:
                                _points_list = point_values.get("discovered_points")
                                if _points_list:
                                    _points_list = _points_list.get("points")
                                    for point_type in _points_list:
                                        point_type = _points_list.get(point_type)
                                        for point in point_type:
                                            point_uuid = point.get("point_uuid")
                                            point_value = point.get("point_value")
                                            from src.bacnet_master.models.model_point_store import BACnetPointStoreModel
                                            point_store = BACnetPointStoreModel.update_point_store(point_uuid, point_value)
                                            if point_store:
                                                point_name = point_store.get("point_name")
                                                point_uuid = point_store.get("point_uuid")
                                                present_value = point_store.get("present_value")
                                                topic = f"{network_uuid}/{network_name}/{device_uuid}/{device_name}/{point_uuid}/{point_name}"
                                                time.sleep(_delay_points)
                                                payload = {"device_name": device_name, "point_name": point_name, "value": present_value, "point_write_value": None,
                                                           "ts": None, "enable": None, "fault": None}
                                                mqtt_client.publish_value(('poll', topic), payload)
                                                logger.info(f"POLLING LOOP ----------- FINISH----------- ")
                                            else:
                                                logger.info(f"POLLING LOOP ----------- FINISH----------- ")
                else:

                    logger.info(f"POLLING LOOP ----------- FINISH----------- ")

    @staticmethod
    def log_response(response):
        return response == 'success'

    @staticmethod
    def enable_polling():
        from src import AppSetting
        from flask import current_app
        setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        enable_polling = setting.bacnet.polling_enable or False
        polling_time = setting.bacnet.polling_time_in_seconds or 5
        enable_point_store = setting.bacnet.enable_point_store or False
        if polling_time <= 0:
            polling_time = 1
        if enable_polling:
            polling2.poll(lambda: Polling.loop(enable_point_store),
                          step=polling_time,
                          poll_forever=True,
                          ignore_exceptions=(),
                          check_success=Polling.log_response)

    @staticmethod
    def run():
        Polling.enable_polling()
