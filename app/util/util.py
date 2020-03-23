from app.config import appconfig


def uniqueName(self, base_name):
    return time.strftime('%Y%m%d%H%M%S', time.localtime()) + base_name


def isImageByExtension(self, image_name):
    return '.' in image_name and image_name.rsplit('.', 1)[1].lower() in appconfig.IMAGE_EXTENSIONS
