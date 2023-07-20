class PurchaseSequence:
    """
    "이것은 구매 기능 동작을 위한 클래스 입니다 매개변수 값으로 user, product_info, quantity_per_one, price_per_one을 입력 받습니다"
    """

    def echo(self):
        return "이것은 구매 기능 동작을 위한 함수 입니다 매개변수 값으로 user, product_info, quantity_per_one, price_per_one을 입력 받습니다"

    def __init__(
        self,
        user: str,
        product_infos: list,
        quantity_per_ones: list,
        price_per_ones: list,
        current_time: str,
        user_point: int,
        all_price: int,
        cart_info: str = None,
    ):
        self.user = user
        self.product_infos = product_infos
        self.quantity_per_ones = quantity_per_ones
        self.price_per_ones = price_per_ones
        self.current_time = current_time
        self.user_point = user_point
        self.price_all = all_price
        self.cart_info = cart_info

    def calc(self) -> dict or None:
        """
        매개변수로 입력 받은 값을 연산을 해서 데이터를 반환해주는 함수입니다
        """
        print("calcurating...")
        _quantity_all = 0
        print(self.price_all)
        print("cart_id", self.cart_info)
        for i in range(len(self.price_per_ones)):
            _quantity_all += int(self.quantity_per_ones[i])
        if int(self.user_point) >= int(self.price_all):
            user_point = int(self.user_point) - int(self.price_all)
            print("user_point:", user_point)

            result = {
                "user": self.user,
                "quantity_all": _quantity_all,
                "price_all": self.price_all,
                "current_time": self.current_time,
                "product_infos": self.product_infos,
                "quantity_per_ones": self.quantity_per_ones,
                "price_per_ones": self.price_per_ones,
                "user_point": user_point,
            }
            
            if self.cart_info != None:
                result["cart_info"] = self.cart_info
                print("product_info: ", type(result["product_infos"]))

        else:
            result = None

       
        return result


class CartSequence:
    pass


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
