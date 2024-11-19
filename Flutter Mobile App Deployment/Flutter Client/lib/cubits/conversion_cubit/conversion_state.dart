part of 'conversion_cubit.dart';

@immutable
abstract class ConversionState {
  const ConversionState();
}

class ConversionInitialState extends ConversionState {
  const ConversionInitialState();
}

class ConversionLoadingState extends ConversionState {
  const ConversionLoadingState();
}

class ConversionErrorState extends ConversionState {
  final String message;
  const ConversionErrorState(this.message);
}
