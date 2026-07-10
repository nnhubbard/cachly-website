/* ==========================================================================
   Cachly Documentation — behaviour
   Builds the sidebar (defined once, here), the mobile drawer, theme toggle,
   on-page table of contents with scroll-spy, and the ⌘K search modal.
   No build step, no dependencies — plain ES.
   ========================================================================== */
(function () {
  "use strict";

  /* ----- Navigation model (single source of truth) -------------------- */
  const NAV = [
    {
      title: "Getting Started",
      items: [
        { id: "index", label: "Welcome", href: "index.html" },
        { id: "getting-started", label: "Accounts & Sign In", href: "getting-started.html" },
        { id: "interface", label: "The Interface", href: "interface.html" },
      ],
    },
    {
      title: "Finding & Logging",
      items: [
        { id: "map", label: "The Map", href: "map.html" },
        { id: "geocache-details", label: "Viewing a Geocache", href: "geocache-details.html" },
        { id: "logging", label: "Logging a Find", href: "logging.html" },
        { id: "logs", label: "Logs, Drafts & History", href: "logs.html" },
        { id: "waypoints", label: "Waypoints & Coordinates", href: "waypoints.html" },
        { id: "trackables", label: "Trackables", href: "trackables.html" },
      ],
    },
    {
      title: "Organize & Search",
      items: [
        { id: "lists", label: "Lists & Offline Sets", href: "lists.html" },
        { id: "search", label: "Search & Filters", href: "search.html" },
        { id: "dt-grid", label: "D/T Grid", href: "dt-grid.html" },
        { id: "profile", label: "Profile & Social", href: "profile.html" },
      ],
    },
    {
      title: "Cachly Pro",
      items: [
        { id: "cachly-pro", label: "Pro Overview", href: "cachly-pro.html", pro: true },
        { id: "offline-maps", label: "Offline Maps & Downloads", href: "offline-maps.html", pro: true },
        { id: "challenge-tools", label: "Challenge Tools", href: "challenge-tools.html", pro: true },
        { id: "multi-user-logging", label: "Multi-User Logging", href: "multi-user-logging.html", pro: true },
        { id: "auto-load", label: "Auto Load Live Map", href: "auto-load.html", pro: true },
        { id: "osm-poi", label: "OSM POI Search", href: "osm-poi.html", pro: true },
        { id: "intelligence", label: "Cachly Intelligence", href: "intelligence.html", pro: true },
        { id: "carplay", label: "CarPlay", href: "carplay.html", pro: true },
      ],
    },
    {
      title: "Offline & Data",
      items: [
        { id: "import-export", label: "Import & Export", href: "import-export.html" },
        { id: "sync-backup", label: "Sync & Backup", href: "sync-backup.html" },
      ],
    },
    {
      title: "Settings & Platforms",
      items: [
        { id: "settings", label: "Settings", href: "settings.html" },
        { id: "apple-watch", label: "Apple Watch", href: "apple-watch.html" },
        { id: "ipad", label: "iPad", href: "ipad.html" },
      ],
    },
    {
      title: "Reference & Help",
      items: [
        { id: "faq", label: "FAQ & Troubleshooting", href: "faq.html" },
        { id: "whats-new", label: "What's New", href: "whats-new.html" },
      ],
    },
  ];

  /* Flat list for prev/next */
  const FLAT = NAV.flatMap((g) => g.items);

  const docPage = document.body.getAttribute("data-page") || "";

  /* ----- Build sidebar ------------------------------------------------- */
  function buildSidebar() {
    const aside = document.getElementById("sidebar");
    if (!aside) return;
    const frag = document.createDocumentFragment();
    NAV.forEach((group) => {
      const g = el("div", "nav-group");
      g.appendChild(el("div", "nav-group-title", group.title));
      group.items.forEach((it) => {
        const a = document.createElement("a");
        a.className = "nav-link" + (it.id === docPage ? " active" : "");
        a.href = it.href;
        a.textContent = it.label;
        if (it.pro) {
          const t = el("span", "pro-tag", "PRO");
          a.appendChild(t);
        }
        g.appendChild(a);
      });
      frag.appendChild(g);
    });
    aside.appendChild(frag);
  }

  /* ----- Build prev/next ---------------------------------------------- */
  function buildPageNav() {
    const host = document.getElementById("page-nav");
    if (!host) return;
    const idx = FLAT.findIndex((p) => p.id === docPage);
    if (idx === -1) return;
    const prev = FLAT[idx - 1];
    const next = FLAT[idx + 1];
    if (prev) {
      const a = document.createElement("a");
      a.className = "prev";
      a.href = prev.href;
      a.innerHTML = '<span class="pn-label">← Previous</span><span class="pn-title"></span>';
      a.querySelector(".pn-title").textContent = prev.label;
      host.appendChild(a);
    }
    if (next) {
      const a = document.createElement("a");
      a.className = "next";
      a.href = next.href;
      a.innerHTML = '<span class="pn-label">Next →</span><span class="pn-title"></span>';
      a.querySelector(".pn-title").textContent = next.label;
      host.appendChild(a);
    }
  }

  /* ----- On-page TOC + scroll-spy ------------------------------------- */
  function buildTOC() {
    const toc = document.getElementById("toc");
    const article = document.querySelector(".doc-article");
    if (!toc || !article) return;
    // Screen-reference headings (one per screen) are excluded so the rail
    // isn't flooded on pages that list 20+ screens.
    const heads = Array.from(article.querySelectorAll("h2, h3"))
      .filter((h) => !h.classList.contains("screen-name"));
    if (heads.length < 2) { toc.style.display = "none"; return; }

    const nav = el("nav");
    nav.appendChild(el("div", "toc-title", "On this page"));
    const links = [];
    heads.forEach((h) => {
      if (!h.id) h.id = slug(h.textContent);
      // add hover anchor
      const anchor = document.createElement("a");
      anchor.className = "anchor";
      anchor.href = "#" + h.id;
      anchor.textContent = "#";
      anchor.setAttribute("aria-hidden", "true");
      h.appendChild(anchor);

      const a = document.createElement("a");
      a.href = "#" + h.id;
      // TOC label without the PRO badge or hover anchor
      const clone = h.cloneNode(true);
      clone.querySelectorAll(".pro-badge, .anchor").forEach((n) => n.remove());
      a.textContent = clone.textContent.replace(/#$/, "").trim();
      if (h.tagName === "H3") a.className = "lvl-3";
      nav.appendChild(a);
      links.push({ a, h });
    });
    toc.appendChild(nav);

    const spy = () => {
      const top = window.scrollY + 90;
      let cur = links[0];
      for (const l of links) {
        if (l.h.offsetTop <= top) cur = l;
      }
      links.forEach((l) => l.a.classList.toggle("active", l === cur));
    };
    window.addEventListener("scroll", throttle(spy, 120), { passive: true });
    spy();
  }

  /* ----- Mobile drawer ------------------------------------------------- */
  function wireDrawer() {
    const toggle = document.querySelector(".menu-toggle");
    const sidebar = document.getElementById("sidebar");
    const scrim = document.getElementById("scrim");
    if (!toggle || !sidebar || !scrim) return;
    const close = () => { sidebar.classList.remove("open"); scrim.classList.remove("open"); };
    toggle.addEventListener("click", () => {
      const open = sidebar.classList.toggle("open");
      scrim.classList.toggle("open", open);
    });
    scrim.addEventListener("click", close);
    sidebar.addEventListener("click", (e) => { if (e.target.closest("a")) close(); });
  }

  /* ----- Theme toggle -------------------------------------------------- */
  function wireTheme() {
    const root = document.documentElement;
    const saved = localStorage.getItem("cachly-docs-theme");
    const sysDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    root.setAttribute("data-theme", saved || (sysDark ? "dark" : "light"));
    const btn = document.querySelector(".theme-toggle");
    if (!btn) return;
    const ICON_SUN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><line x1="12" y1="2" x2="12" y2="4"/><line x1="12" y1="20" x2="12" y2="22"/><line x1="4.9" y1="4.9" x2="6.3" y2="6.3"/><line x1="17.7" y1="17.7" x2="19.1" y2="19.1"/><line x1="2" y1="12" x2="4" y2="12"/><line x1="20" y1="12" x2="22" y2="12"/><line x1="4.9" y1="19.1" x2="6.3" y2="17.7"/><line x1="17.7" y1="6.3" x2="19.1" y2="4.9"/></svg>';
    const ICON_MOON = '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
    const sync = () => { btn.innerHTML = root.getAttribute("data-theme") === "dark" ? ICON_SUN : ICON_MOON; };
    sync();
    btn.addEventListener("click", () => {
      const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      localStorage.setItem("cachly-docs-theme", next);
      sync();
    });
  }

  /* ----- Search -------------------------------------------------------- */
  function wireSearch() {
    const overlay = document.getElementById("search-overlay");
    const trigger = document.querySelector(".search-trigger");
    const input = document.getElementById("search-input");
    const results = document.getElementById("search-results");
    if (!overlay || !input || !results) return;

    let index = null, indexFailed = false;
    let active = -1, current = [];

    function loadIndex() {
      if (index || indexFailed) return Promise.resolve(index);
      return fetch("api/v1/search.json", { cache: "no-cache" })
        .then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then((d) => { index = d.entries || []; return index; })
        .catch(() => { indexFailed = true; return null; });
    }

    const open = () => {
      overlay.classList.add("open");
      input.value = "";
      results.innerHTML = '<div class="search-empty">Loading&hellip;</div>';
      loadIndex().then(() => render(""));
      setTimeout(() => input.focus(), 30);
    };
    const close = () => { overlay.classList.remove("open"); active = -1; };

    function score(item, terms) {
      const heading = item.heading || "";
      const hay = (item.title + " " + heading + " " + item.section + " " + item.text).toLowerCase();
      let s = 0;
      for (const t of terms) {
        if (!t) continue;
        if (item.title.toLowerCase().includes(t)) s += 8;
        if (heading.toLowerCase().includes(t)) s += 6;
        if (item.section.toLowerCase().includes(t)) s += 3;
        if (hay.includes(t)) s += 2; else return -1; // require every term
      }
      if (!item.heading) s += 1; // nudge page-level results above ties
      return s;
    }

    function render(q) {
      const terms = q.toLowerCase().trim().split(/\s+/).filter(Boolean);
      if (indexFailed) {
        results.innerHTML = '<div class="search-empty">Search is unavailable right now.</div>';
        current = []; active = -1;
        return;
      }
      if (!index) return;
      let matches;
      if (!terms.length) {
        matches = index.filter((e) => !e.heading).slice(0, 8);
      } else {
        matches = index
          .map((it) => ({ it, s: score(it, terms) }))
          .filter((x) => x.s >= 0)
          .sort((a, b) => b.s - a.s)
          .slice(0, 12)
          .map((x) => x.it);
      }
      current = matches;
      active = matches.length ? 0 : -1;
      if (!matches.length) {
        results.innerHTML = '<div class="search-empty">No matches. Try “offline”, “projection”, “drafts”, “Pro”…</div>';
        return;
      }
      results.innerHTML = "";
      matches.forEach((m, i) => {
        const a = document.createElement("a");
        a.className = "search-result" + (i === 0 ? " active" : "");
        a.href = m.href;
        a.innerHTML =
          '<div class="sr-title"></div><div class="sr-crumb"></div>' +
          (m.text ? '<div class="sr-snip"></div>' : "");
        a.querySelector(".sr-title").textContent = m.heading ? m.title + " \u203a " + m.heading : m.title;
        a.querySelector(".sr-crumb").textContent = m.section;
        if (m.text) a.querySelector(".sr-snip").textContent = trim(m.text, 110);
        results.appendChild(a);
      });
    }

    function move(d) {
      const items = results.querySelectorAll(".search-result");
      if (!items.length) return;
      items[active] && items[active].classList.remove("active");
      active = (active + d + items.length) % items.length;
      items[active].classList.add("active");
      items[active].scrollIntoView({ block: "nearest" });
    }

    trigger && trigger.addEventListener("click", open);
    input.addEventListener("input", () => render(input.value));
    overlay.addEventListener("click", (e) => { if (e.target === overlay) close(); });
    input.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown") { e.preventDefault(); move(1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); move(-1); }
      else if (e.key === "Enter") {
        const items = results.querySelectorAll(".search-result");
        if (items[active]) window.location.href = items[active].getAttribute("href");
      } else if (e.key === "Escape") close();
    });
    document.addEventListener("keydown", (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") { e.preventDefault(); open(); }
      else if (e.key === "/" && !/INPUT|TEXTAREA/.test(document.activeElement.tagName)) {
        e.preventDefault(); open();
      } else if (e.key === "Escape") close();
    });
  }

  /* ----- helpers ------------------------------------------------------- */
  function el(tag, cls, text) {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function slug(s) {
    return s.toLowerCase().replace(/#/g, "").trim()
      .replace(/[^\w\s-]/g, "").replace(/\s+/g, "-").slice(0, 60);
  }
  function trim(s, n) { return s.length > n ? s.slice(0, n).trim() + "…" : s; }
  function throttle(fn, ms) {
    let t = 0, queued = null;
    return function () {
      const now = Date.now();
      if (now - t >= ms) { t = now; fn(); }
      else { clearTimeout(queued); queued = setTimeout(() => { t = Date.now(); fn(); }, ms); }
    };
  }

  /* ----- init ---------------------------------------------------------- */
  wireTheme();
  document.addEventListener("DOMContentLoaded", function () {
    buildSidebar();
    buildPageNav();
    buildTOC();
    wireDrawer();
    wireSearch();
    document.body.classList.add("docs-ready");
  });
})();
