import os


class DataPoint:
    # provides JSON data sources to further classes
    current_directory = os.getcwd()

    data_optionals = current_directory + '\\acc_list.json'
    data_basic_variant = current_directory + '\\sample_basic_variant.json'
    data_baumuster = current_directory + '\\sample_baumuster.json'
