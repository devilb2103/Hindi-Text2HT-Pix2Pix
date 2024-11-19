import 'package:flutter/material.dart';

void showSnackbarMessage(BuildContext context, bool state, String message) {
  ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      behavior: SnackBarBehavior.fixed,
      dismissDirection: DismissDirection.down,
      duration: const Duration(seconds: 2),
      content: Text(message),
      elevation: 3,
      backgroundColor:
          state == true ? Colors.green.shade300 : Colors.red.shade300));
}
