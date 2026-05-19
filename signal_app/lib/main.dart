import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: TradingScreen(),
    );
  }
}

class TradingScreen extends StatefulWidget {
  const TradingScreen({super.key});

  @override
  State<TradingScreen> createState() => _TradingScreenState();
}

class _TradingScreenState extends State<TradingScreen> {

  Map signal = {};

  final List<FlSpot> chartData = [
    FlSpot(0, 1),
    FlSpot(1, 1.5),
    FlSpot(2, 1.4),
    FlSpot(3, 1.8),
    FlSpot(4, 1.6),
    FlSpot(5, 2),
    FlSpot(6, 1.9),
  ];

  Future<void> getSignal() async {

    try {

      final response = await http.get(
        Uri.parse("https://hasibul-forex-bot.onrender.com/signal"),
      );

      if (response.statusCode == 200) {

        final data = jsonDecode(response.body);

        setState(() {

          if (data is List && data.isNotEmpty) {
            signal = data[0];
          }

        });
      }

    } catch (e) {
      print(e);
    }
  }

  @override
  void initState() {
    super.initState();
    getSignal();
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(

      backgroundColor: const Color(0xff0d1b2a),

      appBar: AppBar(
        backgroundColor: Colors.black,
        title: const Text(
          "HASIBUL AI TRADING",
          style: TextStyle(color: Colors.white),
        ),
      ),

      body: Padding(
        padding: const EdgeInsets.all(12),

        child: Column(
          children: [

            /// SIGNAL CARD
            Container(

              width: double.infinity,

              padding: const EdgeInsets.all(16),

              decoration: BoxDecoration(
                color: const Color(0xff1b263b),
                borderRadius: BorderRadius.circular(20),
              ),

              child: Column(

                crossAxisAlignment: CrossAxisAlignment.start,

                children: [

                  Text(
                    signal["signal"]?.toString() ?? "WAIT SIGNAL",
                    style: TextStyle(
                      color: signal["signal"] == "SELL SIGNAL"
                          ? Colors.red
                          : Colors.green,
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                    ),
                  ),

                  const SizedBox(height: 10),

                  Text(
                    "PAIR: ${signal["pair"] ?? "EUR/USD"}",
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                    ),
                  ),

                  Text(
                    "PRICE: ${signal["price"] ?? "0"}",
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                    ),
                  ),

                  Text(
                    "RSI: ${signal["rsi"] ?? "0"}",
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                    ),
                  ),

                  Text(
                    "MACD: ${signal["macd"] ?? "NONE"}",
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                    ),
                  ),

                  Text(
                    "EMA: ${signal["ema"] ?? "NONE"}",
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                    ),
                  ),

                  Text(
                    "ENTRY TIME: ${signal["entry_time"] ?? "--"}",
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                    ),
                  ),

                  Text(
                    "EXPIRY: ${signal["expiry"] ?? "3 MIN"}",
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                    ),
                  ),

                  Text(
                    "CONFIDENCE: ${signal["confidence"] ?? "90"}%",
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                    ),
                  ),

                ],
              ),
            ),

            const SizedBox(height: 20),

            /// CHART
            Expanded(

              child: Container(

                padding: const EdgeInsets.all(16),

                decoration: BoxDecoration(
                  color: Colors.black,
                  borderRadius: BorderRadius.circular(20),
                ),

                child: LineChart(

                  LineChartData(

                    backgroundColor: Colors.black,

                    gridData: FlGridData(show: true),

                    titlesData: FlTitlesData(show: false),

                    borderData: FlBorderData(show: false),

                    lineBarsData: [

                      LineChartBarData(

                        spots: chartData,

                        isCurved: true,

                        color: signal["signal"] == "SELL SIGNAL"
                            ? Colors.red
                            : Colors.green,

                        barWidth: 4,

                        dotData: FlDotData(show: false),

                      ),

                    ],
                  ),
                ),
              ),
            ),

            const SizedBox(height: 20),

            /// BUY SELL BUTTON
            Row(
              children: [

                Expanded(
                  child: ElevatedButton(

                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.green,
                      padding: const EdgeInsets.all(18),
                    ),

                    onPressed: () {},

                    child: const Text(
                      "BUY",
                      style: TextStyle(fontSize: 22),
                    ),
                  ),
                ),

                const SizedBox(width: 15),

                Expanded(
                  child: ElevatedButton(

                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.red,
                      padding: const EdgeInsets.all(18),
                    ),

                    onPressed: () {},

                    child: const Text(
                      "SELL",
                      style: TextStyle(fontSize: 22),
                    ),
                  ),
                ),

              ],
            ),

          ],
        ),
      ),
    );
  }
}