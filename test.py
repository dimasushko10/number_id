from Func import XlsxFileProcessing, APISearch

file = APISearch.find_inf_db("79006461237")
result = APISearch.process_json_file("output.json")

print(result)