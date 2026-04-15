import { readFileSync } from "node:fs";

const envFile = process.argv[2] ?? ".env.development";
const content = readFileSync(envFile, "utf8");
const values = {};

for (const rawLine of content.split("\n")) {
  const line = rawLine.trim();

  if (!line || line.startsWith("#")) {
    continue;
  }

  const separator = line.indexOf("=");

  if (separator === -1) {
    continue;
  }

  const key = line.slice(0, separator).trim();
  const value = line.slice(separator + 1).trim();
  values[key] = value;
}

const siteConfig = {
  webUrl: values.NEXT_PUBLIC_WEB_URL ?? "",
  projectName: values.NEXT_PUBLIC_PROJECT_NAME ?? "",
  googleAnalyticsId: values.NEXT_PUBLIC_GOOGLE_ANALYTICS_ID ?? "",
  clarityProjectId: values.NEXT_PUBLIC_CLARITY_PROJECT_ID ?? ""
};

process.stdout.write(
  `window.__SITE_CONFIG__ = ${JSON.stringify(siteConfig, null, 2)};\n`
);
