import logging
from threading import Thread

from flask import current_app

from src.bacnet_master.polling.polling import Polling
from .setting import AppSetting

logger = logging.getLogger(__name__)


class FlaskThread(Thread):
    """
    To make every new thread behinds Flask app context.
    Maybe using another lightweight solution but richer: APScheduler <https://github.com/agronholm/apscheduler>
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = current_app._get_current_object()

    def run(self):
        with self.app.app_context():
            super().run()


class Background:
    @staticmethod
    def run():
        from src.bacnet_master.services.network import Network
        from src.mqtt import MqttClient

        setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        logger.info("Running Background Task...")
        if setting.mqtt.enabled:
            FlaskThread(target=MqttClient().start, daemon=True, kwargs={'config': setting.mqtt}).start()

        if setting.bacnet.master_enabled:
            Network.get_instance().start()
            FlaskThread(target=Polling.run, daemon=True).start()
