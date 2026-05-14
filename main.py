import smtplib
import pandas as pd
import time
from email.message import EmailMessage
from datetime import datetime

# ================= CONFIG =================

EMAIL = "your_email@gmail.com"
PASSWORD = "your_app_password"

RESUME_FILE = "resume.pdf"
JOBS_FILE = "jobs.csv"

MY_SKILLS = [
    "Python",
    "Java",
    "AWS",
    "React",
    "SQL",
    "REST APIs"
]

# ================= EMAIL FUNCTION =================

def create_email(company, role):

    skills = ", ".join(MY_SKILLS[:4])

    return f"""
Hello Hiring Team,

I came across the {role} opening at {company} and would like to apply.

I have experience working with {skills} along with backend development, APIs, and cloud-based applications. I have built multiple real-world projects involving automation, full-stack development, and scalable systems.

I believe my technical skills and project experience align well with this role.

Please find my resume attached for consideration.

Thank you for your time. Looking forward to hearing from you.

Best Regards,
Your Name
LinkedIn: linkedin.com/in/yourprofile
GitHub: github.com/yourgithub
""".strip()


def send_email(to_email, company, role):

    msg = EmailMessage()

    msg["Subject"] = f"Application for {role}"
    msg["From"] = EMAIL
    msg["To"] = to_email

    body = create_email(company, role)
    msg.set_content(body)

    # Attach Resume
    with open(RESUME_FILE, "rb") as file:
        msg.add_attachment(
            file.read(),
            maintype="application",
            subtype="pdf",
            filename="resume.pdf"
        )

    # Send Email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(msg)

# ================= MAIN =================

def main():

    jobs = pd.read_csv(JOBS_FILE)

    success = 0
    failed = 0

    print("\nStarting Job Application Automation...\n")

    for index, job in jobs.iterrows():

        company = job["company"]
        email = job["email"]
        role = job["role"]

        try:
            start = time.time()

            send_email(email, company, role)

            end = round(time.time() - start, 2)

            print(f"[{index + 1}] Sent -> {company} ({end}s)")
            success += 1

            time.sleep(2)

        except Exception as e:
            print(f"[{index + 1}] Failed -> {company}")
            print("Error:", e)
            failed += 1

    # Final Report
    print("\n========== REPORT ==========")
    print("Total Jobs :", len(jobs))
    print("Success    :", success)
    print("Failed     :", failed)
    print("Completed  :", datetime.now())
    print("============================")


if __name__ == "__main__":
    main()