from flask import Blueprint, request, jsonify, render_template, redirect, flash

from app.stock_code import stock_growth, stock_time, stock_time

stock_routes = Blueprint("stock_routes", __name__)

@stock_routes.route("/stock/summary.json")
def stock_summary_api():
    print("STOCK SUMMARY (API)...")
    print("URL PARAMS:", dict(request.args))

    symbol = request.args.get("ticker_symbol") or "MSFT"
    shares = request.args.get("stock_shares") or "1"

    results = stock_growth(symbol= symbol, shares= shares)
    if results:
        return jsonify(results)
    else:
        return jsonify({"message":"Invalid Values. Please try again."}), 404

def stock_trends_api():
    print("STOCK TRENDS (API)...")
    print("URL PARAMS:", dict(request.args))

    symbol = request.args.get("ticker_symbol") or "MSFT"
    shares = request.args.get("stock_shares") or "1"

    results = stock_time(symbol= symbol, shares= shares)
    if results:
        return jsonify(results)
    else:
        return jsonify({"message":"Invalid Values. Please try again."}), 404

@stock_routes.route("/stock/form")
def stock_form():
    print("STOCK FORM...")
    return render_template("stock_form.html")

@stock_routes.route("/stock/trends/form")
def stock_trends_form():
    print("STOCK TRENDS FORM...")
    return render_template("stock_trends_form.html")

@stock_routes.route("/stock/summary", methods=["GET", "POST"])
def stock_summary():
    print("STOCK SUMMARY...")

    if request.method == "GET":
        print("URL PARAMS:", dict(request.args))
        request_data = dict(request.args)
    elif request.method == "POST": # the form will send a POST
        print("FORM DATA:", dict(request.form))
        request_data = dict(request.form)

    symbol = request_data.get("ticker_symbol") or "MSFT"
    shares = request_data.get("stock_shares") or "1"

    results = stock_growth(symbol=symbol, shares=shares)
    if results:
        flash(f"Stock Summary Generated Successfully!", "success")
        return render_template("stock_summary.html", symbol=symbol, shares=shares, results=results)
    else:
        flash(f"Symbol or Share Error. Please try again!", "danger")
        return redirect("/stock/form")

@stock_routes.route("/stock/trends", methods=["GET", "POST"])
def stock_trends():
    print("CLOSING PRICE OVER THE PAST MONTH...")

    if request.method == "GET":
        print("URL PARAMS:", dict(request.args))
        request_data = dict(request.args)
    elif request.method == "POST": # the form will send a POST
        print("FORM DATA:", dict(request.form))
        request_data = dict(request.form)

    symbol = request_data.get("ticker_symbol") or "MSFT"
    shares = request_data.get("stock_shares") or "1"

    results = stock_time(symbol=symbol, shares=shares)
    if results:
        flash(f"Stock Summary Generated Successfully!", "success")
        return render_template("stock_trends.html", symbol=symbol, shares=shares, results=results)
    else:
        flash(f"Symbol or Share Error. Please try again!", "danger")
        return redirect("/stock/trends/form")