/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#FF6363',
        secondary: "currentColor"
      },
      animation: {
        typing: "typing 4s steps(30), blink 0.1s step-end infinite"
      },
      keyframes: {
        typing: {
          from: { width: "0" },
          to: { width: "14ch" }
        }
      },
      blink: {
        from: { "border-right-color": "transparent" },
        to: { "border-right-color": "black" },
      },
    },
    container: {
      center: true,
    }
  },
  plugins: [],

}