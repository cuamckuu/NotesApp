#!/usr/bin/env python3

from os import system
import datetime
import pickle
from yattag import Doc, indent
from markdown import markdown

class Note:
    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def __str__(self):
        return "{date} \n{name} \n{text}\n\n".format(date=self.date,\
                                                     name=self.title,\
                                                     text=self.text)

class Manager:
    def __init__(self, filename="./notes"):
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

    def del_note(self, num):
        for i, note in enumerate(reversed(self.notes[:])):
            if i == num:
                self.notes.remove(note)

    def print_menu(self):
        system("clear")
        print("Choose mode:")
        print("1.New note")
        print("2.View notes")
        print("3.Save as HTML")
        print("4.Exit")

    def save_with_pickle(self):
        with open(self.filename, "wb+") as file:
            pickle.dump(self.notes, file)

class Generator:
    def __init__(self, notes=[]):
        self.doc, self.tag, self.text = Doc().tagtext()
        doc, tag, text = self.doc, self.tag, self.text

        doc.asis("<!DOCTYPE html>")
        with tag("html"):
            doc.asis(self.get_head())
            doc.asis(self.get_body(notes))

    def get_head(self):
        doc, tag, text = Doc().tagtext()
        with tag("head"):
            with tag("title"):
                text("Notes App")

            doc.stag("meta", charset="utf-8")
            doc.stag("link",
                     href="https://fonts.googleapis.com/css?family=Fjalla+One",
                     rel="stylesheet")

            doc.stag("link",
                     href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
                     rel="stylesheet")

            doc.stag("link", href="./style.css", rel="stylesheet")

            with tag("script", src="scripts.js", type="text/javascript"):
                pass

        return doc.getvalue()

    def get_button(self, num):
        doc, tag, text = Doc().tagtext()
        with tag("button",   ("class", "del-btn"),
                             ("onclick", "deleteNote({})".format(num))):
            text("Delete this")

        return doc.getvalue()


    def get_note(self, note, num):
        doc, tag, text = Doc().tagtext()
        with tag("div", ("class", "note")):
            with tag("div", ("class", "note-top")):
                with tag("i", ("class", "date")):
                    text(note.date)
                doc.asis(self.get_button(num))

            with tag("b", ("class", "title")):
                text(note.title)
            doc.stag("br")

            doc.asis(markdown(note.text))

        return doc.getvalue()

    def get_form(self):
        doc, tag, text = Doc().tagtext()
        with tag("div", ("class", "note")):
            with tag("form", method="POST"):
                doc.stag("input", type="text",
                                  name="title",
                                  placeholder="Title")
                with tag("textarea", name="text",
                                     placeholder="Your note here",
                                     rows=12):
                    text("")

                doc.stag("input", type="submit",
                                  value="Create")
        return doc.getvalue()

    def get_body(self, notes):
        doc, tag, text = Doc().tagtext()
        with tag("body"):
            with tag("h1", ("class", "logo")):
                text("Notes App ")

            with tag("div", ("class", "background")):
                for i, note in enumerate(reversed(notes)):
                    doc.asis(self.get_note(note, i))

                doc.asis(self.get_form())

        return doc.getvalue()

    def get_html(self):
        return indent(self.doc.getvalue())

    def save_as_html(self):
        with open("notes.html", "w+") as file:
            file.write(self.get_html())
        input()

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
            gen = Generator(man.notes)
            gen.save_as_html()
        elif mode == 4:
            man.save_with_pickle()
            break;
        else:
            print("Unexpected mode")

