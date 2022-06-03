from PIL import Image
import numpy as np
from hashlib import sha1
import sys
sys.setrecursionlimit(1500)

class PreprocessImage():
    img = None
    img_a = None
    digits = []
    iter = 0

    def ImgLoad(self, path):
        self.img = Image.open(path)
        self.img_a = np.asarray(self.img)
        self.clean_image()

        i = 0
        while i <= 5:
            self.digits.append({"c": None, "x_min": 0, "x_max": 0, "y_min": 0, "y_max": 0, "pixelCount": 0,
                                "x_start": 0, "y_start": 0, "start_point_found": False})
            i+=1

        i = 0
        while i <= 5:
            self.digits[i] = {"c": None, "x_min": 0, "x_max": 0, "y_min": 0, "y_max": 0, "pixelCount": 0,
                                    "x_start": 0, "y_start": 0, "start_point_found": False}
            self.iter = i
            self.get_digit()
            if self.digits[i]["start_point_found"]:
                self.digits[i]['x_min'] = self.digits[i]['x_start']
                self.digits[i]['x_max'] = self.digits[i]['x_start']
                self.digits[i]['y_min'] = self.digits[i]['y_start']
                self.digits[i]['y_max'] = self.digits[i]['y_start']
                sys.setrecursionlimit(3000)
                self.plot_area(self.digits[i]["y_start"], self.digits[i]["x_start"])
                sys.setrecursionlimit(1000)

                # Если случайно захватили 2 цифры - вторую половину красим в черный, пересчитываем pixelCount и сужаем фрейм
                if (self.digits[i]['x_max'] - self.digits[i]['x_min']) > 35:
                    x_limit = self.digits[i]['x_min'] + ((self.digits[i]['x_max'] - self.digits[i]['x_min']) // 2)

                    self.digits[i]['pixelCount'] = 0
                    for iy, y in enumerate(self.img_a):
                        for ix, x in enumerate(y):
                            if ix > x_limit:
                                if self.img_a[iy][ix][0] == 100:
                                    self.img_a[iy][ix][0] = 0
                                    self.img_a[iy][ix][1] = 0
                                    self.img_a[iy][ix][2] = 0
                            else:
                                if self.img_a[iy][ix][0] == 100:
                                    self.digits[i]['pixelCount'] += 1
                    self.digits[i]['x_max'] = x_limit

                # im = Image.fromarray(self.img_a)
                # im.save('C:\\Users\\DQ\\Desktop\\OD\\pb_captcha_images\\test_1.bmp')
                if self.digits[i]['pixelCount'] > 250:
                    self.copy_digit()
                else: # Ложное срабатывание
                    i -= 1
                # Затираем закрашенную область
                # im = Image.fromarray(self.img_a)
                # im.save('C:\\Users\\DQ\\Desktop\\OD\\pb_captcha_images\\test_1.bmp')
                self.clean_plotted()
                # im = Image.fromarray(self.img_a)
                # im.save('C:\\Users\\DQ\\Desktop\\OD\\pb_captcha_images\\test_2.bmp')
            else: # Если стартовая точка не найдена - выходим из цикла
                break
            i += 1

    def clean_image(self):
        for iy, y in enumerate(self.img_a):
            for ix, x in enumerate(y):
                if self.img_a[iy][ix][0] > 100 and self.img_a[iy][ix][1] > 100 and self.img_a[iy][ix][2] > 100:
                    self.img_a[iy][ix][0], self.img_a[iy][ix][1], self.img_a[iy][ix][2] = 255, 255, 255
                # Чистим полосы
                if self.img_a[iy][ix][0] >= 27 and self.img_a[iy][ix][0] <= 97 and \
                    self.img_a[iy][ix][1] >= 52 and self.img_a[iy][ix][1] <= 104 and \
                    self.img_a[iy][ix][2] >= 48 and self.img_a[iy][ix][2] <= 117:
                    self.img_a[iy][ix][0], self.img_a[iy][ix][1], self.img_a[iy][ix][2] = 255, 255, 255
                # Все, что осталось, делаем одного цвета
                if not (self.img_a[iy][ix][0] == 255 and self.img_a[iy][ix][1] == 255 and self.img_a[iy][ix][2] == 255):
                    self.img_a[iy][ix][0], self.img_a[iy][ix][1], self.img_a[iy][ix][2] = 0, 0, 0

    def get_digit(self):
        # Вычисляем точку старта
        a = self.img_a
        for ix, x in enumerate(a[0]):
            if not self.digits[self.iter]["start_point_found"]:
                for iy, y in enumerate(a):
                    if iy <= 94: # чтобы не уперется в ограничение по высоте
                        # Если 5 пикселей по вертикали черные - старт найден
                        if a[iy][ix][0] == 0 and a[iy+1][ix][0] == 0 and a[iy+2][ix][0] == 0 and \
                            a[iy+3][ix][0] == 0 and a[iy+4][ix][0] == 0:
                                if not self.digits[self.iter]["start_point_found"]:
                                    self.digits[self.iter]["start_point_found"] = True
                                    self.digits[self.iter]["x_start"] = ix
                                    self.digits[self.iter]["y_start"] = iy + 2
                                    break
            else:
                break

    def plot_area(self, y, x):
        #Если пиксель черный - работаем дальше, иначе ничего не делаем
        if self.img_a[y][x][0] == 0:
            self.img_a[y][x][0] = 100 # Красим пиксель
            self.digits[self.iter]['pixelCount'] += 1 # Считаем количество пикселей
            # Определяем границы области с цифрой
            if x < self.digits[self.iter]['x_min']: self.digits[self.iter]['x_min'] = x
            if x > self.digits[self.iter]['x_max']: self.digits[self.iter]['x_max'] = x
            if y < self.digits[self.iter]['y_min']: self.digits[self.iter]['y_min'] = y
            if y > self.digits[self.iter]['y_max']: self.digits[self.iter]['y_max'] = y

            # Проверяем соседние пиксели по часовой стрелке
            # 1
            if x > 0 and y > 0:
                if self.img_a[y-1][x-1][0] != 100: self.plot_area(y-1, x-1)
            # 2
            if y > 0:
                if self.img_a[y-1][x][0] != 100: self.plot_area(y-1, x)
            # 3
            if x < 199 and y > 0:
                if self.img_a[y-1][x+1][0] != 100: self.plot_area(y-1, x+1)
            # 4
            if x < 199:
                if self.img_a[y][x+1][0] != 100: self.plot_area(y, x+1)
            # 5
            if x < 199 and y < 99:
                if self.img_a[y+1][x+1][0] != 100: self.plot_area(y+1, x+1)
            # 6
            if y < 99:
                if self.img_a[y + 1][x][0] != 100: self.plot_area(y + 1, x)
            # 7
            if x > 0 and y < 99:
                if self.img_a[y + 1][x - 1][0] != 100: self.plot_area(y + 1, x - 1)
            # 8
            if x > 0:
                if self.img_a[y][x - 1][0] != 100: self.plot_area(y, x - 1)

    def clean_plotted(self):
        for iy, y in enumerate(self.img_a):
            for ix, x in enumerate(y):
                if self.img_a[iy][ix][0] == 100:
                    self.img_a[iy][ix][0] = 255
                    self.img_a[iy][ix][1] = 255
                    self.img_a[iy][ix][2] = 255

    def copy_digit(self):
        area = np.zeros((self.digits[self.iter]['y_max'] - self.digits[self.iter]['y_min'] + 1,
                         self.digits[self.iter]['x_max'] - self.digits[self.iter]['x_min'] + 1))
        y = self.digits[self.iter]['y_min']
        while y <= self.digits[self.iter]['y_max']:
            x = self.digits[self.iter]['x_min']
            while x <= self.digits[self.iter]['x_max']:
                if self.img_a[y][x][0] == 100:
                    area[y - self.digits[self.iter]['y_min']][x - self.digits[self.iter]['x_min']] = 255
                x += 1
            y += 1
        self.digits[self.iter]['c'] = area

    def save_digit(self, number, path):
        if self.digits[number]['c'] is not None:
            im = Image.fromarray(self.digits[number]['c'].astype('uint8'), mode='L')
            hash = sha1(self.digits[number]['c'].astype('uint8')).hexdigest()
            im.save(f"{path}{hash}.bmp")








# test = PreprocessImage()
# test.ImgLoad('C:\\Users\\DQ\\Desktop\\OD\\pb_captcha_images\\full\\000a180b5e977f8fda4a0ba069b1843584c1a2c7.jpg')
# pass
# img = Image.open('C:\\Users\\DQ\\Desktop\\OD\\pb_captcha_images\\full\\000a180b5e977f8fda4a0ba069b1843584c1a2c7.jpg')
#
# a = np.asarray(img)
#
#
#
# clean_image()
# get_digit()
#
# img = Image.open('C:\\Users\\DQ\\Desktop\\OD\\pb_captcha_images\\full\\000a180b5e977f8fda4a0ba069b1843584c1a2c7.jpg')
# a = np.asarray(img)
# im = Image.fromarray(a)
# im.save('C:\\Users\\DQ\\Desktop\\OD\\pb_captcha_images\\test.bmp')