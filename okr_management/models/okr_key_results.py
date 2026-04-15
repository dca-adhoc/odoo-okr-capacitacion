from odoo import fields, models


class OKRKeyResult(models.Model):
    _name = "okr.key.result"
    _description = "OKR Key Result"

    name = fields.Char(string="Descripción", required=True)
    objective_id = fields.Many2one("okr.objective", string="Objetivo", required=True)
    responsible_id = fields.Many2one("res.users", string="Responsable")
    state = fields.Selection(
        [
            ("draft", "Borrador"),
            ("in_progress", "Activo"),
            ("cancel", "Cancelado"),
            ("done", "Completado"),
        ],
        string="Estado",
        default="draft",
    )
    weight = fields.Float(string="Peso (%)", default=0.0)
    target = fields.Float(string="Target (%)", default=0.0)
    current_value = fields.Float(string="Resultado Actual", default=0.0)
