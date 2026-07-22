from flask import Flask
from flask_cors import CORS

from database import initialize_database
from routes.auth import auth_bp
from routes.employee import employee_bp
from routes.dashboard import dashboard_bp
from routes.department import department_bp
from routes.attendance import attendance_bp
from routes.leave import leave_bp
from routes.reports import reports_bp
from routes.profile import profile_bp
from routes.payroll import payroll_bp
from routes.recruitment import recruitment_bp
from routes.performance import performance_bp
from routes.notification import notification_bp
from routes.document import document_bp
from routes.asset import asset_bp
from routes.permission import permission_bp
from routes.export import export_bp
from routes.settings import settings_bp

app = Flask(__name__)

app.secret_key = "karnesh_technology_hr_portal"

CORS(
    app,
    supports_credentials=True
)

initialize_database()

# Register Routes
app.register_blueprint(auth_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(department_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(leave_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(payroll_bp)
app.register_blueprint(recruitment_bp)
app.register_blueprint(performance_bp)
app.register_blueprint(notification_bp)
app.register_blueprint(document_bp)
app.register_blueprint(asset_bp)
app.register_blueprint(permission_bp)
app.register_blueprint(export_bp)
app.register_blueprint(settings_bp)

@app.route("/")
def home():

    return {
        "Project": "Karnesh Technology HR Portal",
        "Status": "Running Successfully",
        "Version": "1.0"
    }


if __name__ == "__main__":
    app.run(debug=True, threaded=False)