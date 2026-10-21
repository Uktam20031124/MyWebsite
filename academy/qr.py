"""QR kod — sahifaga to'g'ridan-to'g'ri qo'yiladigan SVG (rasm fayli va tashqi xizmat kerak emas)."""

import qrcode
import qrcode.image.svg
from django.utils.safestring import mark_safe


def svg(data: str) -> str:
    image = qrcode.make(
        data,
        image_factory=qrcode.image.svg.SvgPathImage,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        border=2,
    )
    # Bir sahifada ko'p QR bo'ladi — takrorlanuvchi id olib tashlanadi.
    markup = image.to_string(encoding="unicode").replace(' id="qr-path"', "")
    return mark_safe(markup)  # noqa: S308 — qrcode yaratgan SVG
