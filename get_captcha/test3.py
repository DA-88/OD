from preprocess_img import PreprocessImage
import os

# im = PreprocessImage()
# im.ImgLoad("C:\\Users\\QQ\\Desktop\\OD\\pb_captcha_images\\0\\114.bmp")
# i = 0
# while i <= 5:
#     im.save_digit(number=i, path=f"C:\\Users\\QQ\\Desktop\\OD\\pb_captcha_images\\unsorted\\{i}\\")
#     i += 1


for f in os.walk('C:\\Users\\QQ\\Desktop\\OD\\pb_captcha_images\\0'):
    for ff in f[2]:
        im = PreprocessImage()
        try:
            im.ImgLoad(f"{f[0]}\\{ff}")
            i = 0
            while i <= 5:
                im.save_digit(number=i, path=f"C:\\Users\\QQ\\Desktop\\OD\\pb_captcha_images\\unsorted\\{i}\\")
                i += 1
            print(ff)
        except:
            pass