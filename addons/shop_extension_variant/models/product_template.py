from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template' 

    def getVisibleVariants(self, website):
        return self.product_variant_ids.filtered(
            lambda v: v.shop_visibility in [website.shop_type, 'both']
        )

    def getbVisiblePtavIds(self, website):
        return set(self.getVisibleVariants(website).mapped('product_template_attribute_value_ids').ids)

    def getFilteredAttributeLines(self, visible_ptav_ids):
        return self.valid_product_template_attribute_line_ids.filtered(
            lambda line: any(val.id in visible_ptav_ids for val in line.product_template_value_ids)
        )

    def getPtavs_byLine(self, filtered_lines, visible_ptav_ids):
        return {
            line.id: line.product_template_value_ids.filtered(lambda ptav: ptav.id in visible_ptav_ids)
            for line in filtered_lines
        }

    def getVisibleVariant_or_Default(self, ptavs, website):
        visible_variants = self.getVisibleVariants(website)
        variant = self._get_variant_for_combination(ptavs)
        if not variant or variant.id not in visible_variants.ids:
            variant = visible_variants[:1]
            ptavs = variant.product_template_attribute_value_ids
        return variant, ptavs

    def getValidCombination_or_Default(self, combination, visible_variants):
        if not combination or combination not in visible_variants:
            return visible_variants[:1]
        return combination