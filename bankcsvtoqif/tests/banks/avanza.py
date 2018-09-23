# -*- coding: utf-8 -*-


# BankCSVtoQif - Smart conversion of csv files from a bank to qif
# Copyright (C) 2015-2016  Nikolai Nowaczyk
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import unittest
from datetime import datetime

from bankcsvtoqif.banks.avanza import Avanza
from bankcsvtoqif.tests.banks import csvline_to_line


class TestAvanza(unittest.TestCase):

    def setUp(self):
        self.csv_debit = """2018-01-29;6678344;Köp;This is a debit;0,3027;330,33;-99,99;-;SEK;SE0656516146"""
        self.csv_credit = """2018-01-29;6678344;Insättning;This is a credit;-;-;1000,00;-;SEK;-"""
        self.csv_sell = """2018-06-05;6678344;Sälj;This is a sell;-28,7301;208,05;5977,19;-;SEK;SE034534534"""
        self.csv_buy = """2018-06-04;6678344;Köp;This is a buy;4,6074;217,04;-999,99;-;SEK;SE00345345345"""

    def test_can_instantiate(self):
        account_config = Avanza()
        self.assertEqual(type(account_config), Avanza)

    def test_debit(self):
        account_config = Avanza()
        line = csvline_to_line(self.csv_debit, account_config)
        date = datetime(2018, 1, 29)
        description = 'This is a debit'
        debit = 99.99
        credit = 0
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)

    def test_credit(self):
        account_config = Avanza()
        line = csvline_to_line(self.csv_credit, account_config)
        date = datetime(2018, 1, 29)
        description = 'This is a credit'
        debit = 0
        credit = 1000.00
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)

    def test_sell(self):
        account_config = Avanza()
        line = csvline_to_line(self.csv_sell, account_config)
        date = datetime(2018, 6, 5)
        description = 'This is a sell'
        price = 208.05
        quantity = 28.7301
        amount = 5977.19
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_price(line), price)
        self.assertEqual(account_config.get_quantity(line), quantity)
        self.assertEqual(account_config.get_investment_amount(line), amount)

    def test_buy(self):
        account_config = Avanza()
        line = csvline_to_line(self.csv_buy, account_config)
        date = datetime(2018, 6, 4)
        description = 'This is a buy'
        price = 217.04
        quantity = 4.6074
        amount = 999.99
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_price(line), price)
        self.assertEqual(account_config.get_quantity(line), quantity)
        self.assertEqual(account_config.get_investment_amount(line), amount)