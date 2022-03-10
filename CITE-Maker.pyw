#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python GUI zur Erstellung von .bib Einträgen
# 2021 von Michael Gräf DD4MG
#
# +Update: Automatisches einfügen in .bib-Datei implementiert
#

DEBUG = False
_TIMEOUT_=100


from datetime import date
today = date.today()

import PySimpleGUI as sg
import pyperclip
import os


def create_item(type,tag,author,titel,jahr,puplisher,isbn,urldate,url):


    datastring="@"+type.upper()+"{"+tag
    if(author!=""):
        datastring+=",\n\tAUTHOR={"+author+"}"
    if (titel != ""):
        datastring += ",\n\tTITLE={" + titel + "}"
    if (jahr != ""):
        datastring += ",\n\tYEAR={" + jahr + "}"
    if (puplisher != ""):
        datastring += ",\n\tPUPLISHER={" + puplisher + "}"
    if (isbn != ""):
        datastring += ",\n\tISBN={" + isbn + "}"
    if (urldate != ""):
        datastring += ",\n\tURLDATE={" + urldate + "}"
    if (url != ""):
        datastring += ",\n\tURL={" + url + "}"

    datastring+="\n}"

    return datastring

type_menu=['book', 'paper', 'website', 'manual', 'online']
layout = [
        [sg.Frame(layout=[  [sg.Text("Speicherort: "), sg.Input(disabled=True,key='file_path'), sg.FileBrowse("Wählen")]    ]  , title='lokale .bib-Datei')],

          [sg.Frame(layout=[
            [sg.Text('Quellenart:', size=(25, 1)),                  sg.OptionMenu(type_menu,"book", size=(31, 1),key="bib_type")],
            [sg.Text('.BIB Bezeichnung', size=(25, 1)),             sg.In('book:', size=(36, 1), disabled=False, key="bib_tag")],
            [sg.Text('Author:', size=(25, 1)),                      sg.In('', size=(36, 1), key="bib_author")],
            [sg.Text('Titel:', size=(25, 1)),                       sg.In('', size=(36, 1), key="bib_titel")],
            [sg.Text('Jahr der Veröffentlichung:', size=(25, 1)),   sg.In('', size=(36, 1),  key="bib_jahr")],
            [sg.Text('Verlag:', size=(25, 1)),                      sg.In('', size=(36, 1), key="bib_puplisher")],
            [sg.Text('ISBN:', size=(25, 1)),                        sg.In('', size=(36, 1), key="bib_isbn")],
            [sg.Text('zuletzt besucht (YYYY-MM-DD):', size=(25, 1)),sg.In(today, size=(22, 1), key="bib_urldate"), sg.CalendarButton('Kalender', no_titlebar=True, size=(9, 1),format=('%Y-%m-%d'), target='bib_urldate', pad=None, font=('MS Sans Serif', 10, 'bold'))],
            [sg.Text('URL:', size=(25, 1)),                         sg.In('', size=(36, 1), key="bib_url")]
          ], title='Literaturdaten')],
            [sg.Text('', size=(25, 1)),                             sg.Button('Eingabe löschen', size=(25, 1),key="bib_clear")],
         [sg.Multiline('', size=(66, 9), key="cite_window",disabled=True)],

        [sg.Text('CITE Maker von mg1t', size=(18, 1)),sg.Button('in Datei speichern', size=(18, 1),key="bib_save"),sg.Button('In Ablage Kopieren', size=(18, 1),key="bib_copy")]

          ]  # ende layout

# Create the window
window = sg.Window("CITE Maker", layout, return_keyboard_events=True, element_justification='c')

# notwendige Variablen
old_type="book"
old_path=''
valid_file=False

while True:
    event, values = window.Read(timeout=_TIMEOUT_)
    if event in (sg.WIN_CLOSED, 'Exit'):  # ALWAYS give a way out of program
        break

    if event=="bib_type":
        window.Element("bib_tag").Update(values["bib_type"])

    if event=="bib_copy":
        pyperclip.copy(values["cite_window"])

    if event=="bib_clear":
        window.Element("bib_tag").Update(value=values["bib_type"]+':')
        window.Element("bib_author").Update(value='')
        window.Element("bib_titel").Update(value='')
        window.Element("bib_jahr").Update(value='')
        window.Element("bib_puplisher").Update(value='')
        window.Element("bib_isbn").Update(value='')
        window.Element("bib_urldate").Update(value=today)
        window.Element("bib_url").Update(value='')

    # Wenn Button "in datei speichern" geklickt wurde
    if event=="bib_save":
        if(valid_file):
            file_path=os.path.normpath(new_path)
            with open(file_path, 'a') as file:
                file.write(values["cite_window"])
        else:
            sg.popup('Die ausgewählte Datei ist keine gültige Datei!', title='Fehler', background_color='red', keep_on_top=True, )
        
        
    #if event!="__TIMEOUT__":
    window.Element("cite_window").Update(create_item(values["bib_type"],
                                                     values["bib_tag"],
                                                     values["bib_author"],
                                                     values["bib_titel"],
                                                     values["bib_jahr"],
                                                     values["bib_puplisher"],
                                                     values["bib_isbn"],
                                                     values["bib_urldate"],
                                                     values["bib_url"]))

    #Check ob BIB-Type geändert wurde
    if (old_type != values["bib_type"]):
        new_type=values["bib_type"]+":"
        window.Element("bib_tag").Update(value=new_type)
    old_type=values["bib_type"]

    #Check ob eine Datei gewählt wurde
    if (old_path != values["file_path"]):
        new_path=values["file_path"]
        #Check der Datei
        if(new_path.find('.bib')!=-1):
            valid_file=True
            print(new_path.find('.bib'))
            print('ist ne .bib Datei')
        else:
            valid_file=False
            sg.popup('Die gewählte Datei ist keine .bib-Datei!' ,title='Fehler',background_color = 'red',keep_on_top = True,)

        print('----> Neuer Dateipfad')
    old_path=values["file_path"]

    if(DEBUG):
        print(event)


window.close()
