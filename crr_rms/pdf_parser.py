from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
import re



class pdfPositionHandling:
    """
    This class stores the pdf page's objects into dictionaries
    """
    def __init__(self, file_name, file_path):
        self.file_nm = file_name
        self.file_dir = file_path
        self.text_coord_dict_per_file = {}
        self.text_coord_dict = {}

    def parse_obj(self, lt_objs, pg_height, pg_no):
        # for objects in layout objects
        for obj in lt_objs:
            # check if object is LTTextLine
            if isinstance(obj, pdfminer.layout.LTTextLine):
                # return text content and replace new line chars
                text = obj.get_text().replace('\n', '. ')
                # replace irregular spacing with single space
                text = re.sub(r'(?<!\s)(\s)+(?!\s)', " ", text)

                # x0: the distance from the left of the page to the left edge of the box.
                # y0: the distance from the top of the page to the upper edge of the box.
                # x1: the distance from the left of the page to the right edge of the box.
                # y1: the distance from the top of the page to the lower edge of the box.
                x0, y0 = int(obj.bbox[0]), int(pg_height - obj.bbox[3])
                x1, y1 = int(obj.bbox[2]), int(pg_height - obj.bbox[1])
                coord = (x0, y0, x1, y1)
                pg_no_coord = (pg_no, x0, y0, x1, y1)

                # stores coordinates of pdf text along with page number in dict
                self.text_coord_dict_per_file[pg_no_coord] = text
                # adds file name as key
                self.text_coord_dict[self.file_nm] = self.text_coord_dict_per_file

            if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                self.parse_obj(obj._objs, pg_height, pg_no)
            elif isinstance(obj, pdfminer.layout.LTFigure):
                self.parse_obj(obj._objs, pg_height, pg_no)
            elif isinstance(obj, pdfminer.layout.LTTextBox):
                self.parse_obj(obj._objs, pg_height, pg_no)

    def parsepdf(self):
        # Open a PDF file
        fp = open(self.file_nm, 'rb')
        # Create a PDF parser object associated with the file object
        parser = PDFParser(fp)
        # Create a PDF document object that stores the document structure
        document = PDFDocument(parser)
        # Check if the document allows text extraction...if not, abort
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed
        # Create a PDF resource manager object that stores shared resources
        rsrcmgr = PDFResourceManager()
        # Create a PDF device object
        device = PDFDevice(rsrcmgr)
        # Set parameters for analysis
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # Create a PDF interpreter object
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        pg_no = 0
        # Process each page contained in the document
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            pg_height = page.mediabox[3]
            # receive the LTPage object for the page
            layout = device.get_result()
            self.parse_obj(layout._objs, pg_height, pg_no)
            pg_no += 1

