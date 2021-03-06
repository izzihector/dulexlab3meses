# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.multi
    def open_produce_product(self):
        self.ensure_one()
        for stock_move in self.move_raw_ids:
            location_qty_available = stock_move.product_id.with_context(
                location=stock_move.raw_material_production_id.location_src_id.id).qty_available
            if stock_move.product_uom_qty > location_qty_available:
                raise ValidationError(
                    _('You plan to produce %s %s of %s but you only have %s %s available in %s location.') % \
                    (stock_move.product_uom_qty, stock_move.product_uom.name, stock_move.product_id.name,
                     location_qty_available, stock_move.product_id.uom_id.name,
                     stock_move.raw_material_production_id.location_src_id.display_name))
        return super(MrpProduction, self).open_produce_product()

    @api.multi
    def button_plan(self):
        for production in self:
            for stock_move in production.move_raw_ids:
                location_qty_available = stock_move.product_id.with_context(
                    location=stock_move.raw_material_production_id.location_src_id.id).qty_available
                if stock_move.product_uom_qty > location_qty_available:
                    raise ValidationError(
                        _('You plan to produce %s %s of %s but you only have %s %s available in %s location.') % \
                        (stock_move.product_uom_qty, stock_move.product_uom.name, stock_move.product_id.name,
                         location_qty_available, stock_move.product_id.uom_id.name,
                         stock_move.raw_material_production_id.location_src_id.display_name))
            return super(MrpProduction, self).button_plan()
