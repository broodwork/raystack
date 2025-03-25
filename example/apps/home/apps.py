from cotlette.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = 'cotlette.db.models.BigAutoField'
    name = 'apps.home'
