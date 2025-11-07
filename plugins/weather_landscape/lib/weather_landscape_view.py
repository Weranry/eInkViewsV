import os
import random
import math
import datetime
from PIL import Image, ImageOps
from .weather_landscape_fetcher import WeatherData, SunCalculator

class Sprites:
    """处理精灵图片绘制"""
    DISABLED = -999999
    Black = 0
    White = 1
    Red = 2
    BLACK = 0
    WHITE = 1
    RED = 2
    TRANS = 3
    PLASSPRITE = 10
    MINUSSPRITE = 11
    EXT = ".png"

    def __init__(self, sprites_dir, canvas):
        self.img = canvas
        self.pix = self.img.load()
        self.dir = sprites_dir
        self.ext = self.EXT
        self.w, self.h = self.img.size

    def Dot(self, x, y, color):
        if (y >= self.h) or (x >= self.w) or (y < 0) or (x < 0):
            return
        self.pix[x, y] = color

    def Draw(self, name, index, xpos, ypos, ismirror=False):
        if (xpos < 0) or (ypos < 0):
            return 0
        imagefilename = "%s_%02i%s" % (name, index, self.ext)
        imagepath = os.path.join(self.dir, imagefilename)
        if not os.path.exists(imagepath):
            # 如果找不到该 sprite，直接返回宽度 0，不影响主流程（调用方会继续绘制）
            return 0
        img = Image.open(imagepath)
        if ismirror:
            img = ImageOps.mirror(img)
        w, h = img.size
        pix = img.load()
        ypos -= h
        for x in range(w):
            for y in range(h):
                if (xpos + x >= self.w) or (xpos + x < 0):
                    continue
                if (ypos + y >= self.h) or (ypos + y < 0):
                    continue
                if pix[x, y] == self.BLACK:
                    self.Dot(xpos + x, ypos + y, self.Black)
                elif pix[x, y] == self.WHITE:
                    self.Dot(xpos + x, ypos + y, self.White)
                elif pix[x, y] == self.RED:
                    self.Dot(xpos + x, ypos + y, self.Red)
        return w

    DIGITPLAS = 10
    DIGITMINUS = 11
    DIGITSEMICOLON = 12

    def DrawInt(self, n, xpos, ypos, issign=True, mindigits=1):
        n = round(n)
        if n < 0:
            sign = self.DIGITMINUS
        else:
            sign = self.DIGITPLAS
        n = abs(n)
        n0 = int(n / 100)
        n1 = int((n % 100) / 10)
        n2 = n % 10
        dx = 0
        if (issign) or (sign == self.DIGITMINUS):
            w = self.Draw("digit", sign, xpos + dx, ypos)
            dx += w + 1
        if (n0 != 0) or (mindigits >= 3):
            w = self.Draw("digit", n0, xpos + dx, ypos)
            dx += w
            if (n0 != 1):
                dx += 1
        if (n1 != 0) or (n0 != 0) or (mindigits >= 2):
            if (n1 == 1):
                dx -= 1
            w = self.Draw("digit", n1, xpos + dx, ypos)
            dx += w
            if (n1 != 1):
                dx += 1
        if (n2 == 1):
            dx -= 1
        w = self.Draw("digit", n2, xpos + dx, ypos)
        dx += w
        if (n2 != 1):
            dx += 1
        return dx

    def DrawClock(self, xpos, ypos, h, m):
        dx = 0
        w = self.DrawInt(h, xpos + dx, ypos, False, 2)
        dx += w
        w = self.Draw("digit", self.DIGITSEMICOLON, xpos + dx, ypos)
        dx += w
        dx = self.DrawInt(m, xpos + dx, ypos, False, 2)
        dx += w + 1
        return dx

    CLOUDWMAX = 32
    CLOUDS = [2, 3, 5, 10, 30, 50]
    CLOUDK = 0.5

    def DrawCloud(self, persent, xpos, ypos, width, height):
        if persent < 2:
            return
        elif persent < 5:
            cloudset = [2]
        elif persent < 10:
            cloudset = [3, 2]
        elif persent < 20:
            cloudset = [5, 3, 2]
        elif persent < 30:
            cloudset = [10, 5]
        elif persent < 40:
            cloudset = [10, 10]
        elif persent < 50:
            cloudset = [10, 10, 5]
        elif persent < 60:
            cloudset = [30, 5]
        elif persent < 70:
            cloudset = [30, 10]
        elif persent < 80:
            cloudset = [30, 10, 5, 5]
        elif persent < 90:
            cloudset = [30, 10, 10]
        else:
            cloudset = [50, 30, 10, 10, 5]
        dx = width
        for c in cloudset:
            self.Draw("cloud", c, xpos + random.randrange(dx), ypos)

    HEAVYRAIN = 5.0
    RAINFACTOR = 20

    def DrawRain(self, value, xpos, ypos, width, tline):
        ypos += 1
        r = 1.0 - (value / self.HEAVYRAIN) / self.RAINFACTOR
        for x in range(xpos, xpos + width):
            for y in range(ypos, tline[x], 2):
                if (x >= self.w):
                    continue
                if (y >= self.h):
                    continue
                if (random.random() > r):
                    self.pix[x, y] = self.Black
                    self.pix[x, y - 1] = self.Black

    HEAVYSNOW = 5.0
    SNOWFACTOR = 10

    def DrawSnow(self, value, xpos, ypos, width, tline):
        ypos += 1
        r = 1.0 - (value / self.HEAVYSNOW) / self.SNOWFACTOR
        for x in range(xpos, xpos + width):
            for y in range(ypos, tline[x], 2):
                if (x >= self.w):
                    continue
                if (y >= self.h):
                    continue
                if (random.random() > r):
                    self.pix[x, y] = self.Black

    def DrawWind_degdist(self, deg1, deg2):
        h = max(deg1, deg2)
        l = min(deg1, deg2)
        d = h - l
        if d > 180:
            d = 360 - d
        return d

    def DrawWind_dirsprite(self, dir, dir0, name, list):
        count = [4, 3, 3, 2, 2, 1, 1]
        step = 11.25
        dist = self.DrawWind_degdist(dir, dir0)
        n = int(dist / step)
        if n < len(count):
            for i in range(0, count[n]):
                list.append(name)

    def DrawWind(self, speed, direction, xpos, tline):
        list = []
        self.DrawWind_dirsprite(direction, 0, "pine", list)
        self.DrawWind_dirsprite(direction, 90, "east", list)
        self.DrawWind_dirsprite(direction, 180, "palm", list)
        self.DrawWind_dirsprite(direction, 270, "tree", list)
        random.shuffle(list)
        windindex = None
        if speed <= 0.4:
            windindex = []
        elif speed <= 0.7:
            windindex = [0]
        elif speed <= 1.7:
            windindex = [1, 0, 0]
        elif speed <= 3.3:
            windindex = [1, 1, 0, 0]
        elif speed <= 5.2:
            windindex = [1, 2, 0, 0]
        elif speed <= 7.4:
            windindex = [1, 2, 2, 0]
        elif speed <= 9.8:
            windindex = [1, 2, 3, 0]
        elif speed <= 12.4:
            windindex = [2, 2, 3, 0]
        else:
            windindex = [3, 3, 3, 3]
        if windindex is not None:
            ix = int(xpos)
            random.shuffle(windindex)
            j = 0
            for i in windindex:
                if j >= len(list):
                    break
                xx = ix + random.randint(-1, 1)
                ismirror = random.random() < 0.5
                offset = xx + 5
                if offset >= len(tline):
                    break
                if ismirror:
                    xx -= 16
                self.Draw(list[j], i, xx, tline[offset] + 1, ismirror)
                ix += 9
                j += 1

    SMOKE_R_PX = 30
    PERSENT_DELTA = 4
    SMOKE_SIZE = 60

    def DrawSmoke_makeline(self, angle_deg):
        a = (math.pi * angle_deg) / 180
        r = self.SMOKE_R_PX
        k = r * math.sin(a) / (math.sqrt((r * math.cos(a))))
        yp = 0
        dots = []
        for x in range(0, self.w):
            y = int(k * math.sqrt(x))
            if y > self.h:
                y = self.h
            yi = yp
            while True:
                rr = math.sqrt(x * x + yi * yi)
                dots.append([x, yi, rr])
                if rr > self.SMOKE_SIZE:
                    return dots
                yi += 1
                if yi >= y:
                    yp = y
                    break

    def DrawSmoke(self, x0, y0, percent):
        dots = self.DrawSmoke_makeline(percent)
        for d in dots:
            x = d[0]
            y = d[1]
            r = d[2]
            if random.random() * 1.3 > (r / self.SMOKE_SIZE):
                if random.random() * 1.2 < (r / self.SMOKE_SIZE):
                    dx = random.randint(-1, 1)
                    dy = random.randint(-1, 1)
                else:
                    dx = 0
                    dy = 0
                self.Dot(x0 + x + dx, self.h - (y0 + y) + dy, self.Black)


