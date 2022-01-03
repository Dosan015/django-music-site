#-*-coding:utf-8-*-
from config import settings
import os, uuid, eyed3, time

from django.template.defaultfilters import slugify



def get_file_upload_path(instance, filename):
    if settings.RENAME_FILE_TO_UUID4:
        # set filename as random string
        ext = filename.split('.')[-1]
        uuid_filename = '{}'.format(uuid.uuid4().hex)
        return os.path.join('mp3/', "%s.%s" % (uuid_filename, ext.lower()))

    original_filename = instance.full_name_slug
    return os.path.join('mp3/', "%s.mp3" % original_filename) 

def get_cover_upload_path(instance, filename):
    if settings.RENAME_FILE_TO_UUID4:
        # set filename as random string
        ext = filename.split('.')[-1]
        uuid_filename = '{}'.format(uuid.uuid4().hex)
        return os.path.join('img/', "%s.%s" % (uuid_filename, ext.lower()))
    ext = filename.split('.')[-1]
    original_filename = filename.replace('.'+ext, '')

    return os.path.join('img/', "%s.%s" % (slugify(original_filename), ext.lower()))

def mp3_tag_edit(file, title, singer, img):
    audio_file = eyed3.load(file.temporary_file_path())
    audio_file.tag.clear()
    audio_file.tag.artist = singer.__str__()
    audio_file.tag.title = title
    audio_file.tag.album = settings.DEFAULT_TAG_ALBUM_NAME
    audio_file.tag.album_artist = settings.DEFAULT_TAG_ALBUM_ARTIST
    audio_file.tag.comments.set(settings.DEFAULT_TAG_COMMENT)
    imgdata = open(img, "rb")
    audio_file.tag.images.set(3, imgdata.read(),u"music",img_url=None)
    imgdata.close()
    audio_file.tag.save(encoding='utf-8',version = eyed3.id3.ID3_V2_3)
            
    return time.strftime('%M:%S', time.gmtime(audio_file.info.time_secs))

