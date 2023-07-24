from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template import loader
from django.http.response import HttpResponse, JsonResponse
from store.models import WinStore, WinSell
from detail.models import WinWine
from django.utils.dateformat import DateFormat
from datetime import datetime
from store.db_access.query_set import (
    insert_store_info,
    insert_sell_info,
    delete_store_info,
    check_store_product_info,
    check_store_regist_number,
    get_store_info,
    get_detail_sell_list,
)
from django.db.utils import DatabaseError


# Create your views here.


class StoreRegistrationView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        user_id = "test5555"
        print(check_store_product_info(user_id=user_id))
        if check_store_product_info(user_id=user_id):
            return redirect("storeMyPage")

        else:
            template = loader.get_template("store/storeRegistration.html")
            context = {"user_id": user_id}
            return HttpResponse(template.render(context, request))

    def post(self, request):
        user_id = request.POST.get("userId", None)
        main_address = request.POST.get("mainAddress", None)
        detail_address = request.POST.get("detailAddress", None)
        store_name = request.POST.get("storeName", None)
        store_reg_num = request.POST.get("storeRegNum", None)
        store_email = request.POST.get("storeEmail")
        store_map_url = request.POST.get("storeMapUrl", None)

        store_address = main_address + "@" + detail_address
        # 파이썬에서도 정규식 검증하고 db insert하기

        try:
            insert_store_info(
                user_id=user_id,
                store_address=store_address,
                store_name=store_name,
                store_reg_num=store_reg_num,
                store_email=store_email,
                store_map_url=store_map_url,
            )

        except DatabaseError:
            redirect("storeError")

        return redirect("productAddition")


class CheckStoreRegistNumberView(View):
    def get(self, request):
        reg_num = request.GET.get("regnum", None)

        if reg_num == None:
            return JsonResponse({"result": "문제가 발생했습니다 잠시 후 다시 시도해주세요"}, status=200)

        else:
            result = check_store_regist_number(reg_num=reg_num)

            if result == True:
                return JsonResponse(
                    {"result": "유효한 사업자 등록번호입니다", "code": "1"}, status=200
                )

            else:
                return JsonResponse(
                    {"result": "이미 등록된 사업자 등록번호입니다", "code": "-1"}, status=200
                )


class ProductAdditionView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        user_id = "test5555"

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
        user_id = "test5555"
        store_id = request.POST.get("storeId", None)
        wine_ids = request.POST.getlist("wineId", None)
        sell_prices = request.POST.getlist("sellPrice", None)
        sell_promots = request.POST.getlist("sellPromot", None)
        sell_state = 1
        btn_cancel_regist = request.POST.get("btnCancelRegist", None)
        btn_product_add = request.POST.get("btnProductAdd", None)
        btn_back = request.POST.get("btnBack", None)
        current_time = DateFormat(datetime.now()).format("Y-m-d H:i:s")

        if btn_product_add != None:
            print("product add")
            try:
                insert_sell_info(
                    user_id,
                    store_id,
                    wine_ids,
                    current_time,
                    sell_prices,
                    sell_promots,
                    sell_state,
                )
            except DatabaseError:
                return redirect("storeError")

        elif btn_cancel_regist != None:
            delete_store_info(store_id=store_id)
            return redirect("storeRegistration")  # user mypage로 리다이렉트 해야함

        elif btn_back != None:
            delete_store_info(store_id=store_id)
            return redirect("storeRegistration")

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
        user_id = "test5555"
        template = loader.get_template("store/storeMyPage.html")
        context = {"user_id": user_id}

        return HttpResponse(template.render(context, request))


class SearchReceiveCodeView(View):
    def get(self, request):
        template = loader.get_template("store/searchReceiveCode.html")
        user_id = "test5555"

        context = {}
        return HttpResponse(template.render(context, request))

    # 수령코드 get 방식으로 검색할지 post 방식으로 검색할지 결정하기


class StoreInfoView(View):
    def get(self, request):
        template = loader.get_template("store/storeInfo.html")
        user_id = "test5555"
        info = get_store_info(user_id=user_id)[0]
        full_address = info.get("store_address").split("@")
        main_address = full_address[0]
        detail_address = full_address[1]

        context = {
            "info": info,
            "main_address": main_address,
            "detail_address": detail_address,
        }
        return HttpResponse(template.render(context, request))


class StoreInfoModificationView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return View.dispatch(self, request, *args, **kwargs)

    def get(self, request):
        template = loader.get_template("store/storeInfoModification.html")
        user_id = "test5555"
        info = get_store_info(user_id=user_id)[0]
        full_address = info.get("store_address").split("@")
        main_address = full_address[0]
        detail_address = full_address[1]

        context = {
            "info": info,
            "main_address": main_address,
            "detail_address": detail_address,
        }
        return HttpResponse(template.render(context, request))

    def post(self, request):
        user_id = "test5555"
        main_address = request.POST.get("mainAddress", None)
        detail_address = request.POST.get("detailAddress", None)
        store_name = request.POST.get("storeName", None)
        store_reg_num = request.POST.get("storeRegNum", None)
        store_email = request.POST.get("storeEmail")
        store_map_url = request.POST.get("storeMapUrl", None)

        store_address = main_address + "@" + detail_address
        # 파이썬에서도 정규식 검증하고 db insert하기

        try:
            insert_store_info(
                user_id=user_id,
                store_address=store_address,
                store_name=store_name,
                store_reg_num=store_reg_num,
                store_email=store_email,
                store_map_url=store_map_url,
            )

        except DatabaseError:
            redirect("storeError")

        return redirect("storeInfo")


class SellListView(View):
    def get(self, request):
        user_id = "test6666"
        page_num = request.GET.get("pageNum", 1)
        template = loader.get_template("store/sellList.html")
        list_count = 30
        end = int(list_count) * int(page_num)
        start = end - 29
        # list_info = 



class SellDetailListView(View):
    def get(self, request):
        user_id = "test6666"
        page_num = request.GET.get("pageNum", 1)
        template = loader.get_template("store/sellDetailList.html")
        list_count = 30
        end = int(list_count) * int(page_num)
        start = end - 29
        list_info = get_detail_sell_list(user_id=user_id, start = start, end = end)
        # detail_sell_list()
        list_length = list_info[0]
        detail_sell_list = list_info[1]
        pages = (list_length // list_count) + 1
        print(list_info[0])
        print(list_count)
        
        
        pages = [i + 1 for i in range(pages)]

        context = {"list": detail_sell_list,
                   "pages": pages}
        return HttpResponse(template.render(context, request))
    
    
    
class ProductListView(View):
    def get(self, request):
        template = loader.get_template("store/productList.html")
      #  WinSell/WinWine 해내야함
