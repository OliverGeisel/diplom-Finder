import pathlib
from datetime import datetime

import docx
import pandas

from spiel.PlayerDayCollection import DiplomaPlayerDayCollection


def export_docx(filename, diplomas: DiplomaPlayerDayCollection):
    name = diplomas.get_full_name()
    date = str(diplomas.date.strftime("%d.%m.%Y"))
    for diploma in diplomas.answers.answers:
        sequence = sequenz_string_from_list(diploma.folge, diploma.bereich == "räumer")
        write_document(name, date, sequence, filename)


def sequenz_string_from_list(sequence: list[int], abräumer: bool = False) -> str:
    sum_sequenz = 0
    for number in sequence:
        sum_sequenz += number
    if len(sequence) == 10 and not abräumer:
        return f"10 Wurf {sum_sequenz}"
    elif len(sequence) == 10 and abräumer:
        return f"10 Wurf Abr. {sum_sequenz}"
    elif len(sequence) == 5:
        return f"5 Wurf {sum_sequenz}"
    else:
        str_list = [str(x) for x in sequence]
        return "-".join(str_list)


def write_document(name, date, sequence, base_file_name: str = None, directory: str = "docs",
                   doc_template: str = "_Vorlage_Diplom.docx"):
    document = docx.Document(doc_template)
    context = {
        '[NAME]': name,
        '[FOLGE]': sequence,
        '[DATUM]': date,
    }
    special_name = f"{name}_{date}_({sequence.replace('/', '-')})"

    default_filename = f"{special_name if base_file_name is None else base_file_name + '_' + special_name}"
    default_filename = f"{directory}/{default_filename}"
    for paragraph in document.paragraphs:
        for key, value in context.items():
            if key in paragraph.text:
                for run in paragraph.runs:
                    run.text = run.text.replace(key, value)
    file = pathlib.Path(default_filename + ".docx")
    number = 1
    complete_file_name = default_filename + ".docx"
    while file.exists():
        complete_file_name = f"{default_filename} ({number}).docx"
        file = pathlib.Path(complete_file_name)
        number += 1
    del context
    document.save(complete_file_name)


def export_csv_to_docx(csv_file, base_file_name: str = None, directory: str = "docs"):
    data = pandas.read_csv(csv_file, sep=";", encoding="UTF-8", header=True)

    directory_d = pathlib.Path(directory if directory is not None else ".")
    if not directory_d.exists():
        directory_d.mkdir()

    for columns in data.columns:
        if columns["Typ"] == "NEGATIVE":
            continue
        name = columns["Name"].replace(",", " ")
        vorname = name.split(" ")[1]
        nachname = name.split(" ")[0]
        full_name = f"{vorname} {nachname}"

        sequenz_list = [int(x) for x in columns["Folge"].strip().split("-")]
        abräumer = "Räumer" in columns["Bereich"].strip()
        sequenz = sequenz_string_from_list(sequenz_list, abräumer)

        date = datetime.strptime(columns["Datum"], "%Y-%m-%d").date().strftime("%d.%m.%Y")

        write_document(full_name, date, sequenz, base_file_name, directory)
