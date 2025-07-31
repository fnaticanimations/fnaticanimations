import os
from flask import Blueprint, request, jsonify
import smtplib
from email.mime.text import MIMEText

contact_bp = Blueprint("contact", __name__)

@contact_bp.route("/contact", methods=["POST"])
def contact():
    data = request.get_json()
    name = f"{data.get("firstname", "")} {data.get("lastname", "")}"
    email = data.get("email")
    phone = data.get("phone")
    message = data.get("message")

    # Email details
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    receiver_email = "fnaticanimation@gmail.com"
    subject = "New Contact Form Submission from Fnaticanimations Website"

    body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        return jsonify({"success": True, "message": "Email sent successfully!"})
    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify({"success": False, "message": "Failed to send email."}), 500


