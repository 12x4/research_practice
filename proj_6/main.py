from core.pickle1337 import Pickle1337


if __name__ == "__main__":

    # number = 123
    # string = "a;smdlksmndkjs dlkamdkmmdokfm ownefoi34j05340reakf  or"
    # bytes = bytearray(b"")
    # list_b = [number, string]
    # dump = Pickle1337.dump(list_b)
    dump = b"I\x80\x08"

    print(Pickle1337.load(dump))
    #
    # og = open("test_read.txt", "rb")
    # # print(og.name)
    # dump = Pickle1337.dump(og)
    # print(dump)
    # og.close()
    # dump = dump[:2] + b"x" + dump[3:]
    # new_file = Pickle1337.load(dump)
    # new_file.close()

    pass
