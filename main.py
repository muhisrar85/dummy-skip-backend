from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import random
import string
import uvicorn
from datetime import datetime

app = FastAPI(title="Skip Bin Booking Test API")

def generate_booking_id():
    return "SKP-" + "".join(random.choices(string.digits, k=6))

@app.get("/")
def root():
    return {"status": "Skip Bin Test API is running", "time": datetime.now().isoformat()}

@app.post("/api/pricing")
async def get_pricing(request: Request):
    body = await request.json()
    bin_size = body.get("bin_size", 4)
    suburb = body.get("suburb", "Unknown")

    # Simulated pricing table
    pricing = {2: 220, 4: 310, 6: 395, 8: 480, 10: 560}
    price = pricing.get(int(bin_size), 310)

    # Weekend surcharge simulation
    delivery_date = body.get("delivery_date", "")
    surcharge = 0
    try:
        d = datetime.strptime(delivery_date, "%Y-%m-%d")
        if d.weekday() >= 5:
            surcharge = 40
    except:
        pass

    return {
        "price": price + surcharge,
        "surcharge": surcharge,
        "currency": "AUD",
        "gst_included": True,
        "bin_size": bin_size,
        "suburb": suburb,
        "available": True,
        "message": f"A {bin_size}m³ bin in {suburb} is ${price + surcharge} AUD including GST."
    }

@app.post("/api/bookings")
async def create_booking(request: Request):
    body = await request.json()

    booking_id = generate_booking_id()

    # Log the received booking
    print(f"\n{'='*50}")
    print(f"NEW BOOKING RECEIVED: {booking_id}")
    print(f"Data: {body}")
    print(f"{'='*50}\n")

    return {
        "booking_id": booking_id,
        "status": "confirmed",
        "message": f"Booking confirmed! Your reference number is {booking_id}.",
        "details": {
            "customer_name": body.get("customer_name", ""),
            "phone": body.get("phone", ""),
            "bin_size": body.get("bin_size", ""),
            "suburb": body.get("suburb", ""),
            "delivery_date": body.get("delivery_date", ""),
            "pickup_date": body.get("pickup_date", "")
        }
    }

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
