

def find_sect3_location(mapped_file_text_dict, page_list, top_left_kw, bott_kw):
    file_sect3_table_location = {}
    for file, text_dict in mapped_file_text_dict.items():
        pg_sect3_table_location = {}
        for pg_no_temp in page_list:
            curr_pg_table = []
            for pg_no_coord, text in text_dict.items():
                if int(pg_no_coord[0]) == pg_no_temp:
                    if top_left_kw in text:
                        top_left_kw_x = pg_no_coord[1] - 6
                        top_left_kw_y = pg_no_coord[2] + 24
                    elif bott_kw in text:
                        bott_right_kw_x = pg_no_coord[3] + 400
                        bott_right_kw_y = pg_no_coord[4] - 17
            curr_pg_table.append(top_left_kw_x)
            curr_pg_table.append(top_left_kw_y)
            curr_pg_table.append(bott_right_kw_x)
            curr_pg_table.append(bott_right_kw_y)
            pg_sect3_table_location[pg_no_temp] = curr_pg_table
        file_sect3_table_location[file] = pg_sect3_table_location
    return file_sect3_table_location