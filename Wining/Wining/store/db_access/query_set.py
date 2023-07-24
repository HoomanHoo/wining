from store.models import WinStore, WinStoreUrl, WinSell
from django.db import transaction
from user.models import WinUser, WinUserGrade
from django.db.models.query import QuerySet, Prefetch
from django.db.models import F

@transaction.atomic
def insert_store_info(
    user_id: str,
    store_address: str,
    store_name: str,
    store_reg_num: str,
    store_email: str,
    store_map_url: str,
) -> None:
    try:
        store = WinStore.objects.get(user_id=user_id)

        # store = store[0]

        store.store_id = store.store_id
        store.store_address = store_address
        store.store_name = store_name
        store.store_reg_num = store_reg_num
        store.store_email = store_email

    except:
        store = WinStore(
            user_id=user_id,
            store_address=store_address,
            store_name=store_name,
            store_reg_num=store_reg_num,
            store_email=store_email,
        )

    store.save()

    if store_map_url == "":
        print("No URL!")

    else:
        store_map_url = store_map_url
        win_store_url = WinStoreUrl(
            store_id=store.store_id, store_map_url=store_map_url
        )
        win_store_url.save()


@transaction.atomic
def insert_sell_info(
    user_id: str,
    store_id: str,
    wine_ids: list,
    current_time: str,
    sell_prices: list,
    sell_promots: list,
    sell_state: int,
) -> None:
    win_sells = []
    for i in range(len(wine_ids)):
        win_sell = WinSell(
            store_id=store_id,
            wine_id=wine_ids[i],
            sell_reg_time=current_time,
            sell_price=sell_prices[i],
            sell_promot=sell_promots[i],
            sell_state=sell_state,
        )
        win_sells.append(win_sell)

    WinSell.objects.bulk_create(win_sells)
    win_user = WinUser.objects.get(user_id=user_id)
    win_user.user_grade = WinUserGrade.objects.get(user_grade=2)
    win_user.save()


def delete_store_info(store_id: str) -> None:
    store_url = WinStoreUrl.objects.filter(store_id=store_id)
    if len(store_url) == 1:
        store_url.delete()

    store_info = WinStore.objects.filter(store_id=store_id)
    store_info.delete()


def check_store_product_info(user_id: str) -> dict or None:
    info = (
        WinSell.objects.select_related("store")
        .filter(store__user_id=user_id)
        .values("sell_id")
        .first()
    )


def check_store_regist_number(reg_num: str) -> bool:
    result = (
        WinStore.objects.filter(store_reg_num=reg_num).values("store_reg_num").count()
    )

    if result == 0:
        return True
    else:
        return False


def get_store_info(user_id: str) -> QuerySet:
    store_info = (
        WinStore.objects.filter(user_id=user_id)
        .prefetch_related("storeUrl")
        .values(
            "store_id",
            "user_id",
            "store_address",
            "store_name",
            "store_reg_num",
            "store_email",
            "storeUrl__store_map_url",
        )
    )

    return store_info


def get_sell_list(user_id: str, start: int, end: int):
    store_id = WinStore.objects.get(user_id=user_id)
    sell_list = (
# WinSell.objects.filter(store_id=50).prefetch_related("winpurchasedetail_set", "winpurchasedetail_set__purchase").values("winpurchasedetail__purchase__purchase_id", "winpurchasedetail__purchase__purchase_time",).exclude(sell_id in F(WinSell.objects.exclude(store_id = 50)))
        
    )
    # group_detail_infos =  


def get_detail_sell_list(user_id: str, start: int, end: int):
    store_id = WinStore.objects.get(user_id=user_id)
    list_info = []
    detail_sell_list = (
        WinSell.objects.prefetch_related("winpurchasedetail_set")
        .select_related("wine")
        .filter(store_id=store_id)
        .values(
            "winpurchasedetail__purchase_detail_id",
            "wine__wine_name",
            "winpurchasedetail__purchase_det_number",
            "winpurchasedetail__purchase_det_price",
            "winpurchasedetail__purchase_det_state",
        )
        .order_by("-winpurchasedetail__purchase_detail_id")
    )
    list_info.append(detail_sell_list.count())
    list_info.append(detail_sell_list[start:end])

    return list_info
