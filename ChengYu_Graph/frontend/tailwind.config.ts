import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'bg-documentary': '#232121',
        'card-surface': '#2F2D2D',
        'text-primary': '#E6E0D6',
        'data-birth': '#E07A5F',
        'data-policy': '#81B29A',
        'text-muted': '#9CA3AF',
      },
      fontFamily: {
        serif: ['"Noto Serif SC"', '"Source Han Serif SC"', '"Songti SC"', 'serif'],
        sans: ['"Inter"', '"Noto Sans SC"', '"Source Han Sans SC"', '"PingFang SC"', 'sans-serif'],
      },
      boxShadow: {
        soft: '0 20px 60px rgba(0, 0, 0, 0.45)',
      },
    },
  },
  plugins: [],
}

export default config
