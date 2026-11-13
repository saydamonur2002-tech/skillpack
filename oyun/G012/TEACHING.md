# Learning path: Self-contained HTML5 canvas game builder (top-down city driving game)

## Prerequisites

Reading JSON and tracing a small example by hand. Read SKILL.md first.

## 1. Assembly
Open the generated index.html in a text editor and find the game-config JSON: every value there came from an earlier skill.

## 2. Offline
Turn off the network and open the file: it still runs, because nothing is loaded from outside.

## 3. Real time
Explain why the model is not called while playing: the loop (MainLoop.js) runs the rules in the browser.

## Human check (usta)

Run `python tool/main.py < example.json` and `pytest tests`. Pick one case in tests/references.json and explain where its expected value came from. The usta checks: by playing the generated index.html: controls feel right, missions are clear, police are fair, and nothing breaks on a phone.
