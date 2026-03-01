/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'media',
  theme: {
    extend: {
      colors: {
        background: 'var(--color-background)',
        'primary-text': 'var(--color-primary-text)',
        'card-background': 'var(--color-card-background)',
        accent: 'var(--color-accent)',
        'secondary-accent': 'var(--color-secondary-accent)',
      },
    },
  },
  plugins: [],
}
