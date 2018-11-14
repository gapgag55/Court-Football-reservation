from odoo import models, fields, api, exceptions

class Membership(models.Model):
  _inherit = 'res.partner' 

  reserve_court = fields.Integer(string="Reserve Court", readonly=True)
  reserve_buffet = fields.Integer(string="Reserve Buffet", readonly=True)
  reserve_free = fields.Integer(string="Reserve for Free", readonly=True)