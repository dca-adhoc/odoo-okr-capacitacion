{
    "name": "OKR Management",
    "summary": "Gestión de Objetivos y Resultados Clave (OKRs)",
    "description": """
        Módulo para la capacitación de Odoo.
        Permite crear OKRs, Objetivos y Key Results vinculados.
    """,
    "author": "dca-adhoc",
    "version": "19.0.1.0",
    "license": "AGPL-3",
    "depends": [
        "base",
        "web",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/okr_management_views.xml",
        "views/okr_objective_views.xml",
    ],
    "installable": True,
    "application": True,
}
