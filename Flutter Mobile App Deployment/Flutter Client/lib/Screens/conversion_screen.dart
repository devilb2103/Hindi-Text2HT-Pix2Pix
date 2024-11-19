import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:wmad_app/Screens/imageScreen.dart';
import 'package:wmad_app/cubits/conversion_cubit/conversion_cubit.dart';
import 'package:wmad_app/main.dart';
import 'package:wmad_app/utils/api_service.dart';
import 'package:wmad_app/utils/storage_service.dart';
import 'package:wmad_app/widgets/error_snackbar.dart';
import 'package:wmad_app/widgets/custom_text_input.dart';

class ConversionScreen extends StatefulWidget {
  const ConversionScreen({super.key});

  @override
  State<ConversionScreen> createState() => _ConversionScreenState();
}

class _ConversionScreenState extends State<ConversionScreen> {
  @override
  void initState() {
    super.initState();
    print("Screen has init");
  }

  TextEditingController content = TextEditingController();
  TextEditingController canvasWidth = TextEditingController();
  TextEditingController fontSize = TextEditingController();

  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          centerTitle: true,
          title: const Text("Hindi HT Generator"),
          backgroundColor: Colors.black,
          foregroundColor: Colors.white,
          elevation: 3,
          shadowColor: Colors.black,
        ),
        body: SafeArea(
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 20),
            decoration: const BoxDecoration(color: Colors.white70),
            child: Column(
              children: [
                queryBody(),
                Padding(
                  padding: const EdgeInsets.fromLTRB(30, 10, 30, 10),
                  child: queryButton(),
                ),
                // StorageService().predictedImage != null
                //     ? Column(children: [
                //         Container(
                //           color: Colors.amber,
                //           height: 200,
                //           child: Image.memory(StorageService().predictedImage!),
                //         ),
                //         TextButton(
                //             onPressed: () => Navigator.push(
                //                 context,
                //                 MaterialPageRoute(
                //                     builder: (context) => const ImageScreen())),
                //             child: Text("View Image"))
                //       ])
                //     : Container()
              ],
            ),
          ),
        ));
  }

  Widget queryBody() {
    return Expanded(
      child: ListView(
        physics: const BouncingScrollPhysics(
            parent: AlwaysScrollableScrollPhysics()),
        children: [
          Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 30),
              const Padding(
                  padding: EdgeInsets.fromLTRB(18, 0, 0, 0),
                  child: Text("Enter Text Content",
                      style: TextStyle(color: Colors.black),
                      textAlign: TextAlign.left)),
              CustomTextInput(
                  controller: content,
                  hintText: "Type your text here",
                  maxLines: 10),
              const SizedBox(height: 30),
              const Padding(
                  padding: EdgeInsets.fromLTRB(18, 0, 0, 0),
                  child: Text("Enter Font Size",
                      style: TextStyle(color: Colors.black),
                      textAlign: TextAlign.left)),
              CustomTextInput(
                  controller: fontSize,
                  hintText: "Default: 80",
                  inputFormatters: [FilteringTextInputFormatter.digitsOnly]),
              const SizedBox(height: 30),
              const Padding(
                  padding: EdgeInsets.fromLTRB(18, 0, 0, 0),
                  child: Text("Enter Canvas Width",
                      style: TextStyle(color: Colors.black),
                      textAlign: TextAlign.left)),
              CustomTextInput(
                  controller: canvasWidth,
                  hintText: "Default: 3000",
                  inputFormatters: [FilteringTextInputFormatter.digitsOnly]),
              const SizedBox(height: 30),
              ImagePreview(),
            ],
          ),
        ],
      ),
    );
  }

  Widget queryButton() {
    return TextButton(
      onPressed: () async {
        await context.read<ConversionCubit>().getPrediction(
            content.text != '' ? content.text + " " * 100 : "हमारे " * 100,
            fontSize.text.isNotEmpty ? int.parse(fontSize.text) : 80,
            canvasWidth.text.isNotEmpty ? int.parse(canvasWidth.text) : 2000);
      },
      style: const ButtonStyle(
          shape: WidgetStatePropertyAll(RoundedRectangleBorder(
              borderRadius: BorderRadius.all(Radius.circular(15)))),
          backgroundColor: WidgetStatePropertyAll(Colors.black87),
          foregroundColor: WidgetStatePropertyAll(Colors.white)),
      child: Row(
        children: [
          Expanded(
            child: Container(
              height: 60,
              alignment: Alignment.center,
              child: BlocConsumer<ConversionCubit, ConversionState>(
                listener: (context, state) {
                  if (state is ConversionErrorState) {
                    showSnackbarMessage(context, false, state.message);
                  }
                },
                builder: (context, state) {
                  if (state is ConversionLoadingState) {
                    return Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: const Center(child: CircularProgressIndicator()),
                    );
                  } else {
                    return const Center(
                        child: Text(
                      "Convert Text",
                      style: TextStyle(fontSize: 18),
                    ));
                  }
                },
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget ImagePreview() {
    return BlocBuilder<ConversionCubit, ConversionState>(
      builder: (context, state) {
        return StorageService().predictedImage != null
            ? Column(children: [
                Row(
                  children: [
                    Expanded(
                      child: Container(
                        decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(15),
                            color: Colors.black),
                        height: 300,
                        child: Image.memory(
                          StorageService().predictedImage!,
                          fit: BoxFit.contain,
                        ),
                      ),
                    ),
                  ],
                ),
                SizedBox(height: 12),
                TextButton(
                    onPressed: () => Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (context) => const ImageScreen())),
                    child: Text(
                      "View Image",
                      style: TextStyle(color: Colors.black),
                    ))
              ])
            : Container();
      },
    );
  }
}
