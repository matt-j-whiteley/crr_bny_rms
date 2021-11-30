import os
from datetime import datetime


def read_txt(file_name, file_subfolder_path):
    """
       Read converted text file and save all text data into memory

       Parameters
       ----------
       file_name :
           Name of input PDF file
       file_subfolder_path :
           Output file path
       """
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    os.chdir(file_subfolder_path)
    txt_file_nm = file_name[:-4] + '_convert.txt'
    txt_file_nm = txt_file_nm.replace(' ', '_')
    file_data_all = {}
    pdf_page_count_dict = {}
    try:
        # open and read in txt file
        with open(txt_file_nm, "r", encoding='cp1252', errors='ignore') as file:
            read_in = file.read()
            if '\x0c' in read_in:
                read_in_split = read_in.split('\x0c')
                # print(read_in_split)
                last_pg = read_in_split[-1].strip().strip('.')
                if len(last_pg) == 0:
                    txt_pg_count = len(read_in_split) - 1
                    read_in_split = read_in_split[: -1]
                else:
                    txt_pg_count = len(read_in_split)
            else:
                read_in_split = [' ']
                txt_pg_count = 0
                print(f"{date_time} - ERROR - file has no page break: {txt_file_nm}")
    except Exception as e:
        print(f"{date_time} - ERROR - when reading txt file: {txt_file_nm}")

    # list of total pages in input pdf
    page_no_list = [i for i in range(0, txt_pg_count)]
    # dictionary containing pdf name as key and a dict of page no as key and pdf text as value
    file_data_all[file_name] = dict(zip(page_no_list, read_in_split))
    # dictionary containing pdf name as key and total number of pages as value
    pdf_page_count_dict[file_name] = txt_pg_count
    return file_data_all, pdf_page_count_dict



