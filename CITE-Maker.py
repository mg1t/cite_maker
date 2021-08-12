#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python GUI zur Erstellung von .bib Einträgen
# 2021 von Michael Gräf DD4MG

_DEBUG_ = True
_TIMEOUT_=100

# pip install pysimplegui
import PySimpleGUI as sg
import pyperclip


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
        datastring += ",\n\turldate={" + urldate + "}"
    if (url != ""):
        datastring += ",\n\turl={" + url + "}"

    datastring+="\n}"

    return datastring

type_menu=['book', 'paper', 'website']
layout = [
          [sg.Frame(layout=[
                [sg.Text('Quellenart:', size=(25, 1)),
                 sg.OptionMenu(type_menu,"book", size=(20, 1),key="bib_type")],
              [sg.Text('.BIB Bezeichnung', size=(25, 1)),
               sg.In('book:', size=(25, 1), disabled=False, key="bib_tag")],
            [sg.Text('Author:', size=(25, 1)),
               sg.In('', size=(25, 1), key="bib_author")],
              [sg.Text('Titel:', size=(25, 1)),
               sg.In('', size=(25, 1), key="bib_titel")],
              [sg.Text('Jahr der Veröffentlichung:', size=(25, 1)),
               sg.In('', size=(25, 1),  key="bib_jahr")],
              [sg.Text('Verlag:', size=(25, 1)),
               sg.In('', size=(25, 1), key="bib_puplisher")],
                [sg.Text('ISBN:', size=(25, 1)),
               sg.In('', size=(25, 1), key="bib_isbn")],
                [sg.Text('zuletzt besucht (YYYY-MM-DD):', size=(25, 1)),
               sg.In('', size=(25, 1), key="bib_urldate")],
                [sg.Text('URL:', size=(25, 1)),
               sg.In('', size=(25, 1), key="bib_url")]
          ], title='Literaturdaten')],

               [sg.Multiline('', size=(55, 9), key="cite_window",disabled=True)],

        [sg.Text('CITE Maker von Michael Gräf', size=(25, 1)),sg.Button('Kopieren!', size=(25, 1),key="bib_copy")]

          ]  # ende layout

# Create the window
window = sg.Window("CITE Maker", layout, return_keyboard_events=True, element_justification='c')
old_type="book"
while True:
    event, values = window.Read(timeout=_TIMEOUT_)
    if event in (sg.WIN_CLOSED, 'Exit'):  # ALWAYS give a way out of program
        break

    if event=="bib_type":
        window.Element("bib_tag").Update(values["bib_type"])

    if event=="bib_copy":
        pyperclip.copy(create_item(values["bib_type"],
                                                    values["bib_tag"],
                                                     values["bib_author"],
                                                     values["bib_titel"],
                                                     values["bib_jahr"],
                                                     values["bib_puplisher"],
                                                     values["bib_isbn"],
                                                     values["bib_urldate"],
                                                     values["bib_url"]))

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
   # print(event)

    if (old_type != values["bib_type"]):
        new_type=values["bib_type"]+":"
        window.Element("bib_tag").Update(value=new_type)
    old_type=values["bib_type"]



window.close()
