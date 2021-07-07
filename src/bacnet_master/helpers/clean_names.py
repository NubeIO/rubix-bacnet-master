class CleanStrings:

    @staticmethod
    def remove_all_characters(val: str) -> str:
        if isinstance(val, str):
            return val.translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+'"})

    @staticmethod
    def to_underscore(val: str) -> str:
        val = val.replace(' ', '_')
        val = val.replace('__', '_')
        return val
