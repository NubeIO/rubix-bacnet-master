


class CleanStrings:

    def remove_leading_whitespace(self, text: str) -> str:
        """
        remove white space at front/back of string
        :param text:
        :return:
        """
        return text.strip()

    def replace_and(self, text: str) -> str:
        """
        replace & with AND to help with naming conventions
        :param text:
        :return:
        """
        return text.replace('&', 'AND')

    def remove_double_whitespace(self, text: str) -> str:
        """
        remove double whitespace string
        :param text:
        :return:
        """
        return " ".join(text.split())

    def remove_all_characters(self, text: str) -> str:
        """
        remove all characters of string
        :param text:
        :return:
        """
        return text.translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+'"})

    def replace_white_underscore(self, text: str) -> str:
        """
        remove white
        :param text:
        :return:
        """
        return text.replace(' ', '_')

    def replace_white_dash(self, text: str) -> str:
        """
        remove white
        :param text:
        :return:
        """
        return text.replace(' ', '-')

    def replace_double_underscore_with_single(self, text: str) -> str:
        """
        replace underscores
        :param text:
        :return:
        """
        return text.replace(r"__", "_").replace(r"___", "_")

    def remove_double_underscore(self, text: str) -> str:
        """
        remove double underscores
        :param text:
        :return:
        """
        return text.replace(r"__", "")

    def remove_front_underscore(self, text: str) -> str:
        """
        remove front underscores
        :param text:
        :return:
        """
        prefix = "_"
        return text[len(prefix):] if text.startswith(prefix) else text

    def remove_back_underscore(self, text: str) -> str:
        """
        remove back underscores
        :param text:
        :return:
        """
        prefix = "_"
        return text.rstrip(prefix)

    def capitalize_each_word(self, text: str) -> str:
        """
        capitalize each word in text
        :param text:
        :return:
        """

        return text.title()

    def to_lower(self, text: str) -> str:
        """
        make text lower
        :param text:
        :return:
        """
        return text.lower()

    def to_upper(self, text: str) -> str:
        """
        make text upper
        :param text:
        :return:
        """
        return text.upper()

    def just_clean(self, text: str):
        _out = self.remove_leading_whitespace(text)
        _out = self.replace_and(_out)
        _out = self.remove_all_characters(_out)
        _out = self.remove_double_whitespace(_out)
        _out = self.remove_front_underscore(_out)
        _out = self.remove_back_underscore(_out)
        return _out

    def nube_dash_convention(self, text: str, to_convention: bool = True, to_upper: bool = None, to_lower: bool = None):
        _out = CleanStrings().just_clean(text)
        if to_convention:
            _out = self.replace_white_dash(_out)
            _out = self.capitalize_each_word(_out)
        if to_upper:
            _out = self.to_upper(_out)
        if to_lower:
            _out = self.to_lower(_out)
        return _out

    def nube_underscore_convention(self, text: str, to_convention: bool = True, to_upper: bool = None, to_lower: bool = None):
        _out = CleanStrings().just_clean(text)
        if to_convention:
            _out = self.replace_white_underscore(_out)
            _out = self.capitalize_each_word(_out)
        if to_upper:
            _out = self.to_upper(_out)
        if to_lower:
            _out = self.to_lower(_out)
        return _out


# names = ["FCU A & B", "Whats up in @ustralia", "FCU!#!@ 1 Start/Stop", "  FCU 1!@#/A ", "_FCU!@# 1/A ",
#          "FCU'1!@", "FCU 1\A ", "__FCU 1\A_ ", "FCU_1_A", "FCU1", "FCUA1_L1_"]
#
# for i in names:
#     out = CleanStrings().nube_dash_convention(i, to_upper=True)
#     print(out)
