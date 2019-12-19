from operator import itemgetter


def format_as_table(data,
                    keys,
                    header=None,
                    sort_by_key=None,
                    sort_order_reverse=False):
    """Takes a list of dictionaries, formats the data, and returns the
    formatted data as a text table.

    Required Parameters:
        data - Data to process (list of dictionaries). (Type: List)
        keys - List of keys in the dictionary. (Type: List)

    Optional Parameters:
        header - The table header. (Type: List)
        sort_by_key - The key to sort by. (Type: String)
        sort_order_reverse - Default sort order is ascending, if
            True sort order will change to descending. (Type: Boolean)
    """
    # Sort the data if a sort key is specified (default sort order
    # is ascending)
    if sort_by_key:
        data = sorted(data,
                      key=itemgetter(sort_by_key),
                      reverse=sort_order_reverse)

    # If header is not empty, add header to data
    if header:
        # Get the length of each header and create a divider based
        # on that length
        header_divider = []
        for name in header:
            header_divider.append('-' * len(name))

        # Create a list of dictionary from the keys and the header and
        # insert it at the beginning of the list. Do the same for the
        # divider and insert below the header.
        header_divider = dict(zip(keys, header_divider))
        data.insert(0, header_divider)
        header = dict(zip(keys, header))
        data.insert(0, header)

    column_widths = []
    for key in keys:
        column_widths.append(max(len(str(column[key])) for column in data))

    formatted_data = ''

    # print(data)
    for element in data:
        formatstr = ''
        data_to_format = []
        # Create a tuple that will be used for the formatting in
        # width, value format
        for pair in zip(keys, column_widths):
            formatstr += '{:' + str(pair[1]) + '} '
            data_to_format.append(element[pair[0]])
        formatstr += '\n'
        formatted_data += formatstr.format(*data_to_format)
    return formatted_data


# Test
if __name__ == '__main__':
    header = ['Name', 'Age', 'Sex']
    keys = ['name', 'age', 'sex']
    sort_by_key = 'age'
    sort_order_reverse = True
    data = [{'name': 'John Doe', 'age': 37, 'sex': 'M'},
            {'name': 'Lisa Simpson', 'age': 17, 'sex': 'F'},
            {'name': 'Bill Clinton', 'age': 57, 'sex': 'M'}]

    print(format_as_table(data,
                          keys,
                          header,
                          sort_by_key,
                          sort_order_reverse))
