import os
from django.conf import settings

def get_fonts():
    return {
        "regular": os.path.join(settings.BASE_DIR, "fonts", "NotoSansDevanagari-Regular.ttf"),
        "bold": os.path.join(settings.BASE_DIR, "fonts", "NotoSansDevanagari-Bold.ttf"),
        "dejavu": os.path.join(settings.BASE_DIR, "fonts", "DejaVuSans.ttf"),
    }