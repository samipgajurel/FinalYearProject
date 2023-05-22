from django.shortcuts import render, redirect
from .models import Wallet, Order
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from django.conf import settings # new
from django.http.response import JsonResponse # new
from django.views.decorators.csrf import csrf_exempt # new
import stripe
from cart.models import Cart, CartItem
from django.contrib import messages
from payment.models import Order, OrderItem
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
    # Retrieve the current cart for the logged-in user
    cart, created = Cart.objects.get_or_create(user=request.user)
    # Retrieve the cart items associated with the current cart
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    order = Order(user=request.user,
                  total_amount = total_price,
                  order_status ="Ordered")
    order.save()
    for item in cart_items:
        order_item = OrderItem (order=order,
                                product=item.product,
                                quantity=item.quantity,
                                seller =item.product.creator)
        order_item.save()
        item.delete()
#create order items and order based on cart items and cart
#remove cart items
#redirect to user dashboard
#user dashboard shoud show past order for consumers
    messages.add_message(request, messages.INFO, "Your Order Has Been Placed.")
    return redirect("/cart/")
    # return render(request, 'payment_success.html')


def insufficient_funds(request):
    messages.add_message(request, messages.ERROR, "No Sufficient Funds In Your Wallet.")
    return redirect("/cart/")
def payment_cancel(request):
    messages.add_message(request, messages.ERROR, "Payment Canceled.")
    return redirect("/cart/")

# new
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
    # Retrieve the current cart for the logged-in user
    cart, created = Cart.objects.get_or_create(user=request.user)
    # Retrieve the cart items associated with the current cart
    cart_items = CartItem.objects.filter(cart=cart)
    line_items=[]
    stripe.api_key = settings.STRIPE_SECRET_KEY
    for item in cart_items:
        product=stripe.Product.create(name= item.product.title)
        price=stripe.Price.create(product=product.id,
                                  unit_amount=int(item.product.price*100),
                                  currency="usd",
                                  )
        line_item={
            "price":price.id,
            "quantity":int(item.quantity)
        }
        line_items.append(line_item)

    domain_url = 'http://localhost:8000/'
    customer_data = stripe.Customer.list(email=request.user.email).data
    if len(customer_data) == 0:
        # creating customer
        customer = stripe.Customer.create(
            email=request.user.email,
            payment_method="pm_card_visa",
            invoice_settings={
                'default_payment_method': "pm_card_visa"
            }
        )
    else:
        customer = customer_data[0]
    print(customer)
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            customer=customer,
            success_url= domain_url + '/payment/payment-success/',
            cancel_url= domain_url + '/payment/payment-cancel/',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)
