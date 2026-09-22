import { test } from 'node:test';
import assert from 'node:assert/strict';
import { slugify } from './slugify.js';

test('slugifies an ordinary title', () => {
  assert.equal(slugify('Hello World'), 'hello-world');
});

test('collapses runs of non-alphanumeric characters into one hyphen', () => {
  assert.equal(slugify('Agent   Sessions --- Lab #5!'), 'agent-sessions-lab-5');
});

test('strips leading and trailing hyphens', () => {
  assert.equal(slugify('  ...Trimmed Title...  '), 'trimmed-title');
});

test('returns an empty string for the empty string', () => {
  assert.equal(slugify(''), '');
});

test('returns an empty string for non-string input', () => {
  assert.equal(slugify(null), '');
  assert.equal(slugify(undefined), '');
  assert.equal(slugify(42), '');
  assert.equal(slugify({}), '');
  assert.equal(slugify(['a']), '');
});

test('returns an empty string when the input is only punctuation', () => {
  assert.equal(slugify('---'), '');
  assert.equal(slugify('!!! ??? ...'), '');
});

test('folds accented Latin characters to their ASCII base', () => {
  assert.equal(slugify('Café Über'), 'cafe-uber');
});

test('treats a letter with no ASCII decomposition as a separator', () => {
  assert.equal(slugify('Straße Zwei'), 'stra-e-zwei');
});

test('returns an empty string for scripts with no ASCII equivalent', () => {
  assert.equal(slugify('日本語'), '');
});
