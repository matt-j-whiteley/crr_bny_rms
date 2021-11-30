import pandas as pd
import tabula
import os


def extract_sect4(file_sect4_table_location, input_dir):
    sect4_fileds_dict = {}
    for file, sect4_table_location_dict in file_sect4_table_location.items():
        sect4_fileds_dict_per_file = {}
        df_combine = pd.DataFrame()
        for pg_no_temp, sect4_table_location in sect4_table_location_dict.items():
            y_curr_table_curr_pg = sect4_table_location[1]
            x_curr_table_curr_pg = sect4_table_location[0]
            y1_curr_table_curr_pg = sect4_table_location[3]
            x1_curr_table_curr_pg = sect4_table_location[2]
            file_path = os.path.join(input_dir, file)
            df_list = tabula.read_pdf(file_path,
                                 guess=False, pages=int(pg_no_temp) + 1, stream=True, encoding="utf-8",
                                 area=(y_curr_table_curr_pg, x_curr_table_curr_pg,
                                       y1_curr_table_curr_pg, x1_curr_table_curr_pg),
                                 pandas_options={'header': None, "dtype": str}
                                 )
            df_combine = df_combine.append(df_list[0], ignore_index=True)
            sect4_fileds_dict_per_file[pg_no_temp] = df_list
        sect4_fileds_dict[file] = sect4_fileds_dict_per_file
    return sect4_fileds_dict, df_combine, sect4_fileds_dict_per_file

