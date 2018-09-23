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

import collections
import csv
from itertools import islice


def consume(iterator, n):
    """Advance the iterator n-steps ahead. If n is none, consume entirely."""
    if n is None:
        collections.deque(iterator, maxlen=0)
    else:
        next(islice(iterator, n, n), None)


class Transaction(object):
    """ Represents a transaction obtained from csv-file. """

    def __init__(self, date, description, debit, credit, target_account, source_account='Assets:Current Assets:Checking Account'):
        self.date = date
        self.description = description
        self.debit = debit
        self.credit = credit
        self.target_account = target_account
        self.source_account = source_account

    def __str__(self):
        return '<Transaction %s, %s, %s, %s, %s>'% (
            self.date,
            self.description,
            self.debit,
            self.credit,
            self.target_account
        )

    @property
    def amount(self):
        return self.credit - self.debit

    def to_qif_line(self):
        return [
            '!Type:Cash',
            'D' + self.date.strftime('%m/%d/%y'),
            'S' + self.target_account,
            'P' + self.description,
            '$' + '%.2f' % self.amount,
            '^'
        ]


class TransactionFactory(object):
    """ Creates Transactions from an account_config. """

    def __init__(self, account_config, inclusion_config):
        self.account_config = account_config
        self.inclusion_config = inclusion_config

    def create_from_line(self, line):
        return Transaction(
            date=self.account_config.get_date(line),
            description=self.account_config.get_description(line),
            debit=self.account_config.get_debit(line),
            credit=self.account_config.get_credit(line),
            target_account=self.account_config.get_target_account(line),
            source_account=self.account_config.get_source_account(line)
        )

    def read_from_file(self, f, messenger):
        csv.register_dialect(
            'bank_csv',
            self.account_config.get_csv_dialect()
        )
        c = csv.reader(f, 'bank_csv')
        consume(c, self.account_config.dropped_lines)  # ignore first lines
        transactions = []
        for line in c:
            try:
                transaction = self.create_from_line(line)
                if (self.transaction_in_date_range(transaction)):
                    transactions.append(transaction)
                    messenger.send_message("parsed: " + transaction.__str__())
                else:
                    messenger.send_message("outside date range: " + transaction.__str__())
            except IndexError:
                messenger.send_message('skipped: %s' % line)
                continue
        return transactions

    def transaction_in_date_range(self, transaction):
        d = transaction.date
        return self.inclusion_config['from_date'] <= d and d <= self.inclusion_config['to_date']