import barcode
from barcode.writer import ImageWriter
from PIL import Image
from io import BytesIO
from fastapi import FastAPI
from fastapi.responses import StreamingResponse


app = FastAPI()
@app.get("/generate_barcode/{data}")
def generate_barcode(data, barcode_format="code128"):
    """
    Generate a barcode and return it as a BytesIO object.

    Parameters:
    - data: The data to encode in the barcode.
    - barcode_format: The barcode format (e.g., 'code128').

    Returns:
    - BytesIO: The barcode image as a BytesIO object.
    """
    # Create a barcode object
    code = barcode.get_barcode_class(barcode_format)
    barcode_instance = code(data, writer=ImageWriter())

    # Create a BytesIO object to store the barcode image
    barcode_bytesio = BytesIO()

    # Use the write method of the ImageWriter to write the barcode to the BytesIO object
    barcode_instance.write(barcode_bytesio, options={"write_text": True})

    # print(barcode_bytesio.getvalue())
    # Set the BytesIO object's position to the beginning
    barcode_bytesio.seek(0)

    # return barcode_bytesio
    return StreamingResponse(content=barcode_bytesio, media_type="image/png")

