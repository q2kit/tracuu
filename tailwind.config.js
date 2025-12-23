/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "src/templates/*.html",
      "assets/css/main.css",
      "src/templates/**/*.html",
    ],
    plugins: [require("daisyui")],
    theme: {
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
