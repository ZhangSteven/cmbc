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
						, 'samples', 'sec_pos_08112019.xlsx')
		date, positions = getPositions(inputFile)
		positions = list(map(partial(holdingPosition, date), positions))
		self.assertEqual(1, len(positions))
		self.verifyPosition(positions[0])



	def testGetPositions2(self):
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



	def verifyCashPosition(self, position):
		self.assertEqual('560010910', position['portfolio'])
		self.assertEqual('', position['custodian'])
		self.assertEqual('2019-11-08', position['date'])
		self.assertEqual('HKD', position['currency'])
		self.assertAlmostEqual(60000000.00, position['balance'])