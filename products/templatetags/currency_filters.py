# Di file templatetags/currency_filters.py
from django import template
import locale

register = template.Library()

@register.filter
def idr_format(value):
    """Format angka menjadi format IDR dengan titik sebagai pemisah ribuan"""
    try:
        # Konversi ke integer jika diperlukan
        if isinstance(value, str):
            value = float(value)
        
        # Format dengan pemisah ribuan
        formatted = "{:,.0f}".format(value).replace(',', '.')
        return formatted
    except (ValueError, TypeError):
        return value

# Alternatif menggunakan locale (opsional)
@register.filter  
def idr_locale_format(value):
    """Format menggunakan locale Indonesia"""
    try:
        # Set locale ke Indonesia (perlu diinstall locale id_ID)
        locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')
        return locale.format_string("%.0f", value, grouping=True)
    except:
        # Fallback jika locale tidak tersedia
        return "{:,.0f}".format(value).replace(',', '.')