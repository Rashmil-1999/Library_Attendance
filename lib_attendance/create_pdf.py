from reportlab.pdfgen import canvas
import constants
from query import retrieve_all_data, count_insertion


def exportPdf(fileName, connectionObject, student_count, teacher_count):
    """
    This function consists of logic for generation of pdf
    """
    c = canvas.Canvas(fileName)
    databaseResults = connectionObject.fetchall()
    labels = [
        "id: ",
        "sap: ",
        "   Date: ",
        "   In: ",
        "   out: ",
        "is_in: ",
        "  is_teacher:",
    ]
    y_pos = [x for x in range(750, 0, -30)]
    teacher = "Teachers Count: {}".format(teacher_count)
    student = "Students Count: {}".format(student_count)
    for i, data in enumerate(databaseResults):
        dataStringList = [labels[j] + str(entry)
                          for j, entry in enumerate(data)]
        for j in range(-2, 1):
            dataStringList.pop(j)
        if i % 25 == 0 and i != 0:
            c.showPage()
        c.drawString(100, y_pos[i % 25], " ".join(dataStringList))
    if (i + 1) % 25 == 0 and i != 0:
        c.showPage()
    c.drawString(100, y_pos[(i + 1) % 25], teacher)
    c.drawString(100, y_pos[(i + 2) % 25], student)
    c.save()


def pdf_generation(str_date, conn):
    """
    Trigger exportPdf function and add count of students and teachers to pdf
    """
    file_name = constants.path_to_pdfs + "library-" + str_date + ".pdf"
    p = conn.execute(query.retrieve_all_data)
    total_count = len([row for row in p])
    count = conn.execute(query.count_insertion, (1,))
    teacher_count = len([row for row in count])
    student_count = total_count - teacher_count
    p = conn.execute(query.retrieve_all_data)
    exportPdf(file_name, p, student_count, teacher_count)
