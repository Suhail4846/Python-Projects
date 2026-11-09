import base64
import html
import os
import re
import smtplib
from email.message import EmailMessage

# =========================
# SETTINGS  (paste your NEW app password below)
# =========================

SENDER = "joseph.suhail@gmail.com"
APP_PASSWORD = "wfpa ymli xzwz wefc"   # 16 letters, from myaccount.google.com/apppasswords

RESUME = "Suhail_Khan_Resume_MIS.pdf"
LOG_FILE = "sent_log.txt"

POSITION = "MIS Analyst"
EXPERIENCE = "7+ years"
CURRENT_CTC = "Rs. 4,70,000 per annum"
EXPECTED_CTC = "Rs. 5,20,000 per annum"
NOTICE = "Served; available as an Immediate Joiner"

PHONE = "+919166650160"
WHATSAPP = "https://wa.me/919166650160"
LINKEDIN = "https://www.linkedin.com/in/suhail-khan-0270a673"
GITHUB = "https://github.com/Suhail4846"
EMAIL_LINK = f"mailto:{SENDER}?subject=Re:%20{POSITION.replace(' ', '%20')}%20Application"

EMAIL_RE = r"[\w.+-]+@[\w-]+(\.[\w-]+)+"

# =========================
# BUTTON LOGOS (PNG, embedded so no extra files are needed)
# =========================

ICONS_B64 = {
  "mail": (
    "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"
  ),
  "call": (
    "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"
    "RK5CYII="
  ),
  "wa": (
    "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"
    "RpiM6/8DhnKse2Nr1GcAAAAASUVORK5CYII="
  ),
  "li": (
    "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"
  ),
}

ICON_BYTES = {k: base64.b64decode(v) for k, v in ICONS_B64.items()}


# =========================
# PLAIN TEXT BODY (fallback for apps that do not show HTML)
# =========================

def make_text(company):
    return f"""Dear Hiring Team,

I am writing to express my interest in the position of {POSITION} at {company}, or any other role that aligns with my profile and skill set. I am open to opportunities across any location.

I have {EXPERIENCE} of experience in MIS reporting and data handling across banking and telecom operations. Most recently I worked as a Senior MIS Analyst at AU Small Finance Bank (Jul 2024 - Aug 2026), and earlier at Bharti Telemedia Ltd. (Airtel) and Tata Communications & Transformation Services.

I am strong in Advanced Excel (VLOOKUP, XLOOKUP, ARRAYFORMULA, INDEX-MATCH, Pivot Tables, Power Query, VBA/Macros), Google Sheets automation, SQL and Power BI.

My resume is attached for your review.

Regards,
Suhail Khan
+91 9166650160
joseph.suhail@gmail.com
LinkedIn: {LINKEDIN}
"""


# =========================
# HTML BODY (inline CSS only, so Gmail and Outlook display it correctly)
# =========================

def chip(text):
    return (
        '<span style="display:inline-block; background:#fce1fe;color:#691f6e;'
        'font-size:12px;font-weight:600;padding:5px 11px;border-radius:14px; '
        f'margin:0 2px 2px 0;">{text}</span>'
    )


def job(title, place, dates):
    return f"""
    <tr><td style="padding:0 0 14px 0;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
        <td width="14" valign="top" style="padding-top:5px;">
          <div style="width:10px;height:10px;border-radius:5px;background:#691f6e;"></div>
        </td>
        <td style="padding-left:8px;">
          <div style="font-size:14px;font-weight:700;color:#1b2430;">{title}</div>
          <div style="font-size:13px;color:#5b6675;">{place}</div>
          <div style="font-size:12px;color:#8a94a3;">{dates}</div>
        </td>
      </tr></table>
    </td></tr>"""


def btn(label, href, bg, icon):
    """Email-safe contact button with embedded icon or text fallback."""
    if icon in ICONS_B64:
        mark = (
            f'<img src="cid:ic_{icon}" width="36" height="36" alt="" '
            'style="display:block;margin:0 auto 6px auto;border:0;border-radius:18px;">'
        )
    else:
        mark = (
            f'<span style="display:block;width:36px;height:36px;line-height:36px;'
            f'margin:0 auto 6px auto;border-radius:18px;background:{bg};'
            'color:#ffffff;font-size:14px;font-weight:700;">GH</span>'
        )
    return (
        f'<a href="{href}" style="display:block;background:#f4f7fb;border:1px solid #dbe3ee;'
        'color:#1b2430;text-decoration:none;text-align:center;border-radius:10px;padding:12px 4px;">'
        f'{mark}'
        '<span style="display:block;font-size:14px;font-weight:700;line-height:18px;'
        f'color:#1b2430;">{label}</span></a>'
    )


