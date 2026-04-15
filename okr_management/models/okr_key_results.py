from odoo.exceptions import ValidationError

from odoo import api, fields, models


class OKRKeyResult(models.Model):
    _name = "okr.key.result"
    _description = "OKR Key Result"

    name = fields.Char(string="Description", required=True)
    objective_id = fields.Many2one("okr.objective", string="Objective", required=True)
    responsible_id = fields.Many2one("res.users", string="Responsible")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("active", "Active"),
            ("cancel", "Cancelled"),
            ("done", "Done"),
        ],
        string="State",
        default="draft",
    )
    weight = fields.Float(string="Weight (%)", default=0.0)
    target = fields.Float(string="Target (%)", default=0.0)
    current_value = fields.Float(string="Current Value (%)", default=0.0)

    progress = fields.Float(
        string="Progress (%)", compute="_compute_progress", store=True
    )

    @api.depends("current_value", "target")
    def _compute_progress(self):
        for record in self:
            if record.target > 0:
                record.progress = (record.current_value / record.target) * 100
            else:
                record.progress = 0.0

    @api.constrains("weight", "state")
    def _check_weight(self):
        """Valida que el peso esté en rango y que la suma de activos no sature el 100% del objetivo"""
        for kr in self:
            if kr.weight < 0 or kr.weight > 100:
                raise ValidationError("Weight must be between 0% and 100%.")

            if kr.objective_id and kr.state == "active":
                active_krs = kr.objective_id.key_result_ids.filtered(
                    lambda k: k.state == "active"
                )
                total_weight = sum(active_krs.mapped("weight"))

                if total_weight > 100.0:
                    raise ValidationError(
                        f"The total weight of active Key Results for the objective '{kr.objective_id.name}' "
                        f"cannot exceed 100%. (Current total: {total_weight}%)."
                    )

    @api.constrains("target", "current_value")
    def _check_target_value(self):
        """Asegura la coherencia matemática de las métricas cargadas"""
        for kr in self:
            if kr.target <= 0:
                raise ValidationError(
                    "Target value must be strictly greater than zero."
                )
            if kr.current_value < 0:
                raise ValidationError("Current value cannot be negative.")

    # Botones de acción para la interfaz de usuario
    def action_set_draft(self):
        self.write({"state": "draft"})

    def action_set_active(self):
        self.write({"state": "active"})

    def action_set_cancelled(self):
        self.write({"state": "cancel"})

    def action_set_done(self):
        self.write({"state": "done"})
