import uuid
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
import math
from datetime import datetime, time

# Mapping to store receipt_id and total points
receipts_data = {}

# Class to handle receipt processing and point computation
class ProcessReceiptsView(APIView):
    
    # POST method to process a receipt, validate it, and then compute its total points
    def post(self, request):
        receipt = request.data

        # Check if receipt is valid
        is_valid, error_message = self.check_receipt_validity(receipt)

        if not is_valid:
            return JsonResponse({"error": error_message}, status = 400)

        # Generate a unique receipt ID and compute points
        receipt_id = str(uuid.uuid4())
        total_points = self.compute_points(receipt)

        # Store the computed total points with the associated receipt ID
        receipts_data[receipt_id] = total_points

        return JsonResponse({"id" : receipt_id})

    # Helper method to ensure that the receipt is valid and can be processed accurately
    def check_receipt_validity(self, receipt):
        
        required_fields = ["retailer", "purchaseDate", "purchaseTime", "items", "total"]

        # Check that all required fields are present
        for required_field in required_fields:
            if required_field not in receipt:
                return False, f"Missing required field: {required_field}"

        allItems = receipt["items"]
        recordedTotal = float(receipt["total"])
        computedTotal = round(
            sum(
                float(item["price"]) 
                for item in allItems
            ),
            10
        )
        purchaseDate = receipt["purchaseDate"]
        purchaseTime = receipt["purchaseTime"]

        # Validate that the recorded total matches the actual computed total of the items
        if recordedTotal != computedTotal:
            return False, "Recorded total value is inaccurate"
        
        # Validate the purchase date and time formats
        try:
            datetime.strptime(purchaseDate, "%Y-%m-%d")
        except ValueError:
            return False, "Invalid date format for 'purchaseDate'. Expected YYYY-MM-DD."

        try:
            datetime.strptime(purchaseTime, "%H:%M")
        except ValueError:
            return False, "Invalid time format for 'purchaseTime'. Expected HH:MM."

        return True, ""

    # Helper method to compute points based on receipt data
    def compute_points(self, receipt):
        
        pointsCount = 0
        retailerName = receipt["retailer"]
        total = float(receipt["total"])
        allItems = receipt["items"]
        purchaseDate = receipt["purchaseDate"]
        purchaseTime = receipt["purchaseTime"]

        # 1 point for every alphanumeric character in the retailer name
        pointsCount += sum(c.isalnum() for c in retailerName)

        # 50 points if total is a round dollar amount
        pointsCount += 50 if total.is_integer() else 0

        # 25 points if the total is a multiple of 0.25
        pointsCount += 25 if round(total % 0.25, 10) == 0 else 0

        # 5 points for every pair of items on the receipt
        itemPairs = len(allItems) // 2
        pointsCount += 5 * itemPairs

        for item in allItems:
            
            trimmedDesc = item["shortDescription"].strip()
            itemPrice = item["price"]

            if(len(trimmedDesc) % 3 == 0):
                pointsCount += int(math.ceil(float(itemPrice) * 0.2))

        # This program was not generated using a LLM so 0 points added
        pointsCount += 0

        # 6 points if the day in the purchase date is odd
        purchase_date = datetime.strptime(purchaseDate, "%Y-%m-%d")
        pointsCount += 6 if purchase_date.day % 2 == 1 else 0

        purchase_time = datetime.strptime(purchaseTime, "%H:%M").time()
        earliest_time = time(14,0)
        latest_time = time(16,0)

        # 10 points if the time of purchase is after 2:00 PM and before 4:00 PM
        pointsCount += 10 if earliest_time < purchase_time < latest_time else 0

        return pointsCount

# Class to handle the fetching of computed points for a given receipt ID
class GetReceiptPointsView(APIView):

    # GET method to return the points for a specific receipt ID
    def get(self, request, receipt_id):

        if(receipt_id in receipts_data):
            return JsonResponse({"points": receipts_data[receipt_id]})

        return JsonResponse({"error": "Receipt not found"}, status=404)
        


