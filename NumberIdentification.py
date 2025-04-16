from Func import XlsxFileProcessing, APISearch

if __name__ == '__main__':
    find_list = XlsxFileProcessing.create_input_data(XlsxFileProcessing.open_xls())

    for n in range(len(find_list)): #Дешевий пошук
        json_data = APISearch.find_inf_db(find_list[n])
        data_to_write = APISearch.process_json_file("output.json")
        result = XlsxFileProcessing.write_result_to_file(data_to_write, n)

    """
    for n in range(len(find_list)): #Дорогий пошук
        response_data = APISearch.search_phone(find_list[n])
        data_to_write = APISearch.data_processing(response_data)
        result = XlsxFileProcessing.write_result_to_file(data_to_write, n)
    """