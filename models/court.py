from odoo import models, fields, api

class Court(models.Model):
  _name = "court.court"
  _rec_name = 'court_name'

  court_name = fields.Text()