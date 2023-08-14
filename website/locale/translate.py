# automatic .po file translation

import os
import sys
import polib
import requests
import json
import time
import re


def translate(text, source, target):
    url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=" + \
        source + "&tl=" + target + "&dt=t&q=" + text
    r = requests.get(url)
    r = json.loads(r.text)
    return r[0][0][0]


def translate_file(file, source, target):
    po = polib.pofile(file)
    for entry in po:
        if entry.msgstr == "":
            entry.msgstr = translate(entry.msgid, source, target)
            print(entry.msgid + " -> " + entry.msgstr)
            time.sleep(1)
    po.save(file)


def translate_folder(folder, source, target):
    # browse all files in folder and SUBFOLDERS
    for file in os.listdir(folder):
        if os.path.isdir(folder + "\\" + file):
            translate_folder(folder + "\\" + file, source, target)
        if file.endswith(".po"):
            translate_file(folder + "\\" + file, source, target)
            print("Translated " + file)

    ('bg', 'Bulgarian'),
    ('en', 'English'),
    ('de', 'German'),
    ('cs', 'Czech'),
    ('da', 'Danish'),
    ('el', 'Greek'),
    ('fi', 'Finnish'),
    ('hu', 'Hungarian'),
    ('is', 'Icelandic'),
    ('hr', 'Croatian'),
    ('mk', 'Macedonian'),
    ('sr', 'Serbian'),
    ('ko', 'Korean'),
    ('nl', 'Dutch'),
    ('no', 'Norwegian'),
    ('sv', 'Swedish'),
    ('ru', 'Russian'),
    ('uk', 'Ukrainian'),
    ('fr', 'French'),
    ('es', 'Spanish'),
    ('it', 'Italian'),
    ('pt', 'Portuguese'),
    ('tr', 'Turkish'),
    ('ja', 'Japanese'),

current_unix = int(time.time())
print("-----------------------------")
print("Български")
translate_folder("A:/Repos/adventora/website/locale/bg/", "en", "bg")
print("-----------------------------")
print("Deutsch")
translate_folder("A:/Repos/adventora/website/locale/de/", "en", "de")
print("-----------------------------")
print("Español")
translate_folder("A:/Repos/adventora/website/locale/es/", "en", "es")
print("-----------------------------")
print("Français")
translate_folder("A:/Repos/adventora/website/locale/fr/", "en", "fr")
print("-----------------------------")
print("Italiano")
translate_folder("A:/Repos/adventora/website/locale/it/", "en", "it")
print("-----------------------------")
print("Português")
translate_folder("A:/Repos/adventora/website/locale/pt/", "en", "pt")
print("-----------------------------")
print("Русский")
translate_folder("A:/Repos/adventora/website/locale/ru/", "en", "ru")
print("-----------------------------")
print("Українська")
translate_folder("A:/Repos/adventora/website/locale/uk/", "en", "uk")
print("-----------------------------")
print("Türkçe")
translate_folder("A:/Repos/adventora/website/locale/tr/", "en", "tr")
print("-----------------------------")
print("Japanese")
translate_folder("A:/Repos/adventora/website/locale/ja/", "en", "ja")
print("-----------------------------")
print("Czech")
translate_folder("A:/Repos/adventora/website/locale/cs/", "en", "cs")
print("-----------------------------")
print("Danish")
translate_folder("A:/Repos/adventora/website/locale/da/", "en", "da")
print("-----------------------------")
print("Greek")
translate_folder("A:/Repos/adventora/website/locale/el/", "en", "el")
print("-----------------------------")
print("Finnish")
translate_folder("A:/Repos/adventora/website/locale/fi/", "en", "fi")
print("-----------------------------")
print("Hungarian")
translate_folder("A:/Repos/adventora/website/locale/hu/", "en", "hu")
print("-----------------------------")
print("Icelandic")
translate_folder("A:/Repos/adventora/website/locale/is/", "en", "is")
print("-----------------------------")
print("Croatian")
translate_folder("A:/Repos/adventora/website/locale/hr/", "en", "hr")
print("-----------------------------")
print("Macedonian")
translate_folder("A:/Repos/adventora/website/locale/mk/", "en", "mk")
print("-----------------------------")
print("Serbian")
translate_folder("A:/Repos/adventora/website/locale/sr/", "en", "sr")
print("-----------------------------")
print("Korean")
translate_folder("A:/Repos/adventora/website/locale/ko/", "en", "ko")
print("-----------------------------")
print("Dutch")
translate_folder("A:/Repos/adventora/website/locale/nl/", "en", "nl")
print("-----------------------------")
print("Norwegian")
translate_folder("A:/Repos/adventora/website/locale/no/", "en", "no")
print("-----------------------------")
print("Swedish")
translate_folder("A:/Repos/adventora/website/locale/sv/", "en", "sv")
print("-----------------------------")
print("Done")
new_unix = int(time.time())
elapsed = time.strftime("%H:%M:%S", time.gmtime(new_unix - current_unix))
print("Completed in " + elapsed)