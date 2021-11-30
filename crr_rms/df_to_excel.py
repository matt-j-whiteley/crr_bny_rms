import pandas as pd
import numpy as np
import re


def create_df1(fields1, df_add):
    df = pd.DataFrame(fields1)
    # transpose df so rows and columns interchange
    df = df.T

    # append page numbers from pdf to a list
    pg_lst = []
    for index, row in df.iterrows():
        pg_lst.append(index[:-4].split('_')[-1][4:])

    # convert string data to int
    pg_lst = [int(i) for i in pg_lst]
    # add 1 to pg number as index begins from 0
    pg_lst = [x+1 for x in pg_lst]

    # add pg_lst to current df
    df['Page_Number'] = pg_lst
    # drop current index and set 'Page_Number' as new index
    df.reset_index(drop=True, inplace=True)
    df.set_index('Page_Number', inplace=True)

    # ensure pages appear in ascending order
    df.sort_index(inplace=True)

    new_header = ['REPORT FOR BUSINESS DATE', 'FUND NAME', 'TRADING ADVISOR', 'BROKER/FCM',
                  'ACCOUNT', 'BUSINESS DATE', 'CURRENCY', 'BUSINESS DAY EXCHANGE']
    # assign header
    df.columns = new_header
    # replace : with blanks
    df = df.replace(':', '', regex=True)

    df_add.columns = ['REPORT TYPE']

    # add pg_lst to current df
    df_add['Page_Number'] = pg_lst
    # drop current index and set 'Page_Number' as new index
    df_add.reset_index(drop=True, inplace=True)
    df_add.set_index('Page_Number', inplace=True)

    # merge df and df_add on page_number column
    df = df.merge(df_add, how='left', on='Page_Number')
    return df


def clean_df2(df_1, df_2):

    # sets new page number index
    df_2.set_index('Page_Number', inplace=True)

    new_header = ['col1', 'col2', 'col3', 'col4']
    # assign header
    df_2.columns = new_header

    # take subset of table 1 and only pick out the following columns
    df_1subs = df_1[['ACCOUNT', 'CURRENCY', 'BROKER/FCM', 'REPORT TYPE']]

    # merge df1 and df2 on page_number column
    df_2 = df_2.merge(df_1subs, how='left', on='Page_Number')

    # reorder columns structure i.e. add account, currency and broker columns as first 3 columns
    df_2 = df_2[['ACCOUNT', 'CURRENCY', 'BROKER/FCM', 'REPORT TYPE', 'col1', 'col2', 'col3', 'col4']]

    # replace col1 - col4 with blank strings as no header needed for these columns
    df_2.rename(columns={'col1': ' ', 'col2': ' ', 'col3': ' ', 'col4': ' '}, inplace=True)

    # replace NaN with blanks
    df_2 = df_2.replace(np.nan, '', regex=True)
    return df_2


def clean_df3(df_1, df_3):
    new_header = ['EFFECTIVE DATE', 'Page_Number', 'RECON TYPE', 'BNY/BKR', 'AMOUNT', 'DESCRIPTION']
    # df = df[1:]
    # assign header
    df_3.columns = new_header
    # replace NaN with blanks
    df_3 = df_3.replace(np.nan, '', regex=True)

    # sets new page number index
    df_3.set_index('Page_Number', inplace=True)

    # take subset of table 1 and only pick out the following columns
    df_1subs = df_1[['ACCOUNT', 'CURRENCY', 'BROKER/FCM', 'REPORT TYPE']]

    # merge df1 and df3 on page_number column
    df_3 = df_3.merge(df_1subs, how='left', on='Page_Number')

    # reorder columns structure i.e. add account, currency and broker columns as first 3 columns
    df_3 = df_3[['ACCOUNT', 'CURRENCY', 'BROKER/FCM', 'REPORT TYPE', 'EFFECTIVE DATE', 'RECON TYPE', 'BNY/BKR',
                 'AMOUNT', 'DESCRIPTION']]

    re_pattern = r"[a-zA-Z]+"
    for ix, rw in df_3.iterrows():
        if re.search(re_pattern, rw['AMOUNT']):
            df_3.loc[ix][8] = df_3.loc[ix][7]
            df_3.loc[ix][7] = ''
    return df_3


def clean_df4(df_1, df_4, fields_dict):
    # use first row as df header
    new_header = ['SUB TOTAL/GRAND CASH TOTAL', 'AMOUNT']
    # assign header
    df_4.columns = new_header
    # replace NaN with blanks
    df_4 = df_4.replace(np.nan, '', regex=True)

    re_pattern = r":\s+.+"
    for index, row in df_4.iterrows():
        if re.search(re_pattern, row['SUB TOTAL/GRAND CASH TOTAL']):
            # identifies index where text and amounts are in the same column and reassigns to 2 separate columns
            df_4.loc[index][0], df_4.loc[index][1] = df_4.loc[index][0].split(':')[0], df_4.loc[index][0].split(':')[1]

    temp_pg_no_lst = list(fields_dict.keys())
    pg_no_lst = []
    for i in temp_pg_no_lst:
        pg_no_lst.extend([i + 1, i + 1])
    df_4.insert(2, 'Page_Number', pg_no_lst)
    # sets new page number index
    df_4.set_index('Page_Number', inplace=True)

    # take subset of table 1 and only pick out the following columns
    df_1subs = df_1[['ACCOUNT', 'CURRENCY', 'BROKER/FCM', 'REPORT TYPE']]

    # merge df1 and df3 on page_number column
    df_4 = df_4.merge(df_1subs, how='left', on='Page_Number')

    # reorder columns structure i.e. add account, currency and broker columns as first 3 columns
    df_4 = df_4[['ACCOUNT', 'CURRENCY', 'BROKER/FCM', 'REPORT TYPE', 'SUB TOTAL/GRAND CASH TOTAL', 'AMOUNT']]

    # replace : with blanks
    df_4 = df_4.replace(':', '', regex=True)
    return df_4


def dfs_to_excel(file_name, dataframe1, dataframe2, dataframe3, dataframe4):
    curr_folder_writer = pd.ExcelWriter(f'{file_name[:-4]}.xlsx', engine='xlsxwriter')

    dataframe1.to_excel(curr_folder_writer, sheet_name='Section1')
    dataframe2.to_excel(curr_folder_writer, sheet_name='Section2')
    dataframe3.to_excel(curr_folder_writer, sheet_name='Section3')
    dataframe4.to_excel(curr_folder_writer, sheet_name='Section4')
    curr_folder_writer.save()
