from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta

class CourtBooking(models.Model):
  _name = "court.book"

  date = fields.Date(string='Date', default=fields.Date.today())
  slot_time = fields.Selection(
    string='Time Slot',
    selection=[('1', '06:00 - 17:00'), ('2', '17:01 - 23:00'), ('3', '23:01 - 02:00')],
    default='1'
  )
  book_type = fields.Selection(
    string="Book Type",
    selection=[('guest', 'Guest'), ('member', 'Member'), ('pre', 'Pre(24)')],
    default='guest'
  )
  name = fields.Char(string="Full Name")
  member_id = fields.Many2one(string="Member", comodel_name='res.partner', ondelete='set null')
  phone_number = fields.Char(string="Phone Number")
  price = fields.Integer(string="Price", compute="_get_price")
  court_name = fields.Many2one(
    string=u'Court Reserve',
    comodel_name='court.court',
    ondelete='set null',
  )
  
  start_date = fields.Datetime(compute="_get_start_date", store=True)
  end_date = fields.Datetime(compute="_get_end_date", store=True)

  state = fields.Selection([
    ('payment', 'Payment'),
    ('finished', 'Finished'),
  ], default='payment', string="Status")

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
        
  @api.onchange('date', 'slot_time', 'court_name')
  def _get_avilable_court(self):
    books = self.search([])
    
    for book in books:
      # self.debug = str(book.date == self.date) + str(book.slot_time == self.slot_time) + str(book.court_name == self.court_name)
      if book.date == self.date and book.slot_time == self.slot_time and book.court_name == self.court_name:
        return {
          'warning': {
            'title': "Court is not available",
            'message': "Please select other court",
          },
        }

  @api.depends('date', 'slot_time', 'book_type')
  def _get_price(self):

    if int(self.slot_time) < 1: return

    weekno = datetime.strptime(self.date, "%Y-%m-%d").weekday()
    time = dict(self._fields['slot_time'].selection).get(self.slot_time).split(" ")[0]
    setting = self.env["court.price"].search([])

    if int(weekno) < 5:
        # self.debug = "Weekday, "

        if self.book_type == 'guest':
          # self.debug += "guest, price = "

          if time == "06:00":
            # self.debug += str(setting.weekday_morning_guest)
            self.price = setting.weekday_morning_guest
          elif time == "17:01":
            # self.debug += str(setting.weekday_evening_guest)
            self.price = setting.weekday_evening_guest
          elif time == "23:01":
            # self.debug += str(setting.weekday_night_guest)
            self.price = setting.weekday_night_guest

        elif self.book_type == 'member':
          # self.debug += "member, price = "

          if time == "06:00":
            # self.debug += str(setting.weekday_morning_member)
            self.price = setting.weekday_morning_member
          elif time == "17:01":
            # self.debug += str(setting.weekday_evening_member)
            self.price = setting.weekday_evening_member
          elif time == "23:01":
            # self.debug += str(setting.weekday_night_member)
            self.price = setting.weekday_night_member

        elif self.book_type == 'pre':
          # self.debug += "pre, price = "

          if time == "06:00":
            # self.debug += str(setting.weekday_morning_pre)
            self.price = setting.weekday_morning_pre
          elif time == "17:01":
            # self.debug += str(setting.weekday_evening_pre)
            self.price = setting.weekday_evening_pre
          elif time == "23:01":
            # self.debug += str(setting.weekday_night_pre)
            self.price = setting.weekday_night_pre
    else:
        # self.debug = "Weekend, "

        if self.book_type == 'guest':
          # self.debug += "guest, price = "

          if time == "06:00":
            # self.debug += str(setting.weekend_morning_guest)
            self.price = setting.weekend_morning_guest
          elif time == "17:01":
            # self.debug += str(setting.weekend_evening_guest)
            self.price = setting.weekend_evening_guest
          elif time == "23:01":
            # self.debug += str(setting.weekend_night_guest)
            self.price = setting.weekend_night_guest

        elif self.book_type == 'member':
          # self.debug += "member, price = "
          
          if time == "06:00":
            # self.debug += str(setting.weekend_morning_member)
            self.price = setting.weekend_morning_member
          elif time == "17:01":
            # self.debug += str(setting.weekend_evening_member)
            self.price = setting.weekend_evening_member
          elif time == "23:01":
            # self.debug += str(setting.weekend_night_member)
            self.price = setting.weekend_night_member

        elif self.book_type == 'pre':
          # self.debug += "pre, price = "
          
          if time == "06:00":
            # self.debug += str(setting.weekend_morning_pre)
            self.price = setting.weekend_morning_pre
          elif time == "17:01":
            # self.debug += str(setting.weekend_evening_pre)
            self.price = setting.weekend_evening_pre
          elif time == "23:01":
            # self.debug += str(setting.weekend_night_pre)
            self.price = setting.weekend_night_pre

  @api.depends('date', 'slot_time')
  def _get_start_date(self):
    if int(self.slot_time) > 0:
      date = self.date.split("-")
      time = dict(self._fields['slot_time'].selection).get(self.slot_time).split(" ")

      start_date = date[0] + "-" + date[1] + "-" + date[2] + " " + time[0] + ":01"
      self.start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S") + timedelta(hours=-7)
      # self.debug = self.start_date

  @api.depends('date', 'slot_time')
  def _get_end_date(self):
    if int(self.slot_time) > 0:
      date = self.date.split("-")
      time = dict(self._fields['slot_time'].selection).get(self.slot_time).split(" ")

      end_date = date[0] + "-" + date[1] + "-" + date[2] + " " + time[2] + ":01"

      if (int(self.slot_time) == 3):
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S") + timedelta(hours=-7, days=1)
      else:
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S") + timedelta(hours=-7)
  
  @api.one
  def make_invoice(self):
    self.state = "finished"
    if self.book_type == "member": 
      self.member_id.reserve_court += 1

  @api.one
  def done_progressbar(self):
    self.state = "payment"