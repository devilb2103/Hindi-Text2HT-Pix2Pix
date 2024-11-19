import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class CustomTextInput extends StatefulWidget {
  final TextEditingController controller;
  final String hintText;
  final List<TextInputFormatter>? inputFormatters; // Optional filter parameter
  final int? maxLines;
  const CustomTextInput(
      {super.key,
      required this.controller,
      required this.hintText,
      this.inputFormatters,
      this.maxLines});

  @override
  State<CustomTextInput> createState() => _CustomTextInputState();
}

class _CustomTextInputState extends State<CustomTextInput> {
  @override
  Widget build(BuildContext context) {
    return TextFormField(
      controller: widget.controller,
      minLines: 1,
      maxLines: widget.maxLines ?? 1,
      inputFormatters: widget.inputFormatters,
      decoration: InputDecoration(
        contentPadding: const EdgeInsets.all(21),
        filled: true,
        fillColor: Colors.white,
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(15),
          borderSide: const BorderSide(color: Colors.black12),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(15),
          borderSide: const BorderSide(color: Color.fromARGB(255, 4, 3, 3)),
        ),
        border: const OutlineInputBorder(),
        hintText: widget.hintText,
        hintStyle: TextStyle(color: Colors.black54),
      ),
    );
  }
}
