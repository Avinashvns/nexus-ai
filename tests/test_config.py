from configs.settings import get_settings

settings = get_settings()

print(settings.app_name)
print(settings.default_model)
print(settings.ollama_host)