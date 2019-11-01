# coding=utf-8
#
# Read Nomura holding anc cash reports, convert them to Geneva holding and cash
# format.
# 

from itertools import takewhile, chain
from functools import partial
from utils.excel import worksheetToLines
from utils.utility import fromExcelOrdinal, dictToValues, writeCsv
from utils.iter import pop
from toolz.functoolz import compose
from toolz.dicttoolz import assoc
from nomura.main import fileToLines, getHeadersnLines
from os.path import join, dirname, abspath
import logging
logger = logging.getLogger(__name__)



def addDictValue(key, value, d):
	newD = d.copy()
	newD[key] = value
	return newD



stringToFloat = lambda s: \
	float(s.strip()) if isinstance(s, str) else s



"""
	[Dictionary] p (raw holding position) => 
		[Dictionary] Geneva holding position
"""
holdingPosition = lambda date, p: \
	{ 'portfolio': p['Portfolio']\
	, 'custodian': ''\
	, 'date': date\
	, 'geneva_investment_id': ''\
	, 'ISIN': p['instrument_code']\
	, 'bloomberg_figi': ''\
	, 'name': p['name']\
	, 'currency': p['instrument_ccy']\
	, 'quantity': stringToFloat(p['quantity'])\
	}



"""
	[Dictionary] p (raw cash position) => 
		[Dictionary] Geneva cash position
"""
cashPosition = lambda date, p: \
	{ 'portfolio': p['Portfolio']\
	, 'custodian': ''\
	, 'date': date\
	, 'currency': p['account_ccy_code']\
	, 'balance': stringToFloat(p['ledger_bal_in_acct_ccy'])\
	}



filenameWithoutPath = lambda filename: \
	filename.split('\\')[-1]



"""
	[String] filename => [String] date (yyyy-mm-dd)
"""
dateFromFilename = lambda filename: \
	(lambda s: \
		s[0:4] + '-' + s[4:6] + '-' + s[6:8]
	)(filenameWithoutPath(filename).split('_')[0])



"""
	[String] filename => [String] portfolio id
"""
portfolioFromFileName = lambda filename: \
	filenameWithoutPath(filename).split('_')[1]



"""
	[String] file => [String] date (yyyy-mm-dd), [Iterable] positions
"""
getPositions = lambda file: \
	( dateFromFilename(file)\
	, map( partial(addDictValue, 'Portfolio', portfolioFromFileName(file))\
		 , getRawPositions(file))
	)



"""
	[String] file => [Iterable] positions from the lines

	position: [Dictionary] header -> value
"""
getRawPositions = compose(
	  lambda t: map(lambda line: dict(zip(t[0], line)), t[1])\
	, getHeadersnLines\
	, fileToLines
)



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

	inputFile = join(getCurrentDirectory(), 'samples', '20190828_5600xxxxx_cash_pos.xls')
	date, positions = getPositions(inputFile)
	print(date)
	for x in positions:
		print(x)