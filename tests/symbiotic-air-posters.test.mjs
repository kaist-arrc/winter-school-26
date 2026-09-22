import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const read = file => readFile(new URL(`../${file}`, import.meta.url), 'utf8');

test('the detail poster explicitly frames Symbiotic AIR as reciprocal in-person support', async () => {
  const poster = await read('index.html');

  assert.match(poster, /Symbiotic AIR/);
  assert.match(poster, /AI는 대화를 대신하지 않고/);
  assert.match(poster, /동의한 피드백/);
  assert.match(poster, /class="symbiotic-loop"/);
  assert.equal((poster.match(/data-symbiotic-step/g) ?? []).length, 5);
});

test('the teaser uses a face-to-face meeting rather than a chat exchange', async () => {
  const teaser = await read('teaser.html');

  assert.match(teaser, /Symbiotic AIR/);
  assert.match(teaser, /같은 공간에서 두 사람이/);
  assert.match(teaser, /챗봇과의 대화가 아니라/);
  assert.match(teaser, /class="symbiotic-loop teaser-loop"/);
  assert.equal((teaser.match(/data-symbiotic-step/g) ?? []).length, 5);
  assert.doesNotMatch(teaser, /conversation-row/);
});

test('the teaser pairs the in-person meeting message with its generated hero image', async () => {
  const [teaser, builder] = await Promise.all([
    read('teaser.html'),
    read('scripts/build_public.py'),
  ]);

  assert.match(teaser, /class="symbiotic-hero-image"/);
  assert.match(teaser, /assets\/symbiotic-air-face-to-face\.png/);
  assert.match(builder, /'symbiotic-air-face-to-face\.png'/);
});

test('the teaser presents live social AR beyond a camera query', async () => {
  const teaser = await read('teaser.html');

  assert.match(teaser, /질문을 넘어/);
  assert.match(teaser, /공유된 맥락/);
  assert.match(teaser, /순간의 입력/);
  assert.match(teaser, /공간·3D 표현/);
  assert.match(teaser, /동의·프라이버시/);
  assert.match(teaser, /class="research-frontier"/);
  assert.match(teaser, /class="design-boundaries"/);
});

test('the teaser gives hackathon and internship equal visual priority in the program flow', async () => {
  const teaser = await read('teaser.html');
  const coreSteps = teaser.match(/class="path-step path-step--core"/g) ?? [];

  assert.equal(coreSteps.length, 2);
  assert.match(teaser, /CORE EXPERIENCE/);
  assert.match(teaser, /현장<br>해커톤/);
  assert.match(teaser, /data-program-key="teaser-flow-3">인턴<br>연구/);
  assert.doesNotMatch(teaser, /data-program-key="teaser-flow-note"/);
  assert.equal((teaser.match(/class="path-stage-short">CORE</g) ?? []).length, 2);
});
