import hashlib
from datetime import datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError

SECRET_KEY = "HavanoPOS_Super_Secret_Key_2026_!@#"
BASE_DATE = datetime(2024, 1, 1)

class PosLicense(models.Model):
    _name = 'pos.license'
    _description = 'POS License Management'
    _order = 'create_date desc'

    name = fields.Char(string='Customer Name', required=True)
    machine_id = fields.Char(string='Machine ID', required=True, help="Enter the customer's Machine ID (e.g. XXXX-XXXX-XXXX-XXXX)")
    duration_days = fields.Selection([
        ('30', '30 Days (Trial)'),
        ('180', '180 Days (6 Months)'),
        ('365', '365 Days (1 Year)'),
        ('9999', 'Lifetime (No Expiry)'),
    ], string='License Duration', required=True, default='30')
    
    license_key = fields.Char(string='License Key', readonly=True, copy=False)
    creation_date = fields.Datetime(string='Creation Date', readonly=True)
    expiry_date = fields.Datetime(string='Expiry Date', readonly=True)
    
    status = fields.Selection([
        ('active', 'Active'),
        ('expiring', 'Expiring Soon'),
        ('expired', 'Expired'),
        ('lifetime', 'Lifetime')
    ], string='Status', compute='_compute_status', store=True)

    @api.depends('expiry_date')
    def _compute_status(self):
        now = fields.Datetime.now()
        for record in self:
            if not record.expiry_date:
                record.status = False
                continue
                
            # Safely handle naive/aware datetime differences by standardizing
            try:
                exp_dt = record.expiry_date.replace(tzinfo=None)
                now_dt = now.replace(tzinfo=None)
            except:
                exp_dt = record.expiry_date
                now_dt = now

            if exp_dt.year > 2100:
                record.status = 'lifetime'
            elif exp_dt < now_dt:
                record.status = 'expired'
            elif (exp_dt - now_dt).days <= 7:
                record.status = 'expiring'
            else:
                record.status = 'active'

    def action_generate_license(self):
        for record in self:
            if not record.machine_id:
                raise UserError(_("Machine ID is required to generate a license."))
                
            days = int(record.duration_days)
            machine_id_clean = record.machine_id.replace("-", "").strip()
            
            record.creation_date = fields.Datetime.now()
            
            if days >= 9999:
                record.expiry_date = BASE_DATE + timedelta(days=36500)
            else:
                record.expiry_date = record.creation_date + timedelta(days=days)
                
            try:
                exp_dt_naive = record.expiry_date.replace(tzinfo=None)
            except:
                exp_dt_naive = record.expiry_date

            days_since = (exp_dt_naive - BASE_DATE).days
            days_hex = f"{days_since:04X}"
            
            raw_payload = f"{machine_id_clean}:{days_hex}:{SECRET_KEY}"
            full_hash = hashlib.sha256(raw_payload.encode('utf-8')).hexdigest().upper()
            
            sig_hex = full_hash[:16]
            record.license_key = f"{days_hex}{sig_hex}".replace("-", "")
