import logging
from .rsa import key


class hack_rsa:

    def __init__(self):

        # Словарь для атаки по словарю
        self.dict_attack_dict = None


    # Для стройки словаря атаки по словарю
    def dict_attack(self, k, public_key: key):

        self.dict_attack_dict = {}

        for code in range(0, k):
            new_code = public_key.mod_pow(code)
            self.dict_attack_dict[str(new_code)] = chr(code)

    def hack(self, encrypted_text, sp_lit=" ", attack_dict=None):

        if attack_dict is None:

            if self.dict_attack_dict is None:
                logging.error("Не удалось взломать шифротекст, нету словаря")

            else:
                attack_dict = self.dict_attack_dict

        result_text = ""

        for char in encrypted_text.split(sp_lit):
            try:
                result_text += attack_dict[char]
            except Exception as e:
                result_text += "^"
                logging.info(f"Код {char} из шифротекста не оказался в словаре")
        logging.info(f"Взлом завершен")

        return result_text

    def get_dict(self):
        return self.dict_attack_dict




