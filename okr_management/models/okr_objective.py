from odoo import fields, models


class OKRKeyResult(models.Model):
    _name = "okr.key.result"
    _description = "OKR Key Result"

    name = fields.Char(string="Descripción", required=True)
