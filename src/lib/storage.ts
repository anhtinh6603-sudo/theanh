import AsyncStorage from '@react-native-async-storage/async-storage';
import * as SecureStore from 'expo-secure-store';
import { AppSettings, DEFAULT_SETTINGS, Project } from '../types';

const PROJECTS_KEY = 'theanh:projects';
const SETTINGS_KEY = 'theanh:settings';
const TOKEN_KEY = 'theanh:replicate_token';

export async function loadProjects(): Promise<Project[]> {
  const raw = await AsyncStorage.getItem(PROJECTS_KEY);
  if (!raw) return [];
  try {
    return JSON.parse(raw) as Project[];
  } catch {
    return [];
  }
}

export async function saveProjects(projects: Project[]): Promise<void> {
  await AsyncStorage.setItem(PROJECTS_KEY, JSON.stringify(projects));
}

export async function upsertProject(project: Project): Promise<Project[]> {
  const projects = await loadProjects();
  const index = projects.findIndex((p) => p.id === project.id);
  if (index >= 0) {
    projects[index] = project;
  } else {
    projects.unshift(project);
  }
  await saveProjects(projects);
  return projects;
}

export async function deleteProject(id: string): Promise<Project[]> {
  const projects = await loadProjects();
  const next = projects.filter((p) => p.id !== id);
  await saveProjects(next);
  return next;
}

export async function loadSettings(): Promise<AppSettings> {
  const raw = await AsyncStorage.getItem(SETTINGS_KEY);
  const token = (await SecureStore.getItemAsync(TOKEN_KEY)) ?? '';
  const parsed = raw ? (JSON.parse(raw) as Partial<AppSettings>) : {};
  return { ...DEFAULT_SETTINGS, ...parsed, replicateApiToken: token };
}

export async function saveSettings(settings: AppSettings): Promise<void> {
  const { replicateApiToken, ...rest } = settings;
  await AsyncStorage.setItem(SETTINGS_KEY, JSON.stringify(rest));
  if (replicateApiToken) {
    await SecureStore.setItemAsync(TOKEN_KEY, replicateApiToken);
  } else {
    await SecureStore.deleteItemAsync(TOKEN_KEY);
  }
}
