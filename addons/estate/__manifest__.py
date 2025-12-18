# -*- coding: utf-8 -*-
{
  'name': 'Real Estate',
  'version': '19.0.1.0.0',
  'summary': 'Manage real estate property sales',
  'description': """
Real Estate
===========

This module provides basic functionality to manage property listings and sales.

Features
--------
- Create and manage properties
- Track offers and sales
- Manage property owners and agents

This is a minimal example module intended for learning and local testing with Odoo.
""",
  'author': 'Alex Martinez Juan',
  'website': '',
  'category': 'Sales',
  # Señala que se trata de una aplicación
  'application': True,
  'installable': True,
  # Especifica la lista de módulos requeridos para su correcto funcionamiento
  'depends': ['base'],
  # Incluye los ficheros relativos a políticas de seguridad y vistas
  'data': [
    'security/ir.model.access.csv',
    'views/estate_property_offer_views.xml',
    'views/estate_property_type_views.xml',
    'views/estate_property_tag_views.xml',
    'views/estate_property_views.xml',
    'views/estate_property_kanban_views.xml',
    'views/estate_menus.xml',
    'views/res_users_views.xml',
  ],
}
