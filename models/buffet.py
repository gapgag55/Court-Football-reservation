from odoo import models, fields, api
from datetime import datetime

class Buffet(models.Model):
  _name = "buffet.book"

  book_type = fields.Selection(
    string="Book Type",
    selection=[('guest', 'Guest'), ('member', 'Member')],
    default='guest'
  )
  member_id = fields.Many2one(string="Member", comodel_name='res.partner', ondelete='set null')
  name = fields.Char(string="Full Name", compute="_get_name", store=True)
  phone_number = fields.Char(string="Phone Number", compute="_get_phone", store=True)
  date = fields.Date(string='Date', default=fields.Date.context_today)
  slot_time = fields.Selection(
    string=u'Slot Time',
    selection=[('1', '19:30 - 21:30'), ('2', '21:30 - 23:30')],
    default='1'
  )
  price = fields.Integer(string="Price", compute="_get_price") 
  state = fields.Selection([
    ('concept', 'Concept'),
    ('started', 'Started'),
    ('progress', 'In progress'),
    ('finished', 'Done'),
  ], default='concept')

  debug = fields.Text(readonly=True)
  
  # @api.depends('member_id')
  # def _get_name(self):
  #   for r in self.env['res.partner'].search([]):
  #     if (r.id == self.member_id.id): 
  #       self.name = r.name
  #       break

  # @api.depends('member_id')
  # def _get_phone(self):
  #   for r in self.env['res.partner'].search([]):
  #     if (r.id == self.member_id.id): 
  #       self.phone_number = r.mobile
  #       break

  @api.depends('date')
  def _get_price(self):
    setting = self.env["court.price"].search([])

    weekno = int(datetime.strptime(self.date, "%Y-%m-%d").weekday())
    setting = self.env["court.price"].search([])

    if weekno >= 0 and weekno <= 1:
      self.price = setting.buffet_mon_tues
    elif weekno >= 4 and weekno <= 6:
      self.price = setting.buffet_fri_sat_sun
    else:
      return {
        'warning': {
          'title': "Error",
          'message': "Date is not available for football buffet",
        },
      }

  @api.one
  def generate_record_name(self):
    self.debug = "Action occurs!!"

    