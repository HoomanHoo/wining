from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template import loader
from django.http.response import HttpResponse, JsonResponse
from store.models import WinStore, WinSell, WinStoreUrl
from detail.models import WinWine
from django.utils import timezone
from user.models import WinUser, WinUserGrade
from django.utils.dateformat import DateFormat
from datetime import datetime
from store.db_access.query_set import insert_store_info, insert_sell_info


# Create your views here.


class StoreRegistrationView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        user_id = "test3334"
        if WinStore.objects.filter(user_id=user_id):
            return redirect("storeMyPage")

        else:
            template = loader.get_template("store/storeRegistration.html")
            context = {"user_id": user_id}
            return HttpResponse(template.render(context, request))

    def post(self, request):
        user_id = request.POST.get("userId", None)
        store_address = request.POST.get("storeAddress", None)
        store_name = request.POST.get("storeName", None)
        store_reg_num = request.POST.get("storeRegNum", None)
        store_email = request.POST.get("storeEmail")
        store_map_url = request.POST.get("storeMapUrl", None)

        store = insert_store_info(
            user_id=user_id,
            store_address=store_address,
            store_name=store_name,
            store_reg_num=store_reg_num,
            store_email=store_email,
            store_map_url=store_map_url,
        )

        return redirect("productAddition")


class ProductAdditionView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        user_id = "test3334"

        store_info = WinStore.objects.get(user_id=user_id)
        if WinSell.objects.filter(store_id=store_info.store_id):
            return redirect("storeMyPage")

        else:
            wines = WinWine.objects.values(
                "wine_id", "wine_name", "wine_capacity", "wine_alc"
            )

            store_id = store_info.store_id

            template = loader.get_template("store/productAddition.html")
            context = {"wines": wines, "store_id": store_id}
            return HttpResponse(template.render(context, request))

    def post(self, request):
        user_id = "test2222"
        store_id = request.POST.get("storeId", None)
        wine_ids = request.POST.getlist("wineId", None)
        sell_prices = request.POST.getlist("sellPrice", None)
        sell_promots = request.POST.getlist("sellPromot", None)
        sell_state = 1
        current_time = DateFormat(datetime.now()).format("Y-m-d H:i:s")

        insert_sell_info(
            user_id,
            store_id,
            wine_ids,
            current_time,
            sell_prices,
            sell_promots,
            sell_state,
        )

        return redirect("storeMyPage")


class SearchProduct(View):
    def get(self, request):
        search_keyword = request.GET.get("srhkeyword", None)

        result_obj1 = WinWine.objects.filter(
            wine_name__icontains=search_keyword, wine_name__range=("가", "힣")
        ).values_list("wine_id", "wine_name", "wine_capacity", "wine_alc")
        # print(result_obj1[0][0], result_obj1[0][1], result_obj1[0][2], result_obj1[0][3])
        #
        #
        # print(result_obj1[0])

        result = []
        if result_obj1 == None:
            result = "no result"

        else:
            for i in range(len(result_obj1)):
                result.append(result_obj1[i])

        # result_obj2 = list(result_obj1.wine_id)
        # print(result_obj2)
        # result_obj3 = list(result_obj1.wine_name)
        # print(result_obj3)
        # result_obj4 = list(result_obj1.wine_alc)
        # print(result_obj4)
        # start = time()
        #
        # result = WinWine.objects.filter(wine_name_eng__iconteaints = search_keyword)
        #
        # end = time()
        #
        # print(end - start)

        # return JsonResponse({"result":result}, status = 200)
        return JsonResponse({"result": result}, status=200)


class StoreMyPageView(View):
    def get(self, request):
        user_id = "test2222"
        template = loader.get_template("store/storeMyPage.html")
        context = {"user_id": user_id}

        return HttpResponse(template.render(context, request))
