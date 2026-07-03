/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart } from "@odoo/owl";

export class PosLicenseDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        
        this.state = {
            kpi: {
                total: 0,
                active: 0,
                expiring: 0,
                expired: 0,
                lifetime: 0
            }
        };

        onWillStart(async () => {
            await this.fetchData();
        });
    }

    async fetchData() {
        const result = await this.orm.readGroup("pos.license", [], ["status"], ["status"]);
        
        let total = 0;
        let active = 0;
        let expiring = 0;
        let expired = 0;
        let lifetime = 0;

        for (const group of result) {
            total += group.status_count;
            if (group.status === "active") active = group.status_count;
            else if (group.status === "expiring") expiring = group.status_count;
            else if (group.status === "expired") expired = group.status_count;
            else if (group.status === "lifetime") lifetime = group.status_count;
        }

        this.state.kpi = { total, active, expiring, expired, lifetime };
    }

    openLicenses(status) {
        let domain = [];
        let title = "All Licenses";
        if (status) {
            domain = [["status", "=", status]];
            title = status.charAt(0).toUpperCase() + status.slice(1) + " Licenses";
            if (status === "active") {
                domain = [["status", "in", ["active", "lifetime"]]];
                title = "Active Licenses";
            }
        }
        
        this.action.doAction({
            type: "ir.actions.act_window",
            name: title,
            res_model: "pos.license",
            view_mode: "list,form",
            views: [[false, "list"], [false, "form"]],
            domain: domain,
            target: "current",
        });
    }
}

PosLicenseDashboard.template = "pos_license_management.Dashboard";

registry.category("actions").add("pos_license_dashboard", PosLicenseDashboard);
