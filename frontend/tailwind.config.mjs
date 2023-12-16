/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	theme: {
		extend: {
			colors: {
				'electric-violet': {
					'50': 'hsl(290, 100%, 98%)',
					'100': 'hsl(283, 100%, 95%)',
					'200': 'hsl(286, 100%, 90%)',
					'300': 'hsl(287, 100%, 82%)',
					'400': 'hsl(288, 100%, 71%)',
					'500': 'hsl(286, 100%, 61%)',
					'600': 'hsl(287, 83%, 45%)',
					'700': 'hsl(288, 86%, 40%)',
					'800': 'hsl(289, 83%, 33%)',
					'900': 'hsl(290, 76%, 28%)',
					'950': 'hsl(290, 100%, 17%)',
				},
			}
		},
	},
	plugins: [],
}
