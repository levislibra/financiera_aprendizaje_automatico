# -*- coding: utf-8 -*-

from openerp import models, fields, api


class ExtendsResCompany(models.Model):
	_name = 'res.company'
	_inherit = 'res.company'

	aa_id = fields.Many2one('financiera.aa.config', 'Configuracion Aprendizaje Automatico')
