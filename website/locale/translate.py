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
print("Done")
new_unix = int(time.time())
elapsed = time.strftime("%H:%M:%S", time.gmtime(new_unix - current_unix))
print("Completed in " + elapsed)