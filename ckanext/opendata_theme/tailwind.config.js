/** @type {import('tailwindcss').Config} */
module.exports = {
    prefix: 'rtds-',
    content: [
        // './src/components/**/*.{html,njk,js,yml}',
        // './src/templates/**/*.{html,njk,js,yml}',
        './src/css/**/*.css',
        './templates/**/*.html',
    ],
    theme: {
        screens: {
            'xs': '360px',
            // => @media (min-width: 360px) { ... }

            'sm': '640px',
            // => @media (min-width: 640px) { ... }

            'md': '768px',
            // => @media (min-width: 768px) { ... }

            'lg': '1024px',
            // => @media (min-width: 1024px) { ... }

            'xl': '1280px',
            // => @media (min-width: 1280px) { ... }

            '2xl': '1536px',
            // => @media (min-width: 1536px) { ... }
        },
        spacing: {
            '0': 'var(--spacing-0)',
            '0.5': 'var(--spacing-0-5)',
            '1': 'var(--spacing-1)',
            '1.5': 'var(--spacing-1-5)',
            '2': 'var(--spacing-2)',
            '2.5': 'var(--spacing-2-5)',
            '3': 'var(--spacing-3)',
            '3.5': 'var(--spacing-3-5)',
            '4': 'var(--spacing-4)',
            '5': 'var(--spacing-5)',
            '6': 'var(--spacing-6)',
            '7': 'var(--spacing-7)',
            '8': 'var(--spacing-8)',
            '9': 'var(--spacing-9)',
            '10': 'var(--spacing-10)',
            '11': 'var(--spacing-11)',
            '12': 'var(--spacing-12)',
            '14': 'var(--spacing-14)',
            '16': 'var(--spacing-16)',
            '20': 'var(--spacing-20)',
            '24': 'var(--spacing-24)',
            '28': 'var(--spacing-28)',
            '32': 'var(--spacing-32)',
            '36': 'var(--spacing-36)',
            '40': 'var(--spacing-40)',
            '44': 'var(--spacing-44)',
            '48': 'var(--spacing-48)',
            '52': 'var(--spacing-52)',
            '56': 'var(--spacing-56)',
            '60': 'var(--spacing-60)',
            '64': 'var(--spacing-64)',
            '72': 'var(--spacing-72)',
            '80': 'var(--spacing-80)',
            '96': 'var(--spacing-96)',
        },
        fontFamily: {
            'body': ['var(--fontfamily-body)', 'sans-serif'],
            'heading': ['var(--fontfamily-heading)', 'sans-serif'],
        },
        fontSize: {
            xs: 'var(--fontsize-text-xs)',        // 0.75rem - 12px
            sm: 'var(--fontsize-text-sm)',        // 0.875rem - 14px
            base: 'var(--fontsize-text-base)',    // 1rem - 16px
            lg: 'var(--fontsize-text-lg)',        // 1.125rem - 18px
            xl: 'var(--fontsize-text-xl)',        // 1.25rem - 20px
            '2xl': 'var(--fontsize-text-2xl)',    // 1.5rem - 24px
            '3xl': 'var(--fontsize-text-3xl)',    // 2rem - 32px (1.875rem - 30px body?)
            '4xl': 'var(--fontsize-text-4xl)',    // 2.25rem - 40px (36px heading?)
            '5xl': 'var(--fontsize-text-5xl)',    // 3rem - 48px
            '6xl': 'var(--fontsize-text-6xl)',    // 3.75rem - 60px
            '7xl': 'var(--fontsize-text-7xl)',    // 4.5rem - 72px
            '8xl': 'var(--fontsize-text-8xl)',    // 6rem - 96px
            '9xl': 'var(--fontsize-text-9xl)',    // 8rem - 128px
        },
        colors: {
            transparent: 'transparent',
            current: 'currentColor',
            black: '#000000',
            white: '#ffffff',
            social: {
                facebook: 'var(--color-social-facebook)',
                instagram: 'var(--color-social-instagram)',
                linkedin: 'var(--color-social-linkedin)',
                x: 'var(--color-social-x)',
                youtube: 'var(--color-social-youtube)',
            },
            success: {
                dark: 'var(--color-success-dark)',
                DEFAULT: 'var(--color-success)',
                light: 'var(--color-success-light)',
            },
            error: {
                dark: 'var(--color-error-dark)',
                DEFAULT: 'var(--color-error)',
                light: 'var(--color-error-light)',
            },
            warn: {
                dark: 'var(--color-warn-dark)',
                DEFAULT: 'var(--color-warn)',
                light: 'var(--color-warn-light)',
            },
            info: {
                dark: 'var(--color-info-dark)',
                DEFAULT: 'var(--color-info)',
                light: 'var(--color-info-light)',
            },
            allerta: {
                verde: 'var(--color-allerta-verde)',
                giallo: 'var(--color-allerta-giallo)',
                arancione: 'var(--color-allerta-arancione)',
                rosso: 'var(--color-allerta-rosso)',
            },
            primary: {
                50: 'var(--color-primary-50)',
                100: 'var(--color-primary-100)',
                200: 'var(--color-primary-200)',
                300: 'var(--color-primary-300)',
                400: 'var(--color-primary-400)',
                500: 'var(--color-primary-500)',
                600: 'var(--color-primary-600)',
                700: 'var(--color-primary-700)',
                800: 'var(--color-primary-800)',
                900: 'var(--color-primary-900)'
            },
            secondary: {
                50: 'var(--color-secondary-50)',
                100: 'var(--color-secondary-100)',
                200: 'var(--color-secondary-200)',
                300: 'var(--color-secondary-300)',
                400: 'var(--color-secondary-400)',
                500: 'var(--color-secondary-500)',
                600: 'var(--color-secondary-600)',
                700: 'var(--color-secondary-700)',
                800: 'var(--color-secondary-800)',
                900: 'var(--color-secondary-900)'
            },
            neutral: {
                50: 'var(--color-neutral-50)',
                100: 'var(--color-neutral-100)',
                200: 'var(--color-neutral-200)',
                300: 'var(--color-neutral-300)',
                400: 'var(--color-neutral-400)',
                500: 'var(--color-neutral-500)',
                600: 'var(--color-neutral-600)',
                700: 'var(--color-neutral-700)',
                800: 'var(--color-neutral-800)',
                900: 'var(--color-neutral-900)'
            },
            brand: {
                '00': 'var(--color-brand-00)',
                '01': 'var(--color-brand-01)',
            },
            salvia: {
                DEFAULT: 'var(--color-salvia)',
            },
            bando: {
                'aperto': 'var(--color-bando-aperto)',
                'in-attivazione': 'var(--color-bando-in-attivazione)',
            },
            archiviato: {
                DEFAULT: 'var(--color-archiviato)',
            },
            focusring: {
                DEFAULT: 'var(--color-focusring)',
            }
        },
        container: {
            center: true,
        },
        aspectRatio: {
            auto: 'auto',
            square: '1 / 1',
            video: '16 / 9',
            horizontal: '6.8 / 2.5',
            wide: '3 / 1',
            '2-1': '2 / 1',
            '3-2': '3 / 2',
            '4-3': '4 / 3',
            '5-2': '5 / 2',
            '5-3': '5 / 3',
            1: '1',
            2: '2',
            3: '3',
            4: '4',
            5: '5',
            6: '6',
            7: '7',
            8: '8',
            9: '9',
            10: '10',
            11: '11',
            12: '12',
            13: '13',
            14: '14',
            15: '15',
            16: '16',
        },
        extend: {
            spacing: {
                '1e': '1em',
            },
            lineHeight: {
                'medium': '1.57'
            },
            screens: {
                'md-max-w-480-min-h': { 'raw': '(max-width: 1023px) and (min-height: 480px)' },
                'lg-min-w-480-min-h': { 'raw': '(min-width: 1024px) and (min-height: 480px)' },
                'xl-min-w-480-min-h': { 'raw': '(min-width: 1280px) and (min-height: 480px)' },
                'min-h-480': { 'raw': '(min-height: 480px)' },
            },
            backgroundImage: {
                'gradient-01': 'var(--gradient-01)',   
                'gradient-02': 'var(--gradient-02)',
                'gradient-03': 'var(--gradient-03)',
                'gradient-04': 'var(--gradient-04)',
                'gradient-05': 'var(--gradient-05)'
            },
            flex: {
                '2': '2 2 0%'
            },
            fontSize: {
                '3xl': ['2rem', {
                    lineHeight: '1.2'
                }]
            },
            gridTemplateColumns: {
                '1-2': '1fr 2fr',
                '2-1': '2fr 1fr',
                '1-3': '1fr 3fr'
            },
            maxWidth: {
                '1/2': '50%',
            },
            typography: ({ theme }) => ({
                custom: {
                    css: {
                        '--tw-prose-body': 'var(--custom-prose-body)',
                        '--tw-prose-headings': 'var(--custom-prose-headings)',
                        '--tw-prose-lead': 'var(--custom-prose-lead)',
                        '--tw-prose-links': 'var(--custom-prose-links)',
                        '--tw-prose-bold': 'var(--custom-prose-bold)',
                        '--tw-prose-counters': 'var(--custom-prose-counters)',
                        '--tw-prose-bullets': 'var(--custom-prose-bullets)',
                        '--tw-prose-hr': 'var(--custom-prose-hr)',
                        '--tw-prose-quotes': 'var(--custom-prose-quotes)',
                        '--tw-prose-quote-borders': 'var(--custom-prose-quote-borders)',
                        '--tw-prose-captions': 'var(--custom-prose-captions)',
                        '--tw-prose-code': 'var(--custom-prose-code)',
                        '--tw-prose-pre-code': 'var(--custom-prose-pre-code)',
                        '--tw-prose-pre-bg': 'var(--custom-prose-pre-bg)',
                        '--tw-prose-th-borders': 'var(--custom-prose-th-borders)',
                        '--tw-prose-td-borders': 'var(--custom-prose-td-borders)',
                        '--tw-prose-invert-body': 'var(--custom-prose-invert-body)',
                        '--tw-prose-invert-headings': 'var(--custom-prose-invert-headings)',
                        '--tw-prose-invert-lead': 'var(--custom-prose-invert-lead)',
                        '--tw-prose-invert-links': 'var(--custom-prose-invert-links)',
                        '--tw-prose-invert-bold': 'var(--custom-prose-invert-bold)',
                        '--tw-prose-invert-counters': 'var(--custom-prose-invert-counters)',
                        '--tw-prose-invert-bullets': 'var(--custom-prose-invert-bullets)',
                        '--tw-prose-invert-hr': 'var(--custom-prose-invert-hr)',
                        '--tw-prose-invert-quotes': 'var(--custom-prose-invert-quotes)',
                        '--tw-prose-invert-quote-borders': 'var(--custom-prose-invert-quote-borders)',
                        '--tw-prose-invert-captions': 'var(--custom-prose-invert-captions)',
                        '--tw-prose-invert-code': 'var(--custom-prose-invert-code)',
                        '--tw-prose-invert-pre-code': 'var(--custom-prose-invert-pre-code)',
                        '--tw-prose-invert-pre-bg': 'var(--custom-prose-invert-pre-bg)',
                        '--tw-prose-invert-th-borders': 'var(--custom-prose-invert-th-borders)',
                        '--tw-prose-invert-td-borders': 'var(--custom-prose-invert-td-borders)',
                    },
                },
            }),
        }
    },
    variants: {
        translate: ['responsive', 'hover', 'focus', 'active', 'group-hover'],
        extend: {
            backgroundColor: ['active'],
            borderColor: ['active']
        }
    },
    plugins: [
        require('@tailwindcss/aspect-ratio'),
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
    ],
};
