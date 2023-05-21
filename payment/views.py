from django.shortcuts import render, redirect
from .models import Wallet, Order
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from django.http import  HttpResponse

# def generate_receipt(id):
#     from weasyprint import HTML
#     html_string = receipt(id)
#     html = HTML(string=html_string)
#     location = "/tmp/report.pdf"
#     html.write_pdf(target='/tmp/report.pdf')
#     fs = FileSystemStorage('/tmp')
#     with fs.open(location) as pdf:
#         response = HttpResponse(pdf, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="' + \
#             'report' + '.pdf"'
#
#         return response
#
# def receipt(id):
#     queryset = BalanceLedger.objects.get(id=id)
#     # writing HTML Content
#     now = datetime.now()
#     current_time = now.strftime("%m/%d/%Y %H:%M:%S")
#     voucher = queryset.voucher
#     # if voucher:
#     #print("Voucher value",voucher)
#     course = queryset.order.course
#     if queryset.paytment_type != "STRIPE":
#         item_price = "RS.{}".format(course.price)
#         if course.discount_percentage:
#             item_price = "RS.{}".format(course.price - course.discount_percentage/100 * course.price)
#     else:
#         item_price = "${}".format(course.international_price())
#         if course.discount_percentage:
#             item_price = "${}".format(course.international_price() - course.discount_percentage/100 * course.international_price())
#     currency = "RS." if queryset.paytment_type != "STRIPE" else "$"
#     context = {
#         "order_id":queryset.order.oid,"issue_date":queryset.date.strftime("%b %d, %Y"),
#         "name":"{} {}".format(queryset.created_by.first_name,queryset.created_by.last_name),
#         "phone_number":"+{}-{}".format(queryset.created_by.country_code,queryset.created_by.phone_number) if queryset.created_by.phone_number else "",
#         "item_name":queryset.order.course.name,
#         "paid_price":"{}{}".format(currency,queryset.amount),
#         "receipt_date":current_time,
#         "discount":"{}{}".format(currency,voucher.value if voucher else "") if voucher and voucher.discount_type == "PRICE" else "{}%".format(voucher.value if voucher else "") if voucher and voucher.value is not None else "",
#         "item_price":item_price
#         }
#     html_content =get_template("course/receipt.html").render(
#                     context
#                 )
#     # html_content = render_to_string("course/receipt.html")
#     # html_content = '<div class="table">'
#     return html_content

def checkout(request):
    if request.method == 'POST':
        total_amount = request.POST['total_amount']
        user = request.user
        wallet = Wallet.objects.get(user=user)

        if wallet.balance >= total_amount:
            # Deduct the amount from the wallet balance
            wallet.balance -= total_amount
            wallet.save()

            # Save the order and payment status to the database
            order = Order.objects.create(user=user, total_amount=total_amount)
            # You can perform additional steps like integrating with a payment gateway here
            order.payment_status = True
            order.save()

            return redirect('payment_success')
        else:
            return redirect('insufficient_funds')
    else:
        total_amount = 100  # Example amount
        return render(request, 'checkout.html', {'total_amount': total_amount})


def payment_success(request):
    return render(request, 'payment_success.html')


def insufficient_funds(request):
    return render(request, 'insufficient_funds.html')
