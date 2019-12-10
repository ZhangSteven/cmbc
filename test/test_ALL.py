# coding=utf-8
# 

import unittest2
from os.path import join
from utils.iter import firstOf
from functools import partial
from cmbc.main import getCurrentDirectory, getPositions, holdingPosition\
					, cashPosition, dateFromFilename



class TestALL(unittest2.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestALL, self).__init__(*args, **kwargs)



	def testDateFromFilename(self):
		inputFile = join( getCurrentDirectory()\
						, 'samples', '20191125_560010910_cash_pos.xls')
		self.assertEqual('2019-11-25', dateFromFilename(inputFile))
		inputFile = join( getCurrentDirectory()\
						, 'samples', 'Security Holding 20191209.xls')
		self.assertEqual('2019-12-09', dateFromFilename(inputFile))



	def testGetPositions(self):
		inputFile = join( getCurrentDirectory()\
						, 'samples', 'Security Holding 20191209.xls')
		date, positions = getPositions(inputFile)
		positions = list(map(partial(holdingPosition, date), positions))
		self.assertEqual(28, len(positions))
		self.verifyPosition(positions[4])
		self.verifyPosition2(positions[27])



	def testGetCashPositions(self):
		inputFile = join( getCurrentDirectory()\
						, 'samples', '20191125_560010910_cash_pos.xls')
		date, positions = getPositions(inputFile)
		positions = list(map(partial(cashPosition, date), positions))
		self.assertEqual(2, len(positions))
		self.verifyCashPosition(positions[1])



	def verifyPosition(self, position):
		self.assertEqual('560010910', position['portfolio'])
		self.assertEqual('', position['custodian'])
		self.assertEqual('2019-12-09', position['date'])
		self.assertEqual('', position['geneva_investment_id'])
		self.assertEqual('XS1897158892', position['ISIN'])
		self.assertEqual('', position['bloomberg_figi'])
		self.assertEqual('CHINA CITIC BANK INTL', position['name'])
		self.assertEqual('USD', position['currency'])
		self.assertEqual(400000, position['quantity'])



	def verifyPosition2(self, position):
		self.assertEqual('560010910', position['portfolio'])
		self.assertEqual('', position['custodian'])
		self.assertEqual('2019-12-09', position['date'])
		self.assertEqual('6886 HK', position['geneva_investment_id'])
		self.assertEqual('', position['ISIN'])
		self.assertEqual('', position['bloomberg_figi'])
		self.assertEqual('HUATAI SECURITIES CO LTD-H', position['name'])
		self.assertEqual('HKD', position['currency'])
		self.assertEqual(97000, position['quantity'])



	def verifyCashPosition(self, position):
		self.assertEqual('560010910', position['portfolio'])
		self.assertEqual('', position['custodian'])
		self.assertEqual('2019-11-25', position['date'])
		self.assertEqual('USD', position['currency'])
		self.assertAlmostEqual(-395254.53, position['balance'])