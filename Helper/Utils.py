import sys


class Utils:

    @staticmethod
    def print_list_info(description, list):
        items = 'Items: ' + str(len(list))
        mem_size = 'Mem Size: ' + str(sys.getsizeof(list)/100000) + ' MB'
        print(description + ' - ' + items + ', ' + mem_size)
