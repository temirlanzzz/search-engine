import { test, expect } from '@playwright/test'

test('search, explain, compare, and recover from an empty result', async ({ page }, testInfo) => {
  const errors: string[] = []
  page.on('pageerror', (e) => errors.push(e.message))
  await page.goto('/')
  await expect(
    page.getByRole('heading', { name: 'Good search leaves a paper trail.' }),
  ).toBeVisible()
  await expect(page.locator('.result-card')).not.toHaveCount(0)
  await expect(page.locator('.score-total strong')).toContainText(/\d+\.\d{3}/)
  await page.getByLabel('Subject').selectOption('Data structures')
  await expect(page.locator('.result-card')).toHaveCount(1)
  await expect(page.locator('.comparison')).toContainText('ranks #1')
  await page.getByLabel('Subject').selectOption('All subjects')
  await page.getByLabel('Ranking model').selectOption('tfidf')
  await expect(page.locator('.model-tag')).toHaveText('TFIDF')
  await page.getByLabel('YOUR QUESTION, IN A FEW WORDS').fill('document neverindexedword')
  await page.getByLabel('Match terms').selectOption('AND')
  await expect(page.locator('.result-card')).toHaveCount(0)
  await expect(page.getByText('Every term must match.', { exact: false })).toBeVisible()
  await page.getByLabel('Match terms').selectOption('OR')
  await expect(page.locator('.result-card')).not.toHaveCount(0)
  await page.getByRole('button', { name: 'Clear search' }).click()
  await expect(page.getByText('Start with a word or two.', { exact: false })).toBeVisible()
  await page.getByRole('button', { name: 'document length ↗', exact: true }).click()
  await page.getByLabel('Ranking model').selectOption('bm25')
  await page.getByText('Read the full document', { exact: true }).click()
  await expect(page.locator('.inspector details[open]')).toBeVisible()
  await page.screenshot({ path: testInfo.outputPath('search.png'), fullPage: true })
  expect(
    await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth),
  ).toBeTruthy()
  expect(errors).toEqual([])
})

test('validated import stays local, errors preserve collection, restore is repeatable', async ({
  page,
}, testInfo) => {
  await page.goto('/')
  await page.getByRole('button', { name: 'The reading room', exact: true }).click()
  await page.locator('input[type=file]').setInputFiles({
    name: 'notes.json',
    mimeType: 'application/json',
    buffer: Buffer.from(
      JSON.stringify([{ title: 'My observatory', text: 'Telescopes reveal distant galaxies.' }]),
    ),
  })
  await expect(page.locator('.document-grid article')).toHaveCount(1)
  await page.locator('input[type=file]').setInputFiles({
    name: 'bad.json',
    mimeType: 'application/json',
    buffer: Buffer.from('[{"title":"Missing text"}]'),
  })
  await expect(page.getByRole('status')).toContainText('needs a nonempty title and text')
  await expect(page.locator('.document-grid article')).toHaveCount(1)
  await page.getByRole('button', { name: 'Search collection', exact: true }).click()
  await page.getByLabel('YOUR QUESTION, IN A FEW WORDS').fill('galaxies')
  await expect(page.locator('.result-card')).toHaveCount(1)
  await page.getByRole('button', { name: 'The reading room', exact: true }).click()
  await page.getByRole('button', { name: 'Restore collection' }).click()
  await expect(page.locator('.document-grid article')).toHaveCount(12)
  await page.screenshot({ path: testInfo.outputPath('reading-room.png'), fullPage: true })
})
