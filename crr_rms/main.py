import os

from save_pdf_txt import read_pdf_save_txt
from read_txt import read_txt
from kw_search import search_pg_with_kw
from split_pdf import split_pdf
from extract_text_1 import extract_text
from find_sec2_table import find_sect2_location
from find_sec3_table import find_sect3_location
from find_sect4_table import find_sect4_location
from extract_text_2 import extract_sect2
from extract_text_3 import extract_sect3
from extract_text_4 import extract_sect4
from df_to_excel import create_df1, clean_df2, clean_df3, clean_df4, dfs_to_excel

def main_func(input_path, file_nm):
    """
    Boilerplate function
    """
    os.chdir(input_path)
    output_flag = 'txt'
    current_output_path = os.path.join(input_path, file_nm[: -4])

    # if output dir doesn't exist, create it
    if not os.path.exists(current_output_path):
        os.mkdir(current_output_path)

    # read pdf, save all text into memory, search pdfs for keywords, identify pages of interest and split pdf pages
    read_pdf_save_txt(input_path, file_nm, output_flag, current_output_path)
    all_file_data_dict, pdf_pg_count_dict = read_txt(file_nm, current_output_path)
    keyword = 'FUND NAME'
    page_dict, pg_list = search_pg_with_kw(all_file_data_dict, keyword)
    split_pdf(input_path, file_nm, current_output_path, pg_list)

    # extract fields of interest
    kw_list = ['REPORT FOR BUSINESS DATE', 'FUND NAME', 'TRADING ADVISOR', 'BROKER/FCM', 'ACCOUNT:', 'BUSINESS DATE',
               'CURRENCY:', 'BUSINESS DAY EXCHANGE']
    map_file_text_dict, sect1_fields_dict = extract_text(file_nm, current_output_path, kw_list)
    top_left_keyword = 'BEGINNING BALANCE'
    bott_left_keyword = 'ADJUSTED NET LIQUIDITY'
    header_keyword1 = 'FUTURES RECONCILIATION'
    header_keyword2 = 'CFD RECONCILIATION'
    file_sect2_tab_loc, file_sect2_addon_tab_loc = find_sect2_location(map_file_text_dict, pg_list, top_left_keyword, bott_left_keyword,
                                             header_keyword1, header_keyword2)
    sect2_fields_dict, df_comb, report_type_df = extract_sect2(file_sect2_tab_loc, file_sect2_addon_tab_loc,
                                                                         input_path)
    top_left_keyword1 = 'EFFECTIVE DATE'
    bott_keyword = 'Sub Total'
    file_sect3_tab1_loc = find_sect3_location(map_file_text_dict, pg_list, top_left_keyword1, bott_keyword)
    sect3_fields_dict, df3 = extract_sect3(file_sect3_tab1_loc, input_path)
    top_left_keyword1 = 'Sub Total'
    bott_keyword1 = 'Cash Total'
    file_sect4_tab_loc = find_sect4_location(map_file_text_dict, pg_list, top_left_keyword1, bott_keyword1)
    sect4_fields_dict, df4, sect4_dict_fields_per_file = extract_sect4(file_sect4_tab_loc, input_path)

    # create and clean dataframes
    df1 = create_df1(sect1_fields_dict, report_type_df)
    print('df1 is ', df1)
    df2 = clean_df2(df1, df_comb)
    print('df2 is ', df2)
    df3 = clean_df3(df1, df3)
    df4 = clean_df4(df1, df4, sect4_dict_fields_per_file)

    # convert all dataframes into excel sheets and save data in output dir
    os.chdir(input_path)
    dfs_to_excel(file_nm, df1, df2, df3, df4)

