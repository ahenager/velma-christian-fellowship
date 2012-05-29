from datetime import datetime
import os
import re
import dateutil.parser as dparser
import shutil
import settings
from UserDict import UserDict
from models import AudioMedia, Category

def stripnulls(data):
    return data.replace("\00", "").strip()

class FileInfo(UserDict):
    def __init__(self, filename=None):
        UserDict.__init__(self)
        self["name"] = filename

class MP3FileInfo(FileInfo):
    tagDataMap = {"title"   : (  3,  33, stripnulls),
                  "artist"  : ( 33,  63, stripnulls),
                  "album"   : ( 63,  93, stripnulls),
                  "year"    : ( 93,  97, stripnulls),
                  "comment" : ( 97, 126, stripnulls),
                  "genre"   : (127, 128, ord)}

    def __parse(self, filename):
        self.clear()
        try:
            fsock = open(filename, "rb", 0)
            try:
                fsock.seek(-128, 2)
                tagdata = fsock.read(128)
            finally:
                fsock.close()
            if tagdata[:3] == "TAG":
                for tag, (start, end, parseFunc) in self.tagDataMap.items():
                    self[tag] = parseFunc(tagdata[start:end])
        except IOError:
            pass

    def __setitem__(self, key, item):
        if key == "name" and item:
            self.__parse(item)
        FileInfo.__setitem__(self, key, item)

def do_import():
    source = settings.MEDIA_IMPORT_DIRECTORY + '/'
    dest = settings.MEDIA_ROOT + '/audio/'
    tags = dict([(c.name.lower(), c) for c in Category.objects.all().order_by('name')])
    messages = []

    listing = os.listdir(source)
    messages.append('Beginning import of ' + str(listing.count()) + ' files.')
    for infile in listing:
        messages.append('Importing ' + infile)
        info = dict()
        def_title = infile.replace('.mp3', '')
        def_title = re.sub(r'([0-9][0-9])([0-9][0-9])([0-9][0-9])', r'\1-\2-\3', def_title)
        try:
            info = MP3FileInfo(source + infile)
            info['date'] = dparser.parse(def_title,fuzzy=True)
        except ValueError:
            messages.append('Did not get a date on ' + infile)
        except:
            messages.append('Error reading mp3 info for ' + infile)

        if os.path.isfile(dest + infile):
            shutil.move(source + infile, dest + infile)
            messages.append('File ' + infile + ' already on server, will not update indexing information.')
            continue

        shutil.move(source + infile, dest + infile)

        media = AudioMedia()
        media.name = info.get('title', def_title)
        media.description = info.get('artist', '') + '\n' + info.get('comments', '')
        media.date = info.get('date', datetime.now())
        media.file = 'audio/' + infile
        media.save()

        artist_tag = tags.get(info.get('artist', '').lower())
        if artist_tag is not None:
            media.categories.add(artist_tag)

        year = info.get('year', '')
        year_tag = tags.get(year.lower())
        if year_tag is not None:
            media.categories.add(year_tag)
        elif year != '':
            new_tag = Category()
            new_tag.name = year
            new_tag.save()
            tags[year.lower()] = new_tag
            media.categories.add(new_tag)

        media.save()

    messages.append('Done.')
    return messages