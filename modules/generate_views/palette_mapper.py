def map_palette(palette, mode):
    """
    调色板映射函数
    palette: [r,g,b, r,g,b, ...]
    mode: None, '2bw', 'r2y', 'y2r', 'yr2r', 'yr2y'
    """
    if not mode or mode == 'None':
        return palette
    colors = [tuple(palette[i:i+3]) for i in range(0, len(palette), 3)]
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    RED = (255,0,0)
    YELLOW = (255,255,0)
    if mode == '2bw':
        mapped = [WHITE if c == WHITE else BLACK for c in colors]
    elif mode == 'r2y':
        mapped = [YELLOW if c == RED else c for c in colors]
    elif mode == 'y2r':
        mapped = [RED if c == YELLOW else c for c in colors]
    elif mode == 'yr2r':
        mapped = [RED if c == RED or c == YELLOW else c for c in colors]
    elif mode == 'yr2y':
        mapped = [YELLOW if c == RED or c == YELLOW else c for c in colors]
    else:
        mapped = colors
    return [v for c in mapped for v in c]
