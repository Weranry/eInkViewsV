import io
from PIL import Image
from flask import send_file, make_response
from config import (
    DEFAULT_JPEG_QUALITY,
    DEFAULT_WEBP_QUALITY,
    DEFAULT_PNG_COMPRESS_LEVEL,
    DEFAULT_TIFF_COMPRESSION,
    IMAGE_FORMAT_BLACKLIST,
)
from modules.errors.errors import ParamError

_FORMAT_REGISTRY = {
    'jpg':  {'pillow': 'JPEG', 'mime': 'image/jpeg',  'ext': '.jpg'},
    'jpeg': {'pillow': 'JPEG', 'mime': 'image/jpeg',  'ext': '.jpg'},
    'png':  {'pillow': 'PNG',  'mime': 'image/png',   'ext': '.png'},
    'bmp':  {'pillow': 'BMP',  'mime': 'image/bmp',   'ext': '.bmp'},
    'webp': {'pillow': 'WEBP', 'mime': 'image/webp',  'ext': '.webp'},
    'tiff': {'pillow': 'TIFF', 'mime': 'image/tiff',  'ext': '.tiff'},
    'gif':  {'pillow': 'GIF',  'mime': 'image/gif',   'ext': '.gif'},
}

_FORMAT_SAVE_KWARGS = {
    'jpg':  {'quality': DEFAULT_JPEG_QUALITY, 'subsampling': 0, 'progressive': False},
    'jpeg': {'quality': DEFAULT_JPEG_QUALITY, 'subsampling': 0, 'progressive': False},
    'webp': {'quality': DEFAULT_WEBP_QUALITY},
    'png':  {'compress_level': DEFAULT_PNG_COMPRESS_LEVEL},
    'tiff': {'compression': DEFAULT_TIFF_COMPRESSION},
}


def image_to_raw_array(img):
    img_1bit = img.convert('1', dither=Image.NONE)
    return img_1bit.tobytes()


def _make_array_response(img, name_parts):
    raw_bytes = image_to_raw_array(img)
    buf = io.BytesIO(raw_bytes)
    buf.seek(0)
    filename = '_'.join(name_parts) + '.bin'
    return buf, filename, len(raw_bytes)


def _build_image_response(img, fmt_key, name_parts):
    info = _FORMAT_REGISTRY[fmt_key]
    buf = io.BytesIO()
    save_kwargs = _FORMAT_SAVE_KWARGS.get(fmt_key, {})
    img.save(buf, format=info['pillow'], **save_kwargs)
    buf.seek(0)
    filename = '_'.join(name_parts) + info['ext']
    return make_response(send_file(buf, mimetype=info['mime'], download_name=filename))


def save_image(img, img_format, name_parts):
    img_format = img_format.lower()
    if img_format in IMAGE_FORMAT_BLACKLIST:
        raise ParamError(f'输出格式 {img_format} 已被禁用')
    if img_format == 'array':
        buf, filename, raw_len = _make_array_response(img, name_parts)
        response = make_response(send_file(buf, mimetype='application/octet-stream', download_name=filename))
        response.headers['X-Raw-Bytes'] = str(raw_len)
        return response
    if img_format not in _FORMAT_REGISTRY:
        supported = ', '.join(sorted(k for k in _FORMAT_REGISTRY if k != 'jpeg'))
        raise ParamError(f'不支持的输出格式: {img_format}，支持 {supported} / array')
    return _build_image_response(img, img_format, name_parts)