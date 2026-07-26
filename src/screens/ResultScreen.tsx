import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { File, Paths } from 'expo-file-system';
import * as MediaLibrary from 'expo-media-library';
import * as Sharing from 'expo-sharing';
import { useVideoPlayer, VideoView } from 'expo-video';
import { useCallback, useEffect, useRef, useState } from 'react';
import { ActivityIndicator, Alert, StyleSheet, Text, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { GradientButton } from '../components/GradientButton';
import { colors, radius, spacing, typography } from '../theme';
import { generateVideoFromImage, GenerationCancelledError } from '../lib/videoGenerator';
import { loadProjects, loadSettings, upsertProject } from '../lib/storage';
import { Project } from '../types';
import { RootStackParamList } from '../navigation/types';

type Props = NativeStackScreenProps<RootStackParamList, 'Result'>;

const PROGRESS_LABEL: Record<string, string> = {
  starting: 'Đang khởi tạo...',
  processing: 'Đang tạo video, có thể mất một phút...',
};

async function ensureLocalFile(uri: string): Promise<string> {
  if (uri.startsWith('file://')) return uri;
  const destination = new File(Paths.cache, `theanh-${Date.now()}.mp4`);
  const file = await File.downloadFileAsync(uri, destination);
  return file.uri;
}

export function ResultScreen({ route, navigation }: Props) {
  const { projectId } = route.params;
  const [project, setProject] = useState<Project | null>(null);
  const [progressLabel, setProgressLabel] = useState('Đang khởi tạo...');
  const [busy, setBusy] = useState(false);
  const cancelledRef = useRef(false);
  const startedRef = useRef(false);

  const player = useVideoPlayer(project?.videoUri ?? null, (instance) => {
    instance.loop = true;
  });

  const runGeneration = useCallback(async (current: Project) => {
    cancelledRef.current = false;
    try {
      const settings = await loadSettings();
      const { videoUri, mock } = await generateVideoFromImage(
        settings,
        current.sourceImageUri,
        current.prompt,
        (status) => setProgressLabel(PROGRESS_LABEL[status] ?? status),
        () => cancelledRef.current,
      );
      const finished: Project = { ...current, status: 'succeeded', videoUri, mock, error: null };
      await upsertProject(finished);
      setProject(finished);
    } catch (error) {
      if (error instanceof GenerationCancelledError) {
        navigation.goBack();
        return;
      }
      const message = error instanceof Error ? error.message : 'Đã xảy ra lỗi không xác định';
      const failed: Project = { ...current, status: 'failed', error: message };
      await upsertProject(failed);
      setProject(failed);
    }
  }, [navigation]);

  useEffect(() => {
    loadProjects().then((projects) => {
      const found = projects.find((p) => p.id === projectId) ?? null;
      setProject(found);
      if (found && (found.status === 'starting' || found.status === 'processing') && !startedRef.current) {
        startedRef.current = true;
        runGeneration(found);
      }
    });
  }, [projectId, runGeneration]);

  async function handleCancel() {
    cancelledRef.current = true;
  }

  async function handleRetry() {
    if (!project) return;
    const retryProject: Project = { ...project, status: 'starting', error: null };
    await upsertProject(retryProject);
    setProject(retryProject);
    startedRef.current = true;
    runGeneration(retryProject);
  }

  async function handleSave() {
    if (!project?.videoUri) return;
    setBusy(true);
    try {
      const permission = await MediaLibrary.requestPermissionsAsync();
      if (!permission.granted) {
        Alert.alert('Cần quyền truy cập', 'Vui lòng cho phép lưu vào thư viện ảnh.');
        return;
      }
      const localUri = await ensureLocalFile(project.videoUri);
      await MediaLibrary.saveToLibraryAsync(localUri);
      Alert.alert('Đã lưu', 'Video đã được lưu vào thư viện ảnh của bạn.');
    } catch (error) {
      Alert.alert('Lỗi', 'Không thể lưu video. Vui lòng thử lại.');
    } finally {
      setBusy(false);
    }
  }

  async function handleShare() {
    if (!project?.videoUri) return;
    setBusy(true);
    try {
      const localUri = await ensureLocalFile(project.videoUri);
      const available = await Sharing.isAvailableAsync();
      if (!available) {
        Alert.alert('Không hỗ trợ', 'Chia sẻ không khả dụng trên thiết bị này.');
        return;
      }
      await Sharing.shareAsync(localUri);
    } catch (error) {
      Alert.alert('Lỗi', 'Không thể chia sẻ video. Vui lòng thử lại.');
    } finally {
      setBusy(false);
    }
  }

  if (!project) {
    return (
      <SafeAreaView style={styles.screen}>
        <ActivityIndicator color={colors.cyan} />
      </SafeAreaView>
    );
  }

  const isWorking = project.status === 'starting' || project.status === 'processing';

  return (
    <SafeAreaView style={styles.screen} edges={['top', 'left', 'right']}>
      <Text style={typography.title}>Kết quả</Text>

      {isWorking && (
        <View style={styles.centerBox}>
          <ActivityIndicator color={colors.cyan} size="large" />
          <Text style={[typography.subtitle, { marginTop: spacing.md, textAlign: 'center' }]}>
            {progressLabel}
          </Text>
          <GradientButton
            label="Hủy"
            variant="outline"
            onPress={handleCancel}
            style={{ marginTop: spacing.lg, width: 160 }}
          />
        </View>
      )}

      {project.status === 'failed' && (
        <View style={styles.centerBox}>
          <Text style={{ color: colors.danger, textAlign: 'center' }}>
            {project.error ?? 'Tạo video thất bại.'}
          </Text>
          <GradientButton label="Thử lại" onPress={handleRetry} style={{ marginTop: spacing.lg }} />
        </View>
      )}

      {project.status === 'succeeded' && project.videoUri && (
        <View style={styles.resultBox}>
          <VideoView
            style={styles.video}
            player={player}
            allowsPictureInPicture
            nativeControls
          />
          {project.mock && (
            <Text style={[typography.label, { marginTop: spacing.sm }]}>
              Chế độ demo · thêm Replicate API token trong Cài đặt để tạo video thật
            </Text>
          )}
          <View style={styles.actionsRow}>
            <GradientButton
              label="Lưu vào máy"
              onPress={handleSave}
              loading={busy}
              style={styles.actionButton}
            />
            <GradientButton
              label="Chia sẻ"
              variant="outline"
              onPress={handleShare}
              loading={busy}
              style={styles.actionButton}
            />
          </View>
          <GradientButton
            label="Tạo lại"
            variant="outline"
            onPress={handleRetry}
            style={{ marginTop: spacing.sm }}
          />
        </View>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: colors.background,
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.md,
  },
  centerBox: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  resultBox: {
    marginTop: spacing.lg,
  },
  video: {
    width: '100%',
    aspectRatio: 16 / 9,
    borderRadius: radius.md,
    backgroundColor: colors.surface,
  },
  actionsRow: {
    flexDirection: 'row',
    gap: spacing.sm,
    marginTop: spacing.lg,
  },
  actionButton: {
    flex: 1,
  },
});
