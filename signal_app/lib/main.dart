import 'dart:convert';
import 'dart:async';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const SignalApp());
}

class SignalApp extends StatelessWidget {
  const SignalApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Forex Signal Bot',
      theme: ThemeData.dark(),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  List signals = [];

  bool loading = true;

  String currentTime = "";

  final String apiUrl =
      "https://hasibul-signal-bot.onrender.com/signal";

  @override
  void initState() {
    super.initState();

    fetchSignals();

    currentTime = DateTime.now().toString();

    // Current Time Refresh
    Timer.periodic(
      const Duration(seconds: 1),
      (timer) {
        setState(() {
          currentTime = DateTime.now().toString();
        });
      },
    );

    // Signal Auto Refresh
    Timer.periodic(
      const Duration(seconds: 15),
      (timer) {
        fetchSignals();
      },
    );
  }

  Future<void> fetchSignals() async {
    try {
      final response = await http.get(Uri.parse(apiUrl));

      if (response.statusCode == 200) {
        setState(() {
          signals = json.decode(response.body);
          loading = false;
        });
      }
    } catch (e) {
      setState(() {
        loading = false;
      });
    }
  }

  Color getSignalColor(String signal) {
    if (signal.contains("BUY")) {
      return Colors.green;
    } else if (signal.contains("SELL")) {
      return Colors.red;
    } else {
      return Colors.orange;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.black,
        centerTitle: true,

        title: Column(
          crossAxisAlignment: CrossAxisAlignment.center,

          children: [
            const Text(
              "Forex Signal Bot",

              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),

            Text(
              currentTime,

              style: const TextStyle(
                fontSize: 14,
                color: Colors.greenAccent,
              ),
            ),
          ],
        ),
      ),

      body: loading
          ? const Center(
              child: CircularProgressIndicator(),
            )
          : RefreshIndicator(
              onRefresh: fetchSignals,

              child: ListView.builder(
                itemCount: signals.length,

                itemBuilder: (context, index) {
                  final item = signals[index];

                  return Card(
                    color: Colors.grey[900],

                    margin: const EdgeInsets.all(10),

                    shape: RoundedRectangleBorder(
                      borderRadius:
                          BorderRadius.circular(15),
                    ),

                    child: Padding(
                      padding: const EdgeInsets.all(15),

                      child: Column(
                        crossAxisAlignment:
                            CrossAxisAlignment.start,

                        children: [
                          Text(
                            item["pair"],

                            style: const TextStyle(
                              fontSize: 24,
                              fontWeight: FontWeight.bold,
                              color: Colors.white,
                            ),
                          ),

                          const SizedBox(height: 10),

                          Text(
                            item["signal"],

                            style: TextStyle(
                              fontSize: 22,
                              fontWeight: FontWeight.bold,

                              color: getSignalColor(
                                item["signal"],
                              ),
                            ),
                          ),

                          const SizedBox(height: 10),

                          Text(
                            "Confidence: ${item["confidence"]}%",

                            style: const TextStyle(
                              color: Colors.white,
                            ),
                          ),

                          Text(
                            "EMA Trend: ${item["ema_trend"]}",

                            style: const TextStyle(
                              color: Colors.white,
                            ),
                          ),

                          Text(
                            "MACD: ${item["macd"]}",

                            style: const TextStyle(
                              color: Colors.white,
                            ),
                          ),

                          Text(
                            "RSI: ${item["rsi"]}",

                            style: const TextStyle(
                              color: Colors.white,
                            ),
                          ),

                          Text(
                            "Pattern: ${item["pattern"]}",

                            style: const TextStyle(
                              color: Colors.white,
                            ),
                          ),

                          Text(
                            "Price: ${item["price"]}",

                            style: const TextStyle(
                              color: Colors.white,
                            ),
                          ),

                          Text(
                            "Session: ${item["session"]}",

                            style: const TextStyle(
                              color: Colors.white,
                            ),
                          ),

                          Text(
                            "Trade Duration: ${item["trade_duration"]}",

                            style: const TextStyle(
                              color: Colors.white,
                            ),
                          ),

                          Text(
                            "Expiry Time: ${item["expiry_time"]}",

                            style: const TextStyle(
                              color: Colors.white,
                            ),
                          ),

                          const SizedBox(height: 10),

                          ElevatedButton(
                            onPressed: fetchSignals,

                            child: const Text("Refresh"),
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),
    );
  }
}