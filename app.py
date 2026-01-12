from flask import Flask, render_template
from payments import register_payment_routes
from guests import register_guest_routes
from rooms import register_room_routes
from reservations import register_reservation_routes
from services import register_service_routes
from employees import register_employee_routes
from departments import register_department_routes
from reports import register_report_routes

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home_after_the_sign_in.html")

register_payment_routes(app)
register_guest_routes(app)
register_room_routes(app)
register_reservation_routes(app)
register_service_routes(app)
register_employee_routes(app)
register_department_routes(app)
register_report_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
