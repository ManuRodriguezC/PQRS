/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html', // Ruta a tus archivos HTML de Django
    './**/*.html',           // Otras rutas de HTML en tu proyecto
    './static/js/**/*.js',   // Si tienes archivos JavaScript con clases de Tailwind
  ],
  theme: {
    extend: {
    },
  },
  plugins: [],
}
