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

test('the posters connect the center vision to a validated research path', async () => {
  const [detail, teaser] = await Promise.all([
    read('index.html'),
    read('teaser.html'),
  ]);

  assert.match(detail, /Symbiotic AIR4BTS/);
  assert.match(detail, /작지만 의미 있는 문제/);
  assert.match(detail, /해커톤에서 구현·검증/);
  assert.match(detail, /인턴 연구로 확장/);
  assert.match(teaser, /Symbiotic AIR4BTS/);
  assert.match(teaser, /경험 증거 포착/);
  assert.match(teaser, /모델·XR 자산화/);
  assert.match(teaser, /새 맥락에서 재구성·증강/);
  assert.match(teaser, /발견·구현·검증/);
  assert.match(teaser, /자산화·확장/);
});

test('the hackathon is a supported two-person-team research sprint', async () => {
  const [detail, teaser] = await Promise.all([
    read('index.html'),
    read('teaser.html'),
  ]);

  assert.match(detail, /온라인 공모를 바탕으로 센터가 2인 1팀으로 구성/);
  assert.match(detail, /기본 소프트웨어 플랫폼/);
  assert.match(detail, /개발용 안경 기기/);
  assert.match(detail, /개발 컴퓨터/);
  assert.match(detail, /AI 계정/);
  assert.match(teaser, /2인 1팀/);
});

test('the hackathon agenda and selection sizes are visible', async () => {
  const [detail, program] = await Promise.all([
    read('index.html'),
    read('content/program.md'),
  ]);

  assert.match(program, /hackathon-capacity: 16–30명/);
  assert.match(program, /internship-capacity: 7–10명/);
  assert.match(detail, /09:00–10:00/);
  assert.match(detail, /17:00/);
});
