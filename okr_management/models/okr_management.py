from odoo import api, fields, models


class OKR(models.Model):
    _name = "okr.management"
    _description = "OKR Management"

    name = fields.Char(string="Título", required=True)
    parent_id = fields.Many2one("okr.management", string="OKR Principal")
    period_type = fields.Selection(
        [
            ("anual", "Anual"),
            ("quarterly", "Trimestral"),
        ],
        string="Tipo de Período",
    )
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
    )
    objective_ids = fields.One2many("okr.objective", "okr_id", string="Objetivos")
    responsible_id = fields.Many2one("res.users", string="Responsable", required=True)
    date_start = fields.Date(string="Fecha de Inicio")
    date_end = fields.Date(string="Fecha de Fin")
    year = fields.Integer(string="Año", default=lambda self: fields.Date.today().year)

    @api.onchange("period_type", "period", "year")
    def _onchange_dates(self):
        """Calcula fechas de inicio y fin automáticamente"""
        if not self.year:
            return

        if self.period_type == "anual":
            self.date_start = f"{self.year}-01-01"
            self.date_end = f"{self.year}-12-31"

        elif self.period_type == "quarterly" and self.period:
            # Diccionario de trimestres: (Mes Inicio, Día Inicio, Mes Fin, Día Fin)
            quarters = {
                "q1": ("01", "01", "03", "31"),
                "q2": ("04", "01", "06", "30"),
                "q3": ("07", "01", "09", "30"),
                "q4": ("10", "01", "12", "31"),
            }
            if self.period in quarters:
                data = quarters[self.period]
                self.date_start = f"{self.year}-{data[0]}-{data[1]}"
                self.date_end = f"{self.year}-{data[2]}-{data[3]}"
