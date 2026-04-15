from odoo import fields, models


class OKR(models.Model):
    _name = "okr.management"
    _description = "OKR Management"

    name = fields.Char(string="Título", required=True)
    level = fields.Selection(
        [
            ("organization", "Organización"),
            ("team", "Equipo"),
            ("individual", "Individual"),
        ],
        string="Nivel",
        required=True,
    )
    period = fields.Selection(
        [
            ("anual", "Anual"),
            ("q1", "Q1"),
            ("q2", "Q2"),
            ("q3", "Q3"),
            ("q4", "Q4"),
        ],
        string="Período",
        required=True,
    )
