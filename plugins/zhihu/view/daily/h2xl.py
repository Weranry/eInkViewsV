from plugins.zhihu.lib.fetcher import fetch_zhihu_daily
from modules.generate_views.canvas_factory import create_canvas, finalize_image_common
from modules.generate_views.font_loader import get_font, get_root_font_path
from modules.common_timezone import now_in_timezone
from modules.generate_views.qrcode_util import generate_qrcode
from PIL import Image
import os

def generate_image(rotate=0, invert=False, tz=None, cmode=None, **kwargs):
    # 1. 获取数据
    data = fetch_zhihu_daily()
    
    # 2. 初始化画布
    size_key = kwargs.get('size', 'h2xl')
    canvas, draw = create_canvas(size_key, 'bwr', cmode=cmode)
    width, height = canvas.size
    
    # 3. 准备字体
    font_path = get_root_font_path('font.ttf')
    font_48 = get_font(48, font_path)
    font_32 = get_font(32, font_path)
    font_16 = get_font(16, font_path)

    # 4. 绘制顶部信息
    now = now_in_timezone(tz)
    date_str = now.strftime("%m月%d日")
    weekday_map = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday_str = weekday_map[now.weekday()]
    
    margin = 16
    
    # 居左标头：知乎日报 ZHIHU DAILY （红字）
    draw.text((margin, margin), "知乎日报 ZHIHU DAILY", font=font_16, fill=2)
    
    # 居右：日期信息 （黑字）
    date_text = f"{date_str} | {weekday_str}"
    date_w = draw.textlength(date_text, font=font_16)
    draw.text((width - margin - date_w, margin), date_text, font=font_16, fill=1)
    
    # 分隔线
    line_y = margin + 28
    draw.line([(margin, line_y), (width - margin, line_y)], fill=1, width=2)

    # 5. 确定二维码位置与生成
    qr_size = 96
    qr_x = width - margin - qr_size
    qr_y = height - margin - qr_size
    
    if data.get('link'):
        # 1. 生成二维码 ("black", "white" 会生成标准的 0=黑, 255=白 的 L 模式图像)
        qr_img = generate_qrcode(data['link'], box_size=3, border=1, fill_color="black", back_color="white")
        qr_img = qr_img.resize((qr_size, qr_size), resample=0) # 0 = NEAREST, 杜绝杂色
        
        # 2. 映射颜色索引：在 bwr 的调色板中，1 是黑色，0 是白色
        # 将 L 模式的 0 (黑) 映射为 1, 255 (白) 映射为 0
        qr_img = qr_img.point(lambda x: 1 if x < 128 else 0)
        
        # 3. 粘贴二维码
        canvas.paste(qr_img, (qr_x, qr_y))

    # 6. 动态折行绘制标题
    title_text = data.get('title', '')
    title_start_y = line_y + 16
    line_height = 48
    
    def wrap_text_dynamic(text, font, start_y, line_h):
        lines = []
        line = ''
        y = start_y
        max_width = width - margin * 2
        for char in text:
            # 判断当前行高度是否已延伸到二维码区域
            current_max_width = max_width
            if y + line_h > qr_y - 8:
                # 为避免压到二维码，本行的最大宽度需要缩减
                current_max_width = qr_x - margin * 2
                
            test_line = line + char
            if draw.textlength(test_line, font=font) > current_max_width:
                if line:
                    lines.append((line, y))
                    y += line_h
                line = char
            else:
                line = test_line
        if line:
            lines.append((line, y))
        return lines

    lines = wrap_text_dynamic(title_text, font_32, title_start_y, line_height)
    
    # 限制最多显示5行，并确保字不越界
    for line_str, y_pos in lines[:5]:
        if y_pos + line_height <= height:
            draw.text((margin, y_pos), line_str, font=font_32, fill=1)
    
    return finalize_image_common(canvas, rotate=rotate, invert=invert)
