# -*- coding: utf-8 -*-
from openerp import http

# class FinancieraAprendizajeAutomatico(http.Controller):
#     @http.route('/financiera_aprendizaje_automatico/financiera_aprendizaje_automatico/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/financiera_aprendizaje_automatico/financiera_aprendizaje_automatico/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('financiera_aprendizaje_automatico.listing', {
#             'root': '/financiera_aprendizaje_automatico/financiera_aprendizaje_automatico',
#             'objects': http.request.env['financiera_aprendizaje_automatico.financiera_aprendizaje_automatico'].search([]),
#         })

#     @http.route('/financiera_aprendizaje_automatico/financiera_aprendizaje_automatico/objects/<model("financiera_aprendizaje_automatico.financiera_aprendizaje_automatico"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('financiera_aprendizaje_automatico.object', {
#             'object': obj
#         })