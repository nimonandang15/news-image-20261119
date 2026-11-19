// news-image-20261119: "The World in One Day" — Thursday 19 November 2026.
// Node 22, standard library only. The poster is entry.png beside this file,
// drawn for this competition (see render.py); this program copies it,
// byte for byte, to /output/entry.png and refuses to write anything that
// is not a whole PNG within the gate limits (<= 1 MiB, <= 1024 x 1024).
// Deterministic: the same entry.png always produces the same output bytes.
//
// Local check:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1048576;
const MAX_DIMENSION = 1024;

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const image = readFileSync(new URL('./entry.png', import.meta.url));

if (image.length > MAX_BYTES) {
  throw new Error(`entry.png is ${image.length} bytes, over the 1 MiB gate limit`);
}
if (!image.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error('entry.png is not a PNG (bad signature)');
}
const width = image.readUInt32BE(16);
const height = image.readUInt32BE(20);
if (width > MAX_DIMENSION || height > MAX_DIMENSION) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 gate limit`);
}

mkdirSync(outDir, { recursive: true });
const outPath = join(outDir, 'entry.png');
writeFileSync(outPath, image);

// Read the output back and confirm it is byte-identical to the source:
// a partial or corrupted write must fail loudly instead of shipping.
const written = readFileSync(outPath);
if (!written.equals(image)) {
  throw new Error('output entry.png does not match entry.png after writing');
}

const sha256 = createHash('sha256').update(image).digest('hex');
console.log(`wrote entry.png: ${width}x${height}, ${image.length} bytes, sha256 ${sha256}`);
