import pandas as pd
import tabula
import os


def extract_sect2(file_sect2_table_location, file_sect2_addon_table_location, input_dir):
    sect2_fileds_dict = {}
    sect2_addon_fields_dict = {}

    for file, sect2_table_location_dict in file_sect2_table_location.items():
        sect2_fileds_dict_per_file = {}
        df_combine = pd.DataFrame()
        for pg_no_temp, sect2_table_location in sect2_table_location_dict.items():
            y_curr_table_curr_pg = sect2_table_location[1] - 30
            x_curr_table_curr_pg = sect2_table_location[0]
            y1_curr_table_curr_pg = sect2_table_location[3]
            x1_curr_table_curr_pg = sect2_table_location[2]
            file_path = os.path.join(input_dir, file)
            df_list = tabula.read_pdf(file_path,
                                      guess=False, pages=int(pg_no_temp) + 1, stream=True, encoding="utf-8",
                                      area=(y_curr_table_curr_pg, x_curr_table_curr_pg,
                                            y1_curr_table_curr_pg, x1_curr_table_curr_pg),
                                      pandas_options={'header': None, "dtype": str}
                                      )

            table2_df = df_list[0]
            table2_df['Page_Number'] = pg_no_temp + 1
            # append after every iteration as opposed to right at the end
            df_combine = df_combine.append(table2_df, ignore_index=True)


    for file, sect2_addon_table_location_dict in file_sect2_addon_table_location.items():
        sect2_addon_fileds_dict_per_file = {}

        rprt_df = pd.DataFrame()
        for pg_no_temp, sect2_addon_table_location in sect2_addon_table_location_dict.items():
            y_addon_table_curr_pg = sect2_addon_table_location[1]
            x_addon_table_curr_pg = sect2_addon_table_location[0]
            y1_addon_table_curr_pg = sect2_addon_table_location[3] + 1
            x1_addon_table_curr_pg = sect2_addon_table_location[2] + 5
            file_path = os.path.join(input_dir, file)
            df_list1 = tabula.read_pdf(file_path,
                                       guess=False, pages=int(pg_no_temp) + 1, stream=True, encoding="utf-8",
                                       area=(y_addon_table_curr_pg, x_addon_table_curr_pg,
                                             y1_addon_table_curr_pg, x1_addon_table_curr_pg),
                                       pandas_options={'header': None, "dtype": str}
                                       )

            rprt_type_df = df_list1[0]

            rprt_df = rprt_df.append(rprt_type_df, ignore_index=True)
            sect2_fileds_dict_per_file[pg_no_temp] = df_list
        sect2_fileds_dict[file] = sect2_fileds_dict_per_file
    return sect2_fileds_dict, df_combine, rprt_df

