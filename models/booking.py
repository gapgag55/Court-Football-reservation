from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta

class CourtBooking(models.Model):
  _name = "court.book"

  date = fields.Date(string='Date', default=fields.Date.context_today)
  slot_time = fields.Selection(
    string='Time Slot',
    selection=[('1', '06:00 - 17:00'), ('2', '17:00 - 23:00'), ('3', '23:00 - 02:00')],
    default='1'
  )
  book_type = fields.Selection(
    string="Book Type",
    selection=[('guest', 'Guest'), ('member', 'Member'), ('pre', 'Pre(24)')],
    default='guest'
  )
  
  member_id = fields.Many2one(string="Member", comodel_name='res.partner', ondelete='set null')
  phone_number = fields.Char(string="Phone Number")
  price = fields.Integer(string="Price", compute="_get_price")
  available_court = fields.Many2one(
    string=u'Court Revserve',
    comodel_name='court.court',
    ondelete='set null',
  )
  
  start_date = fields.Datetime(compute="_get_start_date")
  end_date = fields.Datetime(compute="_get_end_date")

  state = fields.Selection([
    ('concept', 'Concept'),
    ('started', 'Started'),
    ('progress', 'In progress'),
    ('finished', 'Done'),
    ],default='concept')

  debug = fields.Text(readonly=True)

  @api.onchange('date', 'slot_time', 'available_court')
  def _get_avilable_court(self):
    books = self.search([])
    
    for book in books:
      # self.debug = str(book.date == self.date) + str(book.slot_time == self.slot_time) + str(book.available_court == self.available_court)
      if book.date == self.date and book.slot_time == self.slot_time and book.available_court == self.available_court:
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
          elif time == "17:00":
            # self.debug += str(setting.weekday_evening_guest)
            self.price = setting.weekday_evening_guest
          elif time == "23:00":
            # self.debug += str(setting.weekday_night_guest)
            self.price = setting.weekday_night_guest

        elif self.book_type == 'member':
          # self.debug += "member, price = "

          if time == "06:00":
            # self.debug += str(setting.weekday_morning_member)
            self.price = setting.weekday_morning_member
          elif time == "17:00":
            # self.debug += str(setting.weekday_evening_member)
            self.price = setting.weekday_evening_member
          elif time == "23:00":
            # self.debug += str(setting.weekday_night_member)
            self.price = setting.weekday_night_member

        elif self.book_type == 'pre':
          # self.debug += "pre, price = "

          if time == "06:00":
            # self.debug += str(setting.weekday_morning_pre)
            self.price = setting.weekday_morning_pre
          elif time == "17:00":
            # self.debug += str(setting.weekday_evening_pre)
            self.price = setting.weekday_evening_pre
          elif time == "23:00":
            # self.debug += str(setting.weekday_night_pre)
            self.price = setting.weekday_night_pre
    else:
        # self.debug = "Weekend, "

        if self.book_type == 'guest':
          # self.debug += "guest, price = "

          if time == "06:00":
            # self.debug += str(setting.weekend_morning_guest)
            self.price = setting.weekend_morning_guest
          elif time == "17:00":
            # self.debug += str(setting.weekend_evening_guest)
            self.price = setting.weekend_evening_guest
          elif time == "23:00":
            # self.debug += str(setting.weekend_night_guest)
            self.price = setting.weekend_night_guest

        elif self.book_type == 'member':
          # self.debug += "member, price = "
          
          if time == "06:00":
            # self.debug += str(setting.weekend_morning_member)
            self.price = setting.weekend_morning_member
          elif time == "17:00":
            # self.debug += str(setting.weekend_evening_member)
            self.price = setting.weekend_evening_member
          elif time == "23:00":
            # self.debug += str(setting.weekend_night_member)
            self.price = setting.weekend_night_member

        elif self.book_type == 'pre':
          # self.debug += "pre, price = "
          
          if time == "06:00":
            # self.debug += str(setting.weekend_morning_pre)
            self.price = setting.weekend_morning_pre
          elif time == "17:00":
            # self.debug += str(setting.weekend_evening_pre)
            self.price = setting.weekend_evening_pre
          elif time == "23:00":
            # self.debug += str(setting.weekend_night_pre)
            self.price = setting.weekend_night_pre

  @api.depends('date', 'slot_time')
  def _get_start_date(self):
    if int(self.slot_time) > 0:
      date = self.date.split("-")
      time = dict(self._fields['slot_time'].selection).get(self.slot_time).split(" ")

      start_date = date[0] + "-" + date[1] + "-" + date[2] + " " + time[0] + ":00"
      self.start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S") + timedelta(hours=-7)
           
  @api.depends('date', 'slot_time')
  def _get_end_date(self):
    if int(self.slot_time) > 0:
      date = self.date.split("-")
      time = dict(self._fields['slot_time'].selection).get(self.slot_time).split(" ")

      end_date = date[0] + "-" + date[1] + "-" + date[2] + " " + time[2] + ":00"

      if (int(self.slot_time) == 3):
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S") + timedelta(hours=-7, days=1)
      else:
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S") + timedelta(hours=-7)

  @api.one
  def generate_record_name(self):
    self.debug = "Action occurs!!"
    # self.debug = str(cr) + " --- " + str(self.env.cr)
    # self.debug = str(cr) + " -- " + str(uid)
    # invoice_id = self.env['account.invoice'].create({
    #   'name' : 'test',
    #   'date_invoice' : self.date,
    # }, {
    #   'account_id': self.env.uid
    # })

    # self.env['account.invoice.line'].create({
    #   'invoice_id' : invoice_id,
    #   'name' : 'name',
    #   'product_id' : '2',
    # })

    # for record in self.browse(cr, uid):

    #   for line in record.line:
    #     self.debug = line.name
    #     self.pool.get('account.invoice.line').create(cr, uid, {
    #       'invoice_id' : invoice_id,
    #       'name' : line.name,
    #       'product_id' : line.product_id.id,
    #     })
