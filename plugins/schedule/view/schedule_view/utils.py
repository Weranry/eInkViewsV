from modules.generate_views.canvas_factory import create_canvas, finalize_image_common
from modules.generate_views.font_loader import get_font, get_root_font_path
from modules.errors.errors import ParamError
def wrap_text(draw, text, font, max_w):
    """简单按字符自动换行，保证不超出给定宽度。"""
    if not text:
        return []
    lines = []
    cur = ""
    for ch in text:
        if draw.textlength(cur + ch, font=font) <= max_w:
            cur += ch
        else:
            if cur:
                lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines


def render_schedule(canvas, draw, schedule_data):
    """通用课表网格渲染引擎，支持网格布局与自动换行。

    约定：保持最小边距 16px（符合 16px 网格），所有字体尺寸为 16 的整数倍。
    """
    width, height = canvas.size
    font_path = get_root_font_path('font.ttf')

    # 基于宽度选择字体（必须为16倍数）
    if width >= 600:
        header_font = get_font(48, font_path)
        date_font = get_font(32, font_path)
        label_font = get_font(32, font_path)
        course_font = get_font(32, font_path)
        info_font = get_font(32, font_path)
        margin = 32
    elif width >= 400:
        header_font = get_font(32, font_path)
        date_font = get_font(16, font_path)
        label_font = get_font(32, font_path)
        course_font = get_font(16, font_path)
        info_font = get_font(16, font_path)
        margin = 16
    else:
        header_font = get_font(16, font_path)
        date_font = get_font(16, font_path)
        label_font = get_font(16, font_path)
        course_font = get_font(16, font_path)
        info_font = get_font(16, font_path)
        margin = 16

    # 强制最小安全边距（仅针对文本），但允许图形/线条延伸到画布边缘
    text_margin = max(margin, 16)
    graphic_margin = 0

    # Header
    date_info = schedule_data.get('dateInfo', {})
    week_str = f"第{date_info.get('weekNumber', '?')}周 周{date_info.get('dayOfWeek', '?')}"

    draw.text((text_margin, text_margin), "今日课表", font=header_font, fill=1)
    date_w = draw.textlength(week_str, font=date_font)
    header_h = header_font.size
    draw.text((width - text_margin - date_w, text_margin + header_h - date_font.size), week_str, font=date_font, fill=2)

    # 首部横线（允许延伸到边缘，视觉更宽）
    curr_y = text_margin + header_h + text_margin
    draw.line([(graphic_margin, curr_y), (width - graphic_margin, curr_y)], fill=1, width=2)

    # 课程网格区域
    schedule = schedule_data.get('schedule', {})
    slots = ["course1", "course2", "course3", "course4", "course5"]
    labels = ["M1", "M2", "A1", "A2", "EV"]

    available_h = height - curr_y - margin

    # 使行高对齐到16像素栅格
    base_row = max(16, (available_h // 5) // 16 * 16)
    if base_row < 16:
        base_row = 16

    row_height = base_row

    # 计算列宽：标签列、内容列、信息列
    label_col_width = max(draw.textlength(l, font=label_font) for l in labels) + 16

    # 预计算 info 最大宽度
    info_w_max = 0
    for slot in slots:
        course = schedule.get(slot, {})
        if course:
            parts = []
            if course.get('room'): parts.append(f"@{course.get('room')}")
            if course.get('teacher'): parts.append(course.get('teacher'))
            txt = " ".join(parts)
            if txt:
                info_w_max = max(info_w_max, draw.textlength(txt, font=info_font))
    info_col_width = info_w_max + 8

    gap = 12
    content_width = max(16, width - text_margin * 2 - label_col_width - info_col_width - gap)

    # 画竖向分栏线（线条延伸到边缘，但文本仍保留安全边距）
    x_label_sep = text_margin + label_col_width
    x_info_sep = width - text_margin - info_col_width
    draw.line([(x_label_sep, curr_y), (x_label_sep, curr_y + row_height * 5)], fill=1, width=1)
    draw.line([(x_info_sep, curr_y), (x_info_sep, curr_y + row_height * 5)], fill=1, width=1)

    # 渲染每行
    for i, slot in enumerate(slots):
        row_y = curr_y + i * row_height

        # 绘制标签（红色）
        lbl_text = labels[i]
        lbl_x = text_margin + 8
        lbl_y = row_y + (row_height - label_font.size) // 2
        draw.text((lbl_x, lbl_y), lbl_text, font=label_font, fill=2)

        course = schedule.get(slot, {})
        if course and course.get('name'):
            course_name = f"《{course.get('name')}》"

            # 右侧附加信息
            info_parts = []
            if course.get('room'): info_parts.append(f"@{course.get('room')}")
            if course.get('teacher'): info_parts.append(course.get('teacher'))
            info_text = " ".join(info_parts)

            # 自动换行显示课程名
            wrap_lines = wrap_text(draw, course_name, course_font, content_width)
            max_lines = max(1, row_height // course_font.size)
            display_lines = wrap_lines[:max_lines]

            # 垂直居中计算
            total_text_h = len(display_lines) * course_font.size
            start_y = row_y + max(2, (row_height - total_text_h) // 2)

            name_x = x_label_sep + 8
            for li, line in enumerate(display_lines):
                draw.text((name_x, start_y + li * course_font.size), line, font=course_font, fill=1)

            # 画右侧信息（靠右对齐）
            if info_text:
                info_w = draw.textlength(info_text, font=info_font)
                info_x = width - text_margin - info_w
                info_y = row_y + (row_height - info_font.size) // 2
                draw.text((info_x, info_y), info_text, font=info_font, fill=1)
        else:
            # 无课：留白（不绘制占位文字）
            pass

        # 行分隔线
        if i < 4:
            line_y = row_y + row_height
            # 横向分隔线可延伸到边缘
            draw.line([(graphic_margin, line_y), (width - graphic_margin, line_y)], fill=1, width=1)

