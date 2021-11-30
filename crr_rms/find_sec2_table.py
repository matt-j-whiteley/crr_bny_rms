
def find_sect2_location(mapped_file_text_dict, page_list, top_left_kw, bott_left_kw, head_kw1, head_kw2):
    file_sect2_table_location = {}
    file_sect2_table_addon_loc = {}
    for file, text_dict in mapped_file_text_dict.items():
        pg_sect2_table_location = {}
        pg_sect2_table_addon_loc = {}
        for pg_no_temp in page_list:
            curr_pg_table = []
            curr_pg_addon_table = []
            for pg_no_coord, text in text_dict.items():
                if int(pg_no_coord[0]) == pg_no_temp:
                    if top_left_kw in text:
                        top_left_kw_x = pg_no_coord[1]
                        top_left_kw_y = pg_no_coord[2]
                    elif bott_left_kw in text:
                        bott_right_kw_x = pg_no_coord[3] + 391
                        bott_right_kw_y = pg_no_coord[4] + 30
                    elif head_kw1 in text or head_kw2 in text:
                                head_kw_x = pg_no_coord[1]
                                head_kw_y = pg_no_coord[2]
                                head_kw_x1 = pg_no_coord[3]
                                head_kw_y1 = pg_no_coord[4]

            curr_pg_table.append(top_left_kw_x)
            curr_pg_table.append(top_left_kw_y)
            curr_pg_table.append(bott_right_kw_x)
            curr_pg_table.append(bott_right_kw_y)

            curr_pg_addon_table.append(head_kw_x)
            curr_pg_addon_table.append(head_kw_y)
            curr_pg_addon_table.append(head_kw_x1)
            curr_pg_addon_table.append(head_kw_y1)

            pg_sect2_table_location[pg_no_temp] = curr_pg_table
            pg_sect2_table_addon_loc[pg_no_temp] = curr_pg_addon_table

        file_sect2_table_location[file] = pg_sect2_table_location
        file_sect2_table_addon_loc[file] = pg_sect2_table_addon_loc
    return file_sect2_table_location, file_sect2_table_addon_loc
