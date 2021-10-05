from odoo import fields, models


class CheckList(models.Model):
    _name = 'check.list'
    name = fields.Char('Name')
    description = fields.Text('Description')
    status = fields.Selection(string="Status",
                              selection=[('done', 'Done'), ('progress', 'In Progress'), ('cancel', 'Cancel')],
                              readonly=True, track_visibility='onchange')

    def do_accept(self):
        self.write({
            'status': 'done',
        })
        # return {'type': 'ir.actions.client', 'tag': 'reload'}

    def do_cancel(self):
        self.write({
            'status': 'cancel',
        })
        # return {'type': 'ir.actions.client', 'tag': 'reload'}

    def do_progress(self):
        self.write({
            'status': 'progress',
        })
        # return {'type': 'ir.actions.client', 'tag': 'reload'}

    def do_set_to(self):
        self.write({
            'status': ''
        })

    class CustomProject(models.Model):
        _inherit = 'project.task'
        info_checklist = fields.One2many(comodel_name="check.list", inverse_name="name", required=True,
                                         track_visibility='onchange')
        progress_rate = fields.Integer(string='Checklist Progress', compute="check_rate")
        total = fields.Integer(string="Max")
        status = fields.Selection(string="Status",
                                  selection=[('done', 'Done'), ('progress', 'In Progress'), ('cancel', 'Cancel')],
                                  readonly=True, track_visibility='onchange')

        maximum_rate = fields.Integer(default=100)

        def check_rate(self):
            for rec in self:
                rec.progress_rate = 0
                total = len(rec.info_checklist.ids)
                done = 0
                cancel = 0
                if total == 0:
                    pass
                else:
                    if rec.info_checklist:
                        for item in rec.info_checklist:
                            if item.status == 'done':
                                done = done + 1
                            rec.progress_rate = round(done / (total - cancel), 2) * 100
