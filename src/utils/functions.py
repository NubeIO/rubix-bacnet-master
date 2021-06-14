import uuid
import ipaddress


class Functions:

    @staticmethod
    def to_int(s):
        try:
            s = float(s)
            s = int(float(s))
            return s
        except ValueError as e:
            return e

    @staticmethod
    def to_float(s):
        try:
            s = float(s)
            return s
        except ValueError as e:
            return e

    @staticmethod
    def to_bool(value):
        if value == True:
            return True
        elif not value:
            return False
        else:
            return {"True": True, "true": True}.get(value, False)

    @staticmethod
    def make_uuid() -> str:
        uuid_str = str(uuid.uuid4()).replace("-", "")
        return uuid_str[:8] + uuid_str[-8:]

    @staticmethod
    def is_valid_ip(address: str) -> bool:
        try:
            ipaddress.ip_address(address)
            return True
        except ValueError:
            return False
        except:
            return False

    @staticmethod
    def cidr_is_in_range(cidr: int) -> str or bool:
        """
        check that netmask/subnet s between 1 and 32 eg: /24
        :param cidr:
        :return:
        """
        return cidr in range(0, 33)

    @staticmethod
    def cidr_to_netmask(cidr: int) -> str or bool:
        try:
            r = ipaddress.IPv4Network(f"0.0.0.0/{cidr}").netmask
            return str(r)
        except ValueError:
            return False
        except:
            return False

    @staticmethod
    def netmask_to_cidr(netmask: str) -> int or bool:
        try:
            r = ipaddress.IPv4Network(f"0.0.0.0/{netmask}").prefixlen
            return int(r)
        except ValueError:
            return False
        except:
            return False

    @staticmethod
    def check_list_in_range(x: int, _list: list) -> bool:
        if x in range(-len(_list), len(_list)):
            return True
        else:
            return False

# @validates('ip')
# def validate_ip(self, _, value):
#     """
#     0.0.0.0 able to bind with 47808 but it unable to start BACnet server due to some reason. And when we insert new
#     IP it won't work, coz 47808 is been already reserved but bacnet client is not there to disconnect.
#     """
#     if value == "0.0.0.0":
#         raise ValueError("IP 0.0.0.0 doesn't not support")
#     return value
