import { File } from 'expo-file-system';
import { AppSettings } from '../types';

const REPLICATE_API_BASE = 'https://api.replicate.com/v1';
const MOCK_SAMPLE_VIDEO =
  'https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4';

export type GenerateProgressCallback = (status: string) => void;

export class GenerationCancelledError extends Error {}

async function fileUriToDataUrl(uri: string): Promise<string> {
  const file = new File(uri);
  const base64 = await file.base64();
  const extension = uri.split('.').pop()?.toLowerCase() ?? 'jpg';
  const mime = extension === 'png' ? 'image/png' : 'image/jpeg';
  return `data:${mime};base64,${base64}`;
}

async function runMockGeneration(
  onProgress: GenerateProgressCallback,
  isCancelled: () => boolean,
): Promise<string> {
  const steps = ['starting', 'processing', 'processing', 'processing'];
  for (const step of steps) {
    if (isCancelled()) throw new GenerationCancelledError();
    onProgress(step);
    await new Promise((resolve) => setTimeout(resolve, 900));
  }
  return MOCK_SAMPLE_VIDEO;
}

async function runReplicateGeneration(
  settings: AppSettings,
  sourceImageUri: string,
  prompt: string,
  onProgress: GenerateProgressCallback,
  isCancelled: () => boolean,
): Promise<string> {
  const imageDataUrl = await fileUriToDataUrl(sourceImageUri);
  const input: Record<string, string> = {
    [settings.imageField]: imageDataUrl,
  };
  if (prompt && settings.promptField) {
    input[settings.promptField] = prompt;
  }

  onProgress('starting');
  const createResponse = await fetch(
    `${REPLICATE_API_BASE}/models/${settings.model}/predictions`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${settings.replicateApiToken}`,
        'Content-Type': 'application/json',
        Prefer: 'wait',
      },
      body: JSON.stringify({ input }),
    },
  );

  if (!createResponse.ok) {
    const errorBody = await createResponse.text();
    throw new Error(`Replicate request failed (${createResponse.status}): ${errorBody}`);
  }

  let prediction = await createResponse.json();

  while (prediction.status === 'starting' || prediction.status === 'processing') {
    if (isCancelled()) {
      await fetch(`${REPLICATE_API_BASE}/predictions/${prediction.id}/cancel`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${settings.replicateApiToken}` },
      }).catch(() => undefined);
      throw new GenerationCancelledError();
    }
    onProgress(prediction.status);
    await new Promise((resolve) => setTimeout(resolve, 2000));
    const pollResponse = await fetch(`${REPLICATE_API_BASE}/predictions/${prediction.id}`, {
      headers: { Authorization: `Bearer ${settings.replicateApiToken}` },
    });
    if (!pollResponse.ok) {
      throw new Error(`Replicate polling failed (${pollResponse.status})`);
    }
    prediction = await pollResponse.json();
  }

  if (prediction.status !== 'succeeded') {
    const detail = prediction.error ? `: ${prediction.error}` : '';
    throw new Error(`Video generation ${prediction.status}${detail}`);
  }

  const output = prediction.output;
  const videoUrl = Array.isArray(output) ? output[0] : output;
  if (typeof videoUrl !== 'string') {
    throw new Error('Unexpected response format from model output');
  }
  return videoUrl;
}

export async function generateVideoFromImage(
  settings: AppSettings,
  sourceImageUri: string,
  prompt: string,
  onProgress: GenerateProgressCallback,
  isCancelled: () => boolean,
): Promise<{ videoUri: string; mock: boolean }> {
  if (!settings.replicateApiToken) {
    const videoUri = await runMockGeneration(onProgress, isCancelled);
    return { videoUri, mock: true };
  }
  const videoUri = await runReplicateGeneration(
    settings,
    sourceImageUri,
    prompt,
    onProgress,
    isCancelled,
  );
  return { videoUri, mock: false };
}
