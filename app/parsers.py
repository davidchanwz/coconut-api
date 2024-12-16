import logging
import io
from transformers import VisionEncoderDecoderModel, DonutProcessor
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Load the Donut model and processor
try:
    model_name = "mychen76/invoice-and-receipts_donut_v1"
    logger.info(f"Loading Donut model: {model_name}")
    model = VisionEncoderDecoderModel.from_pretrained(model_name)
    processor = DonutProcessor.from_pretrained(model_name)
    logger.info(f"Donut model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading Donut model: {str(e)}")
    raise e


def parse_receipt_image(image_data: bytes) -> dict:
    """
    Parses a receipt image using the Donut model to extract structured JSON data.

    Args:
        image_data (bytes): The image data of the receipt.
    
    Returns:
        dict: Parsed receipt as structured JSON.
    """
    try:
        # Step 1: Load and convert the image to RGB
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        logger.info("Image successfully loaded and converted to RGB.")
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return {}

    try:
        # Step 2: Process image into pixel values
        pixel_values = processor(images=image, return_tensors="pt").pixel_values
        logger.info(f"Image successfully processed into pixel values.")

        # Step 3: Generate the Donut model's output
        generated_ids = model.generate(pixel_values)
        logger.info(f"Donut model generated output successfully.")

        # Step 4: Decode the model's output to get the XML-like format
        xml_output = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        logger.info(f"Decoded XML-like output from Donut model: {xml_output}")
        
        # Step 5: Convert XML-like output to JSON using the DonutProcessor's `token2json()` method
        try:
            json_output = processor.token2json(xml_output)
            logger.info(f"Successfully parsed JSON from receipt: {json_output}")
            return json_output
        except Exception as e:
            logger.error(f"Error converting XML-like output to JSON: {str(e)}")
            return {}
    
    except Exception as e:
        logger.error(f"Unexpected error during receipt parsing: {str(e)}")
        return {}