def make_html(company):
    c = html.escape(company)
    chips = "".join(
        chip(s) for s in
        ["Advanced Excel", "VBA / Macros", "Power Query", "Pivot Tables",
         "SQL", "Power BI", "MIS Automation", "Data Reconciliation", "Google Sheets"]
    )
    jobs = (
        job("Senior MIS Analyst", "AU Small Finance Bank,Jaipur", "Jul 2024 &ndash; Aug 2026")
        + job("Senior MIS Analyst", "Bharti Telemedia Ltd. (Airtel),Jaipur", "Jun 2023 &ndash; Jul 2024")
        + job("MIS Executive", "Tata Communications &amp; Transformation Services,Jaipur", "Jan 2018 &ndash; Jun 2023")
    )

    b_reply = btn("Reply", EMAIL_LINK, "#1a56c4", "mail")
    b_call = btn("Call", "tel:" + PHONE, "#2e7d32", "call")
    b_whatsapp = btn("WhatsApp", WHATSAPP, "#25d366", "wa")
    b_linkedin = btn("LinkedIn", LINKEDIN, "#0a66c2", "li")
    b_github = btn("GitHub", GITHUB, "#24292f", "github")

    return f"""<!DOCTYPE html>
<html><style>
@import url('https://fonts.googleapis.com/css2?family=Karla:wght@400;500;600;700&display=swap');
</style><body style="margin:0;padding:0;background:#f2f4f8;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f2f4f8;">
<tr><td align="center" style="padding:24px 12px;">

  <table role="presentation" width="600" cellpadding="0" cellspacing="0"
         style="max-width:600px;width:100%;background:#ffffff;border-radius:12px;overflow:hidden;
                font-family: Roboto, Arial, sans-serif;
font-size: 13px;
line-height: 1.6;
color: #263445;">

    <!-- Header -->
    <tr><td bgcolor="#691f6e" style="background-color:#691F6E;padding:28px 30px;">
      <div style="font-size:24px;font-weight:700;color:#ffffff;">Suhail Khan</div>
      <div style="font-size:14px;color:#ffffff;margin-top:4px;line-height:1.6;">
        MIS Analyst &nbsp;|&nbsp; Excel Automation &nbsp;|&nbsp; Google Sheets Automation &nbsp;|&nbsp; SQL &nbsp;|&nbsp; Power BI
      </div>
    </td></tr>

    <!-- Greeting -->
    <tr><td style="padding:28px 30px 8px 30px;">
      <div style="font-size:15px;color:#1b2430;line-height:1.7;">
        Dear Hiring Team,<br><br>
        I am writing to express my interest in the position of <b>{html.escape(POSITION)}</b> at <b>{c}</b>,
        or any other role that aligns with my profile and skill set. I am open to opportunities across any location.
        I bring <b>{html.escape(EXPERIENCE)}</b> of experience in MIS reporting and data handling
        across banking and telecom operations, with a strong focus on automating recurring reports
        to reduce manual effort and improve accuracy.
      </div>
    </td></tr>

    <!-- Skills -->
    <tr><td style="padding:14px 30px 6px 30px;">
      <div style="font-size:12px;font-weight:700;letter-spacing:1px;color:#691f6e;margin-bottom:10px;">
        KEY SKILLS
      </div>
      {chips}
    </td></tr>

    <!-- Experience -->
    <tr><td style="padding:14px 30px 6px 30px;">
      <div style="font-size:12px;font-weight:700;letter-spacing:1px;color:#691f6e;margin-bottom:12px;">
        EXPERIENCE
      </div>
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0">{jobs}</table>
    </td></tr>

    <!-- Closing -->
    <tr><td style="padding:20px 30px 6px 30px;">
      <div style="font-size:15px;color:#1b2430;line-height:1.7;">
        My resume is attached for your review. I would welcome the opportunity to discuss my
        application further. Thank you for your time and consideration.
      </div>
    </td></tr>

    <!-- Buttons (2x2 grid, all same size) -->
    <tr><td style="padding:14px 30px 24px 30px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
        <tr>
          <td width="50%" style="padding:0 5px 10px 0;">{b_reply}</td>
          <td width="50%" style="padding:0 0 10px 5px;">{b_call}</td>
        </tr>
        <tr>
          <td width="50%" style="padding:0 5px 10px 0;">{b_whatsapp}</td>
          <td width="50%" style="padding:0 0 10px 5px;">{b_linkedin}</td>
        </tr>
        <tr>
          <td width="50%" style="padding:0 5px 0 0;">{b_github}</td>
          <td width="50%" style="padding:0 0 0 5px;"></td>
        </tr>
      </table>
    </td></tr>

    <!-- Signature -->
    <tr>
  <td style="background:#691F6E;padding:24px 30px;
             border-top:3px solid #ffffff;">

    <div style="font-family:Arial,sans-serif;
                font-size:22px;font-weight:700;
                color:#ffffff;margin-bottom:14px;">
      Suhail Khan
    </div>

    <div style="font-family:Arial,sans-serif;
                font-size:14px;line-height:2;">

      <a href="tel:+919166650160"
         style="color:#ffffff;text-decoration:none;">
        +91 9166650160
      </a>

      <br>

      <a href="mailto:joseph.suhail@gmail.com"
         style="color:#ffffff;text-decoration:none;">
        joseph.suhail@gmail.com
      </a>

    </div>

  </td>
</tr>

</table>

</td></tr>
</table>
</body></html>"""
# =========================
# LOAD RESUME AND SENT LOG
# =========================

