from odoo import api, fields, models


class OKRObjective(models.Model):
    _name = "okr.objective"
    _description = "OKR Objective"

    name = fields.Char(string="Descripción", required=True)
    okr_id = fields.Many2one("okr.management", string="OKR", required=True)
    key_result_ids = fields.One2many(
        "okr.key.result", "objective_id", string="Resultados Clave"
    )
    responsible_id = fields.Many2one("res.users", string="Responsable")
    type = fields.Selection(
        [("commited", "Compromiso"), ("aspirational", "Aspiracional")],
        string="Tipo",
    )
    progress = fields.Float(string="Progreso", compute="_compute_progress", store=True)

    @api.depends(
        "key_result_ids.current_value",
        "key_result_ids.target",
        "key_result_ids.weight",
    )
    def _compute_progress(self):
        for obj in self:
            total_progress = 0.0
            active_okrs = obj.key_result_ids.filtered(
                lambda kr: kr.state in ["in_progress", "done"]
            )
            for kr in active_okrs:
                total_progress += (kr.current_value / 100.0) * kr.weight
            obj.progress = total_progress
