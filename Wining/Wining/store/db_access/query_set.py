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
    
    
    
    
    try:
        store = WinStore.objects.get(user_id = user_id)
        print("첫번째 store", store)
        # store = store[0]
        print("두번째 store", store)
        print("store_name", store_name)
        print("store.store_name", store.store_name)
        store.store_id = store.store_id
        store.store_address=store_address
        store.store_name=store_name
        store.store_reg_num=store_reg_num
        store.store_email=store_email
        
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
        print("왜 나와?")
        store_map_url = store_map_url
        print("왜 나와?2")
        win_store_url = WinStoreUrl(
            store_id=store.store_id, store_map_url=store_map_url
        )
        print("왜 나와?3")
        win_store_url.save()
        print("왜 나와?4")
        


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
    
    store_url = WinStoreUrl.objects.filter(store_id = store_id)
    if len(store_url) == 1:
        store_url.delete()
    
    store_info = WinStore.objects.filter(store_id = store_id)
    store_info.delete()
        
def check_store_product_info(user_id: str):
    
    info = WinSell.objects.select_related("store").filter(store__user_id = user_id).values("sell_id").first()
    
    
    
    
    
    