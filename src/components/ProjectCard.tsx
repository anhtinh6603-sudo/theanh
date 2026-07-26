import { Image } from 'expo-image';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { colors, radius, spacing, typography } from '../theme';
import { Project } from '../types';

const STATUS_LABEL: Record<Project['status'], string> = {
  idle: 'Chờ xử lý',
  starting: 'Đang khởi tạo',
  processing: 'Đang tạo video',
  succeeded: 'Hoàn thành',
  failed: 'Lỗi',
};

const STATUS_COLOR: Record<Project['status'], string> = {
  idle: colors.textMuted,
  starting: colors.cyan,
  processing: colors.cyan,
  succeeded: colors.success,
  failed: colors.danger,
};

type Props = {
  project: Project;
  onPress: () => void;
};

export function ProjectCard({ project, onPress }: Props) {
  return (
    <Pressable onPress={onPress} style={styles.card}>
      <Image source={{ uri: project.sourceImageUri }} style={styles.thumb} contentFit="cover" />
      <View style={styles.body}>
        <Text style={typography.body} numberOfLines={2}>
          {project.prompt || 'Không có mô tả'}
        </Text>
        <View style={styles.statusRow}>
          <View style={[styles.dot, { backgroundColor: STATUS_COLOR[project.status] }]} />
          <Text style={[typography.label, { color: STATUS_COLOR[project.status] }]}>
            {STATUS_LABEL[project.status]}
            {project.mock ? ' · demo' : ''}
          </Text>
        </View>
      </View>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    flexDirection: 'row',
    backgroundColor: colors.surface,
    borderRadius: radius.md,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.sm,
    marginBottom: spacing.sm,
    gap: spacing.sm,
  },
  thumb: {
    width: 64,
    height: 64,
    borderRadius: radius.sm,
    backgroundColor: colors.surfaceRaised,
  },
  body: {
    flex: 1,
    justifyContent: 'center',
    gap: spacing.xs,
  },
  statusRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
  },
  dot: {
    width: 6,
    height: 6,
    borderRadius: 3,
  },
});
