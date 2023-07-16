from products.models import Product


class Cart:
    def __int__(self, request):
        """
        initialize the cart
        """
        self.request = request

        self.session = request.session

        cart = self.session.get("cart")

        if not cart:
            cart = self.session["cart"] = {}

        self.cart = cart

    def add(self, product, quantity=1):
        """
        Add a product to the cart if it exists
        """
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer")

        if quantity < 1:
            raise ValueError("Quantity must be greater than zero")

        if product.id not in self.cart:
            self.cart[product.id] = {"quantity": quantity}
        else:
            self.cart[product.id]["quantity"] += quantity

        self.save()

    def remove(self, product):
        """
        Remove a product from the cart
        """
        if product.id in self.cart:
            del self.cart[product.id]

        self.save()

    def save(self):
        """
        Save the cart to the session
        """
        self.session.modified = True

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database
        """
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]["product_obj"] = product

        for item in cart.values():
            # item["total_price"] = item["product"].price * item["quantity"]

            yield item

    def __len__(self):
        return len(self.cart.keys())

    def clear(self):
        del self.session["cart"]
        self.save()

    def get_total_price(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        return sum(product.price for product in products)
