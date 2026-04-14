from modules.generate_views.font_loader import get_font, get_root_font_path

def draw_tide_chart(draw, x, y, width, height, forecast_data, min_wave, max_wave, font, line_color, text_color):
    # Draw a line chart for the wave height forecast inside the bounding box (x, y, width, height)
    if not forecast_data:
        return
        
    num_points = len(forecast_data)
    if num_points < 2:
        return
        
    dx = width / (num_points - 1)
    
    range_wave = max_wave - min_wave
    if range_wave == 0:
        range_wave = 1
        
    points = []
    
    for i, wave in enumerate(forecast_data):
        px = x + i * dx
        py = y + height - ((wave - min_wave) / range_wave) * height
        points.append((px, py))
        
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        draw.line((x1, y1, x2, y2), fill=line_color, width=2)
        
    # Draw min and max labels
    bbox_max = draw.textbbox((0,0), f"{max_wave:.1f}m", font=font)
    w_max = bbox_max[2] - bbox_max[0]
    draw.text((x - w_max - 8, y - 8), f"{max_wave:.1f}m", font=font, fill=text_color)
    
    bbox_min = draw.textbbox((0,0), f"{min_wave:.1f}m", font=font)
    w_min = bbox_min[2] - bbox_min[0]
    draw.text((x - w_min - 8, y + height - 8), f"{min_wave:.1f}m", font=font, fill=text_color)
