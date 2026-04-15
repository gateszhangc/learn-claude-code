const yearNode = document.querySelector("#year");
const siteConfig = window.__SITE_CONFIG__ ?? {};
const isLocalRuntime = ["127.0.0.1", "localhost"].includes(window.location.hostname);

if (yearNode) {
  yearNode.textContent = new Date().getFullYear();
}

const injectScript = (src) => {
  const script = document.createElement("script");
  script.src = src;
  script.async = true;
  document.head.appendChild(script);
};

const setupGoogleAnalytics = () => {
  if (!siteConfig.googleAnalyticsId || isLocalRuntime) {
    return;
  }

  window.dataLayer = window.dataLayer || [];
  window.gtag = function gtag() {
    window.dataLayer.push(arguments);
  };

  injectScript(`https://www.googletagmanager.com/gtag/js?id=${siteConfig.googleAnalyticsId}`);
  window.gtag("js", new Date());
  window.gtag("config", siteConfig.googleAnalyticsId, {
    page_path: window.location.pathname + window.location.hash
  });
};

const setupClarity = () => {
  if (!siteConfig.clarityProjectId || isLocalRuntime) {
    return;
  }

  ((c, l, a, r, i, t, y) => {
    c[a] =
      c[a] ||
      function clarityProxy() {
        (c[a].q = c[a].q || []).push(arguments);
      };
    t = l.createElement(r);
    t.async = 1;
    t.src = `https://www.clarity.ms/tag/${i}`;
    y = l.getElementsByTagName(r)[0];
    y.parentNode.insertBefore(t, y);
  })(window, document, "clarity", "script", siteConfig.clarityProjectId);
};

setupGoogleAnalytics();
setupClarity();

document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener("click", (event) => {
    const href = link.getAttribute("href");

    if (!href || href === "#") {
      return;
    }

    const target = document.querySelector(href);

    if (!target) {
      return;
    }

    event.preventDefault();
    target.scrollIntoView({ behavior: "smooth", block: "start" });
    history.replaceState(null, "", href);

    if (siteConfig.googleAnalyticsId && window.gtag) {
      window.gtag("event", "cta_navigation", {
        target_section: href.replace("#", "")
      });
    }
  });
});
