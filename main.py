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



stringToFloat = lambda s: \
	float(''.join(filter(lambda x: x != ',', s.strip()))) if isinstance(s, str) \
	else s



"""
	[Dictionary] p (raw holding position) => 
		[Dictionary] Geneva holding position

	Assumptions: 

	(1) There are only two types of holdings, bond or equity.
	(2) All equity holdings are HK equity.
"""
holdingPosition = lambda date, p: \
	{ 'portfolio': p['portfolio_code']\
	, 'custodian': ''\
	, 'date': date\
	, 'geneva_investment_id': '' if p['instrument_type'] == 'Bonds' \
								else p['instrument_code'] + ' HK'
	, 'ISIN': p['instrument_code'] if p['instrument_type'] == 'Bonds' else ''
	, 'bloomberg_figi': ''\
	, 'name': p['name']\
	, 'currency': p['instrument_CCY']\
	, 'quantity': stringToFloat(p['quantity'])\
	}



"""
	[Dictionary] p (raw cash position) => 
		[Dictionary] Geneva cash position
"""
cashPosition = lambda date, p: \
	{ 'portfolio': p['portfolio_code']\
	, 'custodian': ''\
	, 'date': date\
	, 'currency': p['account_ccy_code']\
	, 'balance': stringToFloat(p['ledger_bal_in_acct_ccy'])\
	}



filenameWithoutPath = lambda filename: \
	filename.split('\\')[-1]



isCashFile = lambda filename: \
	filenameWithoutPath(filename).split('.')[0].startswith('cash_pos')



"""
	[String] filename => [String] date (yyyy-mm-dd)

	The file looks like: sec_pos_08112019.xlsx

	The date in the file name follows "ddmmyyyy" convention.
"""
dateFromFilename = lambda filename: \
	(lambda s: \
		datetime.strptime(s, '%d%m%Y').strftime('%Y-%m-%d')
	)(filenameWithoutPath(filename).split('.')[0].split('_')[-1])



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

	# inputFile = join(getCurrentDirectory(), 'samples', 'sec_pos_08112019.xlsx')
	inputFile = join(getCurrentDirectory(), 'samples', 'cash_pos_08112019.xlsx')
	print(outputCsv(inputFile, ''))
