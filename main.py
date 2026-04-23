from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import random
import string
import uvicorn
from datetime import datetime

app = FastAPI(title="Cloudbin Skip Bin Test API")

def generate_booking_id():
    return "SKP-" + "".join(random.choices(string.digits, k=6))

@app.get("/")
def root():
    return {"status": "Cloudbin Skip Bin API is running", "time": datetime.now().isoformat()}

@app.post("/api/pricing")
async def get_pricing(request: Request):
    body = await request.json()
    bin_size = body.get("bin_size", 4)
    suburb = body.get("suburb", "Unknown")
    waste_type = body.get("waste_type", "general")
    delivery_date = body.get("delivery_date", "")

    # Base pricing table by bin size
    pricing = {2: 220, 4: 310, 6: 395, 8: 480, 10: 560}
    price = pricing.get(int(bin_size), 310)

    # Waste type surcharge
    waste_surcharges = {
        "general": 0,
        "green": 0,
        "construction": 50,
        "mixed": 30
    }
    waste_surcharge = waste_surcharges.get(waste_type.lower(), 0)

    # Weekend surcharge
    weekend_surcharge = 0
    try:
        d = datetime.strptime(delivery_date, "%Y-%m-%d")
        if d.weekday() >= 5:
            weekend_surcharge = 40
    except:
        pass

    total = price + waste_surcharge + weekend_surcharge

    return {
        "price": total,
        "base_price": price,
        "waste_surcharge": waste_surcharge,
        "weekend_surcharge": weekend_surcharge,
        "currency": "AUD",
        "gst_included": True,
        "bin_size": bin_size,
        "suburb": suburb,
        "waste_type": waste_type,
        "available": True,
        "next_available_date": "",
        "message": f"A {bin_size}m³ bin in {suburb} for {waste_type} waste is ${total} AUD including GST."
    }

@app.post("/api/bookings")
async def create_booking(request: Request):
    body = await request.json()
    booking_id = generate_booking_id()

    print(f"\n{'='*50}")
    print(f"NEW CLOUDBIN BOOKING: {booking_id}")
    print(f"Customer:      {body.get('customer_name', '')}")
    print(f"Phone:         {body.get('phone', '')}")
    print(f"Address:       {body.get('address', '')}")
    print(f"Suburb:        {body.get('suburb', '')}")
    print(f"Bin Size:      {body.get('bin_size', '')}m³")
    print(f"Waste Type:    {body.get('waste_type', '')}")
    print(f"Delivery Date: {body.get('delivery_date', '')}")
    print(f"Pickup Date:   {body.get('pickup_date', '')}")
    print(f"{'='*50}\n")

    return {
        "booking_id": booking_id,
        "status": "confirmed",
        "message": f"Booking confirmed! Your Cloudbin reference number is {booking_id}.",
        "details": {
            "customer_name": body.get("customer_name", ""),
            "phone": body.get("phone", ""),
            "address": body.get("address", ""),
            "suburb": body.get("suburb", ""),
            "bin_size": body.get("bin_size", ""),
            "waste_type": body.get("waste_type", ""),
            "delivery_date": body.get("delivery_date", ""),
            "pickup_date": body.get("pickup_date", "")
        }
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
