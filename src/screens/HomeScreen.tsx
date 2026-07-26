import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { useFocusEffect } from '@react-navigation/native';
import { useCallback, useState } from 'react';
import { FlatList, Pressable, StyleSheet, Text, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { ProjectCard } from '../components/ProjectCard';
import { GradientButton } from '../components/GradientButton';
import { colors, spacing, typography } from '../theme';
import { loadProjects } from '../lib/storage';
import { Project } from '../types';
import { RootStackParamList } from '../navigation/types';

type Props = NativeStackScreenProps<RootStackParamList, 'Home'>;

export function HomeScreen({ navigation }: Props) {
  const [projects, setProjects] = useState<Project[]>([]);

  useFocusEffect(
    useCallback(() => {
      loadProjects().then(setProjects);
    }, []),
  );

  return (
    <SafeAreaView style={styles.screen} edges={['top', 'left', 'right']}>
      <View style={styles.header}>
        <View>
          <Text style={typography.title}>Ảnh thành video</Text>
          <Text style={typography.subtitle}>Biến ảnh của bạn thành video bằng AI</Text>
        </View>
        <Pressable onPress={() => navigation.navigate('Settings')} style={styles.settingsButton}>
          <Text style={{ fontSize: 20 }}>⚙️</Text>
        </Pressable>
      </View>

      <FlatList
        data={projects}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.list}
        ListEmptyComponent={
          <View style={styles.empty}>
            <Text style={typography.subtitle}>
              Chưa có dự án nào. Nhấn "Tạo video mới" để bắt đầu.
            </Text>
          </View>
        }
        renderItem={({ item }) => (
          <ProjectCard
            project={item}
            onPress={() => navigation.navigate('Result', { projectId: item.id })}
          />
        )}
      />

      <View style={styles.footer}>
        <GradientButton label="Tạo video mới" onPress={() => navigation.navigate('Create')} />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: colors.background,
    paddingHorizontal: spacing.lg,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop: spacing.md,
    paddingBottom: spacing.lg,
  },
  settingsButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.border,
    alignItems: 'center',
    justifyContent: 'center',
  },
  list: {
    flexGrow: 1,
  },
  empty: {
    paddingVertical: spacing.xl,
    alignItems: 'center',
  },
  footer: {
    paddingBottom: spacing.lg,
    paddingTop: spacing.sm,
  },
});
