# Odoo OKR Capacitación: OKR Management

This repository hosts the practical implementation and technical artifacts developed during my Odoo advanced training program, specifically focusing on the design and architecture of a custom business solution from scratch.

## Project Purpose

The primary objective of this repository is to demonstrate hands-on mastery of the Odoo framework through the development of the **`okr_management`** application. This project highlights:
- Designing cohesive business logic using the Odoo ORM framework.
- Managing multi-level relational dependencies (Organization, Team, Individual).
- Implementing data constraints and automated computational flows.
- Constructing layered security access matrices (CSV and Record Rules).
- Applying clean coding standards and automated pre-commit quality checks.

## Repository Structure

The core of this repository centers around the `okr_management` directory, an independent Odoo module built to manage corporate Objectives and Key Results. It features fully separated layers for models, backend security configurations, and advanced UI/UX views.

## Technical Competencies Demonstrated

Through this development process, the repository showcases validated experience in:
- **Backend Architecture:** Developing with Odoo 18/19 models, using relational fields (`Many2one`, `One2many`), and processing date manipulations cleanly via native tools.
- **Data Integrity:** Writing Python `@api.depends` and `@api.constrains` methods to dynamically compute progress metrics and enforce business rules.
- **Interface Design:** Tailoring user interactions using multi-mode views including Kanban, customized Lists with dynamic color decorators, and clean, responsive Forms.
- **Access Control:** Establishing strict security separation between Manager and User profiles, including runtime record filtration based on ownership.

## Stack & Ecosystem

- **Platform Version:** Odoo 19
- **Core Languages:** Python, XML
- **Database Engine:** PostgreSQL
- **Workflow Tools:** Git

## Context Note

This repository functions as a technical execution benchmark and a personal training portfolio, reflecting concrete capabilities in building scalable applications within the Odoo ecosystem.

## Author

Carolina Dziubek

## License

AGPL-3
