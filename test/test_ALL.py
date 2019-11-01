# coding=utf-8
# 

import unittest2
from os.path import join
from utils.iter import firstOf
from functools import partial
from cmbc.main import getCurrentDirectory, getPositions, holdingPosition\
					, cashPosition



class TestALL(unittest2.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestALL, self).__init__(*args, **kwargs)



	def testGetPositions(self):
		inputFile = join( getCurrentDirectory()\
						, 'samples', '20190828_5600xxxxx_sec_pos.xls')
		date, positions = getPositions(inputFile)
		positions = list(map(partial(holdingPosition, date), positions))
		self.assertEqual(1, len(positions))
		self.verifyPosition(positions[0])



	def testGetPositions2(self):
		inputFile = join( getCurrentDirectory()\
						, 'samples', '20190828_5600xxxxx_cash_pos.xls')
		date, positions = getPositions(inputFile)
		positions = list(map(partial(cashPosition, date), positions))
		self.assertEqual(4, len(positions))
		self.verifyCashPosition(firstOf( lambda p: p['currency'] == 'USD'\
									   , positions))



	def verifyPosition(self, position):
		self.assertEqual('5600xxxxx', position['portfolio'])
		self.assertEqual('', position['custodian'])
		self.assertEqual('2019-08-28', position['date'])
		self.assertEqual('', position['geneva_investment_id'])
		self.assertEqual('XS1990736644', position['ISIN'])
		self.assertEqual('', position['bloomberg_figi'])
		self.assertEqual('XS1990736644', position['name'])
		self.assertEqual('USD', position['currency'])
		self.assertEqual(150000000, position['quantity'])



	def verifyCashPosition(self, position):
		self.assertEqual('5600xxxxx', position['portfolio'])
		self.assertEqual('', position['custodian'])
		self.assertEqual('2019-08-28', position['date'])
		self.assertEqual('USD', position['currency'])
		self.assertAlmostEqual(56945.18, position['balance'])