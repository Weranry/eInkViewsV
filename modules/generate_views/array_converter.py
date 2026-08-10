from PIL import Image
import io


def image_to_raw_array(img):
    img_1bit = img.convert('1')
    return img_1bit.tobytes()


def image_to_raw_array_response(img, plugin_name, kind, size):
    raw_bytes = image_to_raw_array(img)
    buf = io.BytesIO(raw_bytes)
    buf.seek(0)
    filename = f"{plugin_name}_{kind}_{size}.bin"
    return buf, filename, len(raw_bytes)