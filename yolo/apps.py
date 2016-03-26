from django.apps import AppConfig

class WebappConfig(AppConfig):
    name = 'yolo'
    verbose_name='startupConfig'
    def ready(self):
    	pass