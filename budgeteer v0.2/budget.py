"""
Budgeteer v0.2

Created by Joniel Augustine Jerome
01/11/2024

This module defines the Budgeter program that allows users to track
their expenses.

"""

# standard imports
from datetime import date

# external imports
from flask import Flask, request, render_template

# local imports
from structures import Product, Merchant, Purchase, Transaction


# local data structures
products = {}
merchants = {}
categories = set()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    """
    This method renders the main landing page of the Budgeteer program.

    """
    return render_template("home.html")



@app.route("/add_transaction", methods=["GET"])
def add_transaction():
    """
    This method processes and renders a web form allowing users to
    input a transaction that they completed and the purchases 
    associated with it.

    """
    prods = [p.lower() for p in products]
    merchs = [str(m) for m in merchants]
    cats = list(categories)
    cats_map = {u : v.category for u, v in products.items()}
    return render_template("transaction.html",
        existing_product_names=prods, merchants=merchs,
        today=date.today(), categories=cats, cats_map=cats_map)

@app.route("/test", methods=["GET"])
def test():
    return render_template("receipt.html")


@app.route("/add_transaction", methods=["POST"])
def process_transaction():
    """
    This method processes and renders a web form allowing users to
    input a transaction that they completed and the purchases 
    associated with it.

    """
    product_names = request.form.getlist("product_name[]")
    if product_names[0] != "":
        merchant = request.form["merchant"].upper()
        if merchant not in merchants:
            merchants[merchant] = Merchant(merchant)
        merchant = merchants[merchant]
        dot = request.form["date"]
        product_names = request.form.getlist("product_name[]")
        total_prices = request.form.getlist("total_price[]")
        cats = request.form.getlist("cat[]")
        purchases = []
        for i, p in enumerate(product_names):
            p = p.upper()
            t = float(total_prices[i])
            c = cats[i].upper()
            categories.add(c)
            if p in products:
                pass
            elif p[:-1] in products:
                p = p[:-1]
            elif p[:-2] in products:
                p = p[:-2]
            elif p + "S" in products:
                products[p] = products[p + "S"]
                del products[p + "S"]
            elif p + "ES" in products:
                products[p] = products[p + "ES"]
                del products[p + "ES"]
            else:
                products.update({p: Product(p, c)})
            purchases.append(Purchase(products[p], merchant, t, dot))
        Transaction(merchant, purchases, dot)
    save_all()

    print("\n\nSYSTEM STATUS:")
    for p in products.values():
        print(p)
    return render_template("receipt.html", merchant=merchant.name, date=dot, products=product_names)


def save_all():
    """
    This method saves all data to the associated data files.

    """
    with open("./static/data/products.csv", "w", encoding='utf-8') as f1:
        for p in products.values():
            f1.write(p.file_format())
        f1.close()

    with open("./static/data/merchants.csv", "w", encoding='utf-8') as f2:
        for m in merchants:
            f2.write(m + "\n")
        f2.close()


def extract_all():
    """
    This method loads all data from the associated data files.

    """
    try:
        with open("./static/data/products.csv", "r", encoding='utf-8') as f1:
            lines = f1.readlines()
            for l in lines:
                l = l.strip().split(",")
                if l[0] == "":
                    continue
                name = l[0].strip().upper()
                category = l[1].strip().upper()
                categories.add(category)
                products[name.upper()] = Product(name, category)
            f1.close()

        with open("./static/data/merchants.csv", "r", encoding='utf-8') as f2:
            lines = f2.readlines()
            for l in lines:
                if l[0] == "":
                    continue
                l = l.strip().split(",")
                name = l[0].strip().upper()
                merchants[name.upper()] = Merchant(name)
            f2.close()
    except FileNotFoundError:
        print("File not found!")


if __name__ == "__main__":
    extract_all()
    app.run(host='0.0.0.0', port=8080, debug=False)
