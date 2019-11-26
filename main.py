# coding=utf-8
#
# Read Nomura holding anc cash reports, convert them to Geneva holding and cash
# format.
# 
# Program structure very similar to main.py from package nomura. Output csv
# has exactly the same structure.
# 

from itertools import chain
from functools import partial
from utils.utility import dictToValues, writeCsv
from toolz.functoolz import compose
from nomura.main import fileToLines, getHeadersnLines, getCashHeaders \
						, getHoldingHeaders, getOutputFileName
from os.path import join, dirname, abspath
from datetime import datetime
import logging
logger = logging.getLogger(__name__)



def addDictValue(key, value, d):
	newD = d.copy()
	newD[key] = value
	return newD



"""
	[Object] number string => [Float] number
	
	If the number string is a String object, then it looks like: '-12,345.67',
	we convert it to a floating number. Otherwise return it unchanged.
"""
stringToFloat = lambda s: \
	float(s.replace(',', '')) if isinstance(s, str) else s




"""
	[Dictionary] p (raw holding position) => 
		[Dictionary] Geneva holding position

	Assumptions: 

	(1) There are only two types of holdings, bond or equity.
	(2) All equity holdings are HK equity.
"""
holdingPosition = lambda date, p: \
	{ 'portfolio': p['Account No.']
	, 'custodian': ''
	, 'date': date
	, 'geneva_investment_id': '' if p['Market'].startswith('BOND') \
								else p['Instrument'] + ' HK'
	, 'ISIN': p['Instrument'] if p['Market'].startswith('BOND') else ''
	, 'bloomberg_figi': ''
	, 'name': p['Stock Name']
	, 'currency': p['Currency'].split('-')[0]
	, 'quantity': stringToFloat(p['Available Qty'])
	}



"""
	[Dictionary] p (raw cash position) => 
		[Dictionary] Geneva cash position
"""
cashPosition = lambda date, p: \
	{ 'portfolio': p['portfolio_code']
	, 'custodian': ''
	, 'date': date
	, 'currency': p['account_ccy_code']
	, 'balance': stringToFloat(p['ledger_bal_in_acct_ccy'])
	}



filenameWithoutPath = lambda filename: \
	filename.split('\\')[-1]



isCashFile = lambda filename: \
	filenameWithoutPath(filename).split('.')[0].endswith('cash_pos')



"""
	[String] date string (yyyymmdd) => [String] date string (yyyy-mm-dd)
"""
convertDateString = lambda s : \
	datetime.strptime(s, '%Y%m%d').strftime('%Y-%m-%d')



"""
	[String] filename => [String] date (yyyy-mm-dd)

	The file looks like: 20191125_560010910_cash_pos.xls, or
	StockHoldInfo 20191122.xlsx

	The date in the file name follows "yyyymmdd" convention.
"""
dateFromFilename = compose(
	  convertDateString
	, lambda s : s.split('_')[0] if s[0] == '2' else s.split()[1] 
	, lambda fn: fn.split('.')[0]
	, filenameWithoutPath
)



"""
	[String] file => [String] date (yyyy-mm-dd), [Iterable] positions
"""
getPositions = lambda file: \
	(dateFromFilename(file), getRawPositions(file))



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



"""
	[String] inputFile => [String] file name postfix, [Iterable] rows
"""
toOutputData = lambda inputFile: \
	(lambda date, positions: \
		( '_cmbc_' + date + '_cash'\
		, chain( [getCashHeaders()]\
			   , map( partial(dictToValues, getCashHeaders())\
			   		, map( partial(cashPosition, date)\
			   			 , positions)))\
		) if isCashFile(inputFile) else \

		( '_cmbc_' + date + '_position'\
		, chain( [getHoldingHeaders()]\
			   , map( partial(dictToValues, getHoldingHeaders())\
			   		, map( partial(holdingPosition, date)\
			   			 , positions)))\
		)
	)(*getPositions(inputFile))
	


outputCsv = lambda inputFile, outputDir: \
	(lambda postfix, outputData: \
		writeCsv( getOutputFileName(inputFile, postfix, outputDir)\
				, outputData, delimiter='|')
	)(*toOutputData(inputFile))




if __name__ == '__main__':
	import logging.config
	logging.config.fileConfig('logging.config', disable_existing_loggers=False)

	inputFile = join(getCurrentDirectory(), 'samples', 'StockHoldInfo 20191122.xlsx')
	for p in getRawPositions(inputFile):
		print(p)
		break