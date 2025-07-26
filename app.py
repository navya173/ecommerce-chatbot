from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load correct CSV files (based on actual filenames)
products = pd.read_csv("data/products.csv")
orders = pd.read_csv("data/orders.csv")
order_details = pd.read_csv("data/order_items.csv")

# Endpoint: Top 5 most sold products
@app.route('/top-products')
def top_products():
    top = order_details.groupby("product_id")["quantity"].sum().sort_values(ascending=False).head(5)
    top = top.reset_index()
    top = top.merge(products, on="product_id", how="left")[["product_id", "product_name", "quantity"]]
    return jsonify(top.to_dict(orient="records"))

# Endpoint: Order status by ID
@app.route("/order-status/<int:order_id>")
def order_status(order_id):
    order = orders[orders["order_id"] == order_id]
    if not order.empty:
        return jsonify(order.iloc[0].to_dict())
    else:
        return jsonify({"error": "Order ID not found"}), 404

# Endpoint: Product stock check
@app.route("/stock/<product_name>")
def product_stock(product_name):
    prod = products[products["product_name"].str.lower() == product_name.lower()]
    if not prod.empty:
        return jsonify({"stock": int(prod.iloc[0]["stock"])})
    else:
        return jsonify({"error": "Product not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
