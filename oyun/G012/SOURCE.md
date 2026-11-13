# Source and changes: Self-contained HTML5 canvas game builder (top-down city driving game)

Original work by Skillpack contributors (MIT). No third-party code.

## Design notes

Original builder and game runtime by Skillpack contributors. Embedded third-party code: MainLoop.js build/mainloop.min.js (MIT, leading comment with an author URL replaced by the full MIT notice in an HTML comment so the file has no URLs) and ZzFXMicro.min.js (MIT, wrapped in a function so the AudioContext is created only after a user gesture). The configuration JSON is embedded with <, > and & escaped. The runtime implements the formulas of G003 (car), G004 (circle vs box), G006 (seek/arrive/flee/pursuit), G007 (wanted), G008 (missions), G009 (integer money) and G010 (save envelope); tests/test_flow_e2e.py compares them with the Python tools.

Embedded: https://github.com/IceCreamYou/MainLoop.js @ `3ddadf0ab902da96af7077be40206ac27ba1b1d3` (MIT) — build/mainloop.min.js embedded in the HTML as the real-time loop (leading comment replaced by the full notice).
- [build/mainloop.min.js](https://github.com/IceCreamYou/MainLoop.js/blob/3ddadf0ab902da96af7077be40206ac27ba1b1d3/build/mainloop.min.js) — complete original file; SHA-256 `234a0ee563b7beeb5c527435c28d689575b16aa3f4b51c4973d65830d8f85b58`.

Embedded: https://github.com/KilledByAPixel/ZzFX @ `ac5a4727a44e5506a12f7340087e0b889cfd69dc` (MIT) — ZzFXMicro.min.js embedded in the HTML to play sound parameters.
- [ZzFXMicro.min.js](https://github.com/KilledByAPixel/ZzFX/blob/ac5a4727a44e5506a12f7340087e0b889cfd69dc/ZzFXMicro.min.js) — complete original file; SHA-256 `7f4b89afa67b3029d1462108a02582e7858bf9d76a04e6d7081db418a11bf150`.

## Reference values

Original builder; references are structural (self-contained check, embedded parts, summary counts). Behaviour is checked end to end: the flow runner builds a game and Node.js runs it headless and compares the runtime formulas with G003, G004, G006 and G010.
