from odoo import models, fields, api

class Price(models.Model):
  _name = "court.price"

  name = fields.Text(string="Name", default="Setting", readonly=True)
  
  weekday_morning_guest = fields.Integer(string="Guest")
  weekday_morning_member = fields.Integer(string="Member")
  weekday_morning_pre = fields.Integer(string="Pre(24)")

  weekday_evening_guest = fields.Integer(string="Guest")
  weekday_evening_member = fields.Integer(string="Member")
  weekday_evening_pre = fields.Integer(string="Pre(24)")

  weekday_night_guest = fields.Integer(string="Guest")
  weekday_night_member = fields.Integer(string="Member")
  weekday_night_pre = fields.Integer(string="Pre(24)")

  weekend_morning_guest = fields.Integer(string="Guest")
  weekend_morning_member = fields.Integer(string="Member")
  weekend_morning_pre = fields.Integer(string="Pre(24)")
  weekend_morning_guest = fields.Integer(string="Guest")

  weekend_evening_guest = fields.Integer(string="Guest")
  weekend_evening_member = fields.Integer(string="Member")
  weekend_evening_pre = fields.Integer(string="Pre(24)")

  weekend_night_guest = fields.Integer(string="Guest")
  weekend_night_member = fields.Integer(string="Member")
  weekend_night_pre = fields.Integer(string="Pre(24)")

  buffet_mon_tues = fields.Integer(string="Price")
  buffet_fri_sat_sun = fields.Integer(string="Price")