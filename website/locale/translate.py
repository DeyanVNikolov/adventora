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
            po.save(file)
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


def defuzzier():
    # run this command 'msgattrib --clear-fuzzy --empty -o locale/bg/LC_MESSAGES/django.po locale/bg/LC_MESSAGES/django.po'

    import subprocess
    import os
    import sys
    import polib

    for file in os.listdir("C:/Users/Deyan/Desktop/adventora/website/locale/"):
        # if directory

        if os.path.isdir("C:/Users/Deyan/Desktop/adventora/website/locale/" + file):
            for file2 in os.listdir("C:/Users/Deyan/Desktop/adventora/website/locale/" + file):
                if os.path.isdir("C:/Users/Deyan/Desktop/adventora/website/locale/" + file + "/" + file2):
                    for file3 in os.listdir("C:/Users/Deyan/Desktop/adventora/website/locale/" + file + "/" + file2):
                        if file3.endswith(".po"):
                            subprocess.call(
                                "msgattrib --clear-fuzzy --empty -o C:/Users/Deyan/Desktop/adventora/website/locale/" + file + "/" + file2 + "/" + file3 + " C:/Users/Deyan/Desktop/adventora/website/locale/" + file + "/" + file2 + "/" + file3,
                                shell=True
                            )
                            print("Defuzzied " + file3)
                if file2.endswith(".po"):
                    subprocess.call(
                        "msgattrib --clear-fuzzy --empty -o C:/Users/Deyan/Desktop/adventora/website/locale/" + file + "/" + file2 + " C:/Users/Deyan/Desktop/adventora/website/locale/" + file + "/" + file2,
                        shell=True
                    )
                    print("Defuzzied " + file2)
        if file.endswith(".po"):
            subprocess.call("msgattrib --clear-fuzzy --empty -o C:/Users/Deyan/Desktop/adventora/website/locale/" + file + " C:/Users/Deyan/Desktop/adventora/website/locale/" + file, shell=True)
            print("Defuzzied " + file)


def compilemessages():
    import subprocess
    script_directory = os.path.dirname(os.path.abspath(__file__))
    website_directory = os.path.join(script_directory, '..')
    os.chdir(website_directory)
    subprocess.call("python manage.py compilemessages", shell=True)


def generatemessages():
    import subprocess
    script_directory = os.path.dirname(os.path.abspath(__file__))
    website_directory = os.path.join(script_directory, '..')
    os.chdir(website_directory)
    subprocess.call("python manage.py makemessages -a", shell=True)


def onlycompilemessages():
    compilemessages()


def onlygenerate():
    generatemessages()


def all():
    current_unix = int(time.time())
    print("-----------------------------")
    print("Starting...")
    print("-----------------------------")
    print("Done")
    print("-----------------------------")
    print("Begin translation...")
    print("Български")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/bg/", "en", "bg")
    print("-----------------------------")
    print("Deutsch")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/de/", "en", "de")
    print("-----------------------------")
    print("Español")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/es/", "en", "es")
    print("-----------------------------")
    print("Français")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/fr/", "en", "fr")
    print("-----------------------------")
    print("Italiano")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/it/", "en", "it")
    print("-----------------------------")
    print("Português")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/pt/", "en", "pt")
    print("-----------------------------")
    print("Русский")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/ru/", "en", "ru")
    print("-----------------------------")
    print("Українська")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/uk/", "en", "uk")
    print("-----------------------------")
    print("Türkçe")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/tr/", "en", "tr")
    print("-----------------------------")
    print("Japanese")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/ja/", "en", "ja")
    print("-----------------------------")
    print("Czech")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/cs/", "en", "cs")
    print("-----------------------------")
    print("Danish")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/da/", "en", "da")
    print("-----------------------------")
    print("Greek")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/el/", "en", "el")
    print("-----------------------------")
    print("Finnish")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/fi/", "en", "fi")
    print("-----------------------------")
    print("Hungarian")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/hu/", "en", "hu")
    print("-----------------------------")
    print("Icelandic")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/is/", "en", "is")
    print("-----------------------------")
    print("Croatian")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/hr/", "en", "hr")
    print("-----------------------------")
    print("Macedonian")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/mk/", "en", "mk")
    print("-----------------------------")
    print("Serbian")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/sr/", "en", "sr")
    print("-----------------------------")
    print("Korean")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/ko/", "en", "ko")
    print("-----------------------------")
    print("Dutch")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/nl/", "en", "nl")
    print("-----------------------------")
    print("Norwegian")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/no/", "en", "no")
    print("-----------------------------")
    print("Swedish")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/sv/", "en", "sv")
    print("-----------------------------")
    print("Romanian")
    translate_folder("C:/Users/Deyan/Desktop/adventora/website/locale/ro/", "en", "ro")
    print("-----------------------------")
    print("Finish translation...")
    print("Done")
    print("-----------------------------")
    print("Compiling messages...")
    print("-----------------------------")
    compilemessages()
    print("Done")
    print("-----------------------------")
    new_unix = int(time.time())
    elapsed = time.strftime("%H:%M:%S", time.gmtime(new_unix - current_unix))
    print("Completed in " + elapsed)
    print("-----------------------------")
    print("Program now exiting...")
    exit(0)


all()
