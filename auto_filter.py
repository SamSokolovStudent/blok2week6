import csv


class FilterObject:
    """Generates an object for use of storing multiple types of data.

    Meant for use in dictionary as value to allow for quick accesibility
    of stored data."""
    def __init__(self, filter_value, index_value):
        """Sets initial values when generating object.

        @param:
            self
            filter_value
            index_value"""
        self.__filter_value = filter_value
        self.__index = index_value
        # Filter type defaults to None value.
        # Filter type is specified at "value_splitter()" function.
        self.__filter_type = None

    def set_filter_values(self, filter_value):
        self.__filter_value = filter_value

    def set_filter_type(self, filter_type):
        self.__filter_type = filter_type

    def get_filter_values(self):
        return self.__filter_value

    def get_index_value(self):
        return self.__index

    def get_filter_type(self):
        return self.__filter_type


def file_input():
    """Asks user for desired file to open.

    @return
        file_name"""
    file_name = input("Supports .TSV and .CSV files.\n"
                      "Enter file name: ")
    return file_name


def filter_input():
    """Generates a dictionary based on user input for use in filtering.

    @return:
        filter_dict: a dictionary with columns as key names and
        desired filters as values."""
    filter_dict = {}
    while True:
        filter_value_list = ([])
        # Column key and filter value are requried in first iteration.
        column_key = input("Enter the column name you want to filter on:\n"
                           ).lower()
        filter_value = input("Enter the value of the filter:\n"
                             "Requires ==, >=, >, < or =< operator.\n"
                             "Formatting example: ==,example\n").lower()
        filter_value_list.append(filter_value)
        while True:
            # Extra filters can be added.
            # Extra filters assume OR operator in later filtering step.
            extra_filter = input("Do you want to add another filter? y/n:\n")
            if extra_filter == "y":
                filter_value = input("Enter the value of the extra filter:\n"
                                     ).lower()
                filter_value_list.append(filter_value)
                continue
            else:
                break
        filter_dict[column_key] = filter_value_list
        extra_column = input("Do you want to add another column? y/n:\n")
        if extra_column != "y":
            break
    return filter_dict


def index_finder(filter_dict, open_file):
    """Finds the index of column key, creates & assigns FilterObject as
    new value.

    @param:
        filter_dict
        open_file

    @return:
        filter_dict"""
    with open(open_file) as opened_file:
        opened_tsv_file = csv.reader(opened_file, delimiter='\t')
        # Assigns first line of file through iterator object.
        iterator_first_line = next(opened_tsv_file)
        # Assigns index to every list element.
        for index, element in enumerate(iterator_first_line):
            element = element.lower()
            try:
                if element in filter_dict:
                    # Assigns new value to key.
                    # New value is FilterObject.
                    # FilterObject uses 'old' assigned input as filter.
                    # FilterObject assigns index.
                    filter_dict[element] = FilterObject(filter_dict[element],
                                                        index)
            except ValueError:
                print(f"An error occurred.\n"
                      f"{filter_dict[element]} could not be found in file.")
                keep_running = input("Do you want to ignore this? y/n:\n")
                if keep_running == "y":
                    pass
                else:
                    print("Shutting down.")
                    exit()
        return filter_dict


def value_splitter(filter_dict):
    """Splits filter values to separate operator from desired value.
    Reassigns FilterObject value.
    Assigns FilterObject filter type.

    @param:
        filter_dict

    @return:
        filter_dict
        """
    for column_key in filter_dict:
        temp_list = []
        # Retrieves unsplit values from FilterObject.
        list_of_values = filter_dict[column_key].get_filter_values()
        # Loops through unsplit values.
        for element in list_of_values:
            filter_type, filter_value = element.split(",")
            temp_list.append(filter_value)
            # Assigns new FilterObject filter type.
            filter_dict[column_key].set_filter_type(filter_type)
            # Reassigns FilterObject value.
            filter_dict[column_key].set_filter_values(temp_list)
    return filter_dict


def filter_lookup(object_dictionary, file):
    matching_points = len(object_dictionary)
    compliant_line_list = []
    with open(file) as open_file:
        tsv_file = csv.reader(open_file, delimiter='\t')
        boolean = False
        for line_ in tsv_file:
            points = 0
            if boolean is True:
                for key in object_dictionary:
                    index = object_dictionary[key].get_index_value()
                    value_ = object_dictionary[key].get_filter_values()
                    filter_type = object_dictionary[key].get_filter_type()
                    if filter_type == "==":
                        # print(line_[index], value_)
                        if line_[index] in value_:
                            points += 1
                        elif any(value_ in line_[index].lower() for value_ in
                                 value_
                                 ):
                            points += 1
                    elif filter_type == ">=":
                        if line_[index] == "":
                            break
                        integer_1 = float(line_[index])
                        integer_2 = [float(i) for i in value_]
                        for element in integer_2:
                            if integer_1 >= element:
                                points += 1
                    elif filter_type == ">":
                        if line_[index] == "":
                            break
                        integer_1 = float(line_[index])
                        integer_2 = [float(i) for i in value_]
                        for element in integer_2:
                            if integer_1 > element:
                                points += 1
                    elif filter_type == "<":
                        if line_[index] == "":
                            break
                        integer_1 = float(line_[index])
                        integer_2 = [float(i) for i in value_]
                        for element in integer_2:
                            if integer_1 < element:
                                points += 1
                    elif filter_type == "=<":
                        if line_[index] == "":
                            break
                        integer_1 = float(line_[index])
                        integer_2 = [float(i) for i in value_]
                        for element in integer_2:
                            if integer_1 <= element:
                                points += 1
            boolean = True
            if points >= matching_points:
                compliant_line_list.append(line_)
        return compliant_line_list


if __name__ == '__main__':
    user_input_file = file_input()
    user_filter_dict = filter_input()
    user_filter_dict = index_finder(user_filter_dict, user_input_file)
    user_filter_dict = value_splitter(user_filter_dict)
    total_found = len(filter_lookup(user_filter_dict, user_input_file))
    filtered_list = filter_lookup(user_filter_dict, user_input_file)
    for line in filtered_list:
        print(line)
    print(f"A total of {total_found} matches were found.")
