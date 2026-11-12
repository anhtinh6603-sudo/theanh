#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

function arg(name, fallback = null) {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 ? process.argv[i + 1] : fallback;
}

function base64url(input) {
  const raw = typeof input === 'string' ? input : JSON.stringify(input);
  return Buffer.from(raw)
    .toString('base64')
    .replace(/=/g, '')
    .replace(/\+/g, '-')
    .replace(/\//g, '_');
}

function requireEnv(name) {
  const value = process.env[name];
  if (!value) {
    console.error(`Missing env: ${name}`);
    process.exit(2);
  }
  return value;
}

async function fetchJson(url, options) {
  const res = await fetch(url, options);
  const text = await res.text();
  let json;
  try { json = JSON.parse(text); } catch { json = { raw: text }; }
  if (!res.ok) {
    throw new Error(`${url} -> HTTP ${res.status}: ${JSON.stringify(json)}`);
  }
  return json;
}

async function getAccessToken(clientEmail, privateKey) {
  const now = Math.floor(Date.now() / 1000);
  const header = { alg: 'RS256', typ: 'JWT' };
  const payload = {
    iss: clientEmail,
    scope: 'https://www.googleapis.com/auth/cloud-platform',
    aud: 'https://oauth2.googleapis.com/token',
    iat: now,
    exp: now + 3600,
  };
  const unsignedJWT = `${base64url(header)}.${base64url(payload)}`;
  const signature = crypto
    .createSign('RSA-SHA256')
    .update(unsignedJWT)
    .sign(privateKey, 'base64')
    .replace(/=/g, '')
    .replace(/\+/g, '-')
    .replace(/\//g, '_');
  const jwt = `${unsignedJWT}.${signature}`;

  const body = new URLSearchParams({
    grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
    assertion: jwt,
  });

  const tokenJson = await fetchJson('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  });

  return tokenJson.access_token;
}

async function synthesize(accessToken, text, voiceName, languageCode, audioEncoding) {
  return fetchJson('https://texttospeech.googleapis.com/v1/text:synthesize', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      input: { text },
      voice: {
        languageCode,
        name: voiceName,
      },
      audioConfig: {
        audioEncoding,
      },
    }),
  });
}

async function main() {
  const text = arg('text');
  const out = arg('out', '/tmp/google-tts-reply.mp3');
  if (!text) {
    console.error('Usage: node skills/google-tts-reply/scripts/google-tts.js --text "..." --out /tmp/file.mp3');
    process.exit(1);
  }

  const clientEmail = requireEnv('GOOGLE_TTS_CLIENT_EMAIL');
  const privateKey = requireEnv('GOOGLE_TTS_PRIVATE_KEY').replace(/\\n/g, '\n');
  const voiceName = process.env.GOOGLE_TTS_VOICE || 'vi-VN-Chirp3-HD-Aoede';
  const languageCode = process.env.GOOGLE_TTS_LANGUAGE_CODE || 'vi-VN';
  const audioEncoding = process.env.GOOGLE_TTS_AUDIO_ENCODING || 'MP3';

  const accessToken = await getAccessToken(clientEmail, privateKey);
  const audioJson = await synthesize(accessToken, text, voiceName, languageCode, audioEncoding);
  if (!audioJson.audioContent) {
    throw new Error('Google TTS response missing audioContent');
  }

  const absOut = path.resolve(out);
  fs.mkdirSync(path.dirname(absOut), { recursive: true });
  fs.writeFileSync(absOut, Buffer.from(audioJson.audioContent, 'base64'));
  console.log(absOut);
}

main().catch((err) => {
  console.error(err.message || String(err));
  process.exit(1);
});
