import os
from PyPDF2 import PdfFileReader, PdfFileWriter



def split_pdf(file_path, file_name, file_subfolder_path, page_list):
    """
    Split single PDF into multiple ones

    Parameters
    ----------
    file_path :
        Location of path containing input PDF files
    file_name :
        Name of input PDF file
    file_subfolder_path :
        Location of path containing output subfolders
    pg_no :
        Page number of input PDF
    """
    os.chdir(file_path)
    with open(file_name, 'rb') as input_file:
        file_object = PdfFileReader(input_file)
        for pg_no in page_list:
            os.chdir(file_subfolder_path)
            pdf_writer = PdfFileWriter()
            curr_pg = file_object.getPage(pg_no)
            pdf_writer.addPage(curr_pg)
            file_name = file_name.replace(' ', '_')
            output_file = file_name[: -4] + f'_page{pg_no}.pdf'
            output_file_path = os.path.join(file_subfolder_path, output_file)
            if not os.path.exists(output_file_path):
                with open(output_file, "wb") as out:
                    pdf_writer.write(out)

