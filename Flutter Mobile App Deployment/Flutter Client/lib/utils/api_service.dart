import 'dart:typed_data';
import 'package:dio/dio.dart';

class ApiService {
  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  ApiService._internal();

  final _client = Dio(BaseOptions(
    baseUrl: "http://10.24.84.215:5000/predict",
    // baseUrl: "http://127.0.0.1:5000/predict",
  ));

  Future<Uint8List?> getPrediction(
      String sentence, int fontSize, int canvasWidth) async {
    try {
      final response = await _client.post(
        '',
        data: {
          'sentence': sentence,
          'font_size': fontSize,
          'canvas_width': canvasWidth,
        },
        options: Options(
          responseType: ResponseType.bytes, // Receive image as bytes
        ),
      );

      if (response.statusCode == 200) {
        print("data recieved");
        return response.data; // Returning the image data as Uint8List
      } else {
        throw Exception(
          "Error: ${response.statusCode} - ${response.statusMessage}",
        );
      }
    } on DioError catch (e) {
      throw Exception("Request failed with error: ${e.message}");
    }
  }
}
