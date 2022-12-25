import { hydrateRoot } from 'react-dom/client'
import PageShell from 'renderer/PageShell'
import type { PageContextClient } from 'renderer/PageShell/types'

export { render }

async function render(pageContext: PageContextClient) {
	const { Page, pageProps } = pageContext
	hydrateRoot(
		document.getElementById('root')!,
		<PageShell pageContext={pageContext}>
			<Page {...pageProps} />
		</PageShell>
	)
}
