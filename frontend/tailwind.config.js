/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./**/*.{vue,js,ts}'],
  theme: {
    extend: {
      colors: {
        primary:   '#f3d6ff',
        secondary: '#eeffee',
        tertiary:  '#8923AE',
        accent:    '#DAFF99',
        muted:     '#E9ECEF',
        text:      '#4e0078',
      },
      fontFamily: {
        sans: ['"Inter"', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
