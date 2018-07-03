#!/usr/bin/env python3

from os import system
import datetime
import pickle
from yattag import Doc, indent

class Note:
    def __init__(self, title, text, place=None):
        self.title = title
        self.text = text
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.place = place

    def __str__(self):
        return "{date} \n{name} \n{text}\n\n".format(date=self.date,\
                                                     name=self.title,\
                                                     text=self.text)

class Manager:
    def __init__(self, filename):
        self.filename = filename
        self.notes = []

        try:
            with open(filename, "rb") as file:
                self.notes = pickle.load(file)
        except:
            print("Can't read file")

    def add_note(self, note):
        self.notes.append(note)

    def view_notes(self):
        if self.notes:
            for note in self.notes:
                print(str(note))
        else:
            print("No notes yet")

        input()

    def read_note(self):
        title = input("Enter title: ")
        text = input("Enter text: ")
        return Note(title, text)

    def print_menu(self):
        system("clear")
        print("Choose mode:")
        print("1.New note")
        print("2.View notes")
        print("3.Exit")

    def save_with_pickle(self):
        with open(self.filename, "wb+") as file:
            pickle.dump(self.notes, file)


class Generator:
    def __init__(self, notes):
        self.doc, self.tag, self.text = Doc().tagtext()
        doc, tag, text = self.doc, self.tag, self.text

        doc.asis("<!DOCTYPE html>")
        with tag("html"):
            with tag("head"):
                with tag("title"):
                    text("Notes App")

                doc.stag("link",
                         href="https://fonts.googleapis.com/css?family=Fjalla+One",
                         rel="stylesheet")

                doc.stag("link", rel="stylesheet", type="text/css", href="style.css")

            with tag("body"):
                with tag("div", ("class", "background")):
                    with tag("h1"):
                            text("Notes App")
                    for note in notes:
                        with tag("div", ("class", "note")):
                            with tag("i", ("class", "date")):
                                text(note.date)

                            doc.stag("br")

                            with tag("b", ("class", "title")):
                                text(note.title)

                            doc.stag("br")

                            with tag("text"):
                                text(note.text)

                            doc.stag("br")
                            doc.stag("br")

    def get_html(self):
        return indent(self.doc.getvalue())

    def save_as_html(self):
        with open("notes.html", "w+") as file:
            file.write(self.get_html())

if __name__ == "__main__":
    man = Manager("notes")

    while True:
        man.print_menu()

        try:
            mode = int(input())
        except:
            print("Incorrect input")
            continue

        system("clear")
        if mode == 1:
            note = man.read_note()
            man.add_note(note)
        elif mode == 2:
            man.view_notes()
        elif mode == 3:
            man.save_with_pickle()
            gen = Generator(man.notes)
            gen.save_as_html()
            break
        else:
            print("Unexpected mode")