with open(RESUME, "rb") as f:
    resume_bytes = f.read()

sent = set()
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, encoding="utf-8") as f:
        sent = {line.strip() for line in f if line.strip()}


# =========================
# GMAIL CONNECTION
# =========================

def connect():
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(SENDER, APP_PASSWORD.replace(" ", ""))
    return server


if APP_PASSWORD == "PASTE_APP_PASSWORD_HERE":
    raise SystemExit("Paste your Gmail app password in APP_PASSWORD at the top of the file.")

try:
    server = connect()
except smtplib.SMTPAuthenticationError:
    raise SystemExit("Login failed. Check the app password in the file.")

print("Logged in. Leave the email empty and press Enter to stop.\n")


# =========================
# ASK EMAIL + COMPANY, SEND, REPEAT
# =========================

while True:
    email = input("HR email: ").strip().lower()
    if not email:
        break

    if not re.fullmatch(EMAIL_RE, email):
        print("Invalid email, try again.\n")
        continue

    if email in sent:
        if input("Already sent to this address. Send again? (y/n): ").strip().lower() != "y":
            print()
            continue

    company = input("Company name (Enter to skip): ").strip() or "your organization"

    if input(f"Send to {company} | {email}? (y/n): ").strip().lower() != "y":
        print("Skipped.\n")
        continue

    msg = EmailMessage()
    msg["From"] = f"Suhail Khan <{SENDER}>"
    msg["To"] = email
    msg["Subject"] = (
        f"{POSITION} | {EXPERIENCE} Experience | "
        "Current CTC: 4.7 LPA | Expected CTC: 6 LPA (Negotiable)| Immediate Joiner"
    )
    msg.set_content(make_text(company))
    msg.add_alternative(make_html(company), subtype="html")

    # attach the button icons inside the HTML part (shown inline, not as attachments)
    html_part = msg.get_payload()[1]
    for name, data in ICON_BYTES.items():
        html_part.add_related(data, maintype="image", subtype="png",
                              cid=f"<ic_{name}>", disposition="inline")

    msg.add_attachment(resume_bytes, maintype="application",
                       subtype="pdf", filename=RESUME)

    try:
        try:
            server.send_message(msg, to_addrs=[email])
        except smtplib.SMTPServerDisconnected:
            print("Reconnecting to Gmail...")
            server = connect()
            server.send_message(msg, to_addrs=[email])

        with open(LOG_FILE, "a", encoding="utf-8") as lf:
            lf.write(email + "\n")
        sent.add(email)
        print(f"Sent -> {company} | {email}\n")

    except Exception as e:
        print(f"FAILED -> {company} | {email}")
        print("Error:", e)
        if "5.4.5" in str(e) or "limit exceeded" in str(e).lower():
            print("Gmail daily limit reached. Try again after 24 hours.")
            break
        print()

try:
    server.quit()
except Exception:
    pass

print("Done.")
