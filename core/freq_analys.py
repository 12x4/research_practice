import json
import logging

import numpy as np
from scipy.optimize import linear_sum_assignment
from .utils import *


class freq_dict:
    def __init__(self, abc_dict=None, symb_count=0, ABC=None, num_round=5):

        if abc_dict is None:
            self.main_dict = {}
        else:
            self.main_dict = abc_dict

        # Без словаря проверки не будет
        if ABC is None:
            self.ABC = None
        else:
            self.ABC = "".join(ABC)

        self.symb_count = symb_count
        self.num_round = num_round

        self.percent_dict = None

    # Сам частотный анализ
    def freq_analys_text(self, text=None, sp_lit=None):

        # Проверка на разделение
        if sp_lit is not None:
            chars = text.split(sp_lit)
        else:
            chars = text

        for char in chars:

            # Проверка на наличие в словаре
            if self.check_in_ABC(char):

                if char not in self.main_dict:
                    self.main_dict[char] = 1
                else:
                    self.main_dict[char] += 1

                self.symb_count += 1

        self.calc_precent()

    # В словаре меняет числа на проценты и возвращает
    def calc_precent(self):
        temp_dict = {}

        for char in self.main_dict:
            temp_dict[char] = round(self.main_dict[char] / self.symb_count, self.num_round)

        self.percent_dict = dict(sorted(temp_dict.items(), key=lambda item: item[1], reverse=True))

    # Проверка на наличие в словаре
    def check_in_ABC(self, char):

        if self.ABC is None:
            return True

        return char in self.ABC

    def dict_clear(self):
        self.main_dict.clear()
        self.symb_count = 0

    def __add__(self, other):

        if self.main_dict is None:
            self.main_dict = {}
        self.main_dict |= other.main_dict
        self.symb_count += other.symb_count

        if self.ABC is None:
            self.ABC = other.ABC
        elif other.ABC is None:
            pass
        else:
            self.ABC += other.ABC

        self.calc_precent()

    def __iadd__(self, other):

        if self.main_dict is None:
            self.main_dict = {}
        self.main_dict |= other.main_dict
        self.symb_count += other.symb_count

        if self.ABC is None:
            self.ABC = other.ABC
        elif other.ABC is None:
            pass
        else:
            self.ABC += other.ABC

        self.calc_precent()

        return self

    def __len__(self):
        return len(self.main_dict)

    def __iter__(self):
        return iter(self.percent_dict)

    def __getitem__(self, item):
        return self.percent_dict[item]

    def values(self):
        return self.percent_dict.values()

    def keys(self):
        return self.percent_dict.keys()

    def get_symb_count(self):
        return self.symb_count

    def get_precent_dict(self):
        return self.percent_dict
    
    def get_dict(self):
        return self.main_dict


