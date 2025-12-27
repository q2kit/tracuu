/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "assets/css/main.css",
      "src/templates/**/*.html",
    ],
    plugins: [require("daisyui")],
    theme: {
      fontFamily: {
        sans: ["Calibri", "system-ui", "sans-serif", "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"],
      },
      extend: {
        colors: {
          primary: "#4F46E5",      // Indigo - trust & professionalism
          secondary: "#10B981",    // Emerald - positive action
          accent: "#F59E0B",       // Amber - highlights & CTAs
          success: "#10B981",      // Emerald - success states
          warning: "#F59E0B",      // Amber - warnings
          error: "#EF4444",        // Red - errors & deletions
          info: "#06B6D4",         // Cyan - informational
        },
      },
    },
    daisyui: {
      themes: ["light"],
      base: true,
      styled: true,
      utils: true,
      prefix: "",
      logs: true,
      themeRoot: ":root",
    },
  }
