from odoo.exceptions import ValidationError
from odoo.tools import date_utils

from odoo import api, fields, models


class OKR(models.Model):
    _name = "okr.management"
    _description = "OKR Management"
    _order = "date_start desc, name"

    name = fields.Char(string="Title", required=True)
    parent_id = fields.Many2one(
        "okr.management", string="Parent OKR", ondelete="set null"
    )
    child_ids = fields.One2many("okr.management", "parent_id", string="Child OKRs")
    child_count = fields.Integer(string="Child Count", compute="_compute_child_count")
    level = fields.Selection(
        [
            ("organization", "Organization"),
            ("team", "Team"),
            ("individual", "Individual"),
        ],
        string="Level",
        required=True,
    )
    cadence = fields.Selection(
        [
            ("yearly", "Yearly"),
            ("q1", "Q1"),
            ("q2", "Q2"),
            ("q3", "Q3"),
            ("q4", "Q4"),
        ],
        string="Cadence",
    )
    objective_ids = fields.One2many("okr.objective", "okr_id", string="Objectives")
    responsible_id = fields.Many2one("res.users", string="Responsible", required=True)
    employee_id = fields.Many2one("hr.employee", string="Employee")
    team_ids = fields.Many2many("hr.department", string="Team")
    date_start = fields.Date(
        string="Start Date", compute="_compute_dates", store=True, recursive=True
    )
    date_end = fields.Date(
        string="End Date", compute="_compute_dates", store=True, recursive=True
    )
    year = fields.Integer(string="Year", default=lambda self: fields.Date.today().year)
    progress = fields.Float(string="Progress", compute="_compute_progress")
    company_ids = fields.Many2many(
        "res.company",
        string="Companies",
        default=lambda self: [(6, 0, [self.env.company.id])],
    )

    @api.depends("year", "cadence")
    def _compute_dates(self):
        """Calcula de forma determinista el inicio y fin del periodo usando date_utils"""
        for rec in self:
            if not rec.year:
                rec.date_start = False
                rec.date_end = False
                continue

            base_date = fields.Date.today().replace(year=rec.year, month=1, day=1)

            if rec.cadence == "yearly":
                rec.date_start = date_utils.start_of(base_date, "year")
                rec.date_end = date_utils.end_of(base_date, "year")
            else:
                quarters_months = {"q1": 1, "q2": 4, "q3": 7, "q4": 10}
                month_start = quarters_months.get(rec.cadence, 1)
                target_date = base_date.replace(month=month_start)

                rec.date_start = date_utils.start_of(target_date, "quarter")
                rec.date_end = date_utils.end_of(target_date, "quarter")

    @api.depends("objective_ids.progress")
    def _compute_progress(self):
        """El progreso del OKR es el promedio simple de sus objetivos"""
        for rec in self:
            if rec.objective_ids:
                rec.progress = sum(rec.objective_ids.mapped("progress")) / len(
                    rec.objective_ids
                )
            else:
                rec.progress = 0.0

    @api.depends("child_ids")
    def _compute_child_count(self):
        for rec in self:
            rec.child_count = len(rec.child_ids)

    @api.constrains("parent_id")
    def _check_no_recursive_relationship(self):
        """Evita bucles infinitos: un OKR no puede ser padre de sí mismo"""
        for okr in self:
            parent = okr.parent_id
            while parent:
                if parent == okr:
                    raise ValidationError(
                        "Recursive OKR relationships are not allowed. An OKR cannot be its own parent/ancestor."
                    )
                parent = parent.parent_id

    @api.constrains("cadence", "parent_id")
    def _check_cadence_hierarchy(self):
        """Valida que los quarters y años coincidan de forma lógica entre padres e hijos"""
        for okr in self:
            if okr.parent_id:
                # Un OKR anual no puede depender de uno trimestral
                if okr.cadence == "yearly" and okr.parent_id.cadence != "yearly":
                    raise ValidationError(
                        "A yearly OKR cannot have a quarterly parent OKR."
                    )
                # Si ambos son trimestrales, tienen que ser del mismo quarter (no mezclar Q1 con Q3)
                if (
                    okr.cadence != "yearly"
                    and okr.parent_id.cadence != "yearly"
                    and okr.cadence != okr.parent_id.cadence
                ):
                    raise ValidationError(
                        "A quarterly OKR must share the same quarter cadence as its parent OKR."
                    )

    @api.ondelete(at_uninstall=False)
    def _ondelete_handle_children(self):
        """Si se borra el padre, desvincula a los hijos de forma segura y los vuelve anuales"""
        for okr in self:
            if okr.child_ids:
                okr.child_ids.write({"cadence": "yearly", "parent_id": False})
