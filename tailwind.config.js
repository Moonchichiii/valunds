/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./apps/**/*.html", "./templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        snow: "#F9FAFB",
        birch: "#F4F1EA",
        fjord: "#5B7C88",
        moss: "#7D8C71"
      }
    }
  },
  plugins: []
}
