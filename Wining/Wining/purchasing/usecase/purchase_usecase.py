
def calc(self,
        user: str,
        product_infos: list,
        quantity_per_ones: list,
        price_per_ones: list,
        current_time: str,
        user_point: int,
        all_price: int,
        cart_info: str = None,) -> dict or None:
    """
    매개변수로 입력 받은 값을 연산을 해서 데이터를 반환해주는 함수입니다
    """
    print("calcurating...")
    _quantity_all = 0

    for i in range(len(price_per_ones)):
        _quantity_all += int(quantity_per_ones[i])
    if int(user_point) >= int(all_price):
        user_point = int(user_point) - int(all_price)


        result = {
            "user": user,
            "quantity_all": _quantity_all,
            "price_all": all_price,
            "current_time": current_time,
            "product_infos": product_infos,
            "quantity_per_ones": quantity_per_ones,
            "price_per_ones": price_per_ones,
            "user_point": user_point,
        }
        
        if self.cart_info != None:
            result["cart_info"] = cart_info
            print("product_info: ", type(result["product_infos"]))

    else:
        result = None

   
    return result


def create_receive_code(self, purchase_info: str) -> str:
    """
    receive_code는 n자리의 purchase_detail_info를 16진수화 한 것과 (10 - n)자리의 무작위 라틴문자(대소문자 구별 없음),
    그리고 한 자리의 n 값으로 이루어져 있습니다
    """
    
    import string
    import random

    total_length = 10

    purchase_info = purchase_info
    id_length = len(purchase_info)
    random_key = ""
    
    for i in range(total_length - id_length):
        random_key += str(random.choice(string.ascii_letters))

    hex_base = hex(int(purchase_info))
    receive_code = hex_base + random_key + str(id_length)
    
    return receive_code
    
    
def encrypt_receive_code(receive_code: str) -> str:  
    """
    receive_code를 base64로 한 번, AES128 알고리즘으로 다시 한 번 암호화 해서 리턴합니다
    """  
    
    import base64
    from Crypto.Util.Padding import pad
    from Crypto.Cipher import AES
    
    key = "djangoProjectWiningByaws2"
    # padding(바이트 크기 맞추기 위한 의미 없는 값)설정
    BS = 16  # 바이트 사이즈
    
    # 암호화
    print("enc:value:  ", receive_code)
    m1 = base64.b64encode(receive_code.encode("utf-8"))
    what = AES.new(pad(key.encode(), BS), AES.MODE_ECB)
    m2 = what.encrypt(pad(m1.decode("utf-8").encode(), BS))
    enc_receive_code = str(m2)
    
    return enc_receive_code
    
    
def decrypt_receive_code(self, enc_receive_code: str) ->str: 
    """
    암호화된 receive_code를 AES128 알고리즘으로 한 번, base64로 다시 한 번 복호화 한 뒤,
    16진수화 된 purchase_detail_info를 10진수화 해서 리턴합니다
    """
    
    import base64
    from Crypto.Util.Padding import pad, unpad
    from Crypto.Cipher import AES
    
    total_length = 10
    BS = 16  # 바이트 사이즈
    key = "djangoProjectWiningByaws2"   
    # # 복호화
    cipher = AES.new(pad(key.encode(), BS), AES.MODE_ECB)
    m3 = cipher.decrypt(enc_receive_code)
    m4 = unpad(m3, BS).decode("utf-8")
    m5 = base64.b64decode(m4).decode("utf-8")
    ren = m5[-1:]
    m6 = m5[: -(total_length - int(ren) + 1)]
    purchase_info = int(m6, 16)
    print("purchase_info: ", purchase_info)
    return purchase_info
            

def formating(
    user: str,
    product_info: str,
    quantity: int,
    price_per_one: int,
    wine_name: str,
    wine_image: str,
    identifier: str = None,
) -> dict:
    dto = {
        "user": user,
        "identifier": identifier,
        "product_info": product_info,
        "quantity": quantity,
        "price_per_one": price_per_one,
        "purchase_price": int(price_per_one) * int(quantity),
        "wine_image": wine_image,
        "wine_name": wine_name,
    }
    return dto
