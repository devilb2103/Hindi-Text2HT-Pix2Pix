from quart import Quart, request, jsonify, Response
from PIL import Image
from quart_cors import cors
from createSrcImg import place_words_on_canvas
import io

app = Quart(__name__)
app = cors(app)

@app.route('/predict', methods=['POST'])
async def predict():
    data = await request.get_json()  # Retrieve JSON data from the request
    
    if not data or any(key not in data for key in ['sentence', 'font_size', 'canvas_width']):
        return jsonify({"error": "Request Body must contain 'sentence', 'font_size' and 'canvas_width'"}), 400
    
    sentence = data['sentence']
    font_size = data['font_size']
    canvas_width = data['canvas_width']
    
    try:
        # Generate image from the given word
        processed_image = place_words_on_canvas(font_size, sentence, canvas_width, debug=False)
        
        # Convert the processed image to bytes for response
        img_byte_arr = io.BytesIO()
        processed_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Return the image in the response
        return Response(img_byte_arr, mimetype='image/png')
    
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)
