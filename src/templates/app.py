from random_transaction import send_random_abandonned_cart
from flask import Flask, jsonify, render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/abandoned-cart')
def abandoned_cart():
    cart_items = send_random_abandonned_cart()
    return render_template('abandoned_cart.html', cart_items=cart_items)
    

if __name__ == '__main__':
    app.run(debug=True)


