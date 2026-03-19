from .rsa import key
# from core.cipher import cipher
from .freq_analys import freq_analisys
from .hack_rsa import hack_rsa
from .utils import *

import json
import logging
import sys


class dict_for_attack(dict):
    def __init__(self, name, attack_dict):
        super().__init__(attack_dict)
        self.name = name
        pass


class console_app:

    def __init__(self, config_file="json_saves/save_dict.json"):
        self.config_file = get_resource_path(config_file.split("/"))
        self.list_dict = []

        self.fr = freq_analisys()
        self.hack = hack_rsa()

        self.read_in_file()


    def main(self):

        while True:
            self.main_info()
            user_input = input("Ввод:")

            # Частотный анализ текста
            if user_input == "1":

                print("Введите текст для взлома Ctrl + D для завершения ввода:")

                text = sys.stdin.read()

                # Тут выбор языков ДОЛЖЕН БЫТЬ ЖЕЛАТЕЛЬНО

                self.fr.analys_enc_text(text)
                self.fr.create_etalon(num=True, symb=True)
                self.fr.merging_dict()

                temp_dict = self.fr.get_diff_dict()

                name = input("Название нового словаря:")
                self.list_dict.append(dict_for_attack(name, temp_dict))

            # Атака по словарю
            elif user_input == "2":

                k = None
                degree = None
                module = None

                # Ввод k
                while True:
                    user_input = input("Введите k (2000):")

                    if user_input == "":
                        k = 2000
                        break

                    elif user_input == "0":
                        break

                    else:
                        try:
                            k = int(user_input)
                            break
                        except Exception as e:
                            print("Некорректный ввод!")

                if k is None:
                    continue

                # Ввод степени
                while True:
                    user_input = input("Введите степень открытого ключа:")

                    if user_input == "":
                        degree = 1000
                        break

                    elif user_input == "0":
                        break

                    else:
                        try:
                            degree = int(user_input)
                            break
                        except Exception as e:
                            print("Некорректный ввод!")

                if degree is None:
                    continue

                # Ввод модули
                while True:
                    user_input = input("Введите модуль открытого ключа:")

                    if user_input == "":
                        module = 1000
                        break

                    elif user_input == "0":
                        break

                    else:
                        try:
                            module = int(user_input)
                            break
                        except Exception as e:
                            print("Некорректный ввод!")

                if module is None:
                    continue


                self.hack.dict_attack(k, key(degree, module))
                temp_dict = self.hack.get_dict()

                name = input("Название нового словаря:")
                self.list_dict.append(dict_for_attack(name, temp_dict))

            # Дешифровка с выбором словаря
            elif user_input == "3":

                select_dict = None

                self.print_list_dict()

                print("Выберите словарь введя его индекс(левое число)")
                user_input = input("Ввод:")

                if 1 <= int(user_input) <= len(self.list_dict):
                    select_dict = int(user_input) - 1
                    print(f"Выбран словарь {self.list_dict[int(user_input) - 1].name}")
                else:
                    print("Некорректный ввод!")

                print("Введите текст для взлома Ctrl + D для завершения ввода:")
                encrypted_text = sys.stdin.read()

                decrypted_text = self.hack.hack(encrypted_text, attack_dict=self.list_dict[select_dict])
                print(decrypted_text)


            # Редактор словарей
            elif user_input == "4":

                while True:

                    self.print_list_dict()

                    print()
                    print("0 Выход")
                    print("- удалить словарь")
                    print("Для редактирования словаря введите его индекс(левое число)")

                    user_input = input("Ввод:")

                    if user_input == "0":
                        break

                    # Удаление
                    elif user_input == "-":
                        print("Для удаления словаря введите его индекс(левое число)")
                        user_input = input("Ввод:")
                        if 1 <= int(user_input) <= len(self.list_dict):
                            del self.list_dict[int(user_input) - 1]
                        else:
                            print("Некорректный ввод!")

                    # Редактирование
                    elif 1 <= int(user_input) <= len(self.list_dict):
                        temp_dict = self.replace_dict(self.list_dict[int(user_input) - 1])
                        self.list_dict[int(user_input) - 1] = dict_for_attack(self.list_dict[int(user_input) - 1].name, temp_dict)

                    else:
                        print("Некорректный ввод!")

                pass

            # Загрузка\выгрузка словарей
            elif user_input == "5":

                print("0 Выход")
                print("1 Загрузка из файла")
                print("2 Выгрузка в файл")

                user_input = input("Ввод:")

                # Загрузка из файла словарей
                if user_input == "1":
                    self.read_in_file()

                # Выгрузка в файл
                elif user_input == "2":
                    self.write_to_file()

                elif user_input == "0":
                    pass

                else:
                    print("Некорректный ввод!")

            elif user_input == "0":
                break

            else:
                print("Некорректный ввод!")

    def main_info(self):
        print("\n0 Выход")
        print("1 Создание частотного словаря")
        print("2 Создание 'Атаки по словарю'")
        print("3 Дешифровка словарем")
        print("4 Редактирование словарей")
        print("5 Загрузка/выгрузка словарей из файла\n")

    # Заменя элементов в словаре для юзера
    def replace_dict(self, temp_dict):

        count_item = len(temp_dict)

        while True:
            self.print_dict(temp_dict)

            print("Для выхода из этой опции введите 0")
            print("Для изменения связки введите его индекс, расположены слева")

            user_input = input("Ввод:")

            if user_input == "0":
                break

            elif 1 <= int(user_input) <= count_item:

                print("Введите это чтобы оставить без изменений - '\\0/'")
                key = input("key:")
                value = input("value:")

                temp_list = list(temp_dict.keys())

                if value != "\\0//":
                    temp_dict[temp_list[int(user_input) - 1]] = value

                if key != "\\0/":
                    temp_list[int(user_input) - 1] = key

                temp_dict = dict(zip(temp_list, list(temp_dict.values())))

            else:
                print("Некорректный ввод!")

        return temp_dict

    # Для печати словаря юзеру
    def print_dict(self, temp_dict):

        for ind, item  in enumerate(temp_dict, start=1):
            print(f"{ind}. {item} - {temp_dict[item]}")

    # Вывод списка словарей
    def print_list_dict(self):
        for ind, item in enumerate(self.list_dict, start=1):
            print(f"{ind}. {item.name}")

    # Подгрузка словарей из файла
    def read_in_file(self):
        data = {}

        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                # Загружаем данные из файла в переменную
                data = json.load(f)
            logging.info(f"Чтение config.json успешно")

        except Exception as e:
            logging.warning(f"Не ужалось прочитать config.json \n {e}")

        # Собираем список словарей
        for item in data:
            self.list_dict.append(dict_for_attack(item, data[item]))

    # Запись словарей в файл
    def write_to_file(self):

        data = {}
        for item in self.list_dict:
            data[item.name] = item

        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logging.info(f"Запись config.json успешно")

        except Exception as e:
            logging.error(f"Не смог записать в конфигурационный файл \n{e}")

