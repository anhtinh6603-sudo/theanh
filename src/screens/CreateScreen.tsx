import { NativeStackScreenProps } from '@react-navigation/native-stack';
import * as ImagePicker from 'expo-image-picker';
import { Image } from 'expo-image';
import { useState } from 'react';
import { Alert, Pressable, StyleSheet, Text, TextInput, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { GradientButton } from '../components/GradientButton';
import { colors, radius, spacing, typography } from '../theme';
import { upsertProject } from '../lib/storage';
import { RootStackParamList } from '../navigation/types';

type Props = NativeStackScreenProps<RootStackParamList, 'Create'>;

function createProjectId(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

export function CreateScreen({ navigation }: Props) {
  const [imageUri, setImageUri] = useState<string | null>(null);
  const [prompt, setPrompt] = useState('');
  const [submitting, setSubmitting] = useState(false);

  async function pickFromLibrary() {
    const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!permission.granted) {
      Alert.alert('Cần quyền truy cập', 'Vui lòng cho phép truy cập thư viện ảnh.');
      return;
    }
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ['images'],
      quality: 0.9,
      allowsEditing: true,
    });
    if (!result.canceled && result.assets[0]) {
      setImageUri(result.assets[0].uri);
    }
  }

  async function pickFromCamera() {
    const permission = await ImagePicker.requestCameraPermissionsAsync();
    if (!permission.granted) {
      Alert.alert('Cần quyền truy cập', 'Vui lòng cho phép truy cập máy ảnh.');
      return;
    }
    const result = await ImagePicker.launchCameraAsync({ quality: 0.9, allowsEditing: true });
    if (!result.canceled && result.assets[0]) {
      setImageUri(result.assets[0].uri);
    }
  }

  async function handleGenerate() {
    if (!imageUri) {
      Alert.alert('Thiếu ảnh', 'Hãy chọn một ảnh để tạo video.');
      return;
    }
    setSubmitting(true);
    const project = {
      id: createProjectId(),
      createdAt: Date.now(),
      prompt: prompt.trim(),
      sourceImageUri: imageUri,
      videoUri: null,
      status: 'starting' as const,
      error: null,
      mock: false,
    };
    await upsertProject(project);
    setSubmitting(false);
    navigation.replace('Result', { projectId: project.id });
  }

  return (
    <SafeAreaView style={styles.screen} edges={['top', 'left', 'right']}>
      <Text style={typography.title}>Tạo video mới</Text>
      <Text style={[typography.subtitle, { marginTop: spacing.xs, marginBottom: spacing.lg }]}>
        Chọn một ảnh và mô tả chuyển động bạn muốn
      </Text>

      <Pressable style={styles.imageBox} onPress={pickFromLibrary}>
        {imageUri ? (
          <Image source={{ uri: imageUri }} style={styles.image} contentFit="cover" />
        ) : (
          <Text style={typography.subtitle}>Nhấn để chọn ảnh từ thư viện</Text>
        )}
      </Pressable>

      <Pressable onPress={pickFromCamera} style={styles.cameraLink}>
        <Text style={{ color: colors.cyan, fontWeight: '600' }}>Hoặc chụp ảnh mới</Text>
      </Pressable>

      <Text style={[typography.label, { marginTop: spacing.lg, marginBottom: spacing.xs }]}>
        MÔ TẢ CHUYỂN ĐỘNG (không bắt buộc)
      </Text>
      <TextInput
        value={prompt}
        onChangeText={setPrompt}
        placeholder="Ví dụ: máy quay lia nhẹ, khói bốc lên từ món ăn..."
        placeholderTextColor={colors.textMuted}
        style={styles.input}
        multiline
      />

      <View style={styles.spacer} />

      <GradientButton label="Tạo video" onPress={handleGenerate} loading={submitting} />
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
  imageBox: {
    height: 220,
    borderRadius: radius.md,
    borderWidth: 1,
    borderColor: colors.border,
    backgroundColor: colors.surface,
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden',
  },
  image: {
    width: '100%',
    height: '100%',
  },
  cameraLink: {
    alignSelf: 'center',
    marginTop: spacing.sm,
  },
  input: {
    minHeight: 90,
    borderRadius: radius.md,
    borderWidth: 1,
    borderColor: colors.border,
    backgroundColor: colors.surface,
    color: colors.text,
    padding: spacing.md,
    textAlignVertical: 'top',
  },
  spacer: {
    flex: 1,
  },
});
