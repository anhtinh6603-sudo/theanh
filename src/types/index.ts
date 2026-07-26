export type GenerationStatus = 'idle' | 'starting' | 'processing' | 'succeeded' | 'failed';

export type Project = {
  id: string;
  createdAt: number;
  prompt: string;
  sourceImageUri: string;
  videoUri: string | null;
  status: GenerationStatus;
  error: string | null;
  mock: boolean;
};

export type AppSettings = {
  replicateApiToken: string;
  model: string;
  imageField: string;
  promptField: string;
};

export const DEFAULT_SETTINGS: AppSettings = {
  replicateApiToken: '',
  model: 'minimax/video-01',
  imageField: 'first_frame_image',
  promptField: 'prompt',
};
