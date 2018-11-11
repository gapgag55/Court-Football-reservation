from odoo import models, fields, api

class Buffet(models.Model):
  _name = "buffet.book"

  name = fields.Text()