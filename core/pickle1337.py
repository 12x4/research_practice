import pickle
import io

INT = b'I' # code 73
STR = b'S' # code 83
BYTE = b"B" # code 66
LIST = b"U" # code 85
FILE = b"F" # code 70


class Pickle1337:
    def __init__(self):
        pass

    @staticmethod
    def dump(obj):

        result = bytearray()
        obj_type = str(type(obj))

        if isinstance(obj, int):
            byte_count = (obj.bit_length() + 7) // 8

            if byte_count > 128:
                raise Exception("Слишком большое число, макс 258 ** 127 - 1 байт")

            if obj == 0:
                result += INT + b"\x01\x00"

            elif obj > 0:
                result += INT + byte_count.to_bytes() + obj.to_bytes(byte_count)

            elif obj < 0:
                result += INT + (byte_count + 127).to_bytes() + (obj * -1).to_bytes(byte_count)

        elif isinstance(obj, str):
            byte_count = len(obj.encode())

            if byte_count > 256 ** 4:
                raise Exception("Слишком большая строка, макс 4GB - 1")

            result += STR

            if byte_count == 0:
                result += b"\x00\x00\x00\x00"

            else:
                result += byte_count.to_bytes(4) + obj.encode()

        elif isinstance(obj, bytearray):

            result += BYTE
            len_obj = len(obj)

            result += len_obj.to_bytes(4) + obj
            pass

        elif isinstance(obj, list):

            for ind in obj:

                if isinstance(ind, str) or isinstance(ind, int):
                    result += Pickle1337.dump(ind)
                else:
                    raise Exception("Пу-пу-пу")

            len_obj = len(result)

            if len_obj > 256 ** 6:
                raise Exception("Слишком большой обьем данных в списке, макс 256 ** 6 - 1 байт")

            result = LIST + len_obj.to_bytes(6) + result
            pass

        elif "io" in obj_type:

            data = obj.read()

            if "TextIOWrapper" in obj_type:
                data = data.encode()

            len_obj = len(data)
            obj_name = obj.name

            if len(obj_name) > 256:
                raise Exception("Слишком большое имя файла, макс 256 - 1 байт")
            if len(data) > 256 ** 6:
                raise Exception("Слишком много данных в файле, макс 256 ** 6 - 1 байт")

            result += FILE + len(obj_name).to_bytes(1) + obj_name.encode() + len_obj.to_bytes(6) + data

        else:
            return pickle.dump(obj)

        return result

    @staticmethod
    def load(data):

        cursor = 0
        redump_list = []

        while cursor < len(data):

            if data[cursor] == 73:
                len_obj = data[cursor + 1]
                cursor += 2

                _flag = False
                if len_obj >= 128:
                    len_obj -= 127
                    _flag = True

                _int = data[cursor: cursor + len_obj]
                cursor += len_obj

                if _flag:
                    redump_list.append(int.from_bytes(_int) * -1)
                    continue
                redump_list.append(int.from_bytes(_int))

            elif data[cursor] == 83:

                len_obj = int.from_bytes(data[cursor + 1: cursor + 5])
                cursor += 5

                if len_obj == 0:
                    redump_list.append("")

                redump_list.append(data[cursor: cursor + len_obj].decode())
                cursor += len_obj

            elif data[cursor] == 66:

                len_obj = int.from_bytes(data[cursor + 1: cursor + 5])

                cursor += 5

                if len_obj == 0:
                    redump_list.append(bytearray())
                redump_list.append(bytearray(data[cursor: cursor + len_obj]))

                cursor += len_obj

            elif data[cursor] == 85:

                len_obj = int.from_bytes(data[cursor + 1: cursor + 7])
                cursor += 7

                if len_obj == 0:
                    return []
                return Pickle1337.load(data[cursor: cursor + len_obj])

            elif data[cursor] == 70:

                len_obj_name = int.from_bytes(data[cursor + 1: cursor + 2])
                cursor += 2
                obj_name = data[cursor: cursor + len_obj_name].decode()
                cursor += len_obj_name

                len_obj = int.from_bytes(data[cursor: cursor + 6])
                cursor += 6
                file_data = data[cursor: cursor + len_obj]

                new_file = open(obj_name, "w+b")
                new_file.write(file_data)

                cursor += len_obj

                redump_list.append(new_file)

            else:
                pass

            if cursor > len(data):
                raise Exception("Невозможно десериализовать объекты")
            # cursor += 1

        if len(redump_list) == 1:
            return redump_list[0]
        return redump_list

    def __str__(self):
        return "HIHIIHIHIHIHIHI"


