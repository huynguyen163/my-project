from odoo import fields, models, api


class ImportSalePersonWizard(models.TransientModel):
    _name = "import.sale.person.wizard"
    _description = "Import Sale Person"

    def default_lead_ids(self):
        active_ids = self.env.context.get('active_ids', [])
        lead_ids = self.env['crm.lead'].browse(active_ids)
        if active_ids:
            return lead_ids
        return []

    total_record = fields.Integer(
        'Total Record', compute="_total_record_sale")
    team_id = fields.Many2one('crm.team', 'Sales Team', required=True)
    sale_person_ids = fields.Many2many(
        'crm.team.member', string='Sale Person')
    lead_ids = fields.Many2many('crm.lead', default=default_lead_ids)
    assign_ids = fields.One2many('import.sale.person.detail.wizard', 'wizard_id', string='Assign Lead')
    
    
    def generate_lead(self):
        self.ensure_one
        lead_ids = self.lead_ids
        total_lead = len(self.lead_ids)
        total_sale_person = len(self.sale_person_ids)
        chunk_list = []
        num = total_lead // total_sale_person
        remainder = total_lead % total_sale_person
        self.assign_ids.unlink()
        vals = []
        detail_ids = []
        for sale_person in self.sale_person_ids:
            val = {
                'user_id': sale_person.user_id.id,
                'total_lead': num
            }
            vals.append(val)
        if remainder:
            end = vals[len(vals) - 1]
            end['total_lead'] += remainder
            vals[len(vals) - 1] = end

        for val in vals:
            detail_id = self.env['import.sale.person.detail.wizard'].sudo().create(val)
            detail_ids.append(detail_id.id)
        self.assign_ids = [(6,0,detail_ids)]
        return {
            'name': 'Import Sale Person',
            'view_mode': 'form',
            'view_id': False,
            'res_model': self._name,
            'domain': [],
            'context': dict(self._context, active_ids=self.ids),
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': self.id,
        }
    def apply(self):
        i = 0
        lead_ids = self.lead_ids.ids
        for line in self.assign_ids:
            new_lead = lead_ids[i : line.total_lead + i]
            new_lead_ids = self.env['crm.lead'].browse(new_lead)
            new_lead_ids.write({'user_id': line.user_id.id})
            i += line.total_lead


    @api.depends('lead_ids')
    def _total_record_sale(self):
        self.total_record = len(self.lead_ids)


class ImportSalePersonDetailWizard(models.TransientModel):
    _name = "import.sale.person.detail.wizard"
    _description = "Import Sale Person"

    wizard_id = fields.Many2one('import.sale.person.wizard', string="Wiz")
    user_id = fields.Many2one('res.users', string='Sale Person')
    total_lead = fields.Integer('Total Lead')