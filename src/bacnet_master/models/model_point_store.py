import logging
from rubix_http.exceptions.exception import NotFoundException
from src import db

logger = logging.getLogger(__name__)


class BACnetPointStoreModel(db.Model):
    __tablename__ = 'bacnet_points_store'
    point_uuid = db.Column(db.String, db.ForeignKey('bacnet_points.point_uuid'), primary_key=True, nullable=False)
    present_value = db.Column(db.Float(), nullable=False)
    ts = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f"PointStore(point_uuid = {self.point_uuid})"

    @classmethod
    def find_by_point_uuid(cls, point_uuid):
        return cls.query.filter_by(point_uuid=point_uuid).first()

    @classmethod
    def create_new_point_store_model(cls, point_uuid):
        return BACnetPointStoreModel(point_uuid=point_uuid, present_value=0)

    @classmethod
    def _check_cov(cls, _new, _existing_data, cov):
        if abs(_new - _existing_data) < cov:
            return [False, _existing_data]
        else:
            return [True, _new]

    @staticmethod
    def update_point_store(point_uuid: str, present_value: float):
        from src.bacnet_master.models.point import BacnetPointModel
        point = BacnetPointModel.find_by_point_uuid(point_uuid)
        if point.point_name:
            points_store = BACnetPointStoreModel.find_by_point_uuid(point_uuid)
            from flask import current_app
            from src import AppSetting
            setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
            point_name = point.point_name
            existing = points_store.present_value
            if not point.cov:
                cov = setting.bacnet.default_point_cov
            else:
                cov = point.cov or 0.1
            if cov <= 0:
                logger.info(
                    f"UPDATED POINT STORE  WHEN COV IS AT 0 point_name:{point_name} present_value{present_value} existing{existing} cov:{cov}")
                points_store.present_value = present_value
                db.session.commit()
                return {
                        "present_value": present_value,
                        "point_uuid": point_uuid,
                        "point_name": point_name
                    }
            else:
                check_for_cov = BACnetPointStoreModel()._check_cov(present_value, existing, cov)
                if check_for_cov[0]:
                    logger.info(
                        f"UPDATED POINT STORE point_name:{point_name} present_value{present_value} existing{existing} cov:{cov}")
                    points_store.present_value = present_value
                    db.session.commit()
                    return {
                        "present_value": present_value,
                        "point_uuid": point_uuid,
                        "point_name": point_name
                    }
                else:
                    logger.info(
                        f"DID NOT UPDATE POINT STORE point_name:{point.point_name} present_value{present_value} existing{existing} cov:{cov}")
        else:
            logger.info(
                f"DID NOT UPDATE POINT STORE point_uuid:{point_uuid} dosnt exists")
