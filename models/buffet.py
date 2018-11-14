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
  name = fields.Char(string="Full Name")
  phone_number = fields.Char(string="Phone Number")
  date = fields.Date(string='Date', default=fields.Date.context_today)
  slot_time = fields.Selection(
    string=u'Slot Time',
    selection=[('1', '19:30 - 21:30'), ('2', '21:31 - 23:30')],
    default='1'
  )
  price = fields.Integer(string="Price", compute="_get_price") 
  state = fields.Selection([
    ('payment', 'Payment'),
    ('finished', 'Finished'),
  ], default='payment')

  debug = fields.Text(readonly=True)
  
  @api.onchange('member_id')
  def _get_name(self):
    for r in self.env['res.partner'].search([]):
      if (r.id == self.member_id.id): 
        self.name = r.name
        break

  @api.onchange('member_id')
  def _get_phone(self):
    for r in self.env['res.partner'].search([]):
      if (r.id == self.member_id.id): 
        self.phone_number = r.mobile
        break

  @api.onchange('date')
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
  def make_invoice(self):
    self.debug = "Action occurs!!"

    if self.book_type == "member": 
      self.member_id.reserve_buffet += 1

  @api.one
  def done_progressbar(self):
    self.state = "payment"