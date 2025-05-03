from odoo import models, fields


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    def _get_website_filtered_variants(self):
        self.ensure_one()
        website = self.env['website'].get_current_website()
        return self.product_variant_ids.filtered(lambda p: p.shop_visibility in [website.shop_type, 'both'])

    @property
    def website_product_variant_ids(self):
        if self.env.context.get('website_shop_filter'):
            return self._get_website_filtered_variants()
        return self.product_variant_ids
    
    def _get_filtered_attribute_lines_for_website(self):
        self.ensure_one()
        website = self.env['website'].get_current_website()

        visible_variants = self.product_variant_ids.filtered(
            lambda v: v.shop_visibility in [website.shop_type, 'both']
        )
        visible_value_ids = set(visible_variants.mapped('product_template_attribute_value_ids').ids)

        lines = self.valid_product_template_attribute_line_ids.filtered(
            lambda line: any(v.id in visible_value_ids for v in line.product_template_value_ids)
        )

        # Return lines with an extra dict that includes visible values
        result = []
        for line in lines:
            visible_values = line.product_template_value_ids.filtered(lambda v: v.id in visible_value_ids)
            result.append({
                'attribute_id': line.attribute_id,
                'product_template_value_ids': visible_values,
                'display_type': line.display_type,
                'id': line.id,
            })
        return result
        
    def _get_variant_for_combination(self, combination):
        variant = super()._get_variant_for_combination(combination)
        website = self.env['website'].get_current_website()

        if variant and variant.shop_visibility not in [website.shop_type, 'both']:
            return self.env['product.product']  # Return empty recordset if not visible

        return variant
    
class ProductTemplateAttributeLine(models.Model):
    _inherit = 'product.template.attribute.line'

    visible_ptavs = fields.Many2many(
        'product.template.attribute.value',
        compute='_compute_visible_ptavs',
        store=False,
        string='Visible PTAVs',
    )

    display_type = fields.Selection(
        related='attribute_id.display_type',
        store=False,
        readonly=True,
    )

    def _compute_visible_ptavs(self):
        # Dummy placeholder to allow dynamic assignment at runtime
        pass