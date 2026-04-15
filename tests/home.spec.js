import { expect, test } from "@playwright/test";

test("homepage renders the keyword-focused hero and SEO metadata", async ({ page }) => {
  await page.goto("/");

  await expect(page).toHaveTitle(/Learn Claude Code/i);
  await expect(page.getByRole("heading", { level: 1, name: /learn claude code/i })).toBeVisible();

  await expect(page.locator('meta[name="description"]')).toHaveAttribute(
    "content",
    /learn Claude Code/i
  );
  await expect(page.locator('link[rel="canonical"]')).toHaveAttribute(
    "href",
    "https://learn-claude-code.lol/"
  );
  await expect(page.locator('meta[property="og:image"]')).toHaveAttribute(
    "content",
    "https://learn-claude-code.lol/assets/brand/og-card.png"
  );
  await expect(page.locator('meta[property="og:site_name"]')).toHaveAttribute(
    "content",
    "Learn Claude Code"
  );
});

test("primary call to action jumps to the learning path", async ({ page }) => {
  await page.goto("/");

  await page.getByRole("link", { name: "Start Learning" }).first().click();
  await expect(page).toHaveURL(/#learning-path$/);
  await expect(page.locator("#learning-path")).toBeInViewport();
});

test("brand and favicon assets are reachable", async ({ page }) => {
  const responses = await Promise.all([
    page.request.get("/assets/brand/logo.svg"),
    page.request.get("/assets/brand/favicon.svg"),
    page.request.get("/assets/brand/og-card.png"),
    page.request.get("/favicon.ico"),
    page.request.get("/apple-touch-icon.png"),
    page.request.get("/site-config.js")
  ]);

  responses.forEach((response) => expect(response.ok()).toBeTruthy());
});

test("site config exposes analytics settings for production wiring", async ({ page }) => {
  const response = await page.request.get("/site-config.js");
  const body = await response.text();

  expect(body).toContain("clarityProjectId");
  expect(body).toContain("wc06my50va");
});

test("desktop and mobile layouts render without collapsing key sections", async ({ page }, testInfo) => {
  await page.goto("/");
  await expect(page.locator(".hero")).toBeVisible();
  await expect(page.locator(".card-grid")).toBeVisible();
  await expect(page.locator(".faq-section")).toBeVisible();

  await page.screenshot({ path: testInfo.outputPath("homepage.png"), fullPage: true });
});
