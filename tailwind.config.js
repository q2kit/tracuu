/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "templates/*.html",
      "assets/css/main.css",
      "templates/**/*.html",
    ],
    plugins: [require("daisyui")],
    theme: {
      fontFamily: {
        sans: ['Calibri', 'system-ui', 'sans-serif'],
      },
      extend: {
        colors: {
        },
      },
    },
    daisyui: {
      themes: [
        {
          light: {
            ...require("daisyui/src/theming/themes")["light"],
          },
        }
      ],
      base: true,
      styled: true,
      utils: true,
      prefix: "",
      logs: true,
      themeRoot: ":root",
    },
  }
