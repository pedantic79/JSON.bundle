import os
import json
from dateutil.parser import parse


def Start():
    Log("Starting JSON Agent")


def find_info_json(part):
    directory = os.path.dirname(part)
    Log("find_info_json " + directory + "]")

    i = 0
    while i < 2:
        Log("Searching " + directory)
        path = os.path.join(directory, 'Info.json')
        if os.path.exists(path):
            Log("Found Info.json at: " + path)
            return path
        else:
            directory = os.path.dirname(directory)
            i += 1

    raise FileNotFoundError()


class JSONAgent(Agent.Movies):
    name = 'JSON Metadata'
    languages = [Locale.Language.English]
    primary_provider = False
    persist_stored_files = False
    contributes_to = ['com.plexapp.agents.none']

    def search(self, results, media, lang):
        Log("JSON search: enter")
        try:
            part = media.items[0].parts[0]
            Log("JSON search: [" + part.file + "]")
            find_info_json(part.file)
        except Exception as exp:
            Log("Exception occurred: [" + exp.message + "]")
            return

        results.Append(MetadataSearchResult(id='null', score=100))

    def update(self, metadata, media, lang):
        Log("JSON update: enter")
        part = media.items[0].parts[0]

        try:
            path = find_info_json(part.file)
            basename = os.path.basename(part.file)
            basenameLC = basename.lower()
        except:
            return

        info_full = json.loads(Core.storage.load(path))
        try:
            info = info_full[basenameLC]
            Log("FOUND: [" + basenameLC + "]")
        except Exception as exp:
            Log("Exception occurred: [" + exp.message + "]")
            return

        try:
            metadata.title = info['title']
        except:
            pass

        try:
            metadata.summary = info['summary']
        except:
            pass

        try:
            metadata.year = info['year']
        except:
            pass

        try:
            date_object = parse(info['originally_available_at'])
            metadata.originally_available_at = date_object
            metadata.year = metadata.originally_available_at.year
        except:
            pass

        try:
            metadata.rating = info['rating']
        except:
            pass

        try:
            metadata.content_rating = info['content_rating']
        except:
            pass

        try:
            metadata.studio = info['studio']
        except:
            pass

        try:
            metadata.duration = info['duration']
        except:
            pass

        metadata.directors.clear()

        try:
            for d in info['directors']:
                metadata.directors.add(d)
        except:
            pass

        metadata.genres.clear()

        try:
            for g in info['genres']:
                metadata.genres.add(g)
        except:
            pass

        metadata.roles.clear()

        try:
            for r in info['cast']:
                role = metadata.roles.new()

                try:
                    role.name = r
                except:
                    pass

        except:
            pass

        metadata.collections.clear()

        try:
            for c in info['collections']:
                metadata.collections.add(c)
            metadata.collections.add('InfoJSON')
        except:
            pass
