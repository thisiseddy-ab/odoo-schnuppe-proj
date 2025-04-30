odoo.define('shop_extension_pr_vr.variant_override', function (require) {
    "use strict";

    const publicWidget = require('web.public.widget');

    publicWidget.registry.WebsiteSale.include({
        _onChangeCombination: function (ev, $parent, combination) {
            this._super.apply(this, arguments);

            // Wait a tick for default rendering to finish
            setTimeout(() => {
                if (combination.variant_html) {
                    const $newVariants = $(combination.variant_html);
                    const $variantsContainer = $parent.find('.js_add_cart_variants');
                    if ($variantsContainer.length) {
                        $variantsContainer.replaceWith($newVariants);
                    }
                }
            }, 0);
        }
    });
});