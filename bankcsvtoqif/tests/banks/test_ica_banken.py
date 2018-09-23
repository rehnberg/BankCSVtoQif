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

from bankcsvtoqif.banks.ica_banken import IcaBanken
from bankcsvtoqif.tests.banks import csvline_to_line


class TestIcaBanken(unittest.TestCase):

    def setUp(self):
        self.csv = """2018-01-21;This is a debit;Korttransaktion;Övrigt;-318,45 kr;10,56 kr"""
        self.csv2 = """2018-01-26;This is a credit;Insättning;Övrigt;2 000,00 kr;2 010,56 kr"""

    def test_can_instantiate(self):
        account_config = IcaBanken()
        self.assertEqual(type(account_config), IcaBanken)

    def test_debit(self):
        account_config = IcaBanken()
        line = csvline_to_line(self.csv, account_config)
        date = datetime(2018, 1, 21)
        description = 'This is a debit'
        debit = 318.45
        credit = 0
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)

    def test_credit(self):
        account_config = IcaBanken()
        line = csvline_to_line(self.csv2, account_config)
        date = datetime(2018, 1, 26)
        description = 'This is a credit'
        debit = 0
        credit = 2000.00
        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)
