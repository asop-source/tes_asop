
from odoo import api, fields, models
import time
import datetime
from io import BytesIO
import xlsxwriter
import base64
from datetime import datetime
from odoo.exceptions import Warning
import logging
_logger = logging.getLogger(__name__)


class Components(models.Model):
	_name = 'components'


	name = fields.Char(string="Nama Komponents")
	date_start = fields.Date(string="Tanggal Mulai")
	date_end = fields.Date(string="Tanggal Selesai")

	items_id = fields.Many2one('items','Nama Items')




class Items(models.Model):
	_name = 'items'

	name = fields.Char(string="Nama Items")
	date_start = fields.Date(string="Tanggal Mulai")
	date_end = fields.Date(string="Tanggal Selesai")


	components_ids = fields.One2many('components','items_id',string="Nama Components")



	def cell_format(self, workbook):
		cell_format = {}
		cell_format['title'] = workbook.add_format({
			'bold': True,
			'align': 'center',
			'valign': 'vcenter',
			'font_size': 20,
			'font_name': 'Arial',
		})
		cell_format['header'] = workbook.add_format({
			'bold': True,
			'align': 'center',
			'border': True,
			'font_name': 'Arial',
		})
		cell_format['content'] = workbook.add_format({
			'font_size': 11,
			'border': False,
			'font_name': 'Arial',
		})
		cell_format['content_float'] = workbook.add_format({
			'font_size': 11,
			'border': True,
			'num_format': '#,##0.00',
			'font_name': 'Arial',
		})
		cell_format['total'] = workbook.add_format({
			'bold': True,
			'num_format': '#,##0.00',
			'border': True,
			'font_name': 'Arial',
		})
		return cell_format, workbook



	data = fields.Binary('File')

	@api.multi
	def export_excel(self):
		headers = [
					"Nomor",
					"Nama Components",
					"Date Start",
					"Date End",
					]

		fp = BytesIO()
		workbook = xlsxwriter.Workbook(fp)
		cell_format, workbook = self.cell_format(workbook)

		if not self.components_ids:
			raise Warning("Data Components Kosong. Mohon Lengkapi terlebih dahulu")

		worksheet = workbook.add_worksheet()
		worksheet.set_column('A:ZZ', 30)
		column_length = len(headers)

		########## parameters
		worksheet.write(0, 2, "REPORT ITEMS", cell_format['title'])
		worksheet.write(1, 0, "Nama", cell_format['content'])
		worksheet.write(1, 1, self.name , cell_format['content'])
		worksheet.write(2, 0, "Tanggal", cell_format['content'])
		worksheet.write(2, 1, self.date_start.strftime("%d-%b-%Y") + ' sampai ' + self.date_end.strftime("%d-%b-%Y"), cell_format['content'])

		########### header
		column = 0
		row = 4
		for col in headers:
			worksheet.write(row, column, col, cell_format['header'])
			column += 1

		########### contents
		row = 5
		final_data=[]
		no=1
		for data in self.components_ids :
			final_data.append([
				no,
				data.name,
				data.date_start.strftime("%d-%b-%Y"),
				data.date_end.strftime("%d-%b-%Y")
			])

			no += 1

		for data in final_data:
			column = 0
			for col in data:
				worksheet.write(row, column, col, cell_format['content'] if column<2 else  cell_format['content_float'])
				column += 1
			row += 1

		workbook.close()
		result = base64.encodestring(fp.getvalue())
		filename = self.name + '-' +'%2Exlsx'
		self.write({'data':result})
		url = "web/content/?model="+self._name+"&id="+str(self.id)+"&field=data&download=true&filename="+filename
		return {
			'type': 'ir.actions.act_url',
			'url': url,
			'target': 'new',
		}



#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100