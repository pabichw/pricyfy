const defaultConfig = require('tailwindcss/defaultConfig')
const formsPlugin = require('@tailwindcss/forms')

/** @type {import('tailwindcss/types').Config} */
const config = {
	content: ['src/**/*.{tsx,html}'],
	theme: {
		extend: {
			fontFamily: {
				sans: ['Inter var', ...defaultConfig.theme.fontFamily.sans]
			}
		}
	},
	experimental: { optimizeUniversalDefaults: true },
	plugins: [formsPlugin]
}
module.exports = config
