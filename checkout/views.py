from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from checkout.models import Order
from course.models import Course
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def success(request):
    return render(request, "success.html")


def cancel(request):
    return render(request, "cancel.html")


class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        try:
            # Fetch the course object
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response(
                {"error": "Course doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            # Check if the order already exists
            order = Order.objects.filter(course=course, user=user).first()
            # check if the order is already paid
            if order and order.status == 1:
                return Response(
                    {"detail": "Order already paid"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if order:
                # If the order exists, retrieve the session ID from the order and get session details from Stripe
                if order.stripe_session_id:
                    try:
                        # Retrieve the session from Stripe using the session_id stored in the order
                        stripe_session = stripe.checkout.Session.retrieve(
                            order.stripe_session_id
                        )
                        return Response(
                            {
                                "data": stripe_session,
                                "detail": "Order already exists with Stripe session data",
                            },
                            status=status.HTTP_200_OK,
                        )
                    except stripe.error.StripeError as stripe_error:
                        return Response(
                            {"error": f"Stripe error: {stripe_error.user_message}"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    return Response(
                        {"error": "Order exists but no Stripe session found."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            else:
                # Create a new order if it does not exist
                amount = course.price
                order = Order.objects.create(
                    course=course,
                    user=user,
                    total_amount=amount,
                    status=0,
                )

                # Create a new checkout session with Stripe
                checkOutSession = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    line_items=[
                        {
                            "price_data": {
                                "currency": "usd",
                                "product_data": {
                                    "name": course.name,
                                    "description": course.description,
                                },
                                "unit_amount": int(course.price * 100),
                            },
                            "quantity": 1,
                        },
                    ],
                    metadata={
                        "order_num": str(order.id),
                        "user": str(user.id),
                        "order_id": str(order.id),
                    },
                    payment_intent_data={
                        "metadata": {
                            "order_num": str(order.id),
                            "user": str(user.id),
                            "order_id": str(order.id),
                        },
                    },
                    mode="payment",
                    success_url=settings.FRONTEND_URL + "api/checkout/success",
                    cancel_url=settings.FRONTEND_URL + "api/checkout/cancel",
                )

                # Save the Stripe session ID in the order
                order.stripe_session_id = checkOutSession.id
                order.save()
                # checkOutSession.modify(order_id=order.id)

                return Response(
                    {"data": checkOutSession, "detail": "Order created successfully"},
                    status=status.HTTP_201_CREATED,
                )

        except Exception as e:
            print("Error:", str(e))
            return Response(
                {"error": f"Something went wrong: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


@csrf_exempt
@api_view(["POST"])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        print("error STRIPEONE", e)
        # Invalid payload
        return Response(
            {"error": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST
        )
    except stripe.error.SignatureVerificationError as e:
        print("error STRIPETWO", e)
        # Invalid signature
        return Response(
            {"error": "Invalid signature "}, status=status.HTTP_400_BAD_REQUEST
        )

    # Handle the event
    if event["type"] == "checkout.session.completed":
        print("Checkout session completed!")
        print('event["data"]', event["data"])
        print('event["data"]["object"]', event["data"]["object"])
        session = event["data"]["object"]
        handle_checkout_session(session)

    return Response(status=status.HTTP_200_OK)


def handle_checkout_session(session):
    try:
        order_id = session["metadata"].get("order_id")
        print("metadata", session["metadata"])
        if not order_id:
            raise ValueError("order_id not found in session metadata")

        order = Order.objects.get(id=order_id)
        # Mark the order as paid (status=1 means paid and status=0 means unpaid)
        order.status = 1
        order.save()
    except Order.DoesNotExist:
        print(f"Order with ID {order_id} does not exist.")
    except Exception as e:
        print(f"Error handling checkout session: {str(e)}")
