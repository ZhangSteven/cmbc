# coding=utf-8
#
# Read Nomura holding anc cash reports, convert them to Geneva holding and cash
# format.
# 

from xlrd import open_workbook
from itertools import takewhile, chain
from functools import partial
from utils.excel import worksheetToLines
from utils.utility import fromExcelOrdinal, dictToValues, writeCsv
from utils.iter import pop
from os.path import join, dirname, abspath
import logging
logger = logging.getLogger(__name__)






"""
	Get the absolute path to the directory where this module is in.

	This piece of code comes from:

	http://stackoverflow.com/questions/3430372/how-to-get-full-path-of-current-files-directory-in-python
"""
getCurrentDirectory = lambda: \
	dirname(abspath(__file__))
	



if __name__ == '__main__':
	import logging.config
	logging.config.fileConfig('logging.config', disable_existing_loggers=False)

	print(getCurrentDirectory())