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
						, 'samples', 'StockHoldInfo 20191122.xlsx')
		self.assertEqual('2019-11-22', dateFromFilename(inputFile))



	def testGetPositions(self):
		inputFile = join( getCurrentDirectory()\
						, 'samples', 'sec_pos_08112019.xlsx')
		date, positions = getPositions(inputFile)
		positions = list(map(partial(holdingPosition, date), positions))
		self.assertEqual(1, len(positions))
		self.verifyPosition(positions[0])



	def testGetPositions2(self):
		inputFile = join( getCurrentDirectory()\
						, 'samples', 'sec_pos_19112019.xls')
		date, positions = getPositions(inputFile)
		positions = list(map(partial(holdingPosition, date), positions))
		self.assertEqual(13, len(positions))
		self.verifyPosition2(positions[0])



	def testGetCashPositions(self):
		inputFile = join( getCurrentDirectory()\
						, 'samples', 'cash_pos_08112019.xlsx')
		date, positions = getPositions(inputFile)
		positions = list(map(partial(cashPosition, date), positions))
		self.assertEqual(1, len(positions))
		self.verifyCashPosition(positions[0])



	def verifyPosition(self, position):
		self.assertEqual('560010910', position['portfolio'])
		self.assertEqual('', position['custodian'])
		self.assertEqual('2019-11-08', position['date'])
		self.assertEqual('', position['geneva_investment_id'])
		self.assertEqual('XS1990736644', position['ISIN'])
		self.assertEqual('', position['bloomberg_figi'])
		self.assertEqual('XS1990736644', position['name'])
		self.assertEqual('USD', position['currency'])
		self.assertEqual(150000000, position['quantity'])



	def verifyPosition2(self, position):
		self.assertEqual('560010910', position['portfolio'])
		self.assertEqual('', position['custodian'])
		self.assertEqual('2019-11-19', position['date'])
		self.assertEqual('1818 HK', position['geneva_investment_id'])
		self.assertEqual('', position['ISIN'])
		self.assertEqual('', position['bloomberg_figi'])
		self.assertEqual('ZHAOJIN MINING INDUSTRY - H', position['name'])
		self.assertEqual('HKD', position['currency'])
		self.assertEqual(144500, position['quantity'])



	def verifyCashPosition(self, position):
		self.assertEqual('560010910', position['portfolio'])
		self.assertEqual('', position['custodian'])
		self.assertEqual('2019-11-08', position['date'])
		self.assertEqual('HKD', position['currency'])
		self.assertAlmostEqual(60000000.00, position['balance'])