export const colors = {
  background: '#07060d',
  surface: '#13111f',
  surfaceRaised: '#1c1930',
  border: '#2a2640',
  text: '#f4f2fb',
  textMuted: '#9891b5',
  pink: '#ec4899',
  pinkMuted: 'rgba(236, 72, 153, 0.16)',
  cyan: '#22d3ee',
  cyanMuted: 'rgba(34, 211, 238, 0.16)',
  success: '#34d399',
  danger: '#f87171',
  overlay: 'rgba(7, 6, 13, 0.72)',
};

export const gradients = {
  primary: [colors.pink, colors.cyan] as const,
  card: ['#1c1930', '#13111f'] as const,
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
};

export const radius = {
  sm: 10,
  md: 16,
  lg: 24,
  pill: 999,
};

export const typography = {
  title: { fontSize: 24, fontWeight: '700' as const, color: colors.text },
  subtitle: { fontSize: 15, fontWeight: '500' as const, color: colors.textMuted },
  body: { fontSize: 15, fontWeight: '400' as const, color: colors.text },
  label: { fontSize: 13, fontWeight: '600' as const, color: colors.textMuted },
};
