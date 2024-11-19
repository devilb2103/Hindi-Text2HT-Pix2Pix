import 'dart:typed_data';

class StorageService {
  static final StorageService _instance = StorageService._internal();
  factory StorageService() => _instance;
  StorageService._internal();

  Uint8List? predictedImage = null;
}
