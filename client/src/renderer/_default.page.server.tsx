import ReactDOMServer from 'react-dom/server'
import PageShell from 'renderer/PageShell'
import type { PageContextServer } from 'renderer/PageShell/types'
import { dangerouslySkipEscape, escapeInject } from 'vite-plugin-ssr'
import logoUrl from './logo.svg'

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

	const documentHtml = escapeInject`<!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <link rel="icon" href="${logoUrl}" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta name="description" content="${desc}" />
        <title>${title}</title>
      </head>
      <body>
        <div id="root">${dangerouslySkipEscape(pageHtml)}</div>
      </body>
    </html>`

	return {
		documentHtml,
		pageContext: {
			// We can add some `pageContext` here, which is useful if we want to do page redirection https://vite-plugin-ssr.com/page-redirection
		}
	}
}
