from collections import defaultdict
import os

from pdf_parser import pdfPositionHandling


def extract_text(file_name, file_subfolder_path, kw_list_in):
    os.chdir(file_subfolder_path)
    file_name_no_extension = file_name[: -4].replace(' ', '_')
    convert_pdf_list = []
    for file in os.listdir(file_subfolder_path):
        if file.endswith('.pdf'):
            # list of split pdf pages
            convert_pdf_list.append(file)

    mapped_file_text_dict = {}
    file_text_dict = {}
    section1_fields_dict = {}

    for i, curr_pdf in enumerate(convert_pdf_list):
        # str containing split pdf names
        convert_pdf = convert_pdf_list[i]
        # page number in str form
        pg_no = convert_pdf[: -4].split('_')[-1][4:]

        # instantiate class
        handler = pdfPositionHandling(convert_pdf, file_subfolder_path)
        handler.parsepdf()

        # obtain text coordinates
        file_text_dict_page = handler.text_coord_dict
        # each dict per page
        # key is tuple with 0 and text coordinates, value is text
        pg_text_dict = file_text_dict_page[convert_pdf]
        # print(pg_text_dict)

        temp_file_text = {}
        kw_value = defaultdict(list)
        # print(kw_value)

        for kw in kw_list_in:
            # list of text per pdf page
            pg_text_list = list(pg_text_dict.values())

            pg_text_index = 0

            # pg number needs to be fixed as currently showing 0
            for pgno_coord, text in pg_text_dict.items():
                text = text.strip().strip('.')

                # text index
                pg_text_index += 1

                if len(text) > 0:
                    # fixed page number key to reflect actual pages of split pdf
                    # convert to list to access first element
                    pgno_coord = list(pgno_coord)
                    # assign to actual page number
                    pgno_coord[0] = pg_no
                    # convert back into tuple
                    pgno_coord = tuple(pgno_coord)

                    temp_file_text[pgno_coord] = text
                    file_text_dict.update(temp_file_text)

                    kw_found_flag = 0

                    if kw.lower() in text.lower():
                        temp = pg_text_index+1

                        # dict containing keyword as key and page no as value
                        # kw_value[kw].append(pg_no)

                        val = pg_text_list[pg_text_index].strip().strip('.').strip()
                        # print(val)
                        if len(val) == 0:
                            kw_value[kw].append(pg_text_list[pg_text_index+1].strip().strip('.').strip())
                        else:
                            kw_value[kw].append(pg_text_list[pg_text_index].strip().strip('.').strip())

        # convert values from list to str
        for key, value in kw_value.items():
            kw_value.update({key: str(value[0])})
        # print(dict(kw_value))

        section1_fields_dict[convert_pdf] = kw_value
    mapped_file_text_dict[file_name] = file_text_dict
    return mapped_file_text_dict, section1_fields_dict