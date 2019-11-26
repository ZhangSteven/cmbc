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
						, 'samples', 'StockHoldInfo 20191122.xlsx')
		date, positions = getPositions(inputFile)
		positions = list(map(partial(holdingPosition, date), positions))
		self.assertEqual(26, len(positions))
		self.verifyPosition(positions[22])
		self.verifyPosition2(positions[23])



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
		self.assertEqual('2019-11-22', position['date'])
		self.assertEqual('', position['geneva_investment_id'])
		self.assertEqual('US69370RAA59', position['ISIN'])
		self.assertEqual('', position['bloomberg_figi'])
		self.assertEqual('PERTAMINA PERSERO PT', position['name'])
		self.assertEqual('USD', position['currency'])
		self.assertEqual(200000, position['quantity'])



	def verifyPosition2(self, position):
		self.assertEqual('560010910', position['portfolio'])
		self.assertEqual('', position['custodian'])
		self.assertEqual('2019-11-22', position['date'])
		self.assertEqual('1776 HK', position['geneva_investment_id'])
		self.assertEqual('', position['ISIN'])
		self.assertEqual('', position['bloomberg_figi'])
		self.assertEqual('GF SECURITIES CO LTD-H', position['name'])
		self.assertEqual('HKD', position['currency'])
		self.assertEqual(144000, position['quantity'])



	def verifyCashPosition(self, position):
		self.assertEqual('560010910', position['portfolio'])
		self.assertEqual('', position['custodian'])
		self.assertEqual('2019-11-25', position['date'])
		self.assertEqual('USD', position['currency'])
		self.assertAlmostEqual(19001.03 , position['balance'])