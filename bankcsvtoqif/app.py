# -*- coding: utf-8 -*-


# BankCSVtoQif - Smart conversion of csv files from a bank to qif
# Copyright (C) 2015-2017  Nikolai Nowaczyk
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


import argparse
import importlib
import inspect
import pkgutil

from bankcsvtoqif import banks

# create dict of all bank account types
bank_dict = {}
for importer, modname, ispkg in pkgutil.iter_modules(banks.__path__):
    module = importlib.import_module('bankcsvtoqif.banks.' + modname)
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, banks.BankAccountConfig) and not obj is banks.BankAccountConfig:
            bank_dict[modname] = obj

# create an argument parser for the app
parser = argparse.ArgumentParser(
    description="Smart conversion of csv files from bank statements to qif.",
    epilog="Exampe: python b2q.py db_giro statement_june_15.csv"
)
parser.add_argument('type', choices=bank_dict.keys(), help="account type from which you want to convert")
parser.add_argument('csv_file', help="csv file you want to convert")
parser.add_argument('qif_file', nargs='?', default='', help="name of qif file output")
parser.add_argument('-s', '--source_account', nargs='?', const='Assets:Current Assets:Checking Account',
                    help="default source account")
parser.add_argument('-t', '--target_account', nargs='?', const='Imbalance-EUR', help="default target account")
parser.add_argument('-r', '--replacements', nargs='?', const='replacements.ini',
                    help="config file for automatic replacements")
parser.add_argument('-v', action='store_true', help="produce output during conversion")
parser.add_argument('-F', '--from_date', default='0001-01-01', help="start date, inclusive, to include from input")
parser.add_argument('-T', '--to_date', default='2999-12-31', help="end date, inclusive, to include from input")