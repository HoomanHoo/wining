from store.models import WinStore, WinStoreUrl, WinSell
from django.db import transaction
from user.models import WinUser, WinUserGrade


@transaction.atomic
def insert_store_info(
    user_id: str,
    store_address: str,
    store_name: str,
    store_reg_num: str,
    store_email: str,
    store_map_url: str,
) -> None:
    store = WinStore(
        user_id=user_id,
        store_address=store_address,
        store_name=store_name,
        store_reg_num=store_reg_num,
        store_email=store_email,
    )

    store.save()

    if store_map_url != "" or store_map_url != None:
        store_map_url = store_map_url
        win_store_url = WinStoreUrl(
            store_id=store.store_id, store_map_url=store_map_url
        )
        win_store_url.save()
    else:
        print("No URL!")


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
