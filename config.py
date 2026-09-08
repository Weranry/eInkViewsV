#--------------------------------图像参数配置----------------------------------#
# 默认旋转角度
DEFAULT_ROTATE = 0
# 默认是否反色
DEFAULT_INVERT = False
# 默认JPEG质量 (0-100)
DEFAULT_JPEG_QUALITY = 85
# 默认WEBP质量 (0-100)
DEFAULT_WEBP_QUALITY = 85
# 默认PNG压缩等级 (0-9, 0=无压缩, 9=最高压缩)
DEFAULT_PNG_COMPRESS_LEVEL = 6
# 默认TIFF压缩方式 (tiff_lzw 无损 / tiff_zlib 无损 / tiff_adobe_deflate 无损 / raw 无压缩)
DEFAULT_TIFF_COMPRESSION = 'tiff_lzw'
# 默认输出格式：jpg / png / bmp / webp / tiff / gif / array
DEFAULT_IMAGE_FORMAT = 'jpg'
# 输出格式黑名单，禁止列表中的格式被渲染（节省恶意开销）
IMAGE_FORMAT_BLACKLIST = []
#-----------------------------------时区配置-----------------------------------#
# 默认时区偏移（小时），如中国为8，印度为5.5，英国为0
DEFAULT_TIMEZONE_OFFSET = 8

#----------------------鉴权系统配置--------------------------------------------#
# 是否启用鉴权
AUTH_ENABLE = False
# 鉴权白名单（可访问的路径列表，支持字符串前缀匹配）
AUTH_WHITELIST = [
	'/public',
	'/favicon.ico',
	'/static',
	'/assets',
	'/pages',
	'/index.html',
]