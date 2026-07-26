import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { useEffect, useState } from 'react';
import { Alert, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { GradientButton } from '../components/GradientButton';
import { colors, radius, spacing, typography } from '../theme';
import { loadSettings, saveSettings } from '../lib/storage';
import { AppSettings, DEFAULT_SETTINGS } from '../types';
import { RootStackParamList } from '../navigation/types';

type Props = NativeStackScreenProps<RootStackParamList, 'Settings'>;

export function SettingsScreen({ navigation }: Props) {
  const [settings, setSettings] = useState<AppSettings>(DEFAULT_SETTINGS);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadSettings().then(setSettings);
  }, []);

  async function handleSave() {
    setSaving(true);
    try {
      await saveSettings(settings);
      Alert.alert('Đã lưu', 'Cài đặt của bạn đã được lưu.');
      navigation.goBack();
    } finally {
      setSaving(false);
    }
  }

  return (
    <SafeAreaView style={styles.screen} edges={['top', 'left', 'right']}>
      <ScrollView keyboardShouldPersistTaps="handled">
        <Text style={typography.title}>Cài đặt</Text>
        <Text style={[typography.subtitle, { marginTop: spacing.xs, marginBottom: spacing.lg }]}>
          Kết nối API tạo video thật bằng Replicate. Bỏ trống để dùng chế độ demo.
        </Text>

        <Field
          label="REPLICATE API TOKEN"
          value={settings.replicateApiToken}
          onChangeText={(replicateApiToken) => setSettings((s) => ({ ...s, replicateApiToken }))}
          placeholder="r8_..."
          secure
        />
        <Field
          label="MODEL (owner/name)"
          value={settings.model}
          onChangeText={(model) => setSettings((s) => ({ ...s, model }))}
          placeholder="minimax/video-01"
        />
        <Field
          label="TÊN TRƯỜNG ẢNH ĐẦU VÀO"
          value={settings.imageField}
          onChangeText={(imageField) => setSettings((s) => ({ ...s, imageField }))}
          placeholder="first_frame_image"
        />
        <Field
          label="TÊN TRƯỜNG MÔ TẢ (PROMPT)"
          value={settings.promptField}
          onChangeText={(promptField) => setSettings((s) => ({ ...s, promptField }))}
          placeholder="prompt"
        />

        <Text style={[typography.subtitle, { marginTop: spacing.sm, marginBottom: spacing.lg }]}>
          Lưu ý: tên trường đầu vào tùy theo model bạn chọn trên Replicate. Kiểm tra trang model đó
          để biết tên trường chính xác.
        </Text>

        <GradientButton label="Lưu cài đặt" onPress={handleSave} loading={saving} />
      </ScrollView>
    </SafeAreaView>
  );
}

function Field({
  label,
  value,
  onChangeText,
  placeholder,
  secure,
}: {
  label: string;
  value: string;
  onChangeText: (text: string) => void;
  placeholder?: string;
  secure?: boolean;
}) {
  return (
    <View style={{ marginBottom: spacing.md }}>
      <Text style={[typography.label, { marginBottom: spacing.xs }]}>{label}</Text>
      <TextInput
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder}
        placeholderTextColor={colors.textMuted}
        autoCapitalize="none"
        autoCorrect={false}
        secureTextEntry={secure}
        style={styles.input}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: colors.background,
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.md,
  },
  input: {
    borderRadius: radius.md,
    borderWidth: 1,
    borderColor: colors.border,
    backgroundColor: colors.surface,
    color: colors.text,
    padding: spacing.md,
  },
});
