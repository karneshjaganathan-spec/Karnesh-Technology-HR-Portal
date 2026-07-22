from flask import Blueprint, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename

from middleware.auth_middleware import login_required, hr_required
from services.document_service import DocumentService

document_bp = Blueprint(
    "document",
    __name__,
    url_prefix="/api/documents"
)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================================
# Get All Documents
# ==========================================

@document_bp.route("/", methods=["GET"])
@login_required
def get_documents():

    documents = DocumentService.get_all()

    return jsonify({
        "success": True,
        "count": len(documents),
        "data": documents
    })


# ==========================================
# Get Single Document
# ==========================================

@document_bp.route("/<int:document_id>", methods=["GET"])
@login_required
def get_document(document_id):

    document = DocumentService.get(document_id)

    if document is None:

        return jsonify({
            "success": False,
            "message": "Document not found."
        }), 404

    return jsonify({
        "success": True,
        "data": document
    })


# ==========================================
# Upload Document
# ==========================================

@document_bp.route("/upload", methods=["POST"])
@hr_required
def upload_document():

    if "file" not in request.files:

        return jsonify({
            "success": False,
            "message": "No file uploaded."
        }), 400

    file = request.files["file"]

    if file.filename == "":

        return jsonify({
            "success": False,
            "message": "No file selected."
        }), 400

    filename = secure_filename(file.filename)

    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(filepath)

    data = {

        "employee_id":
            request.form["employee_id"],

        "document_name":
            request.form["document_name"],

        "document_type":
            request.form["document_type"],

        "file_name":
            filename,

        "file_path":
            filepath,

        "uploaded_by":
            request.form["uploaded_by"],

        "remarks":
            request.form.get(
                "remarks",
                ""
            )

    }

    document_id = DocumentService.add(data)

    return jsonify({

        "success": True,
        "document_id": document_id,
        "message": "Document uploaded successfully."

    })


# ==========================================
# Download Document
# ==========================================

@document_bp.route(
    "/download/<int:document_id>",
    methods=["GET"]
)
@login_required
def download_document(document_id):

    document = DocumentService.get(document_id)

    if document is None:

        return jsonify({

            "success": False,
            "message": "Document not found."

        }), 404

    return send_from_directory(

        UPLOAD_FOLDER,

        document["file_name"],

        as_attachment=True

    )


# ==========================================
# Delete Document
# ==========================================

@document_bp.route(
    "/<int:document_id>",
    methods=["DELETE"]
)
@hr_required
def delete_document(document_id):

    document = DocumentService.get(document_id)

    if document is None:

        return jsonify({

            "success": False,
            "message": "Document not found."

        }), 404

    if os.path.exists(document["file_path"]):

        os.remove(document["file_path"])

    DocumentService.delete(document_id)

    return jsonify({

        "success": True,
        "message": "Document deleted successfully."

    })