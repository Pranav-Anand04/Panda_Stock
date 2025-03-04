from flask import Blueprint, jsonify, request
from utils import fetch_stock_data
from models import db
from models.user_model import User 
from models.user_stock_model import UserStock, Stock

stock_blueprint = Blueprint('stock', __name__)

@stock_blueprint.route('/stock/<symbol>', methods=['GET'])
def get_stock_details(symbol):
    stock_data = fetch_stock_data(symbol)
    if "error" in stock_data:
        return jsonify({"message": stock_data["error"]}), 400
    return jsonify(stock_data), 200

@stock_blueprint.route('/transaction/buy', methods=['POST'])
def buy_stock():
    data = request.get_json()
    user_id = data.get('user_id')
    symbol = data.get('symbol')
    quantity = data.get('quantity')

    # Input validation
    if not user_id or not symbol or not quantity or quantity <= 0:
        return jsonify({"message": "Invalid input"}), 400

    # Fetch stock data
    stock_data = fetch_stock_data(symbol)
    if not stock_data:
        return jsonify({"message": "Invalid stock symbol"}), 400

    price = float(stock_data['price'])
    total_cost = price * quantity

    # Get user and verify buying power
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    if user.buyers_power < total_cost:
        return jsonify({"message": "Insufficient buying power"}), 400

    # Deduct buying power and add to portfolio
    user.buyers_power -= total_cost
    stock = Stock.query.filter_by(symbol=symbol).first()
    if not stock:
        stock = Stock(symbol=symbol, name=stock_data['company_name'])
        db.session.add(stock)
        db.session.commit()

    user_stock = UserStock.query.filter_by(user_id=user_id, stock_id=stock.id).first()
    if user_stock:
        user_stock.quantity += quantity
    else:
        user_stock = UserStock(user_id=user_id, stock_id=stock.id, quantity=quantity, purchase_price=price)
        db.session.add(user_stock)

    db.session.commit()
    return jsonify({"message": f"Successfully bought {quantity} shares of {symbol}"}), 200

@stock_blueprint.route('/transaction/sell', methods=['POST'])
def sell_stock():
    data = request.get_json()
    user_id = data.get('user_id')
    symbol = data.get('symbol')
    quantity = data.get('quantity')

    if not user_id or not symbol or not quantity or quantity <= 0:
        return jsonify({"message": "Invalid input"}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    stock = Stock.query.filter_by(symbol = symbol).first()
    if not stock:
        return jsonify({"message": f"Stock {symbol} not found"}), 404
    
    user_stock = UserStock.query.filter_by(user_id=user_id, stock_id=stock.id).first()
    if not user_stock or user_stock.quantity < quantity:
        return jsonify({"message": "Insufficient shares to sell"}), 400

    # Fetch stock price
    stock_data = fetch_stock_data(symbol)
    if not stock_data:
        return jsonify({"message": "Unable to fetch stock data"}), 400
    
    sell_price = float(stock_data['price'])
    total_revenue = sell_price * quantity

    user_stock.quantity -= quantity
    if UserStock.quantity == 0:
        db.session.delete(user_stock)

    user.buyers_power += total_revenue
    db.session.commit()

    return jsonify({"message": f"Successfully sold {quantity} shares of {symbol} for ${total_revenue:.2f}"}), 200

@stock_blueprint.route('/user/portfolio', methods=['GET'])
def get_user_portfolio():
    user_id = request.args.get('user_id')
    if not user_id: 
        return jsonify({"message": "User ID is required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    user_stocks = UserStock.query.filter_by(user_id=user_id).all()
    portfolio = []

    for user_stock in user_stocks:
        stock = Stock.query.get(user_stock.stock_id)
        stock_data = fetch_stock_data(stock.symbol)
        if not stock_data:
            continue

        current_price = stock_data['price']
        profit_or_loss = (current_price - user_stock.purchase_price) * user_stock.quantity

        portfolio.append({
            "id": stock.id,
            "name": stock.name,
            "symbol": stock.symbol,
            "shares": user_stock.quantity,
            "current_price": current_price,
            "profit_or_loss": profit_or_loss,
        })

    return jsonify({"portfolio": portfolio}), 200

