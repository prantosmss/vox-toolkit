#!/usr/bin/env node
const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const src = path.resolve(__dirname, "..");
const dest = process.cwd();
const COPY = ["scripts", "instructions.md", "script.md", "init.py", "requirements.txt", ".env.example"];

function copy(from, to) {
  if (fs.statSync(from).isDirectory()) {
    fs.mkdirSync(to, { recursive: true });
    for (const name of fs.readdirSync(from)) {
      if (name === "__pycache__") continue;
      copy(path.join(from, name), path.join(to, name));
    }
  } else if (fs.existsSync(to)) {
    console.log("skipped (already exists): " + path.relative(dest, to));
  } else {
    fs.copyFileSync(from, to);
    console.log("copied: " + path.relative(dest, to));
  }
}

for (const item of COPY) {
  copy(path.join(src, item), path.join(dest, item));
}

const py = process.platform === "win32" ? "python" : "python3";
console.log("\nRunning init.py ...");
const result = spawnSync(py, ["init.py"], { cwd: dest, stdio: "inherit" });
process.exit(result.status === null ? 1 : result.status);
