# -*- coding: utf-8 -*-
from openerp import http

# class Sysnotas(http.Controller):
#     @http.route('/sysnotas/sysnotas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sysnotas/sysnotas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sysnotas.listing', {
#             'root': '/sysnotas/sysnotas',
#             'objects': http.request.env['sysnotas.sysnotas'].search([]),
#         })

#     @http.route('/sysnotas/sysnotas/objects/<model("sysnotas.sysnotas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sysnotas.object', {
#             'object': obj
#         })