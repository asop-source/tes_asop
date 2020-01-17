# -*- coding: utf-8 -*-
from odoo import http

# class TesAsop(http.Controller):
#     @http.route('/tes_asop/tes_asop/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tes_asop/tes_asop/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tes_asop.listing', {
#             'root': '/tes_asop/tes_asop',
#             'objects': http.request.env['tes_asop.tes_asop'].search([]),
#         })

#     @http.route('/tes_asop/tes_asop/objects/<model("tes_asop.tes_asop"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tes_asop.object', {
#             'object': obj
#         })