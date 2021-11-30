import os
from datetime import datetime
import win32com.client
import win32com.client.makepy
import winerror
from win32com.client.dynamic import ERRORS_BAD_CONTEXT
import locale
locale.setlocale(locale.LC_ALL, 'C')
ERRORS_BAD_CONTEXT.append(winerror.E_NOTIMPL)


def read_pdf_save_txt(file_path, file_name, output_flag, file_subfolder_path):
    """
    Read original pdf file and return 1 if pdf read successful, if not, return -1

    Parameters
    ----------
    file_path: str
        Input file path
    file_name :
        Name of input PDF file
    output_flag :
        Hard coded '.txt' in output_flag variable in the main function
    file_subfolder_path :
        Output file path

    Returns
    -------
    """
    os.chdir(file_path)

    try:
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        # connect to adobe acrobat
        avDoc = win32com.client.DispatchEx('AcroExch.AVDoc')
        src = os.path.abspath(file_name)
        if output_flag == 'txt':
            opened_flag = avDoc.Open(src, src)
            if opened_flag:
                pdDoc = avDoc.GetPDDoc()
                jObject = pdDoc.GetJSObject()
                out_file_nm = file_name[:-4] + '_convert.txt'
                out_file_nm = out_file_nm.replace(' ', '_')
                dst = os.path.join(file_subfolder_path, out_file_nm)
                if not os.path.exists(dst):
                    # os.mkdir(dst)
                    print(f"{date_time} - Info - Converting pdf file to text file: {file_name}")

                    flag = jObject.SaveAs(dst, "com.adobe.acrobat.accesstext")
                    jObject.closeDoc(True)
                    print(f"{date_time} - Info - Conversion done")
                pdDoc.Close()
                del pdDoc
            else:
                print(f"{date_time} - ERROR - Cannot open pdf file: {file_name}")
            avDoc.Close(True)
    except Exception as e:
        print(f"{date_time} - ERROR - during converting pdf to text file: {file_name}")
        return -1
    return 1

