from changellybinance import views as changellybinance_views
from fourchan_scanner import views as fourchan_scanner_views
from coinmarketcap import views as coinmarketcap_views

from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import RedirectView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/', changellybinance_views.home, name="home"),
    url(r'^submit_price_deltas/', changellybinance_views.submit_price_deltas, name="submit_price_deltas"),
    url(r'^get_price_deltas/', changellybinance_views.get_price_deltas, name="get_price_deltas"),
    url(r'^fourchan_scanner/', fourchan_scanner_views.fourchan_scanner, name="fourchan_scanner"),
    url(r'^update_fourchan_posts/', fourchan_scanner_views.update_fourchan_posts, name="update_fourchan_posts"),
    url(r'^sync_coin_list_with_coinmarketcap/', coinmarketcap_views.sync_coin_list_with_coinmarketcap, name="sync_coin_list_with_coinmarketcap"),

    # api methods
    url(r'^add_sms_notification_number/',  changellybinance_views.add_sms_notification_number, name="add_sms_notification_number"),
    url(r'^remove_number/',  changellybinance_views.remove_number, name="remove_number"),
    url(r'^delete_all_arb_data/',  changellybinance_views.delete_all_arb_data, name="delete_all_arb_data"),

]
