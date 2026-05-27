/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'ypf-blue': '#0033A0',
        'ypf-yellow': '#FFD700',
      },
    },
  },
  plugins: [],
}
