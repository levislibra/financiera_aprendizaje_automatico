# -*- coding: utf-8 -*-

from openerp import models, fields, api
import tensorflow.keras as kr
import numpy as np

class AprendizajeAutomaticoConfig(models.Model):
	_name = 'financiera.aa.config'

	name = fields.Char('Nombre')
	name_model = fields.Char('Nombre del modelo')
	company_id = fields.Many2one('res.company', 'Empresa', required=False)

	@api.model
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
		