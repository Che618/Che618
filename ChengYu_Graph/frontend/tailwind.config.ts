import type { Config } from 'tailwindcss'

export default {
  content: ['./index.html', './src/**/*.{vue,ts,tsx,js,jsx}'],
  theme: {
    extend: {
      colors: {
        'bg-documentary': '#232121',
        'card-surface': '#2F2D2D',
        'text-primary': '#E6E0D6',
        'data-birth': '#E07A5F',
        'data-policy': '#81B29A',
        'text-muted': '#9CA3AF'
      },
      fontFamily: {
        serif: ['"Noto Serif SC"', '"Songti SC"', 'serif'],
        sans: ['"Inter"', '"Noto Sans SC"', 'system-ui', 'sans-serif']
      }
    }
  },
  plugins: []
} satisfies Config
