import ReactDOMServer from 'react-dom/server'
import PageShell from 'renderer/PageShell'
import type { PageContextServer } from 'renderer/PageShell/types'
import { dangerouslySkipEscape, escapeInject } from 'vite-plugin-ssr'
import logoUrl from './logo.svg'

import '../index.css'

export { render }
export const passToClient = ['pageProps', 'urlPathname']

async function render(pageContext: PageContextServer) {
	const { Page, pageProps } = pageContext
	const pageHtml = ReactDOMServer.renderToString(
		<PageShell pageContext={pageContext}>
			<Page {...pageProps} />
		</PageShell>
	)

	const { documentProps } = pageContext.exports
	const title = (documentProps && documentProps.title) || 'Vite SSR app'
	const desc =
		(documentProps && documentProps.description) ||
		'App using Vite + vite-plugin-ssr'

	const documentHtml = escapeInject`
		<!DOCTYPE html>
		<html
			lang="en"
			class="text-gray-900 antialiased bg-gray-100"
		>
			<head>
				<meta charset="UTF-8" />
				<link rel="icon" type="image/png" href="${logoUrl}" />
				<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
				<link rel="stylesheet" href="https://rsms.me/inter/inter.css"> 
				<meta name="viewport" content="width=device-width, initial-scale=1.0" />
				<meta name="description" content="${desc}" />
				<meta name="theme-color" content="#42b883" />
				<title>${title}</title>
			</head>
			<body>
				<noscript>You need to enable JavaScript to run this app.</noscript>
				<div id="root">${dangerouslySkipEscape(pageHtml)}</div>
			</body>
		</html>
	`

	return {
		documentHtml,
		pageContext: {
			// We can add some `pageContext` here, which is useful if we want to do page redirection https://vite-plugin-ssr.com/page-redirection
		}
	}
}
