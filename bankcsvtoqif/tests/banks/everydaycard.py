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

from bankcsvtoqif.banks.everydaycard import Everydaycard
from bankcsvtoqif.tests.banks import csvline_to_line


class TestEverydaycard(unittest.TestCase):

    def setUp(self):
        self.csv_debit_quoted = """2019-03-27,Huvudkort,Mat,This is a debit,\"1086,78\",\"120,61\""""
        self.csv_debit_unquoted = """2019-03-27,Huvudkort,Mat,This is also a debit,85,0"""
        # self.csv_credit = """"""

    def test_can_instantiate(self):
        account_config = Everydaycard()
        self.assertEqual(type(account_config), Everydaycard)

    def test_debit_quoted(self):
        date = datetime(2019, 3, 27)
        description = 'This is a debit'
        debit = 1086.78
        credit = 0
        self.__do_debit(self.csv_debit_quoted, date, description, debit, credit)

    def test_debit_unquoted(self):
        date = datetime(2019, 3, 27)
        description = 'This is also a debit'
        debit = 85
        credit = 0
        self.__do_debit(self.csv_debit_unquoted, date, description, debit, credit)

    def __do_debit(self, test_line, date, description, debit, credit):
        account_config = Everydaycard()
        line = csvline_to_line(test_line, account_config)

        self.assertEqual(account_config.get_date(line), date)
        self.assertEqual(account_config.get_description(line), description)
        self.assertEqual(account_config.get_debit(line), debit)
        self.assertEqual(account_config.get_credit(line), credit)

    # def test_credit(self):
    #     account_config = Everydaycard()