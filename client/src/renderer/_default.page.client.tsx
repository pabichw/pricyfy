import { hydrateRoot } from 'react-dom/client'
import PageShell from 'renderer/PageShell'
import type { PageContextClient } from 'renderer/PageShell/types'

import '../index.css'

export { render }

async function render(pageContext: PageContextClient) {
	const { Page, pageProps } = pageContext
	hydrateRoot(
		document.querySelector('#root')!,
		<PageShell pageContext={pageContext}>
			<Page {...pageProps} />
		</PageShell>
	)
}
