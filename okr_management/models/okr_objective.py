from odoo.exceptions import ValidationError

from odoo import api, fields, models


class OKRObjective(models.Model):
    _name = "okr.objective"
    _description = "OKR Objective"
    _order = "date_start desc, name"

    name = fields.Char(string="Description", required=True)
    okr_id = fields.Many2one(
        "okr.management", string="OKR", required=True, ondelete="cascade"
    )
    key_result_ids = fields.One2many(
        "okr.key.result", "objective_id", string="Key Results"
    )
    responsible_id = fields.Many2one(
        "res.users", string="Responsible", default=lambda self: self.env.user
    )

    type = fields.Selection(
        [("commited", "Committed"), ("aspirational", "Aspirational")],
        string="Type",
        required=True,
        default="commited",
    )

    progress = fields.Float(
        string="Progress (%)", compute="_compute_progress", store=True
    )

    # Hierarchical fields mirrored from the parent OKR
    cadence = fields.Selection(related="okr_id.cadence", string="Cadence", store=True)
    date_start = fields.Date(
        related="okr_id.date_start", string="Start Date", store=True
    )
    date_end = fields.Date(related="okr_id.date_end", string="End Date", store=True)

    @api.depends(
        "key_result_ids.current_value",
        "key_result_ids.target",
        "key_result_ids.weight",
        "key_result_ids.state",
    )
    def _compute_progress(self):
        """Calculates objective progress based on the normalized weight of its active KRs"""
        for obj in self:
            total_progress = 0.0
            active_krs = obj.key_result_ids.filtered(lambda kr: kr.state == "active")
            total_weight = sum(active_krs.mapped("weight"))

            if total_weight > 0:
                for kr in active_krs:
                    if kr.target > 0:
                        # KR completion percentage
                        kr_completion = kr.current_value / kr.target
                        # Normalized weight relative to total active weight
                        normalized_weight = kr.weight / total_weight
                        # Add to total progress
                        total_progress += (kr_completion * normalized_weight) * 100

            obj.progress = total_progress

    @api.constrains("key_result_ids")
    def _check_weights(self):
        """Ensures that the sum of active key result weights does not exceed 100%"""
        for obj in self:
            active_weights = obj.key_result_ids.filtered(
                lambda x: x.state == "active"
            ).mapped("weight")
            if sum(active_weights) > 100.0:
                raise ValidationError(
                    f"The total weight of active Key Results for the objective '{obj.name}' "
                    f"cannot exceed 100%. (Current total: {sum(active_weights)}%)."
                )

    @api.model
    def _cron_finished_objectives(self):
        """Scheduled Action (Cron) to close expired objectives and set active KRs to done"""
        today = fields.Date.today()
        expired_objectives = self.search([("date_end", "<", today)])
        for obj in expired_objectives:
            active_krs = obj.key_result_ids.filtered(lambda kr: kr.state == "active")
            if active_krs:
                active_krs.write({"state": "done"})

    @api.ondelete(at_uninstall=False)
    def _ondelete_change_state(self):
        """Cancels related key results when an objective is deleted instead of breaking constraints"""
        for obj in self:
            if obj.key_result_ids:
                obj.key_result_ids.write({"state": "cancel"})
