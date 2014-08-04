#! /bin/sh
i18ndude rebuild-pot \
    --pot locales/collective.depositbox.pot \
    --create collective.depositbox \
    .

for po in locales/*/LC_MESSAGES/collective.depositbox.po; do
    i18ndude sync --pot locales/collective.depositbox.pot $po
done
