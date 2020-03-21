import os, json
from datetime import datetime
from flask import Flask, url_for, render_template, redirect, flash, request, jsonify, make_response
import uuid
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from forms import ContactForm, OrgContactForm

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

app = Flask(__name__)

app.config['SECRET_KEY']=os.environ["SECRET_KEY"]
app.config['RECAPTCHA_USE_SSL']= False
app.config['RECAPTCHA_PUBLIC_KEY']=os.environ["RECAPTCHA_PUBLIC_KEY"]
app.config['RECAPTCHA_PRIVATE_KEY']=os.environ["RECAPTCHA_PRIVATE_KEY"]
app.config['RECAPTCHA_OPTIONS']= {'theme':'black'}
GOOGLE_SHEET_CREDS = ServiceAccountCredentials.from_json_keyfile_name(
    'medical supplies-3abda9c4c6a3.json',scope
    )

def flash_errors(form):
    for field, errors in form.errors.items():
        if field != "recaptcha":
            for error in errors:
                flash(error)

def get_sheet(sheet_name):
    client = gspread.authorize(GOOGLE_SHEET_CREDS)
    sheet = client.open('med supplies')
    return sheet.worksheet(sheet_name)


@app.route('/', methods=('GET', 'POST'))
def start():
    if request.method == 'POST':
        parameter = request.form['submit_button']
        return redirect(url_for('supplies', parameter=parameter))
    else:
        cookie = uuid.uuid1().hex
        resp = make_response(render_template('pre.html'))
        resp.set_cookie('ilmedsupplies', cookie)
        return resp



@app.route('/supplies', methods=('GET', 'POST'))
def supplies():
    parameter = request.args.get('parameter')
    if request.method == "POST":
        submissions = json.loads(request.form.get('finalresults'))
        if len(submissions[0]) < 1:
            worksheet = get_sheet("items")
            items = worksheet.get_all_records()
            flash("You must make a selection in order to proceed!")
            return render_template('start.html', items=items, parameter=parameter)
        else:
            now = datetime.utcnow().isoformat()
            cookie = uuid.uuid1().hex
            if parameter == "have":
                submissions_ws = get_sheet("submissions")
                for k,v in submissions[0].items():
                    submissions_ws.append_row([cookie,k,v,now])

            else:
                org_needs_ws = get_sheet("org_needs")
                for k,v in submissions[0].items():
                    org_needs_ws.append_row([cookie,k,v,now])

            resp = make_response(redirect(url_for('finish', parameter=parameter)))
            resp.set_cookie('ilmedsupplies', cookie)
            return resp
    else:
        worksheet = get_sheet("items")
        items = worksheet.get_all_records()
        return render_template('start.html', items=items, parameter=parameter)

@app.route('/finish', methods=('GET', 'POST'))
def finish():
    parameter = request.args.get('parameter')
    if parameter == "have":
        form = ContactForm()
    else:
        form = OrgContactForm()
    if request.method == "POST":
        if form.validate_on_submit():
            cookie = request.cookies.get('ilmedsupplies')
            if cookie:
                if parameter == "have":
                    name = form.name.data
                    email = form.email.data
                    phone = form.phone.data
                    zip = form.zip.data
                    people_ws = get_sheet("people")
                    now = datetime.utcnow().isoformat()
                    people_ws.append_row([cookie,name,email,phone, zip, now])
                else:
                    org_name = form.org_name.data
                    contact_name = form.contact_name.data
                    email = form.email.data
                    phone = form.phone.data
                    zip = form.zip.data
                    info = form.info.data
                    orgs_ws = get_sheet("orgs")
                    now = datetime.utcnow().isoformat()
                    orgs_ws.append_row([cookie,org_name,contact_name, email,phone, zip,info, now])
                resp = make_response(render_template('success.html'))
                resp.set_cookie('ilmedsupplies', '', expires=0)
                return resp
            else:
                return redirect(url_for('start'))
        else:
            flash_errors(form)
            return render_template(f"{parameter}.html", form=form)

    else:
        if 'ilmedsupplies' in request.cookies:
            return render_template(f"{parameter}.html", form=form)
        else:
            return redirect(url_for('start'))






@app.route('/org', methods=('GET', 'POST'))
def need():
    form = OrgContactForm()
    if request.method == "POST":
        if form.validate_on_submit():
            org_name = form.org_name.data
            contact_name = form.contact_name.data
            email = form.email.data
            phone = form.phone.data
            zip = form.zip.data
            info = form.info.data
            people_ws = get_sheet("orgs")
            now = datetime.utcnow().isoformat()
            people_ws.append_row([cookie,org_name,contact_name, email,phone, zip,info, now])
            resp = make_response(render_template('success.html'))
            resp.set_cookie('ilmedsupplies', '', expires=0)
            return resp
        else:
            flash_errors(form)
            return render_template('need.html', form=form)

    else:
        return render_template('need.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
