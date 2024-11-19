import 'package:flutter/material.dart';
import 'package:wmad_app/Screens/conversion_screen.dart';

class AppNavigator extends StatefulWidget {
  const AppNavigator({super.key});

  @override
  State<AppNavigator> createState() => _AppNavigatorState();
}

class _AppNavigatorState extends State<AppNavigator> {
  @override
  Widget build(BuildContext context) {
    return Navigator(
      pages: const [
        MaterialPage(child: ConversionScreen()),
        // MaterialPage(child: MainScreen()),
      ],
      onPopPage: (route, result) {
        return route.didPop(result);
      },
    );
  }
}
