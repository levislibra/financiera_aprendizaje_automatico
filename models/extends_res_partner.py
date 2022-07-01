# -*- coding: utf-8 -*-

import openerp
from openerp import models, fields, api
from openerp.exceptions import UserError, ValidationError
import tensorflow.keras as kr
import numpy as np

class ExtendsResPartner(models.Model):
	_name = 'res.partner'
	_inherit = 'res.partner'

	aa_score = fields.Integer('AA Score')

	def aa_devolver_variables(self):
		print('aa_devolver_variables')
		vars = []
		# Variable 1: Email
		variable1 = 0
		if self.email and 'gmail' in self.email:
			variable1 = 1
		elif self.email and 'hotmail' in self.email:
			variable1 = 2
		print('variable1: ', variable1)
		vars.append(variable1)
		# Variable 2: Hora del alta
		variable2 = self.create_date.split(' ')[1].split(':')[0]
		print('variable2: ', variable2)
		vars.append(variable2)
		# variable 3: Score Nosis
		variable3 = self.nosis_variable_1.split(': ')[1]
		print('variable3: ', variable3)
		vars.append(variable3)
		# variable 4: Peor situacion
		variable4 = self.nosis_variable_2.split(': ')[1]
		print('variable4: ', variable4)
		vars.append(variable4)
		# variable 5: Financiacion BCRA
		variable5 = self.nosis_variable_4.split(': ')[1]
		print('variable5: ', variable5)
		vars.append(variable5)
		# variable 6: Ratio deuda actual / deuda hace 6 meses
		variable6 = float(self.nosis_variable_5.split(': ')[1])
		print('variable6: ', variable6)
		vars.append(variable6)
		# variable 7: Ingreso declarado por la persona
		variable7 = float(self.app_ingreso)
		print('variable7: ', variable7)
		vars.append(variable7)
		resultado = 10
		if self.alerta_cuotas_temprana > 0:
			resultado = 9
		if self.alerta_cuotas_media > 0:
			resultado = 4
		if self.alerta_cuotas_tardia > 0:
			resultado = 2
		if self.alerta_cuotas_incobrable:
			resultado = 1
		print('resultado: ', resultado)
		return vars, resultado

	@api.one
	def aa_trainer(self):
		# Inputs
		partner_obj = self.pool.get('res.partner')
		partner_ids = partner_obj.search(self.env.cr, self.env.uid, [
			('company_id', '=', self.company_id.id),
			# '|', ('alerta_prestamos_activos', '>', 0), ('alerta_prestamos_cobrados', '>', 0),
			'|', ('alerta_cuotas_cobradas', '>', 2), ('alerta_cuotas_tardia', '>', 0),
			('nosis_variable_1', '!=', False)
		])
		filtered = filter(lambda id: id % 2 == 0, partner_ids)
		training_list = []
		target_list = []
		for _id in filtered:
			partner_id = partner_obj.browse(self.env.cr, self.env.uid, _id)
			valores = partner_id.aa_devolver_variables()
			print('valores:: ', valores)
			training_list.append(valores[0])
			target_list.append(valores[1])

		# cargamos las entradas
		training_data = np.array(training_list, "float32")
		
		# y estos son los resultados que se obtienen, en el mismo orden
		target_data = np.array(target_list, "float32")

		lr = 0.01 #learning rate
		nn = [2, 16, 8, 1]

		# Creamos la estructura que contendra nuestro modelo
		model = kr.Sequential()

		# Capa 1
		model.add(kr.layers.Dense(nn[1], input_dim=5, activation='relu'))
		# Capa 2
		model.add(kr.layers.Dense(nn[2], activation='relu'))
		# Capa 3
		model.add(kr.layers.Dense(nn[3], activation='sigmoid'))
		# Compilamos el modelo
		model.compile(loss='mse', optimizer=kr.optimizers.SGD(lr=lr), metrics=['acc'])
		# Y entrenamos el modelo
		model.fit(training_data, target_data, epochs=250)
		score_predict = model.predict(self.aa_devolver_variables()[0])
		print('score_predict:: ', score_predict)
		self.aa_score = score_predict