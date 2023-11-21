import datetime
import secrets

from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect

from .calculator import get_insulin_units
from .google_sheet import insert_values_in_sheet
from .models import InputForm

app = Flask(__name__)
app_key = secrets.token_urlsafe(16)
app.secret_key = app_key

bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

SPREADSHEET_ID = "<SPREADSHEET ID FROM GOOGLE SHEETS URL>"


def valid_date(value: datetime.date):
    return isinstance(value, datetime.date)


def valid_time(value: datetime.time):
    return isinstance(value, datetime.time)


def valid_uint(value: int | str):
    try:
        return int(value) == abs(int(value))
    except (TypeError, ValueError):
        return False


@app.route("/", methods=["GET", "POST"])
def index():
    form = InputForm()
    message = ""
    warning = ""
    special = None
    insulin_units = None
    if form.validate_on_submit():
        date = form.date.data
        time = form.time.data
        carbs = form.carbs.data
        bg = form.bg.data
        if not valid_date(date):
            message = {
                "type": "error",
                "value": "Invalid date format was passed, expected: mm/dd/yyyy",
            }
        if not valid_time(time):
            message = {
                "type": "error",
                "value": "Invalid time format was passed, expected: HH:MM",
            }
        if not valid_uint(carbs):
            message = {"type": "error", "value": "Invalid value was passed for carbs"}
        if not valid_uint(bg):
            message = {
                "type": "error",
                "value": "Invalid value was passed for blood glucose leves (BG)",
            }
        
        # getting the calculator to find the insulin units
        insulin_units = get_insulin_units(
            carbs=carbs,
            sugar=bg,
            special=special
        )

        # edge cases as we want inserted in the spreadsheet
        if not message:
            if carbs > 200:
                warning="TOO MANY CARBS! CHECK VALUES"
        
            if bg < 70:
                warning="SUGAR IS LOW, CARBS NEEDED TO COMPENSATE!"
            
            if bg > 630:
                warning="SUGAR IS DANGEROUSLY HIGH! GET TO ER"
            date = datetime.datetime.strftime(date, "%m/%d/%Y")
            time = time.isoformat(timespec='auto')
            split_time = time.split(":")
            if int(split_time[0]) < 4:
                carbs = "MIDNIGHT"
            elif (
                (int(split_time[1]) == 20 and int(split_time[1]) >= 30) or
                (int(split_time[0]) > 20)
            ):
                carbs = "BEDTIME"
            composed_time = f"{date} {time}"

            # spreadsheet update results

            if insert_values_in_sheet(
                data_to_insert=[
                    date,
                    time,
                    composed_time,
                    carbs,
                    bg
                ],
                spreadseet_id=SPREADSHEET_ID,
            ):
                message = {"type": "success", "value": "Values inserted correctly"}
            else:
                message = {
                    "type": "error",
                    "value": "Values could not be inserted in spreadsheet",
                }

    return render_template(
        "index.html",
        form=form,
        spreadsheet_id=SPREADSHEET_ID,
        message=message,
        warning=warning,
        insulin_units=insulin_units
    )
