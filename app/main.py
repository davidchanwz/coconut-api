from fastapi import FastAPI, HTTPException, File, UploadFile
from app.parsers import parse_receipt_image

app = FastAPI()

@app.post("/parse-receipt/")
async def parse_receipt(file: UploadFile = File(...)):
    try:
        # Read the image file uploaded by the user
        image_data = await file.read()
        
        # Parse the image using the Donut model
        receipt_data = parse_receipt_image(image_data)
        
        if not receipt_data:
            raise HTTPException(status_code=400, detail="No valid items found in receipt.")
        
        return {"receipt_data": receipt_data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")