# -*- coding: utf8 -*
import doc_export as de
import gui


def run():
    window = gui.create_start_window()
    gui.run_start(window)


def run_export():
    de.export_csv_to_docx("csv/export.csv")


if __name__ == '__main__':
    run()

