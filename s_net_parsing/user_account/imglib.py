from PIL import Image


def resize_image(avatar, size=(380, 500)):
    image = Image.open(avatar.path)
    image.resize(size, Image.ANTIALIAS).save(avatar.path, 'JPEG', quality=80)
