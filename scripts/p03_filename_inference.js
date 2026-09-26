#!/usr/bin/env node
const path = require('path');

function inferTypeFromFilename(filename) {
  if (!filename)
    return undefined;
  switch (path.extname(filename).toLowerCase()) {
    case '.png': return 'png';
    case '.jpg':
    case '.jpeg': return 'jpeg';
    case '.webp': return 'webp';
  }
  return undefined;
}

function selectedType(type, filename) {
  return type ?? inferTypeFromFilename(filename) ?? 'png';
}

const tests = [
  {type: undefined, filename: 'capture.webp', expected: 'webp'},
  {type: undefined, filename: 'capture.WEBP', expected: 'webp'},
  {type: undefined, filename: 'capture.jpg', expected: 'jpeg'},
  {type: undefined, filename: 'capture.jpeg', expected: 'jpeg'},
  {type: undefined, filename: 'capture.png', expected: 'png'},
  {type: undefined, filename: 'capture.bin', expected: 'png'},
  {type: undefined, filename: undefined, expected: 'png'},
  {type: 'jpeg', filename: 'capture.webp', expected: 'jpeg'},
];

let failed = 0;
const results = tests.map((t, i) => {
  const actual = selectedType(t.type, t.filename);
  const pass = actual === t.expected;
  if (!pass) failed++;
  return {case: i + 1, ...t, actual, pass};
});

console.log(JSON.stringify({results, failed}, null, 2));
if (failed)
  process.exit(1);