class freq_analisys:
    def __init__(self, conf_file="json_saves/config.json"):
        
        # конфигурационный файл
        # Хранятся частоты разных алфавитов с количеством символов 
        # Для дальнейшего объединения в один эталонный словарь с "пропорциональным" сохранением частот 
        self.conf_file = get_resource_path(conf_file.split("/"))
        
        # Алфавиты
        self.abc_num = "1234567890"
        self.abc_eng = "abcdefghijklmnopqrstuvwxyz"
        self.abc_rus = "абвгдеёжзийклмнопрстуфхцщшчъыьэюя"
        self.abc_symbols = ",./\\!@#$%^&*()_-+="

        # Словари для записи в файл
        self.eng_dict = freq_dict(ABC=[self.abc_eng])
        self.rus_dict = freq_dict(ABC=[self.abc_rus])
        self.num_dict = freq_dict(ABC=[self.abc_num])
        self.symb_dict = freq_dict(ABC=[self.abc_symbols])

        # Частотный словарь шифро текста
        self.enc_dict = freq_dict()
        # Частотный эталонный словарь
        self.etalon_dict = freq_dict()

        # Объединение эталонного и шифро словарей для дешифровки
        self.diff_dict = {}

        # Сюда подгружаются все словари из config_file
        self.data_dict = {}
        self.read_witch_file()

    # Создает частотный словарь для шифро текста
    def analys_enc_text(self, text):
        self.enc_dict.freq_analys_text(text, sp_lit=" ")

    # Подсчитывает частоты обычного(не зашифрованного) текста
    # C проверка на наличие символа в алфавите
    def analys_abc_text(self, text=None, file_name=None, eng=True, rus=False, num=False, symb=False):

        if file_name is not None and text is not None:
            logging.warning("В функцию analys_abc_text поданы и текст и файл, анализирую только текст")

        # Анализ текста
        if text is not None:

            if eng:
                self.eng_dict.freq_analys_text(text)
            if rus:
                self.rus_dict.freq_analys_text(text)
            if num:
                self.num_dict.freq_analys_text(text)
            if symb:
                self.symb_dict.freq_analys_text(text)

        # Анализ файла
        elif file_name is not None:

            try:
                with open(file_name, "r") as f:
                    for line in f:

                        if eng:
                            self.eng_dict.freq_analys_text(line)
                        if rus:
                            self.rus_dict.freq_analys_text(line)
                        if num:
                            self.num_dict.freq_analys_text(line)
                        if symb:
                            self.symb_dict.freq_analys_text(line)

            except Exception as e:
                logging.warning(f"Не смог прочитать файл {file_name} \n {e}")

        else:
            logging.info("analys_abc_text был вызван без данных")

    # Создание эталонного словаря из данных конфигурационного файла
    def create_etalon(self, eng=True, rus=False, num=False, symb=False):
        
        self.etalon_dict.dict_clear()

        if eng:
            self.etalon_dict += freq_dict(self.data_dict["eng"]["dict"], self.data_dict["eng"]["symb_count"], self.abc_eng)
        if rus:
            self.etalon_dict += freq_dict(self.data_dict["rus"]["dict"], self.data_dict["rus"]["symb_count"], self.abc_rus)
        if num:
            self.etalon_dict += freq_dict(self.data_dict["num"]["dict"], self.data_dict["num"]["symb_count"], self.abc_num)
        if symb:
            self.etalon_dict += freq_dict(self.data_dict["symb"]["dict"], self.data_dict["symb"]["symb_count"], self.abc_symbols)

    # Для соединений словарей
    # Пример эталонный и зашифрованный, соединение по частотам
    def merging_dict(self, dict_1=None, dict_2=None):

        if dict_1 is None and dict_2 is None:

            dict_1 = self.enc_dict
            dict_2 = self.etalon_dict

        else:
            logging.error("На входе merge неправильно поданы словари")
            return

        result_dict = {}

        if len(dict_1) == len(dict_2):

            list_1 = list(dict_1)
            list_2 = list(dict_2)

            for ind in range(len(list_1)):
                result_dict[list_1[ind]] = list_2[ind]

        elif True:

            # Венгерский алгоритм
            cipher_keys = list(dict_1.keys())
            ref_keys = list(dict_2.keys())

            n = len(cipher_keys)
            m = len(ref_keys)

            # создаём матрицу стоимости
            cost = np.zeros((n, m))

            for i, c in enumerate(cipher_keys):
                for j, r in enumerate(ref_keys):
                    cost[i][j] = abs(dict_1[c] - dict_2[r])

            row_ind, col_ind = linear_sum_assignment(cost)

            result_dict = {}
            for i, j in zip(row_ind, col_ind):
                result_dict[cipher_keys[i]] = ref_keys[j]

            # если символов больше, чем соответствий
            for i in range(n):
                if cipher_keys[i] not in result_dict:
                    result_dict[cipher_keys[i]] = None

        self.diff_dict.clear()
        self.diff_dict = result_dict

    # Запись в файл словарей
    def write_to_file(self):

        data = {
            "eng": {
                "symb_count": self.eng_dict.symb_count,
                "dict": self.eng_dict.get_dict()
            },
            "rus": {
                "symb_count": self.rus_dict.symb_count,
                "dict": self.rus_dict.get_dict()
            },
            "num": {
                "symb_count": self.num_dict.symb_count,
                "dict": self.num_dict.get_dict()
            },
            "symb": {
                "symb_count": self.symb_dict.symb_count,
                "dict": self.symb_dict.get_dict()
            }
        }

        try:
            with open(self.conf_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logging.info(f"Запись config.json успешно")

        except Exception as e:
            logging.error(f"Не смог прочитать конфигурационный файл \n{e}")

    # Чтение из файла словарей
    def read_witch_file(self):

        try:
            with open(self.conf_file, "r", encoding="utf-8") as f:
                # Загружаем данные из файла в переменную
                self.data_dict = json.load(f)
            logging.info(f"Чтение config.json успешно")

        except Exception as e:
            logging.warning(f"Не ужалось прочитать config.json \n {e}")

    def get_etalon_dict(self):
        return self.etalon_dict

    def get_enc_dict(self):
        return self.enc_dict

    def get_diff_dict(self):
        return self.diff_dict




