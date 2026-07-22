from flask import Blueprint, send_file
import os

from middleware.auth_middleware import login_required
from services.employee_service import EmployeeService
from services.export_service import ExportService

export_bp = Blueprint(
    "export",
    __name__,
    url_prefix="/api/export"
)

EXPORT_FOLDER = "exports"

os.makedirs(EXPORT_FOLDER, exist_ok=True)


# ==========================================
# Export Employees - Excel
# ==========================================

@export_bp.route("/employees/excel", methods=["GET"])
@login_required
def export_employee_excel():

    employees = EmployeeService.get_all()

    filename = os.path.join(

        EXPORT_FOLDER,

        "employees.xlsx"

    )

    ExportService.export_employees_excel(

        employees,

        filename

    )

    return send_file(

        filename,

        as_attachment=True

    )


# ==========================================
# Export Employees - PDF
# ==========================================

@export_bp.route("/employees/pdf", methods=["GET"])
@login_required
def export_employee_pdf():

    employees = EmployeeService.get_all()

    filename = os.path.join(

        EXPORT_FOLDER,

        "employees.pdf"

    )

    ExportService.export_employees_pdf(

        employees,

        filename

    )

    return send_file(

        filename,

        as_attachment=True

    )