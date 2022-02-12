# import logging
import re
# from datetime import datetime
# from os import makedirs, path, remove, walk
# from shutil import rmtree

import demoji
# from xlrd import open_workbook
# from xlwt import Workbook

from settings import COMPS

def emoji_filter(text: str) -> str:
    """Delete all emoji in text."""
    emoji_in_message = demoji.findall(text)
    for emoji in emoji_in_message:
        emoji_desc = emoji_in_message[emoji].split()
        if emoji_desc[0] == 'flag:':
            text = text.replace(emoji, f' {emoji_desc[1:]} ')
        else:
            text = text.replace(emoji, '')
    return text



def get_price(row: str) -> int:
    row = row.strip()
    findall_digit = re.findall(r'\d+[.,_]?[\d+]{3}', row)
    if findall_digit:
        try:
            return int(findall_digit[-1])
        except ValueError:
            return int(re.sub(r'\D', r'', findall_digit[-1]))
    return None


# class Firm:
#     def __init__(self, model=None, memo=None, color=None, etc):
#         pass


def extract_from_text(text: str) -> list:
    result = []
    # some_firm = Firm()
    prev_lines = ''
    for row in text.split('\n'):
        row = row.replace('——', '').replace('  ', ' ')
        price = get_price(row)
        if price:
            pass
            # find_model_data() # iter on COMPS icontains in prev_lines
            # work with row of price
        else:
            prev_lines += row

#     def get_text_before_dash(text: str) -> str:
#         if '-' in text:
#             dash_index = text.rindex('-')
#             result = text[0:dash_index]
#             if result:
#                 return result.strip()
#         return None


#     for line in text.split('\n'):
#         last_digit: int = get_last_digit(line)
#         text_before_dash: str = None
#         if last_digit:
#             text_before_dash = get_text_before_dash(line)

#         if prev_line:
#             if text_before_dash and last_digit and not prev_line.cost:
#                 if prev_line.title:
#                     text_before_dash = join_by_one_space(prev_line.title, text_before_dash)
#                 else:
#                     text_before_dash = join_by_one_space(prev_line.raw_text, text_before_dash)
#             elif not text_before_dash and last_digit and not prev_line.cost:
#                 if prev_line.title:
#                     text_before_dash = prev_line.title
#                 elif prev_line.raw_text:
#                     text_before_dash = prev_line.raw_text
#             elif not prev_line.title and not prev_line.cost:
#                 pass
#         else:
#             pass

#         if text_before_dash and last_digit:
#             result.append([text_before_dash, last_digit])

#         prev_line = Line(line, text_before_dash, last_digit)
#     return result



# def get_today_extract_container_path():
#     return 'extracted/%s' % datetime.today().date()


# def get_today_extract_path(filename: str):
#     return '%s/%s' % (get_today_extract_container_path(), filename)



# def extract_from_file(filepath: str) -> list:
#     result = []
#     workbook = open_workbook(filepath)
#     sheet = workbook.sheet_by_index(0)
#     for row_index in range(sheet.nrows):
#         title_cell = sheet.cell(row_index, 0)
#         price_cell = sheet.cell(row_index, 1)
#         result.append([title_cell.value, price_cell.value])
#     return result


# def extract_to_xls_file(extract: list, filename: str):
#     workbook = Workbook()
#     sheet = workbook.add_sheet("Таблица 1")
#     for row_index in range(len(extract)):
#         row_data = extract[row_index]
#         sheet.write(row_index, 0, row_data[0])
#         sheet.write(row_index, 1, row_data[1])
#     try:
#         makedirs(filename)
#     except IOError as error:
#         logging.exception(error)
#     workbook.save('%s.xls' % filename)


# def extract_to_today_xls_file(extract: list, filename: str):
#     return extract_to_xls_file(extract, get_today_extract_path(filename))


# def __fix__get_today_extract_fullpaths_by_filename(filename: str) -> list:
#     result = []
#     fullname = '%s.xls' % filename
#     for (root, _, filenames) in walk(get_today_extract_container_path()):
#         for filename0 in filenames:
#             if filename0 == fullname:
#                 result.append(path.join(root, filename0))
#     logging.info("__fix__get_today_extract_fullpaths_by_filename=[%s]" % ','.join(result))
#     return result


# def __dirty__delete_extract_xls_file(a: str):
#     for file in __fix__get_today_extract_fullpaths_by_filename(a):
#         remove(file)


# def delete_extract_container_folder(a: str):
#     try:
#         dir_to_rm = get_today_extract_path(a)
#         logging.info('delete_extract_container_folder(%s)' % dir_to_rm)
#         rmtree(dir_to_rm, ignore_errors=True)
#     except:
#         pass


# def create_today_actual_xls(filepath: str):
#     xml_files = []
#     today_extract_path = get_today_extract_path(filepath)

#     # need to modify for support tree files
#     for (root, _, filenames) in walk(today_extract_path):
#         xml_files.extend(filenames)
#         break

#     extracts = []
#     for xml_file in xml_files:
#         extracts.extend(extract_from_file('%s/%s' % (today_extract_path, xml_file)))

#     save_today_actual_xls(extracts, filepath)


# def save_today_actual_xls(today_extract: list, filepath: str):
#     extract_to_xls_file(today_extract, 'public/%s/actual' % filepath)
