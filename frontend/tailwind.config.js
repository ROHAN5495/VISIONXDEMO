/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        investigative: {
          950: '#060B18',
          900: '#0B132B',
          850: '#111D3E',
          800: '#1C2541',
          700: '#2A3B5C',
          600: '#3A506B',
          500: '#5C769D',
          400: '#8FA4C4',
          300: '#C2D1E4',
          100: '#E9EEF5',
          50: '#F4F7FB'
        },
        electric: {
          500: '#2563EB',
          600: '#1D4ED8',
          700: '#1E40AF',
          glow: '#3B82F6'
        },
        evidence: {
          support: '#10B981',
          contradict: '#EF4444',
          amber: '#F59E0B',
          context: '#3B82F6'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'Consolas', 'monospace']
      }
    },
  },
  plugins: [],
}
