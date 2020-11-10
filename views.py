import re
import traceback
from models import Payment
from app import app, webpay, db
from flask import render_template, request, redirect, url_for, flash


@app.route('/', methods=['GET'])
def donation_page():
    return render_template('index.html')


@app.route('/make_payment', methods=['POST'])
def make_payment():
    try:
        amount = int(request.form.get('amount')) * 10  # toman to rial
        if amount < 10000:
            raise ValueError("حداقل مبلغ مجاز برای پرداخت ۱۰۰۰ تومان است.")

        phone_number = request.form.get('phone')
        if phone_number:
            if not phone_number.isnumeric():
                raise ValueError("شماره تماس وارد شده نامعتبر است.")

            phone_number = f'0{int(phone_number)}'  # convert to english digits
            if not re.match(r'^09\d{9}$', str(phone_number)):
                raise ValueError("شماره تماس وارد شده نامعتبر است.")

        # record payment data in database
        payment = Payment()
        payment.name = request.form.get('name')
        payment.email = request.form.get('email')
        payment.description = request.form.get('description')
        payment.amount = amount
        payment.phone_number = phone_number
        db.session.add(payment)
        db.session.commit()

        payment_url = webpay.payment(
            reference=payment.id,  # unique ID
            amount_irr=amount,
            callback_url=url_for('verify_payment', _external=True),
            payer_mobile=phone_number
        )
        return redirect(payment_url)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for('donation_page'))
    except Exception:
        db.session.rollback()  # ensure database session works after error
        traceback.print_exc()  # print traceback and continue
        return redirect(url_for('donation_page'))


@ app.route('/verify_payment', methods=['GET'])
def verify_payment():
    reference = request.args.get('reference')
    if not reference:
        return redirect(url_for('donation_page'))

    payment = Payment.query.get(reference)
    if not payment:
        return render_template('verify.html', verified=False)

    if payment.paid is True:
        # payment once previously verified
        return render_template('verify.html', verified=True, again=True)

    verified = False
    try:
        payment_data = webpay.verify(
            reference=payment.id,
            amount_irr=payment.amount
        )
        if payment_data.get("state") == "paid":
            verified = True
    except Exception as api_error:
        if api_error.error_key == 'NOT_CONFIRMED':
            verified = False
        else:
            traceback.print_exc()  # print unknown api error and continue

    if verified is True:
        payment.paid = True
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # ensure database session works after error
            raise e

        amount = int(payment.amount / 10)  # rial to toman
        date, _time = payment_data['pay_time'].split("T")
        pay_time = f'{_time.split(".", 1)[0]} ({date})'

        return render_template('verify.html',
                               verified=True,
                               pay_trace=payment_data['pay_trace'],
                               amount=amount,
                               pay_pan=payment_data['pay_pan'],
                               pay_time=pay_time)

    return render_template('verify.html', verified=False)
