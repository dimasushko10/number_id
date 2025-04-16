import pylightxl as xl
import itertools


# open file with numbers, return readed xlsx file
def open_xls ():

    raw_db = xl.readxl(fn='/Users/bohdan.makedonskyi/PycharmProjects/Number_identification_usersbox/test_data/test_data_numb_1.xlsx')
    return raw_db


# return list of numbers in opened xlsx file
def create_input_data (db):

    #for cell in
     temp = db.ws(ws='Sheet1').range(address='A1:A40')
     num_list = list(itertools.chain(*temp))

     return num_list


def write_result_to_file(data_to_write, index_n):
    # Шлях до файлу
    file_path = "/Users/bohdan.makedonskyi/PycharmProjects/Number_identification_usersbox/test_data/test_data_numb_1.xlsx"

    # Завантажуємо наявні дані
    db = xl.readxl(fn=file_path)
    sheet = db.ws(ws="Sheet1")  # Отримуємо доступ до першого аркуша

    cells = "BCDE"  # Визначаємо доступні колонки

    if data_to_write:
        for col, value in zip(cells, data_to_write):  # Використовуємо zip() для обмеження довжини
            cell_address = f"{col}{index_n + 1}"  # Формуємо адресу комірки
            #print(f"Updating {cell_address} with value: {value}")  # Логування

            sheet.update_address(address=cell_address, val=value)  # Оновлення комірки

    # Зберігаємо зміни, не перезаписуючи інші дані
    xl.writexl(db=db, fn=file_path)
    #print(f"Дані успішно записані в {file_path}")


"""def write_result_to_file (data_to_write, index_n):
    db = xl.readxl(fn='/Users/bohdan.makedonskyi/PycharmProjects/Number_identification_usersbox/test_data/test_data_numb_1.xlsx')

    cells = "BCDE"
    if data_to_write is not None:
        for i in range(len(data_to_write)):
            index = cells[i] + str(index_n+1)
            print(index)
            db.ws(ws='Sheet1').update_address(address=str(index), val=data_to_write[i])
            db.ws(ws='Sheet1').address(address=str(index))
        xl.writexl(db=db, fn='test_data_numb.xlsx')
    return db"""
