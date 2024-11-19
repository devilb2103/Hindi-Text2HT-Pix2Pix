import 'package:flutter/material.dart';
import 'package:gal/gal.dart';
import 'package:wmad_app/utils/storage_service.dart';
import 'package:path_provider/path_provider.dart';
import 'package:photo_view/photo_view.dart';
import 'dart:io' as io;

class ImageScreen extends StatelessWidget {
  const ImageScreen({super.key});

  void saveImage() async {
    final directory = await getApplicationDocumentsDirectory();
    final path =
        '${directory.path}/image_${DateTime.now().millisecondsSinceEpoch}.png';
    final file = io.File(path);

    final imageData = StorageService().predictedImage;
    if (imageData != null) {
      await file.writeAsBytes(imageData);
      print('Image saved to $path');
      await Gal.putImage(file.path);
      print('Image saved to gallery!');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.black,
        foregroundColor: Colors.white,
        elevation: 3,
        shadowColor: Colors.black,
        leading: IconButton(
            onPressed: () {
              Navigator.pop(context);
            },
            icon: Icon(Icons.arrow_back_ios)),
      ),
      body: SafeArea(
        child: Column(children: [
          // Align(
          //   alignment: Alignment.topLeft,
          //   child: IconButton(
          //       onPressed: () => Navigator.pop(context),
          //       icon: const Icon(Icons.close)),
          // ),
          Expanded(
            child: PhotoView(
              imageProvider: MemoryImage(StorageService()
                  .predictedImage!), // Display the image from Uint8List
              backgroundDecoration: BoxDecoration(
                  color: Colors.black), // Optional: black background
            ),
          ),
          SizedBox(height: 10),
          TextButton(
              onPressed: () async {
                saveImage();
              },
              child: Text(
                "Save Image",
                style: TextStyle(color: Colors.black),
              )),
          SizedBox(height: 10),
        ]),
      ),
    );
  }
}
