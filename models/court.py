from odoo import models, fields, api

class Court(models.Model):
  _name = "court.court"

  court_name = fields.Text()