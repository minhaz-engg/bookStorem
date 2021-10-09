from django.contrib.auth.decorators import login_required
from django.http import request
from django.http.response import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from basket.basket import Basket

from .models import Order, OrderItem


def add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':

        order_key = request.POST.get('order_key')
        user_id = request.user.id
        baskettotal = basket.get_total_price()

        full_name = request.POST.get('custName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address1 = request.POST.get('custAdd')
        address2 = request.POST.get('custAdd2')
        country = request.POST.get('country')
        state = request.POST.get('state')
        post_code = request.POST.get('postCode')

        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            # order = Order.objects.create(user_id=user_id, full_name='name', address1='add1',address2='add2', total_paid=baskettotal, order_key=order_key)
            order = Order.objects.create(user_id=user_id, full_name=full_name, email=email, phone=phone, address1=address1,
                                         address2=address2, country=country, state=state, post_code=post_code, total_paid=baskettotal, order_key=order_key)
            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(
                    order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])

        response = JsonResponse({'success': 'Return something'})
        return response


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(approved=True)


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(approved=True)
    return orders


def order_list(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(approved=True)

    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_control(request):
    if request.user.is_superuser:
        upapproved_orders = Order.objects.filter(approved=False)
        return render(request, 'orders/admin_order_control.html', {"orders": upapproved_orders})
    else:
        raise Http404


@login_required
def order_approve(request, id):
    if request.user.is_superuser:
        order = get_object_or_404(Order, id=id)
        order.approved = True
        order.save()
        return HttpResponseRedirect(reverse('orders:order_control'))
    else:
        raise Http404


@login_required
def single_order(request, id):
    if request.user.is_superuser:
        order = get_object_or_404(Order, id=id)
        order_item = OrderItem.objects.filter(order=order)
        return render(request, 'orders/single.html', {'order_item': order_item, 'singleorder': order})
    else:
        raise Http404
