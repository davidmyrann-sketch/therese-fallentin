import os, smtplib, threading
from flask import Flask, render_template, request, redirect, url_for
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

PROBLEMS = [
    {"icon": "↔", "title": "Kommunikasjonen låser seg fast", "desc": "Ting blir sagt, men ikke hørt. Møter ender uten klarhet. Folk tolker istedenfor å spørre."},
    {"icon": "🥚", "title": "Alle går på eggeskall", "desc": "Ingen sier det de egentlig mener. Konflikter ulmer under overflaten. Klimaet er spent."},
    {"icon": "↕", "title": "Generasjonskonflikten er reell", "desc": "Ulike verdier, ulike forventninger, ulik kommunikasjonsstil. Misforståelsene hoper seg opp."},
    {"icon": "⚡", "title": "Utbrenthet lurer", "desc": "Du eller teamet ditt er i ferd med å løpe tomt. Prioriteringene er uklare og presset øker."},
    {"icon": "🔄", "title": "Samme problem, igjen og igjen", "desc": "Du ser mønsteret men klarer ikke bryte det. Det føles som om du løper i ring."},
    {"icon": "🧭", "title": "Du vet ikke hva du skal prioritere", "desc": "Alt føles viktig. Ingenting blir ferdig. Du mangler et tydelig neste steg."},
]

APPROACH = [
    {"num": "01", "title": "Jeg lytter etter det som ikke sies", "desc": "Mønstrene, motsetningene, det du sirkler rundt uten å lande. Det er der svaret ofte er."},
    {"num": "02", "title": "Jeg speiler det jeg ser — tydelig", "desc": "Ikke det du vil høre. Det som er sant. Uten omsvøp, uten sukkerbelegg."},
    {"num": "03", "title": "Du tar valget", "desc": "Jeg gir deg klarhet og retning. Du bestemmer hva du gjør med det. Ingen forpliktelse utover det."},
]

SERVICES = [
    {
        "tag": "Individuelt",
        "title": "Strategisk klarhets-sesjon",
        "desc": "75 minutters strukturert samtale — online eller i Oslo. For deg som sitter fast, trenger en beslutning eller vil forstå et mønster. Vi ser hva som er sant og hva du kan gjøre med det.",
    },
    {
        "tag": "Team & organisasjon",
        "title": "Workshop",
        "desc": "For team som vil kommunisere bedre på tvers av roller, aldre og forventninger. Praktisk, direkte og skreddersydd til der dere faktisk er.",
    },
    {
        "tag": "Foredrag",
        "title": "Foredrag & innlegg",
        "desc": "Om kommunikasjon, generasjonsforståelse, å eie sin egen fortelling og å bli tydelig som leder. Bestilles til konferanser, samlinger og interne fagdager.",
    },
]

TAGS = [
    "Internkommunikasjon",
    "Generasjonsforståelse",
    "Konflikthåndtering",
    "Ledelse",
    "Selvledelse",
    "Utbrenthet",
]

QUOTES = [
    {"text": "Therese hjelper deg å se det du ikke klarer å se selv — og sier det rett ut.", "who": "Klient, leder i privat sektor"},
    {"text": "Endelig noen som ikke bare validerer meg, men faktisk utfordrer meg til å tenke annerledes.", "who": "Klient, HR-direktør"},
    {"text": "Etter én sesjon hadde jeg klarhet i noe jeg hadde gått rundt i måneder.", "who": "Klient, virksomhetsleder"},
]

GOOD_FIT = [
    "Du er leder og vil bli tydeligere i kommunikasjonen din",
    "Teamet ditt sliter med å forstå hverandre på tvers av generasjoner",
    "Du har prøvd å løse det selv, men kommer ingen vei",
    "Du vil ha klarhet, ikke bare noen å snakke med",
    "Du tåler direkte tilbakemeldinger og er klar til å ta ansvar",
    "Du er klar for et faktisk neste steg — ikke bare en analyse",
]

@app.route('/')
def index():
    return render_template('index.html',
        problems=PROBLEMS,
        approach=APPROACH,
        services=SERVICES,
        tags=TAGS,
        good_fit=GOOD_FIT,
        quotes=QUOTES,
        success=request.args.get('ok') == '1',
    )

@app.route('/kontakt', methods=['POST'])
def kontakt():
    navn   = request.form.get('navn', '').strip()
    epost  = request.form.get('epost', '').strip()
    melding = request.form.get('melding', '').strip()

    def _send():
        try:
            body = f"Ny henvendelse fra theresefallentin.no\n\nNavn: {navn}\nE-post: {epost}\n\nMelding:\n{melding}"
            msg = MIMEMultipart()
            msg["From"]    = "master@goldenbusinessadvice.com"
            msg["To"]      = "tfallentine@gmail.com"
            msg["Subject"] = f"Ny henvendelse: {navn}"
            msg.attach(MIMEText(body, "plain", "utf-8"))
            with smtplib.SMTP_SSL("smtp.domeneshop.no", 465, timeout=15) as s:
                s.login("master@goldenbusinessadvice.com",
                        os.environ.get("SMTP_PASS", ""))
                s.send_message(msg)
        except Exception as e:
            print(f"[email error] {e}")

    threading.Thread(target=_send, daemon=True).start()
    return redirect(url_for('index', ok='1') + '#kontakt')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
