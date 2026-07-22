from openpyxl import Workbook
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


class ExportService:

    # ======================================
    # Export Excel
    # ======================================

    @staticmethod
    def export_employees_excel(employees, filename):

        workbook = Workbook()

        sheet = workbook.active

        sheet.title = "Employees"

        sheet.append([
            "Employee Code",
            "First Name",
            "Last Name",
            "Department",
            "Email",
            "Phone"
        ])

        for emp in employees:

            sheet.append([

                emp["employee_code"],
                emp["first_name"],
                emp["last_name"],
                emp.get("department_name", ""),
                emp["email"],
                emp["phone"]

            ])

        workbook.save(filename)

        return filename


    # ======================================
    # Export PDF
    # ======================================

    @staticmethod
    def export_employees_pdf(employees, filename):

        pdf = SimpleDocTemplate(filename)

        data = [[

            "Code",
            "Name",
            "Department",
            "Email",
            "Phone"

        ]]

        for emp in employees:

            data.append([

                emp["employee_code"],

                emp["first_name"] + " " + emp["last_name"],

                emp.get("department_name", ""),

                emp["email"],

                emp["phone"]

            ])

        table = Table(data)

        table.setStyle(TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.darkblue),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("GRID", (0,0), (-1,-1), 1, colors.black),

            ("ALIGN", (0,0), (-1,-1), "CENTER"),

            ("BOTTOMPADDING", (0,0), (-1,0), 10)

        ]))

        pdf.build([table])

        return filename