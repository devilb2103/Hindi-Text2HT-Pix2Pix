import 'dart:typed_data';

import 'package:bloc/bloc.dart';
import 'package:meta/meta.dart';
import 'package:wmad_app/utils/api_service.dart';
import 'package:wmad_app/utils/storage_service.dart';

part 'conversion_state.dart';

class ConversionCubit extends Cubit<ConversionState> {
  ConversionCubit() : super(const ConversionInitialState());
  bool _canTriggerActions = true;

  Future<void> getPrediction(
      String sentence, int fontSize, int canvasWidth) async {
    if (!_canTriggerActions) return;
    _canTriggerActions = false;
    emit(const ConversionLoadingState());

    try {
      Uint8List? response =
          await ApiService().getPrediction(sentence, fontSize, canvasWidth);
      //   print(response.statusMessage);print(response.statusMessage);
      if (response == null) return;
      StorageService service = StorageService();
      service.predictedImage = response;
      if (service.predictedImage!.isNotEmpty) {
        print(service.predictedImage!);
        // print(response.data["message"].toString());
        // Navigator.push(context,
        //     MaterialPageRoute(builder: (context) => const PDFScreen()));
      } else {
        String message = "Response Image bytes are corrupted";
        print(message.toString());
        emit(ConversionErrorState(message));
      }
    } catch (e) {
      print(e.toString());
      emit(ConversionErrorState(e.toString()));
    }
    emit(const ConversionInitialState());
    _canTriggerActions = true;
  }
}
