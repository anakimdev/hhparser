def make_desc_company(data: list[tuple[str, str]]) -> dict[str, list[str]]:
    list_of_strings = None
    if list_of_strings is None:
        list_of_strings = []

    for item in data:
        string = f'{item[0]}: {item[1]}'
        list_of_strings.append(string)

    common_data = [list_of_strings[1], list_of_strings[9], list_of_strings[10]]
    requisites = [list_of_strings[5], list_of_strings[2], list_of_strings[8]]
    background_data = [list_of_strings[4], list_of_strings[3], list_of_strings[6], list_of_strings[11],
                       list_of_strings[12]]

    data = {'common_data': common_data, 'requisites': requisites, 'background_data': background_data}
    return data
