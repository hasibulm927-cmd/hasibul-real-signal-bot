import 'dart:async';
import 'dart:convert';
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
      home: HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {

  Map data = {};

  String selectedPair = "EURUSD";

  List pairs = [
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "AUDUSD",
    "USDCHF",
    "USDCAD",
    "EURJPY",
    "GBPJPY"
  ];

  @override
  void initState() {
    super.initState();

    loadSignal();

    Timer.periodic(
      Duration(seconds: 15),
      (timer) {
        loadSignal();
      },
    );
  }

  Future loadSignal() async {

    final url =
        "YOUR_RENDER_LINK/signal/$selectedPair";

    final response = await http.get(
      Uri.parse(url),
    );

    final jsonData = json.decode(response.body);

    setState(() {
      data = jsonData;
    });
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(

      backgroundColor: Colors.black,

      appBar: AppBar(
        backgroundColor: Colors.black,
        title: Text(
          "REAL SIGNAL BOT",
          style: TextStyle(color: Colors.white),
        ),
      ),

      body: Padding(
        padding: EdgeInsets.all(16),

        child: Column(

          children: [

            Container(
              padding: EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.orange,
                borderRadius: BorderRadius.circular(12),
              ),

              child: Row(
                mainAxisAlignment:
                MainAxisAlignment.spaceBetween,

                children: [

                  Text(
                    "LIVE SESSION",
                    style: TextStyle(
                      color: Colors.black,
                      fontWeight: FontWeight.bold,
                    ),
                  ),

                  Text(
                    "LONDON",
                    style: TextStyle(
                      color: Colors.black,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),

            SizedBox(height: 20),

            DropdownButton(
              dropdownColor: Colors.black,
              value: selectedPair,

              items: pairs.map((e) {

                return DropdownMenuItem(
                  value: e,
                  child: Text(
                    e,
                    style: TextStyle(
                      color: Colors.white,
                    ),
                  ),
                );
              }).toList(),

              onChanged: (v) {

                selectedPair = v.toString();

                loadSignal();

                setState(() {});
              },
            ),

            SizedBox(height: 20),

            Expanded(
              child: Container(

                width: double.infinity,

                padding: EdgeInsets.all(20),

                decoration: BoxDecoration(
                  color: Colors.grey.shade900,
                  borderRadius:
                  BorderRadius.circular(20),
                ),

                child: Column(

                  crossAxisAlignment:
                  CrossAxisAlignment.start,

                  children: [

                    Text(
                      selectedPair,
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 28,
                        fontWeight: FontWeight.bold,
                      ),
                    ),

                    SizedBox(height: 20),

                    Text(
                      "SIGNAL",
                      style: TextStyle(
                        color: Colors.grey,
                      ),
                    ),

                    SizedBox(height: 10),

                    Text(
                      "${data['signal'] ?? '--'}",
                      style: TextStyle(
                        color:
                        data['signal'] == "BUY"
                            ? Colors.green
                            : Colors.red,

                        fontSize: 42,
                        fontWeight: FontWeight.bold,
                      ),
                    ),

                    SizedBox(height: 20),

                    Text(
                      "PRICE : ${data['price'] ?? '--'}",
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 20,
                      ),
                    ),

                    SizedBox(height: 10),

                    Text(
                      "RSI : ${data['rsi'] ?? '--'}",
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                      ),
                    ),

                    SizedBox(height: 10),

                    Text(
                      "EMA : ${data['ema'] ?? '--'}",
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                      ),
                    ),

                    SizedBox(height: 10),

                    Text(
                      "CONFIDENCE : ${data['strength'] ?? '--'}%",
                      style: TextStyle(
                        color: Colors.orange,
                        fontSize: 18,
                      ),
                    ),

                    SizedBox(height: 20),

                    Row(

                      children: [

                        Expanded(
                          child: ElevatedButton(

                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.green,
                            ),

                            onPressed: () {},

                            child: Text(
                              "BUY",
                            ),
                          ),
                        ),

                        SizedBox(width: 20),

                        Expanded(
                          child: ElevatedButton(

                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.red,
                            ),

                            onPressed: () {},

                            child: Text(
                              "SELL",
                            ),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}