# Importing necessary modules
import datetime
from Webapp.models import Donor
from django.shortcuts import render, redirect

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.views.decorators.csrf import csrf_exempt

import razorpay

# Home page
def index(request):
    return render(request, 'index.html')

# Donation-Form page
def donate(request):
    return render(request, 'donate_form.html')

# Payment page
def pay(request):

    if request.method == 'POST':

        amount = float(request.POST['amount'])
        name = request.POST['name']
        email = request.POST['email']
        number = request.POST['number']
        anonymous = request.POST.get('anonymous', False)
        receipt = request.POST.get('receipt', False)
        d = datetime.date.today()
        d = d.strftime("%Y-%m-%d")

        # Creating order
        rp_amount = (amount * 100)
        currency = 'INR'
        client = razorpay.Client(auth=("test keyid", "secret key"))
        payment = client.order.create({'amount':rp_amount, 'currency':currency, 'payment_capture':'1'})

        # Creating instance (record) of model class / database table
        donor = Donor(
                    date=d, 
                    payment_id=payment['id'],  
                    name=name, email=email, 
                    number=number, 
                    anonymous=anonymous, 
                    amount=amount, 
                    receipt=receipt,
                    )
        donor.save()

        context = {
            'payment':payment,
        }

        return render(request, 'pay.html', context)

    return render(request, 'donate_form.html')

# Payment-Successful page
# Bypassing csrf verification
@csrf_exempt
def success(request):

    if request.method == 'POST':

        a = request.POST
        order_id = ''

        for key, value in a.items():
            if key == 'razorpay_order_id':
                order_id = value
                break
            
        donor = Donor.objects.filter(payment_id=order_id).first()
        donor.paid = True
        donor.save()

        msg_plain = render_to_string('email.txt')

        msg_html = render_to_string('thankyou_mail.html')
        send_mail(
            'Thank you, Your donation has been received.',
            msg_plain,
            settings.EMAIL_HOST_USER,
            [donor.email],
            html_message = msg_html
            )

        if donor.receipt == True:

            data = {
                'date' : donor.date,
                'id' : donor.payment_id,
                'name': donor.name,
                'amount': donor.amount,
            }
            
            receipt_html = render_to_string('receipt_mail.html', data)
            send_mail(
                'Thank you, Your receipt has been generated.',
                msg_plain,
                settings.EMAIL_HOST_USER,
                [donor.email],
                html_message = receipt_html
                )

        return render(request, 'success.html')
    
    return redirect('/')
    