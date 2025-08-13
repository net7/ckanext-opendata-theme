module.exports = {
    plugins: [
      require('postcss-import-ext-glob'),
      require('postcss-import'),
      require('tailwindcss'),
      require('autoprefixer'),
    ]
}
// module.exports = {
//     plugins: {
//         "postcss-import-ext-glob": {},
//         "postcss-import": {},
//         tailwindcss: {},
//         autoprefixer: {},
//     },
// };