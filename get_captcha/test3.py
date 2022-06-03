from preprocess_img import PreprocessImage
import os

for f in os.walk('C:\\Users\\QQ\\Desktop\\OD\\pb_captcha_images\\0'):
    for ff in f[2]:
        im = PreprocessImage()
        im.ImgLoad(f"{f[0]}\\{ff}")
        i = 0
        while i <= 5:
            im.save_digit(number=i, path=f"C:\\Users\\QQ\\Desktop\\OD\\pb_captcha_images\\unsorted\\{i}\\")
            i += 1
        print(ff)

# im = PreprocessImage()
# im.ImgLoad(f"C:\\Users\\DQ\\Desktop\\OD\\pb_captcha_images\\0\\4.bmp")
#
# i = 0
# while i <= 5:
#     im.save_digit(number=i, path=f"C:\\Users\\DQ\\Desktop\\OD\\pb_captcha_images\\test\\")
#     i += 1