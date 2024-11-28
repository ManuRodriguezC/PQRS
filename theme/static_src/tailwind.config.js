/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
    ],
    theme: {
        extend: {
            backgroundColor: {
                'cootra': '#2F52A0',
            },
            backgroundImage: {
                'backlogin': 'radial-gradient(circle at 19% 90%, rgba(190, 190, 190,0.04) 0%, rgba(190, 190, 190,0.04) 17%,transparent 17%, transparent 100%),radial-gradient(circle at 73% 2%, rgba(78, 78, 78,0.04) 0%, rgba(78, 78, 78,0.04) 94%,transparent 94%, transparent 100%),radial-gradient(circle at 45% 2%, rgba(18, 18, 18,0.04) 0%, rgba(18, 18, 18,0.04) 55%,transparent 55%, transparent 100%),radial-gradient(circle at 76% 60%, rgba(110, 110, 110,0.04) 0%, rgba(110, 110, 110,0.04) 34%,transparent 34%, transparent 100%),radial-gradient(circle at 68% 56%, rgba(246, 246, 246,0.04) 0%, rgba(246, 246, 246,0.04) 16%,transparent 16%, transparent 100%),radial-gradient(circle at 71% 42%, rgba(156, 156, 156,0.04) 0%, rgba(156, 156, 156,0.04) 47%,transparent 47%, transparent 100%),radial-gradient(circle at 46% 82%, rgba(247, 247, 247,0.04) 0%, rgba(247, 247, 247,0.04) 39%,transparent 39%, transparent 100%),radial-gradient(circle at 50% 47%, rgba(209, 209, 209,0.04) 0%, rgba(209, 209, 209,0.04) 45%,transparent 45%, transparent 100%),linear-gradient(90deg, rgb(23,0,90),rgb(23,2,147));',
                'backpqr': 'radial-gradient(circle at 28% 51%, rgba(206, 206, 206,0.03) 0%, rgba(206, 206, 206,0.03) 17%,transparent 17%, transparent 100%),radial-gradient(circle at 45% 10%, rgba(10, 10, 10,0.03) 0%, rgba(10, 10, 10,0.03) 45%,transparent 45%, transparent 100%),radial-gradient(circle at 48% 44%, rgba(74, 74, 74,0.03) 0%, rgba(74, 74, 74,0.03) 84%,transparent 84%, transparent 100%),radial-gradient(circle at 47% 50%, rgba(186, 186, 186,0.03) 0%, rgba(186, 186, 186,0.03) 23%,transparent 23%, transparent 100%),radial-gradient(circle at 29% 70%, rgba(9, 9, 9,0.03) 0%, rgba(9, 9, 9,0.03) 32%,transparent 32%, transparent 100%),radial-gradient(circle at 2% 75%, rgba(179, 179, 179,0.03) 0%, rgba(179, 179, 179,0.03) 19%,transparent 19%, transparent 100%),radial-gradient(circle at 2% 36%, rgba(26, 26, 26,0.03) 0%, rgba(26, 26, 26,0.03) 1%,transparent 1%, transparent 100%),radial-gradient(circle at 53% 70%, rgba(90, 90, 90,0.03) 0%, rgba(90, 90, 90,0.03) 55%,transparent 55%, transparent 100%),radial-gradient(circle at 28% 92%, rgba(31, 31, 31,0.03) 0%, rgba(31, 31, 31,0.03) 35%,transparent 35%, transparent 100%),linear-gradient(90deg, rgb(255,255,255),rgb(255,255,255));',
            },
            colors: {
                'cootra': '#2F52A0'
            },
            boxShadow: {
                'con': 'rgba(0, 0, 0, 0.35) 0px 5px 15px;'
            },
            scale: {
                '102': '1.02'
            },
            screen: {
                'ss': '30px'
            }
          },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
