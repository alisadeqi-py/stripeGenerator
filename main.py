from flask import Flask, jsonify
import stripe

app = Flask(__name__)

# Set your Stripe API key
stripe.api_key = 'sk_test_51NVSeGLr45RTCMcPf9fT5iKSOaAoms51LqOnq6KEA0PTF9ETbtFGQm1nMqIz767ZohTsc6NPGHF4GXEjTpwoSHKt00qidiwn9J'

# Define a route to create a Checkout Session with a custom amount
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session(request):
    try:
        # Retrieve the amount from the request data
        data = request.get_json()
        amount = data['amount']

        # Create a Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Custom product',
                    },
                    'unit_amount': amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:5000/success.html',
            cancel_url='http://localhost:5000/cancel.html',
        )

        # Return the session ID to the client
        return jsonify({'sessionId': session.url})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