class WeatherDrawer:
    """天气绘图器"""
    XSTART = 32
    XSTEP = 44
    XFLAT = 10
    YSTEP = 50
    DEFAULT_DEGREE_PER_PIXEL = 0.5
    FLOWER_RIGHT_PX = 15
    FLOWER_LEFT_PX = 10
    DRAWOFFSET = 235
    IMAGE_WIDTH = 400
    IMAGE_HEIGHT = 300

    @staticmethod
    def ensure_sprites_dir():
        # 在插件内查找 sprite 文件夹（相对于本文件）
        sprites_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "sprite"))
        if not os.path.exists(sprites_dir):
            # 如果插件 sprite 不存在，尝试回退到同级 sprite（兼容旧位置）
            alt = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprite"))
            if os.path.exists(alt):
                return alt
            # 最后尝试包外的原路径（宽松兼容）
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            alt_sprites_dir = os.path.join(parent_dir, "lib", "Weather_landscape", "sprite")
            if os.path.exists(alt_sprites_dir):
                return alt_sprites_dir
            # 未找到时返回首选路径（调用处会打印警告/失败）
            return sprites_dir
        return sprites_dir

    SPRITES_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sprite"))

    @staticmethod
    def my_bezier_func(t, d0, d1, d2, d3):
        return (1 - t) * ((1 - t) * ((1 - t) * d0 + t * d1) + t * ((1 - t) * d1 + t * d2)) + t * ((1 - t) * ((1 - t) * d1 + t * d2) + t * ((1 - t) * d2 + t * d3))

    def my_bezier(self, x, xa, ya, xb, yb):
        xc = (xb + xa) / 2.0
        d = xb - xa
        t = float(x - xa) / float(d)
        y = WeatherDrawer.my_bezier_func(t, ya, ya, yb, yb)
        return int(y)

    def __init__(self):
        pass

    def time_diff_to_pixels(self, dt):
        ds = dt.total_seconds()
        seconds_per_pixel = (WeatherData.FORECAST_PERIOD_HOURS * 60 * 60) / WeatherDrawer.XSTEP
        return int(ds / seconds_per_pixel)

    def deg_to_pix(self, t):
        n = (t - self.tmin) / self.degree_per_pixel
        y = self.ypos + self.YSTEP - int(n)
        return y

    def block_range(self, tline, x0, x1):
        for x in range(x0, x1):
            if x < len(tline):
                tline[x] = Sprites.DISABLED

    def draw_temperature(self, f, x, y, sprite):
        temp = f['temp'] if f['is_celsius'] else f['temp_fahrenheit']
        if f['is_celsius']:
            sprite.DrawInt(temp, x, y + 10, True, 2)
        else:
            sprite.DrawInt(temp, x, y + 10, False, 1)

    def draw_weather(self, weather_data):
        img = Image.new('P', (self.IMAGE_WIDTH, self.IMAGE_HEIGHT), color=1)
        palette = [0, 0, 0, 255, 255, 255, 255, 0, 0]
        for i in range(3, 256):
            palette.extend([0, 0, 0])
        img.putpalette(palette)

        sprites_dir = self.ensure_sprites_dir()
        sprite = Sprites(sprites_dir, img)

        self.pic_height = self.IMAGE_HEIGHT
        self.pic_width = self.IMAGE_WIDTH
        self.ypos = self.DRAWOFFSET

        n_forecast = ((self.pic_width - self.XSTART) / self.XSTEP)
        max_time = datetime.datetime.now() + datetime.timedelta(hours=WeatherData.FORECAST_PERIOD_HOURS * n_forecast)

        (self.tmin, self.tmax) = weather_data.get_temp_range(max_time)
        self.temp_range = self.tmax - self.tmin

        if self.temp_range < self.YSTEP:
            self.degree_per_pixel = self.DEFAULT_DEGREE_PER_PIXEL
        else:
            self.degree_per_pixel = self.temp_range / float(self.YSTEP)

        xpos = 0
        tline = [0] * (self.pic_width + self.XSTEP * 2)

        f = weather_data.get_current()
        old_temp = f['temp']
        old_y = self.deg_to_pix(old_temp)

        for i in range(self.XSTART):
            tline[i] = old_y

        y_clouds = int(self.ypos - self.YSTEP / 2)
        sprite.Draw("house", 0, xpos, old_y)

        curr_hpa = f['pressure']
        smoke_angle_deg = ((curr_hpa - weather_data.pressure_min) / (weather_data.pressure_max - weather_data.pressure_min)) * 85 + 5

        if smoke_angle_deg < 0:
            smoke_angle_deg = 0
        if smoke_angle_deg > 90:
            smoke_angle_deg = 90

        sprite.DrawSmoke(xpos + 21, self.pic_height - old_y + 23, smoke_angle_deg)
        self.draw_temperature(f, xpos + 8, old_y, sprite)
        sprite.DrawCloud(f['clouds'], xpos, y_clouds, self.XSTART, self.YSTEP / 2)
        sprite.DrawRain(f['rain'], xpos, y_clouds, self.XSTART, tline)
        sprite.DrawSnow(f['snow'], xpos, y_clouds, self.XSTART, tline)

        t = datetime.datetime.now()
        dt = datetime.timedelta(hours=WeatherData.FORECAST_PERIOD_HOURS)
        tf = t

        x0 = int(self.XSTART)
        xpos = x0
        n_forecast = int(n_forecast)

        n = int((self.XSTEP - self.XFLAT) / 2)
        for i in range(n_forecast + 1):
            f = weather_data.get_forecast_at_time(tf)
            if f is None:
                continue
            new_temp = f['temp']
            new_y = self.deg_to_pix(new_temp)
            for i in range(n):
                if xpos + i < len(tline):
                    tline[xpos + i] = self.my_bezier(xpos + i, xpos, old_y, xpos + n, new_y)
            for i in range(self.XFLAT):
                if int(xpos + i + n) < len(tline):
                    tline[int(xpos + i + n)] = new_y
            xpos += n + self.XFLAT
            n = (self.XSTEP - self.XFLAT)
            old_temp = new_temp
            old_y = new_y
            tf += dt

        # Fix: 填充 tline 右侧未赋值的部分，使用最后一个 old_y（参考 Components/250.py 的修复）
        for x in range(xpos, int(self.pic_width)):
            if x < len(tline):
                tline[x] = old_y

        tline0 = tline.copy()
        self.block_range(tline, 0, x0)

        sun_calc = SunCalculator(weather_data.lat, weather_data.lon)
        tf = t
        xpos = self.XSTART
        obj_counter = 0

        for i in range(n_forecast + 1):
            f = weather_data.get_forecast_at_time(tf)
            if f is None:
                continue
            t_sunrise = sun_calc.sunrise(tf)
            t_sunset = sun_calc.sunset(tf)
            t_noon = datetime.datetime(tf.year, tf.month, tf.day, 12, 0, 0, 0)
            t_midn = datetime.datetime(tf.year, tf.month, tf.day, 0, 0, 0, 0) + datetime.timedelta(days=1)
            y_moon = self.ypos - self.YSTEP * 5 / 8

            if (tf <= t_sunrise) and (tf + dt > t_sunrise):
                dx = self.time_diff_to_pixels(t_sunrise - tf) - self.XSTEP / 2
                sprite.Draw("sun", 0, xpos + dx, y_moon)
                obj_counter += 1
                if obj_counter == 2:
                    break

            if (tf <= t_sunset) and (tf + dt > t_sunset):
                dx = self.time_diff_to_pixels(t_sunset - tf) - self.XSTEP / 2
                sprite.Draw("moon", 0, xpos + dx, y_moon)
                obj_counter += 1
                if obj_counter == 2:
                    break

            if (tf <= t_noon) and (tf + dt > t_noon):
                dx = self.time_diff_to_pixels(t_noon - tf) - self.XSTEP / 2
                ix = int(xpos + dx)
                if ix < len(tline):
                    sprite.Draw("flower", 1, ix, tline[ix] + 1)
                    self.block_range(tline, ix - self.FLOWER_LEFT_PX, ix + self.FLOWER_RIGHT_PX)

            if (tf <= t_midn) and (tf + dt > t_midn):
                dx = self.time_diff_to_pixels(t_midn - tf) - self.XSTEP / 2
                ix = int(xpos + dx)
                if ix < len(tline):
                    sprite.Draw("flower", 0, ix, tline[ix] + 1)
                    self.block_range(tline, ix - self.FLOWER_LEFT_PX, ix + self.FLOWER_RIGHT_PX)

            xpos += self.XSTEP
            tf += dt

        is_tmin_printed = False
        is_tmax_printed = False
        tf = t
        xpos = self.XSTART
        n = int((self.XSTEP - self.XFLAT) / 2)
        f_used = []

        for i in range(n_forecast + 1):
            f = weather_data.get_forecast_at_time(tf)
            if f is None:
                continue
            dx = self.time_diff_to_pixels(f['time'] - tf) - self.XSTEP / 2
            ix = int(xpos + dx)
            y_clouds = int(self.ypos - self.YSTEP / 2)
            if (f['temp'] == self.tmin) and (not is_tmin_printed):
                if xpos + n < len(tline0):
                    self.draw_temperature(f, xpos + n, tline0[xpos + n], sprite)
                    is_tmin_printed = True
            if (f['temp'] == self.tmax) and (not is_tmax_printed):
                if xpos + n < len(tline0):
                    self.draw_temperature(f, xpos + n, tline0[xpos + n], sprite)
                    is_tmax_printed = True
            if f not in f_used:
                sprite.DrawWind(f['windspeed'], f['winddeg'], ix, tline)
                sprite.DrawCloud(f['clouds'], ix, y_clouds, self.XSTEP, self.YSTEP / 2)
                sprite.DrawRain(f['rain'], ix, y_clouds, self.XSTEP, tline0)
                sprite.DrawSnow(f['snow'], ix, y_clouds, self.XSTEP, tline0)
                f_used.append(f)
            xpos += self.XSTEP
            tf += dt

        for x in range(self.pic_width):
            if x < len(tline0) and tline0[x] < self.pic_height:
                sprite.Dot(x, tline0[x], Sprites.BLACK)

        # 返回单通道图像，交由 finalize_image_common 处理
        return img
