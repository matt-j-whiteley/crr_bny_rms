import re


def search_pg_with_kw(file_content_dict, kw):
    """
    Search through the text file data and find pages of interest

    Parameters
    ----------
    file_content_dict :
        Dictionary containing file name and page number

    """
    page_dict = {}
    for file_nm, pgno_text_dict in file_content_dict.items():
        page_list = []
        for pgno, text in pgno_text_dict.items():
            if pgno not in page_list:
                # regular expression searches keywords in text
                if re.search(kw, text):
                    # list of pages containing keywords 1 and 2
                    page_list.append(pgno)
        # dictionary containing file name and corresponding list of pages containing keywords 1 and 2
        page_dict[file_nm] = page_list
    return page_dict, page_list

