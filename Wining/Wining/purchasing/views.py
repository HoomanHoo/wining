from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.template import loader
from django.http.response import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from purchasing.usecase import purchase_usecase as p


from django.utils.dateformat import DateFormat
from django.utils.datetime_safe import datetime
from purchasing.db_access.query_set import (
    get_product_info,
    get_info_of_buy_one,
    get_user_point,
    insert_purchase,
    get_store_lists,
    add_cart_info,
    get_cart_info,
    get_cart_list_page_info,
)

from purchasing.usecase.purchase_usecase import formating
from django.db import DatabaseError
import json
from purchasing.models import WinCartDetail
import errorhandling


# Create your views here.
class StoreListView(View):
    def get(self, request):
        wine_id = 9
        template = loader.get_template("purchasing/storeList.html")

        store_lists = get_store_lists(wine_id=wine_id)
        context = {"store_lists": store_lists}

        return HttpResponse(template.render(context, request))


class DetailProductInfoView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        sell_id = request.GET.get("sellid", None)
        user_id = "test1111"
        template = loader.get_template("purchasing/detailProductInfo.html")

        product_info = get_product_info(sell_id=sell_id)

        # 리뷰 코드는 아직 model에 존재하지 않기 때문에 차후 작성

        rdtos = []
        product_info = product_info
        if product_info["store__storeUrl__store_map_url"] == None:
            url_value = 0

        else:
            url_value = 1

        context = {
            "product_info": product_info,
            "url_value": url_value,
            "user_id": user_id,
            "rdtos": rdtos,
        }

        return HttpResponse(template.render(context, request))


class BuyListView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        user_id = "test1111"
        sell_id = request.GET.get("sellid", None)
        cart_id = request.GET.get("cartid", None)
        quantity = request.GET.get("qnty", None)
        user_point = get_user_point(user_id)
        template = loader.get_template("purchasing/buyList.html")
        context = {"user_point": user_point}
        dtos = []
        all_price = 0

        if sell_id != None:
            info = get_info_of_buy_one(sell_id)
            sell_price = info["sell_price"]

            dto = formating(
                user=user_id,
                product_info=sell_id,
                quantity=quantity,
                price_per_one=sell_price,
                wine_image=info["wine__wine_image"],
                wine_name=info["wine__wine_name"],
            )
            all_price = dto["purchase_price"]
            dtos.append(dto)

        else:
            cart_info = get_cart_info(user_id=user_id)
            if cart_info != None:
                cart_id = cart_info.cart_id
                infos = get_cart_list_page_info(cart_id=cart_id)

                for info in infos:
                    all_price += info.get("purchase_price")
                    dto = formating(
                        user=user_id,
                        product_info=info.get("sell__sell_id"),
                        quantity=info.get("cart_det_qnty"),
                        price_per_one=info.get("sell__sell_price"),
                        wine_name=info.get("sell__wine__wine_name"),
                        wine_image=info.get("sell__wine__wine_image"),
                    )
                    dtos.append(dto)
                context["cart_id"] = cart_id

        context["dtos"] = dtos
        context["all_price"] = all_price

        return HttpResponse(template.render(context, request))

    def post(self, request):
        user_id = "test1111"
        sell_id = request.POST.getlist("sellId", None)
        quantity = request.POST.getlist("quantity", None)
        purchase_price = request.POST.getlist("purchasePrice", None)
        user_point = request.POST.get("userPoint", None)
        all_price = request.POST.get("allPrice", None)
        cart_id = request.POST.get("cartId", None)
        current_time = DateFormat(datetime.now()).format("Y-m-d H:i:s")

        ps = p.PurchaseSequence(
            user=user_id,
            product_infos=sell_id,
            quantity_per_ones=quantity,
            price_per_ones=purchase_price,
            user_point=int(user_point),
            all_price=int(all_price),
            current_time=current_time,
            cart_info=cart_id,
        )
        result = ps.calc()
        if result == None:
            template = loader.get_template("purchasing/buyList.html")
            context = {"pointError": -1}
            return HttpResponse(template.render(context, request))
        else:
            try:
                insert_purchase(result)

            except DatabaseError:
                return redirect("purchaseError")

            return redirect("orderPage")


class AddPickListView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def post(self, request):
        user_id = request.POST.get("userId")
        sell_id = request.POST.get("sellId", None)
        quantity = int(request.POST.get("qnty", None))
        current_time = DateFormat(datetime.now()).format("Y-m-d H:i:s")

        try:
            add_cart_info(
                user_id=user_id,
                sell_id=sell_id,
                quantity=quantity,
                current_time=current_time,
            )

        except DatabaseError:
            return redirect("errorPage")

        return redirect("cartList")


class PickListView(View):
    def get(self, request):
        user_id = "test1111"
        cart_info = get_cart_info(user_id=user_id)
        context = {}
        if cart_info != None:
            page_infos = get_cart_list_page_info(cart_id=cart_info.cart_id)
            cart_id = cart_info.cart_id
            all_price = 0
            for page_info in page_infos:
                all_price += page_info.get("purchase_price")

        else:
            page_infos = []
            all_price = 0
            cart_id = -1

        template = loader.get_template("purchasing/pickList.html")
        context = {
            "page_infos": page_infos,
            "all_price": all_price,
            "cart_id": cart_id,
        }

        return HttpResponse(template.render(context, request))

    def post(self, request):
        request_body = json.loads(request.body)
        cart_detail_id = request_body.get("cartDetailId", None)
        detail_cart = WinCartDetail.objects.get(cart_det_id=cart_detail_id)
        detail_cart.delete()

        return JsonResponse({"result": "삭제되었습니다"}, status=200)


class OrderPageView(View):
    def get(self, request):
        template = loader.get_template("purchasing/orderPage.html")
        context = {}
        return HttpResponse(template.render(context, request))
