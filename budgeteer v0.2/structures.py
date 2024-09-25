"""
Structures for Budgeteer

Created by Joniel Augustine Jerome
01/09/2024

This module defines four structure classes for representation of data
in the Budgeteer application.

"""

class Product:
    """
    This class represents individual products.

    Attributes:
    - name (str) : the name of the product
    - category (str) : the budget category of the product
    - purchase_history (list) : all purchases made of the product

    """
    def __init__(self, name, category):
        """
        The constructor creates a product with a specified name and 
        belonging to a specified budget category.

        Arguments:
        - name (str) : the name of the product
        - category (str) : the budget category of the product

        """
        self.name = name.upper()
        self.category = category.upper()

        self.purchase_history = []
        self.price = 0

    def file_format(self):
        """
        This method creates a representation of the product for storing
        in a CSV file

        Returns:
        - str : the comma-separated representation of the product

        """
        return f"{self.name.lower()},{self.category}\n"

    def __str__(self):
        purchases_str = "".join([f"\t{p}\n"
            for p in self.purchase_history])
        return (
            f"{self.name} - {self.category}\n"
            f"Purchase History:\n{purchases_str}"
        )


class Merchant:
    """
    This class represents merchants from whom purchases and 
    transactions are made.

    Attributes:
    - name (str) : the name of the merchant
    - transaction (list) : all transactions associated with the merchant

    """
    def __init__(self, name):
        """
        The constructor creates a merchant with a specified name.

        Arguments:
        - name (str) :  the name of the merchant

        """
        self.name = name.upper()
        self.transactions = []

    def __str__(self):
        return self.name


class Purchase:
    """
    This class represents the purchase of a single product and the 
    associated details.

    Attributes:
    - product (Product) :  the item purchased
    - merchant (Merchant) : the seller of the purchased item
    - price (float) : the monetary amount spent on the purchase
    - date (str) : the date on which the purchase occurred

    """
    def __init__(self, product, merchant, price, date):
        """
        The constructor creates a purchase of a specified item from a
        specified merchant completed on a specified date for a specified
        monetary value

        Attributes:
        - product (Product) : the item purchased
        - merchant (Merchant) : the seller of the purchased item
        - price (float) : the monetary amount spent on the purchase
        - date (str) : the date on which the purchase occurred

        """
        self.product = product
        self.merchant = merchant
        self.price = price
        self.date = date

        product.purchase_history.append(self)
        product.price = price

    def __str__(self):
        return (
            f"{self.product.name} bought for ${self.price:.2f} " 
            f"from {self.merchant.name}"
        )


class Transaction:
    """
    This class can represent a transaction completed with a merchant.

    Attributes:
    - merchant (Merchant) : the merchant of the transaction
    - date (str) : the date on which the transaction occurred
    - total (float) : the total monetary value of the transaction
    - purchases (list) : all the purchases making up the transaction 

    """
    def __init__(self, merchant, summary, date):
        """
        The constructor creates a transaction of a specified item from a
        specified merchant completed on a specified date for a specified
        monetary value

        Attributes:
        - merchant (Merchant) : the merchant of the transaction
        - summary 
            - (float) : the total monetary value of the transaction
            - (list) : all the purchases making up the transaction 
        - date (str) : the date on which the transaction occurred

        """
        self.merchant = merchant
        self.date = date

        if isinstance(summary, list):
            self.purchases = summary
            self.add_up()
        else:
            self.purchases = None
            self.total = summary
        merchant.transactions.append(self)

    def add_up(self):
        """
        This method calculates the total monetary value of the 
        transaction from the purchases that it is composed of

        """
        self.total = 0
        for purchase in self.purchases:
            self.total += purchase.price

    def __str__(self):
        return f"{self.total:>6.2f} spent at {self.merchant}"
