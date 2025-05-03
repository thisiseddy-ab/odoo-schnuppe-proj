from odoo import models, fields, api, SUPERUSER_ID

import logging
_logger = logging.getLogger(__name__)


def _generate_proxy_fields(cls):
    exclude = getattr(cls, '__exclude_proxy_fields__', [])

    for name, field in cls._inherit_model._fields.items():
        if name in exclude or name in cls._fields:
            continue

        if field.compute:
            continue  # You can support computed fields separately if needed

        # Build base override args
        field_overrides = {
            'compute': '_compute_all_proxy_fields',
            'store': False,
            'string': (field.string or name) + ' (Virtual)',
        }

        try:
            # Try recreating the field with original args + overrides
            proxy_field = type(field)(*getattr(field, 'args', ()), **{**field._kwargs, **field_overrides})
            setattr(cls, name, proxy_field)
        except Exception as e:
            _logger.warning(f"❌ Failed to proxy field '{name}': {e}")
            continue


class ProductTemplateVirtual(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'
    _table = 'product_template'  # 👈 This is key!
    _description = 'Website-Filtered Product Template View'
    _auto = False

    # 🧼 Exclude fields that crash, are not used, or belong to mail/thread systems
    __exclude_proxy_fields__ = [
        "product_variant_ids",
    ]

    product_variant_ids = fields.Many2many(
        'product.product',
        compute='_compute_visible_variants',
        store=False,
        string='Visible Product Variants',
    )

    def _compute_visible_variants(self):
        website = self.env['website'].get_current_website().with_context(self.env.context)
        for template in self:
            if website:
                template.product_variant_ids = template._origin.product_variant_ids.filtered( lambda v: v.shop_visibility in [website.shop_type, 'both'])
    
    '''
    @classmethod
    def _finalize_fields(cls):
        super()._finalize_fields()  # Call base first

        if cls._name != 'product.template.virtual':
            return  # Avoid affecting children, just in case

        env = api.Environment(api.Environment.manage().cr, SUPERUSER_ID, {})
        cls._inherit_model = type(env['product.template'])
        _generate_proxy_fields(cls)
        _logger.info(f"✅ Finalized proxy fields for {cls._name}")
    '''


    @api.depends(lambda self: self._get_all_proxy_field_depends())
    def _compute_all_proxy_fields(self):
        for record in self:
            for field_name in self._fields_to_proxy():
                setattr(record, field_name, getattr(record._origin, field_name))

    @classmethod
    def _fields_to_proxy(cls):
        return [
            name for name in cls._fields
            if name not in getattr(cls, '__exclude_proxy_fields__', [])
        ]

    @classmethod
    def _get_all_proxy_field_depends(cls):
        return [f'_origin.{field}' for field in cls._fields_to_proxy()]

    def _get_combination_info(
        self, combination=False, product_id=False, add_qty=1.0,
        parent_combination=False, only_template=False,
    ):
        website = self.env['website'].get_current_website().with_context(self.env.context)
        if website:
            return self._filtered_get_combination_info(
                combination=combination,
                product_id=product_id,
                add_qty=add_qty,
                parent_combination=parent_combination,
                only_template=only_template,
            )
        return super()._get_combination_info(
            combination=combination,
            product_id=product_id,
            add_qty=add_qty,
            parent_combination=parent_combination,
            only_template=only_template,
        )
    
    def _filtered_get_combination_info(
        self, combination=False, product_id=False, add_qty=1.0,
        parent_combination=False, only_template=False,
    ):
        self.ensure_one()

        combination = combination or self.env['product.template.attribute.value']
        parent_combination = parent_combination or self.env['product.template.attribute.value']
        website = self.env['website'].get_current_website().with_context(self.env.context)

        # Filter available variants based on your custom shop visibility logic
        visible_variants = self.product_variant_ids

        # Optionally: restrict to `website_id` or other domain logic
        # visible_variants = self.product_variant_ids.filtered(lambda v: v.shop_visibility and v.website_id == website.id)

        product = False

        if only_template:
            product = self.env['product.product']
        elif product_id:
            product = self.env['product.product'].browse(product_id)
            if product not in visible_variants:
                return {
                    'error': 'This variant is not available for the current shop.',
                    'is_combination_possible': False,
                    'product_id': False,
                    'product_template_id': self.id,
                }
            if (combination - product.product_template_attribute_value_ids):
                product = self._get_variant_for_combination(combination)
        else:
            product = self._get_variant_for_combination(combination)

        if product and product not in visible_variants:
            return {
                'error': 'This variant is not visible in this shop.',
                'is_combination_possible': False,
                'product_id': False,
                'product_template_id': self.id,
            }

        product_or_template = product or self
        combination = combination or product.product_template_attribute_value_ids
        display_name = product_or_template.with_context(display_default_code=False).display_name

        if not product:
            combination_name = combination._get_combination_name()
            if combination_name:
                display_name = f"{display_name} ({combination_name})"

        price_context = product_or_template._get_product_price_context(combination)
        product_or_template = product_or_template.with_context(**price_context)

        combination_info = {
            'combination': combination,
            'product_id': product.id if product else False,
            'product_template_id': self.id,
            'display_name': display_name,
            'display_image': bool(product_or_template.image_128),
            'is_combination_possible': self._is_combination_possible(combination=combination, parent_combination=parent_combination),
            'parent_exclusions': self._get_parent_attribute_exclusions(parent_combination=parent_combination),
            **self._get_additionnal_combination_info(
                product_or_template=product_or_template,
                quantity=add_qty or 1.0,
                date=fields.Date.context_today(self),
                website=website,
            )
        }

        if website.google_analytics_key:
            combination_info['product_tracking_info'] = self._get_google_analytics_data(
                product,
                combination_info,
            )

        if (
            product_or_template.type == 'combo'
            and website.show_line_subtotals_tax_selection == 'tax_included'
            and not all(tax.price_include for tax in product_or_template.combo_ids.sudo().combo_item_ids.product_id.taxes_id)
        ):
            combination_info['tax_disclaimer'] = _(
                "Final price may vary based on selection. Tax will be calculated at checkout."
            )

        return combination_info
    

    def _get_first_possible_combination(self, parent_combination=None):
        website = self.env['website'].get_current_website().with_context(self.env.context)
        if website:
            return self._filtered_get_first_possible_combination(parent_combination=parent_combination)
        return super()._get_first_possible_combination(parent_combination=parent_combination)
    
    def _filtered_get_first_possible_combination(self, parent_combination=None):
        self.ensure_one()
        parent_combination = parent_combination or self.env['product.template.attribute.value']

        # Filter variants visible in this shop/website
        visible_variants = self.product_variant_ids

        # Optionally: limit to current website
        # visible_variants = visible_variants.filtered(lambda v: v.website_id == website.id)

        # Pick the first valid visible variant
        variant = visible_variants[:1]

        if not variant:
            return self.env['product.template.attribute_value'].browse()

        # Return the attribute values of the visible variant
        return variant.product_template_attribute_value_ids
    
    def _get_variant_for_combination(self, combination):
        website = self.env['website'].get_current_website().with_context(self.env.context)
        if website:
            return self._filtered_get_variant_for_combination(combination=combination)
        return super()._get_variant_for_combination(combination=combination)
    
    def _filtered_get_variant_for_combination(self, combination):
        self.ensure_one()
        variant = super()._get_variant_for_combination(combination)
        # Filter out invisible variant
        if variant and variant not in self.product_variant_ids:
            return self.env['product.product']
        return variant