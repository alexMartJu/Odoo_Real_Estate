# -*- coding: utf-8 -*-
{
  'name': 'Real Estate Account',
  'version': '19.0.1.0.0',
  'summary': 'Link module to create invoices when properties are sold',
  'description': """
Real Estate Account
========================

Small glue module that creates a customer invoice when a property is sold.
It depends on the `estate` module (real estate) and the `account` module (invoicing).

This module keeps both concerns decoupled: installing it activates the
automatic invoice creation behaviour in the estate workflow.
""",
  'author': 'Alex Martinez Juan',
  'website': '',
  'category': 'Sales',
  'application': False,
  'installable': True,
  'depends': ['estate', 'account'],
  'data': [],
}
