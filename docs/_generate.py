#!/usr/bin/env python3
"""
Generator for the Cachly documentation site.

This is a *build convenience*, not a runtime dependency: it wraps each page's
content in the shared shell (header, sidebar mount, search modal, scripts) so
all pages stay consistent. The output is plain static HTML in this folder —
upload the .html files + assets/ to your website as-is.

To edit a page: change its body below and re-run `python3 _generate.py`.
(index.html is hand-maintained and intentionally NOT regenerated here.)
"""
import os, json, html, re

DOCS = os.path.dirname(os.path.abspath(__file__))

# Public base URL of the deployed docs site (canonical URLs, sitemap, JSON-LD).
BASE_URL = "https://www.cachly.com/docs"

SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — Cachly Documentation</title>
  <meta name="description" content="{desc}">
{seo}
  <link rel="stylesheet" href="assets/cachly-docs.css?v=3">
</head>
<body data-page="{id}">
  <header class="doc-header">
    <button class="icon-btn menu-toggle" aria-label="Open menu">&#9776;</button>
    <a class="brand" href="index.html"><img class="brand-logo" src="assets/logo.png" alt="Cachly logo" width="35" height="28">Cachly<span class="brand-sub">User Guide</span></a>
    <div class="header-spacer"></div>
    <button class="search-trigger" aria-label="Search"><span aria-hidden="true">&#128269;</span><span class="search-label">Search the docs</span><span class="kbd-hint">&#8984;K</span></button>
    <button class="icon-btn theme-toggle" aria-label="Toggle dark mode">&#9790;</button>
  </header>
  <div class="scrim" id="scrim"></div>
  <div class="doc-shell">
    <aside class="doc-sidebar" id="sidebar"></aside>
    <main class="doc-content">
      <article class="doc-article">
        <div class="breadcrumb"><a href="index.html">Docs</a> &rsaquo; {crumb}</div>
        <h1>{h1}</h1>
        <p class="doc-lead">{lead}</p>
{body}
        <nav class="page-nav" id="page-nav"></nav>
        <div class="feedback-box">
          <div class="feedback-text"><strong>Spotted a problem, or have an idea?</strong> Bug reports and feature requests are tracked on GitHub.</div>
          <div class="feedback-actions">
            <a class="btn-feedback" href="https://github.com/cachly/issues-tracker/issues/new?labels=bug" target="_blank" rel="noopener">Report a Bug</a>
            <a class="btn-feedback" href="https://github.com/cachly/issues-tracker/issues/new?labels=enhancement" target="_blank" rel="noopener">Request a Feature</a>
            <a class="feedback-browse" href="https://github.com/cachly/issues-tracker/issues" target="_blank" rel="noopener">Browse existing issues &rarr;</a>
          </div>
        </div>
        <footer class="doc-footer">Cachly User Guide. Cachly is a product of Zed Said Studio. Geocaching is a trademark of Groundspeak, Inc.</footer>
      </article>
    </main>
    <aside class="doc-toc" id="toc"></aside>
  </div>
  <div class="search-overlay" id="search-overlay">
    <div class="search-box">
      <div class="search-input-row"><span aria-hidden="true">&#128269;</span><input id="search-input" type="text" placeholder="Search the documentation&hellip;" autocomplete="off" spellcheck="false" aria-label="Search"></div>
      <div class="search-results" id="search-results"></div>
      <div class="search-foot"><span><kbd>&uarr;</kbd> <kbd>&darr;</kbd> to navigate</span><span><kbd>&crarr;</kbd> to open</span><span><kbd>esc</kbd> to close</span></div>
    </div>
  </div>
  <script src="assets/docs.js"></script>
</body>
</html>
"""

PAGES = []

def page(id, title, desc, crumb, h1, lead, body):
    PAGES.append(dict(id=id, title=title, desc=desc, crumb=crumb, h1=h1,
                      lead=lead, body=body.rstrip() + "\n"))

# ===========================================================================
# Getting Started
# ===========================================================================

page("getting-started", "Accounts & Sign In",
     "Sign in to Cachly with your geocaching.com account, understand basic vs premium membership, and how Cachly Pro differs.",
     "Accounts &amp; Sign In", "Accounts &amp; Sign In",
     "Cachly connects to your Geocaching.com (Groundspeak) account. Here&rsquo;s how to sign in, what your membership level unlocks, and how that differs from a Cachly Pro subscription.",
"""        <h2 id="signing-in">Signing in</h2>
        <p>The first time you open Cachly you&rsquo;ll see the <strong>Login</strong> screen with three choices:</p>
        <ul>
          <li><strong>Sign In</strong> &mdash; authenticate with an existing geocaching.com account.</li>
          <li><strong>Sign Up</strong> &mdash; create a new geocaching.com account, then return to sign in.</li>
          <li><strong>Skip</strong> &mdash; explore the app first; you can sign in later from <span class="ui-path">More &rsaquo; your profile</span>.</li>
        </ul>
        <p>Cachly signs you in using <strong>OAuth</strong> through Geocaching.com&rsquo;s own secure login page &mdash; Cachly never sees or stores your password. You may be asked to authorize Cachly the first time; approve it to continue. You can also authenticate with <strong>Facebook</strong> credentials, which guides you through initial setup and lets you use Facebook for future logins.</p>

        <div class="callout note">
          <span class="callout-icon" aria-hidden="true">&#128272;</span>
          <div class="callout-body">Because login goes through Geocaching.com directly, your credentials stay between you and Groundspeak. Cachly receives only an access token.</div>
        </div>

        <h2 id="membership">Basic vs. premium membership</h2>
        <p>Your <strong>geocaching.com membership level</strong> is set by Groundspeak, not by Cachly, and it governs what cache data the service returns. These limits come from geocaching.com and apply to every partner app:</p>
        <table>
          <thead><tr><th></th><th>Basic (free)</th><th>Premium</th></tr></thead>
          <tbody>
            <tr><td><strong>Full cache downloads / day</strong></td><td>3</td><td>16,000</td></tr>
            <tr><td><strong>Lite cache downloads / day</strong></td><td>10,000</td><td>10,000</td></tr>
            <tr><td><strong>Cache types in live search</strong></td><td>Traditional &amp; Event only</td><td>All types, incl. premium-only</td></tr>
            <tr><td><strong>Favorite points</strong></td><td>Cannot award</td><td>Can award</td></tr>
            <tr><td><strong>Pocket queries &amp; online lists</strong></td><td>No</td><td>Yes</td></tr>
          </tbody>
        </table>
        <p><strong>Lite vs. full downloads:</strong> a <em>lite</em> cache includes only basic info (title, D/T, size, coordinates); a <em>full</em> cache adds the hint, description, attributes, waypoints and logs. Cachly downloads lite by default for speed &mdash; enable <a href="settings.html">Full Cache Data</a> to load everything up front. If a feature is unavailable due to your membership, Cachly explains and prompts a geocaching.com Premium upgrade.</p>

        <h2 id="vs-pro">Membership vs. Cachly Pro</h2>
        <p>These are two separate things:</p>
        <ul>
          <li><strong>Geocaching.com premium</strong> &mdash; purchased from Groundspeak; unlocks server-side cache data and pocket queries.</li>
          <li><strong>Cachly Pro</strong> &mdash; purchased in-app; unlocks Cachly features like offline vector maps and county tools. See <a href="cachly-pro.html">Cachly Pro</a>.</li>
        </ul>

        <h2 id="multiple-accounts">Multiple accounts</h2>
        <p>Cachly supports more than one geocaching.com identity, which powers <a href="logging.html#multi-user">multi-user logging</a> &mdash; logging a find under several accounts at once (handy for families or shared finds). Additional usernames are managed in settings and used when you choose who to log as.</p>
""")

page("interface", "The Interface",
     "A tour of Cachly's five tabs — Live map, Lists, Logs, Trackables and More — and how the app is organized.",
     "The Interface", "The Interface",
     "Cachly is organized into five tabs along the bottom of the screen. Knowing what lives where makes everything else in this guide easier to follow.",
"""        <h2 id="tabs">The five tabs</h2>
        <table>
          <thead><tr><th>Tab</th><th>What you&rsquo;ll find</th></tr></thead>
          <tbody>
            <tr><td><strong>Live</strong></td><td>The map and list of caches around you. The hub of day-to-day caching. See <a href="map.html">The Map</a>.</td></tr>
            <tr><td><strong>Lists</strong></td><td>Your bookmark lists, custom lists and offline sets, plus search and filtering. See <a href="lists.html">Lists</a> and <a href="search.html">Search &amp; Filters</a>.</td></tr>
            <tr><td><strong>Logs</strong></td><td>Logs you&rsquo;ve written &mdash; pending uploads, drafts and history. See <a href="logs.html">Logs, Drafts &amp; History</a>.</td></tr>
            <tr><td><strong>Trackables</strong></td><td>Travel Bugs and geocoins in your inventory and that you own. See <a href="trackables.html">Trackables</a>.</td></tr>
            <tr><td><strong>More</strong></td><td>Your profile, settings, import/export, downloads, backups and utilities.</td></tr>
          </tbody>
        </table>

        <div class="screen-fig">
<pre>
 &#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;
   [ map / list of nearby caches ]

 &#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;
  Live    Lists   Logs   Trackables   More
</pre>
          <div class="screen-cap">The tab bar anchors navigation throughout Cachly.</div>
        </div>

        <h2 id="the-more-tab">Inside the More tab</h2>
        <p>The <strong>More</strong> tab is where less-frequent but powerful tools live:</p>
        <ul>
          <li><strong>Profile &amp; social</strong> &mdash; your stats, friends, souvenirs and notifications (<a href="profile.html">Profile &amp; Social</a>).</li>
          <li><strong>Settings</strong> &mdash; coordinate format, units, map sources, themes and more (<a href="settings.html">Settings</a>).</li>
          <li><strong>Import &amp; export</strong> &mdash; GPX files and pocket queries (<a href="import-export.html">Import &amp; Export</a>).</li>
          <li><strong>Downloads &amp; backups</strong> &mdash; offline maps, iCloud backups (<a href="offline-maps.html">Offline Maps</a>, <a href="sync-backup.html">Sync &amp; Backup</a>).</li>
          <li><strong>Help</strong> &mdash; in-app documentation, about and privacy.</li>
        </ul>

        <h2 id="adaptive">iPad layout</h2>
        <p>On iPad, Cachly adapts to the bigger screen with a sidebar and split views instead of a bottom tab bar &mdash; the same features, arranged for more space. See <a href="ipad.html">iPad</a>.</p>
""")

page("cachly-pro", "Cachly Pro",
     "What Cachly Pro unlocks — offline vector maps, DeLorme, county tools, advanced live map — plus subscription plans and restoring purchases.",
     "Cachly Pro", "Cachly Pro",
     "Cachly Pro is an optional in-app subscription that unlocks Cachly&rsquo;s premium capabilities. Everyday geocaching works without it &mdash; Pro adds power-user and offline tooling.",
"""        <p>Cachly Pro is a subscription-based collection of premium features introduced in version 8.0.</p>

        <h2 id="whats-included">What&rsquo;s included</h2>
        <table>
          <thead><tr><th>Feature</th><th>Details</th></tr></thead>
          <tbody>
            <tr><td><strong>Pro Offline Maps</strong></td><td>Worldwide offline vector maps from OpenStreetMap, with contours, hillshades, trails, 3D buildings and offline search. See <a href="offline-maps.html">Offline Maps</a>.</td></tr>
            <tr><td><strong>Counties / Regions</strong></td><td>Visually track finds across counties/regions in Australia, Austria, France, Germany, the UK and the US. See <a href="challenge-tools.html#counties">Counties</a>.</td></tr>
            <tr><td><strong>DeLorme Grid</strong></td><td>Track found/unfound caches by DeLorme grid page across US states and select Canadian regions. See <a href="challenge-tools.html#delorme-grid">DeLorme Grid</a>.</td></tr>
            <tr><td><strong>Auto Load Live Map</strong></td><td>Automatically load caches as you move the live map. See <a href="auto-load.html">Auto Load</a>.</td></tr>
            <tr><td><strong>CarPlay</strong></td><td>Browse, route to and voice-log caches from your car. See <a href="carplay.html">CarPlay</a>.</td></tr>
            <tr><td><strong>Multiple User Logging</strong></td><td>Log a find under several accounts at once (added in 8.2). See <a href="multi-user-logging.html">Multi-User Logging</a>.</td></tr>
            <tr><td><strong>Cachly Intelligence</strong></td><td>AI summaries of logs and descriptions, and AI-drafted logs. See <a href="intelligence.html">Cachly Intelligence</a>.</td></tr>
            <tr><td><strong>OSM POI Search</strong></td><td>Search OpenStreetMap points of interest on the map. See <a href="osm-poi.html">OSM POI Search</a>.</td></tr>
          </tbody>
        </table>

        <div class="callout pro">
          <span class="callout-icon" aria-hidden="true">&#11088;</span>
          <div class="callout-body">Throughout this guide, a <span class="pro-badge">PRO</span> badge marks features that require a Cachly Pro subscription.</div>
        </div>

        <h2 id="vs-premium">Cachly Pro is not geocaching.com Premium</h2>
        <p>They&rsquo;re different things. <strong>Cachly Pro</strong> adds features inside the Cachly app. A <strong>geocaching.com Premium</strong> membership (bought from Groundspeak) unlocks server-side data &mdash; more cache types, higher daily cache limits, pocket queries &mdash; across all partner apps. A Cachly Pro subscription does <em>not</em> grant extra cache types or higher cache-load limits; those require geocaching.com Premium. See <a href="getting-started.html#membership">Accounts &amp; Sign In</a>.</p>

        <h2 id="plans">Plans &amp; pricing</h2>
        <p>Billed through your Apple&nbsp;ID, with a <strong>7-day free trial</strong>. Representative pricing (your local prices are shown live on the <span class="ui-path">More &rsaquo; Cachly Pro</span> screen):</p>
        <table>
          <thead><tr><th>Plan</th><th>USD</th><th>GBP</th><th>EUR</th></tr></thead>
          <tbody>
            <tr><td>Monthly</td><td>$1.99</td><td>&pound;1.59</td><td>&euro;1.99</td></tr>
            <tr><td>Yearly (saves ~37%)</td><td>$14.99</td><td>&pound;11.99</td><td>&euro;12.99</td></tr>
            <tr><td>Offline Maps only (yearly)</td><td>$4.99</td><td>&pound;3.99</td><td>&euro;4.99</td></tr>
          </tbody>
        </table>
        <p>Subscriptions support Family Sharing, and you can upgrade, downgrade or crossgrade through your subscription settings.</p>

        <h2 id="restore">Restoring purchases</h2>
        <p>Already subscribed on another device or after reinstalling? Use <strong>Restore Purchases</strong> in <span class="ui-path">More &rsaquo; Settings</span> to re-activate &mdash; it&rsquo;s tied to your Apple&nbsp;ID, so there&rsquo;s no separate Cachly login for it.</p>

        <div class="callout note">
          <span class="callout-icon" aria-hidden="true">&#128241;</span>
          <div class="callout-body">Subscriptions are managed in <strong>iOS Settings &rsaquo; your name &rsaquo; Subscriptions</strong>, where you can change plan or cancel. Cachly can&rsquo;t change billing on your behalf.</div>
        </div>
""")

page("multi-user-logging", "Multi-User Logging",
     "Log a single geocache under several geocaching.com accounts at once with Cachly Pro.",
     "Multi-User Logging", "Multi-User Logging",
     "Cache as a couple, family or team and log everyone\u2019s find in one pass \u2014 each account with its own message, favorites and trackables. Added in Cachly 8.2 for Pro subscribers.",
"""        <h2 id="setup">Setting up users</h2>
        <p>Accounts are managed in <span class="ui-path">Settings &rsaquo; Users</span>:</p>
        <ul>
          <li><strong>Primary User</strong> &mdash; the account used for all of Cachly, including searching for caches.</li>
          <li><strong>Other Users</strong> &mdash; additional accounts used for logging. Tap <strong>+</strong> to add one; each signs in through geocaching.com&rsquo;s own authorization page, so Cachly never sees their password. Each user&rsquo;s <strong>&hellip;</strong> menu offers <strong>Set as Primary</strong>, their own <strong>Text Templates</strong>, <strong>Auto-Visit Trackables</strong>, and <strong>Delete</strong>.</li>
          <li><strong>Multi-User Logging</strong> toggle &mdash; when enabled, logging a cache lets you submit logs for all added users at once.</li>
        </ul>

        <h2 id="how-it-works">How it works</h2>
        <p>Cachly can log a single cache under <strong>multiple geocaching.com accounts at the same time</strong> &mdash; ideal for couples, families or groups who find together. With users added, the log screen gains an <strong>Other Users</strong> section where every account appears with its own controls:</p>
        <ul>
          <li><strong>Choose who&rsquo;s logging</strong> &mdash; each additional account has a <strong>checkmark</strong> beside its name; tap to include or exclude that person from this log. Your own account is always logged. Tap an account&rsquo;s row to expand its options.</li>
          <li><strong>Per-account details</strong> &mdash; every selected account gets its own <strong>message</strong>, <strong>Favorite Cache</strong> toggle, <strong>Save as Draft</strong> toggle and <strong>trackables</strong>, set independently. Each account&rsquo;s own <a href="logging.html#templates">text templates</a> are filled in automatically.</li>
          <li><strong>Shared settings</strong> &mdash; the <strong>date</strong>, <strong>log type</strong> and (when updating) the <strong>coordinates</strong> apply to everyone at once.</li>
        </ul>
        <p>Favorite points are a premium-member feature, so the toggle only appears for accounts that are geocaching.com Premium (and it&rsquo;s hidden entirely on event caches, where it doesn&rsquo;t apply). When you tap Send, Cachly submits a separate, real log for each selected account.</p>

        <div class="callout note">
          <span class="callout-icon" aria-hidden="true">&#128101;</span>
          <div class="callout-body">Multi-user logging applies when you <em>create</em> a log. Editing an existing <a href="logs.html#pending">pending log</a> is single-account. Each added account must stay signed in &mdash; if its session expires, re-add it under <span class="ui-path">Settings &rsaquo; Users</span> before logging.</div>
        </div>
""")

page("auto-load", "Auto Load Live Map",
     "Cachly Pro's Auto Load feature loads geocaches automatically as you move the live map.",
     "Auto Load Live Map", "Auto Load Live Map",
     "With Auto Load, the live map fills itself: pan or zoom and Cachly fetches the caches for the new area \u2014 no need to tap refresh.",
"""        <h2 id="how-it-works">How it works</h2>
        <p>Normally the Live map loads caches when you tap the <strong>refresh</strong> button in the <a href="map.html#map-controls">tool stack</a>. With <strong>Auto Load</strong> enabled, Cachly requests caches automatically whenever you move the map to a new area, so browsing a region feels continuous.</p>

        <div class="callout note">
          <span class="callout-icon" aria-hidden="true">&#8505;</span>
          <div class="callout-body">Every load counts against your geocaching.com <a href="profile.html#usage">API limits</a> like a manual refresh does &mdash; Cachly loads lite cache data to keep usage light, but if you pan across a continent, expect it to add up.</div>
        </div>
""")

page("osm-poi", "OSM POI Search",
     "Search OpenStreetMap points of interest on the map with Cachly Pro, using Overpass turbo Wizard syntax.",
     "OSM POI Search", "OpenStreetMap POI Search",
     "Find parking, bus stops, viewpoints \u2014 any OpenStreetMap point of interest \u2014 right on Cachly\u2019s map with a q: query.",
"""        <h2 id="how-it-works">How it works</h2>
        <p>With Pro Offline Maps enabled, you can search OpenStreetMap points of interest right on the map. Start a search with <code>q:</code> followed by a tag query, e.g. <code>q:amenity=parking</code>, and combine conditions with <code>and</code>/<code>or</code> (<code>q:highway=bus_stop and shelter=yes</code>). Queries use the <a href="https://wiki.openstreetmap.org/wiki/Overpass_turbo/Wizard" target="_blank" rel="noopener">Overpass turbo Wizard syntax</a> &mdash; that page documents the full grammar (comparison operators, wildcards, quoting) and is a handy reference for discovering tag names. Results are limited to the visible map area &mdash; tap a placed icon to inspect its tags, create an offline geocache, or navigate.</p>

        <h2 id="examples">Example queries</h2>
        <p>These are drawn from the Overpass turbo Wizard documentation, with Cachly&rsquo;s <code>q:</code> prefix added &mdash; try them as-is, then swap in your own tags:</p>
        <table>
          <thead><tr><th>Query</th><th>Finds</th></tr></thead>
          <tbody>
            <tr><td><code>q:tourism=hotel</code></td><td>Hotels &mdash; handy when planning a caching trip.</td></tr>
            <tr><td><code>q:amenity=drinking_water</code></td><td>Drinking water fountains along the trail.</td></tr>
            <tr><td><code>q:amenity=parking</code></td><td>Parking &mdash; find a spot near the trailhead.</td></tr>
            <tr><td><code>q:highway=bus_stop or railway=platform</code></td><td>Bus stops <em>or</em> railway platforms (<code>or</code> matches either).</td></tr>
            <tr><td><code>q:highway=bus_stop and shelter=yes</code></td><td>Only bus stops that have a shelter (<code>and</code> requires both).</td></tr>
            <tr><td><code>q:(highway=primary or highway=secondary) and type:way</code></td><td>Primary or secondary roads &mdash; parentheses group conditions, and <code>type:way</code> restricts the element type (<code>node</code>, <code>way</code> or <code>relation</code>).</td></tr>
            <tr><td><code>q:cycleway:opp</code></td><td>A bare word matches partially &mdash; this finds <code>opposite</code>, <code>opposite_track</code>, <code>opposite_lane</code>&hellip;</td></tr>
            <tr><td><code>q:name~"^DB0.*"</code></td><td>Regular expressions with <code>~</code> &mdash; here, names starting with &ldquo;DB0&rdquo;.</td></tr>
          </tbody>
        </table>

        <div class="callout note">
          <span class="callout-icon" aria-hidden="true">&#8505;</span>
          <div class="callout-body">The Wizard&rsquo;s place-based forms (<code>in Vienna</code>, <code>around &hellip;</code>) aren&rsquo;t needed in Cachly &mdash; the search area is always the map you&rsquo;re looking at. Pan or zoom, then search again.</div>
        </div>
""")

# ===========================================================================
# Finding & Logging
# ===========================================================================

page("map", "The Map",
     "Cachly's live map and list: map sources, view types, navigation and the compass.",
     "The Map", "The Map",
     "The Live tab is where most caching happens. It shows caches around you on a map (or as a list), lets you switch between map sources and view types, and gets you to a cache with the compass or turn-by-turn navigation.",
"""        <h2 id="map-and-list">Map and list</h2>
        <p>The Live tab toggles between a <strong>map</strong> and a <strong>list</strong> of the same caches. Tap a cache pin (or row) to open its <a href="geocache-details.html">details</a>. Pins are colored and iconed by cache type and status (found, owned, etc.), and you can layer <a href="search.html#highlights">highlights</a> on top to mark caches visually.</p>
        <p>List rows pack in the essentials &mdash; name, distance, difficulty, terrain, size, favorite count and GC code. The <strong>sort</strong> button (up/down arrows) opens a sheet with a Direction (ascending/descending) and a long list of sort types: Date Found, Date Last Found, Date Placed, Difficulty, Distance, FTF, Favorite Count, Favorite Percentage, Found, GC Code, Highlight Color and more. The same sort sheet is used in <a href="lists.html">offline lists</a>.</p>

        <h2 id="cache-callout">The cache callout</h2>
        <p>Tapping a pin pops up a <strong>callout</strong> that summarizes the cache without leaving the map: its name and type icon, distance from you, trackable and favorite counts, <strong>difficulty</strong> and <strong>terrain</strong> dots, container <strong>size</strong> and the GC code. Tap the callout itself to open the full <a href="geocache-details.html">detail screen</a>; the <strong>&hellip;</strong> button on the callout opens quick cache actions (log, add to list, navigate and so on) without opening details first.</p>

        <h2 id="map-sources">Map types</h2>
        <p>The <strong>map options</strong> icon in the map&rsquo;s tool stack opens the <strong>Map Types</strong> panel; long-press it to jump between the last 3 types you used. The panel is organized into sections:</p>
        <ul>
          <li><strong>Pro Offline Maps</strong> <span class="pro-badge">PRO</span> &mdash; a <strong>Download Offline Maps</strong> entry for OpenStreetMap-based vector maps. See <a href="offline-maps.html">Offline Maps</a>.</li>
          <li><strong>Apple Maps</strong> &mdash; Standard, Standard Muted, Satellite, Hybrid, Satellite Flyover and Hybrid Flyover.</li>
          <li><strong>Google Maps</strong> &mdash; Standard, Satellite, Hybrid and Terrain.</li>
          <li><strong>Open Maps</strong> &mdash; Open Street and Open Cycle.</li>
          <li><strong>Arc GIS</strong> &mdash; Satellite, Topo, Clarity and Nat Geo World Map.</li>
          <li><strong>USGS</strong> &mdash; USGS Topo.</li>
          <li><strong>Ordnance Survey (UK)</strong> &mdash; Street View (see below).</li>
          <li><strong>Custom Tile URLs</strong> &mdash; point Cachly at your own tile server (see <a href="offline-maps.html#custom-tiles">Custom Tile URLs</a>).</li>
        </ul>
        <p>From the same panel you can download Pro Offline Maps, adjust offline settings (contours, points of interest) or add custom tile URLs. Defaults and per-service API keys are set in <a href="settings.html#map-options">Settings &rsaquo; Map Options &amp; Navigation</a>.</p>

        <h2 id="map-controls">On-map controls</h2>
        <p>A tool stack sits along the right edge of the live map. From top to bottom: the <strong>compass / re-center</strong> control (appears when the map is rotated &mdash; tap to snap back to north), <strong>Reload Geocaches</strong> (refresh the current area), <strong>Proximity Alert</strong>, the <strong>map options</strong> (layers) icon &mdash; tap to choose a <a href="#map-sources">map type</a>, long-press to jump between your last 3 &mdash; and <strong>Current Location</strong> (recenter / cycle follow modes).</p>
        <p><strong>Auto Load Map</strong> <span class="pro-badge">PRO</span> &mdash; long-press the Reload icon (or enable it in <a href="settings.html">Settings &rsaquo; Cachly Pro</a>) and caches load automatically as you pan, no tapping Reload. It needs a sufficient zoom level (the button dims when you&rsquo;re zoomed too far out).</p>

        <h2 id="bulk-actions">Bulk actions from the map</h2>
        <p>The <strong>&hellip;</strong> menu at the top-left of the live map acts on the caches currently loaded, not just one pin. It offers <strong>Add to List</strong>, <strong>Highlight</strong> and <strong>Export GPX</strong>, and each action asks for a scope:</p>
        <ul>
          <li><strong>All Caches</strong> &mdash; everything loaded on the map.</li>
          <li><strong>Visible Caches</strong> &mdash; only what&rsquo;s inside the current viewport.</li>
          <li><strong>Highlighted Caches</strong> &mdash; only caches with a <a href="search.html#highlights">highlight</a> applied.</li>
        </ul>
        <p>It&rsquo;s the fastest way to sweep an area&rsquo;s results into an <a href="lists.html">offline list</a> or a GPX file.</p>

        <h2 id="uk-os">UK Ordnance Survey maps</h2>
        <p>Online <strong>UK OS</strong> maps need a free <strong>Bing Maps</strong> API key (from <a href="https://www.bingmapsportal.com/">bingmapsportal.com</a>, or reuse a GME key). Add it in the map-type chooser via <strong>Add Custom Tile URL &rarr; UK OS Maps</strong> preset, paste the key, Save.</p>

        <h2 id="current-location">Your location &amp; following</h2>
        <p>Your position shows as a <strong>pulsing icon</strong> with a red heading indicator; tap it for current coordinates, GPS accuracy and elevation. The follow button (in the right-side tool stack) cycles through follow modes:</p>
        <ul>
          <li><strong>No Follow</strong> &mdash; the map stays where you put it.</li>
          <li><strong>Follow</strong> &mdash; the map tracks your location; panning disengages it.</li>
          <li><strong>Follow With Heading</strong> &mdash; follows <em>and</em> rotates the map to match the direction you&rsquo;re facing.</li>
          <li><strong>Lock Follow</strong> &mdash; long-press to lock follow on and prevent accidental map moves.</li>
        </ul>

        <h2 id="view-types">View types</h2>
        <p>Beyond the default live view, the map can show many different sets of caches. Switch the view type from the map&rsquo;s controls:</p>
        <table>
          <thead><tr><th>View</th><th>Shows</th></tr></thead>
          <tbody>
            <tr><td>Live</td><td>Caches near the current map region, fetched on the fly.</td></tr>
            <tr><td>User&rsquo;s Found / Hidden</td><td>Caches you&rsquo;ve found, or that you own and hid.</td></tr>
            <tr><td>Bookmarks</td><td>A bookmark list from your account.</td></tr>
            <tr><td>Offline Lists</td><td>Caches saved in an <a href="lists.html">offline set</a>.</td></tr>
            <tr><td>Favorites</td><td>Caches with favorite points.</td></tr>
            <tr><td>Search Results</td><td>The output of an <a href="search.html">advanced search</a>.</td></tr>
            <tr><td>Navigation</td><td>A route to your selected cache.</td></tr>
            <tr><td>Trackable Travels</td><td>The path a trackable has traveled.</td></tr>
            <tr><td>Counties</td><td>County boundaries for county challenges <span class="pro-badge">PRO</span>.</td></tr>
            <tr><td>DeLorme Grid</td><td>DeLorme atlas grid pages for DeLorme challenges <span class="pro-badge">PRO</span>.</td></tr>
          </tbody>
        </table>

        <h2 id="sync-position">Sync Live &amp; offline map position</h2>
        <p>The Live map and an <a href="lists.html#offline">offline list</a>&rsquo;s map normally remember their own positions. Turn on <span class="ui-path">Settings &rsaquo; Map Options &amp; Navigation &rsaquo; Sync Live &amp; Offline Map Position</span> and the two stay together: pan or zoom one, switch to the other, and it picks up at the same place and zoom. It&rsquo;s handy when you&rsquo;re comparing live caches against an offline set in the same area. The shared position lasts for the session and isn&rsquo;t saved between launches.</p>

        <h2 id="compass">Navigating to a cache</h2>
        <p>From a cache&rsquo;s details, choose to navigate. The <strong>Navigate to Cache</strong> screen draws a direct line to the target and shows distance, bearing and accuracy alongside a compass arrow &mdash; ideal for the final approach where street maps run out. Related waypoints (parking, trailheads) appear with distinct symbols, and other caches within 5&nbsp;miles are shown. You can switch the target, zoom to fit both you and the cache, peek at <strong>Google Street View</strong> for terrain, or set a <a href="settings.html#proximity">proximity alert</a> that fires even with the screen locked. To drive there, hand off to an external app (Apple Maps, Google Maps, Waze and others); the preferred app is set in <a href="settings.html">Settings</a>.</p>

        <h2 id="searching">Searching the map</h2>
        <p>The search field accepts a place name, one or more <strong>GC codes</strong> (comma-separated), a coord.info URL, raw coordinates, or an OpenStreetMap POI query (<code>q:</code> &mdash; see <a href="osm-poi.html">OSM POI search</a>); recent searches are kept for reuse. The <strong>refresh</strong> button (circular arrows, in the tool stack) loads caches for the current region; three dots on it mean more results are available &mdash; tap again to load them.</p>

        <h2 id="dropped-pin">Dropping a pin</h2>
        <p><strong>Long-press</strong> any empty spot on the map to drop a movable pin. Its callout shows the point&rsquo;s <strong>coordinates and elevation</strong>, and the <strong>&hellip;</strong> button opens a menu of actions for that spot:</p>
        <ul>
          <li><strong>Create Offline Geocache</strong> &mdash; make your own offline cache at the pin, stored in an <a href="lists.html">offline list</a>.</li>
          <li><strong>Save Location</strong> &mdash; store the point in your <a href="#saved-locations">Saved Locations</a>.</li>
          <li><strong>Navigate to Location</strong> &mdash; open navigation straight to the pin.</li>
          <li><strong>Copy Coordinates</strong> &mdash; copy the point to the clipboard.</li>
          <li><strong>Remove</strong> &mdash; clear the pin from the map.</li>
        </ul>
        <p>While the Navigate screen is showing, the same menu adds <strong>Set as Target</strong> so you can retarget the compass at the dropped point. Dropping a pin is also the starting point for a <a href="waypoints.html#projection">coordinate projection</a>.</p>

        <h2 id="saved-locations">Saved locations</h2>
        <p>Choosing <strong>Save Location</strong> from a dropped pin opens the <strong>Save Location</strong> screen: give the spot a name and fine-tune its position with the coordinate picker (the same picker used for waypoints, with selectable coordinate formats). Saved spots collect under <span class="ui-path">More &rsaquo; Saved Locations</span>, where each row shows the name and coordinates with a count badge on the list. Each row&rsquo;s <strong>&hellip;</strong> menu offers <strong>Share</strong> and <strong>Copy Coordinates</strong> &mdash; handy for trailheads, parking spots or anywhere you&rsquo;ll want to find again.</p>

""")

page("geocache-details", "Viewing a Geocache",
     "The geocache detail screen in Cachly — difficulty, terrain, attributes, description, hints, logs, photos, waypoints and the solution checker.",
     "Viewing a Geocache", "Viewing a Geocache",
     "Tap any cache to open its detail screen &mdash; the single place that gathers everything you need to find it: the essentials, the full description, the hint, recent logs, photos and waypoints.",
"""        <h2 id="essentials">The essentials</h2>
        <p>The top of the detail screen shows the cache&rsquo;s identity at a glance: its <strong>name</strong> and code (GC&hellip;), who placed it and when, its type icon, <strong>difficulty</strong> and <strong>terrain</strong> ratings and container <strong>size</strong>. Below that sit the cache&rsquo;s <strong>coordinates</strong> with your current <strong>distance</strong> to it, plus three quick counters: <strong>trackables</strong> in the cache, the cache&rsquo;s find/happiness score, and its <strong>favorite points</strong>.</p>
        <p>Those header elements are interactive:</p>
        <ul>
          <li>Tap the <strong>favorites count</strong> to see the users who awarded the cache a favorite point.</li>
          <li>Tap the <strong>cache icon</strong> to see your own logs for this cache; long-press the middle finds area for <strong>My Logs</strong> and <strong>Friends Logs</strong>.</li>
          <li>Long-press the <strong>cache code</strong> in the title bar to copy it.</li>
          <li>Tap the <strong>coordinates</strong> to cycle through display formats; long-press them to copy.</li>
        </ul>
        <p>The rest of the screen is a list of sections &mdash; <strong>Description</strong>, <strong>Hint</strong>, <strong>Logs</strong>, <strong>Personal Note</strong>, <strong>Images</strong>, <strong>Attributes</strong>, <strong>Waypoints</strong> and <strong>Trackables</strong> (rows show a count where useful, e.g. &ldquo;Waypoints&nbsp;6&rdquo;) &mdash; followed by <strong>Corrected Coordinates</strong> and <strong>Additional Information</strong>. Pinned to the bottom are the <strong>Log Geocache</strong> button and the round <strong>navigate</strong> button, so logging and navigation are always one tap away.</p>

        <h2 id="cache-types">Cache types &amp; icons</h2>
        <p>Cachly recognizes <strong>more than 20 cache types</strong> &mdash; including Traditional, Multi-cache, Mystery (Unknown), Virtual, Letterbox Hybrid, EarthCache, Wherigo, Webcam, Event, CITO, Mega/Giga Event and Adventure Lab &mdash; each with its own colored icon. Map pins are inverted teardrops colored by type, with decorations layered on:</p>
        <ul>
          <li>A <strong>checkmark</strong> = found; an <strong>X</strong> = your DNF; a <strong>star</strong> = a cache you own.</li>
          <li><strong>FTF</strong> badge = first-to-find available; indicators also mark &ldquo;lonely&rdquo; caches and upcoming events.</li>
          <li><strong>Strikethrough</strong> text = archived, disabled or unpublished.</li>
        </ul>

        <h2 id="description">Description</h2>
        <p>The full listing description offers three viewing modes, and Cachly remembers your preference:</p>
        <ul>
          <li><strong>Text</strong> &mdash; a clean standardized format with links and images.</li>
          <li><strong>Web</strong> &mdash; the web-rendered version, useful when text formatting misbehaves.</li>
          <li><strong>Source</strong> &mdash; the raw HTML, handy for puzzle caches that hide clues in the markup.</li>
        </ul>
        <p>The options menu adds <strong>Translate with Google</strong> and print, and the <strong>sparkle</strong> button summarizes a long description with <a href="intelligence.html">Cachly Intelligence</a>. Coordinates found in the description are tappable for quick actions such as Create Waypoint, Set as Corrected Coordinates, Copy Coordinates and Navigate.</p>

        <h2 id="hint">Hints &amp; the solution checker</h2>
        <p>The owner&rsquo;s <strong>hint</strong> is stored encrypted (ROT13) and Cachly decrypts it for you only when you open the Hint screen &mdash; so you won&rsquo;t spoil yourself by accident. If a cache has no hint, the row is grayed out on the detail screen. For mystery/puzzle caches, Cachly includes a <strong>solution checker</strong> that verifies your proposed final coordinates against the listing&rsquo;s checker, confirming you&rsquo;ve solved it before you head out.</p>

        <h2 id="logs-photos">Recent logs &amp; photos</h2>
        <p>Recent <strong>logs</strong> from other cachers tell you whether the cache is healthy and give hints about the hide. Each entry shows the log type icon and date, the finder&rsquo;s name with their find count, badges for logs voted <strong>Great Story</strong> or <strong>Helpful</strong>, and a photo count when images are attached. The <strong>photo gallery</strong> shows images attached to the listing and to logs; downloaded caches keep their photos available <a href="offline-maps.html">offline</a>.</p>

        <h2 id="images">Images</h2>
        <p>The <strong>Images</strong> gallery shows photos from the listing and logs in a grid grouped by date; tap one for the full-screen viewer with save and share, and swipe through. For <a href="lists.html#offline">offline</a> caches you can <strong>Download Current Images</strong>, <strong>Download More Images</strong> (fetch additional photos from geocaching.com), or <strong>Delete All Images</strong> to reclaim space.</p>

        <h2 id="personal-notes">Personal notes</h2>
        <p>A <strong>personal note</strong> stores your own info about a cache &mdash; up to <strong>2,500 characters</strong> &mdash; and the text syncs with your geocaching.com account. Notes found in a GPX file can be kept or merged during <a href="import-export.html">import</a>. Cachly detects coordinates you type into a note; tap them for quick actions: <strong>Create Waypoint</strong>, <strong>Set as Corrected Coordinates</strong>, <strong>Check Solution</strong> (for caches with a checker), <strong>Copy Coordinates</strong> and <strong>Navigate</strong>.</p>
        <p>The <strong>+</strong> button at the bottom left of the note editor attaches <strong>photos</strong> to the note &mdash; take a photo or choose one from your library. Attached images are stored in <strong>iCloud</strong> (under the cache&rsquo;s GC code), so they sync to all of your devices running Cachly.</p>

        <div class="callout note">
          <span class="callout-icon" aria-hidden="true">&#128246;</span>
          <div class="callout-body">Only the note <em>text</em> syncs to geocaching.com. Photo attachments stay within Cachly and iCloud &mdash; they are never sent to the website.</div>
        </div>

        <h2 id="attributes">Attributes</h2>
        <p>Cache <strong>attributes</strong> summarize conditions and requirements &mdash; Available at all Times, Stealth Required, Field Puzzle, Tourist Friendly, and so on. The Attributes screen lists them in plain language with their icons so you can plan before you go.</p>

        <h2 id="waypoints">Waypoints</h2>
        <p>The Waypoints screen starts with the cache&rsquo;s <strong>Original Coordinates</strong> and then lists its additional <strong>waypoints</strong> &mdash; parking, trailheads and the stages of a multi, each with its own description and coordinates &mdash; along with any <strong>user waypoints</strong> you add yourself with the <strong>+</strong> button (including projections). See <a href="waypoints.html">Waypoints &amp; Coordinates</a>.</p>

        <h2 id="trackables">Trackables in the cache</h2>
        <p>The <strong>Trackables</strong> row shows how many Travel Bugs and geocoins are currently in the cache. Open it to see each trackable with where it was <strong>last seen</strong>; tap one for its full details. To grab or discover a trackable, use the <a href="logging.html">log flow</a> when you log the cache.</p>

        <h2 id="corrected-coordinates">Corrected coordinates</h2>
        <p><strong>Corrected coordinates</strong> mark a cache&rsquo;s real/final location &mdash; common on Mystery, Wherigo and Multi-caches &mdash; and <strong>sync automatically with geocaching.com</strong>. A corrected cache shows a red triangle on its pin and its coordinates in green at the top of the detail screen; by default it&rsquo;s shown at the corrected spot. To view original locations instead (e.g. for Geo Art), enable <a href="settings.html">Settings &rsaquo; Caches &amp; Waypoints &rsaquo; Ignore Corrected Coordinates</a> (the triangle then shows a question mark). Corrected coordinates can be removed at any time.</p>
        <p>Tap <span class="ui-path">Corrected Coordinates &rsaquo; Add</span> on the detail screen to open the editor:</p>
        <ul>
          <li><strong>Is Corrected Coordinate</strong> &mdash; the toggle that marks the entry as the cache&rsquo;s corrected location.</li>
          <li><strong>Coordinate entry</strong> &mdash; a <strong>DDM picker</strong> by default; the format menu switches between <strong>DDM Picker</strong>, <strong>Degrees Decimal Minutes</strong>, <strong>Decimal Degrees</strong>, <strong>Degrees Minutes Seconds</strong> and <strong>Plain Text</strong>, and offers <strong>Current Location</strong>, <strong>Copy</strong> and <strong>Paste</strong>. The same menu appears in coordinate editors throughout Cachly.</li>
          <li><strong>Presets</strong> &mdash; fill in your <strong>Current Location</strong> or the <strong>Geocache Location</strong> as a starting point.</li>
          <li><strong>Tools</strong> &mdash; <strong>Project Coordinate</strong> computes a point from a distance and bearing.</li>
        </ul>

        <h2 id="additional-information">Additional Information</h2>
        <p>The <strong>Additional Information</strong> screen at the bottom of the details list collects everything else about the cache in one table: your <strong>found</strong> and <strong>DNF</strong> dates, the name and code, <strong>county</strong>, <strong>state/region</strong> and <strong>country</strong>, <strong>elevation</strong>, whether the cache is <strong>premium</strong>, <strong>archived</strong> or <strong>available</strong>, its <strong>type</strong>, the <strong>date hidden</strong>, the <strong>last found</strong> date, difficulty and more.</p>

        <h2 id="found-not-logged">Found but not logged</h2>
        <p>If you log a find but save it as a <a href="logs.html#pending">pending log</a> or draft rather than posting it, the cache is marked <strong>Found but not Logged</strong> &mdash; a checkmark on the map pin and list icon so you can see at a glance that you&rsquo;ve found it but haven&rsquo;t finished the log.</p>

        <h2 id="buttons-menus">Buttons &amp; menus</h2>
        <p>Along the bottom of the detail screen, <strong>Log Geocache</strong> opens the <a href="logging.html">logging</a> flow and the round <strong>compass</strong> button starts <a href="map.html#compass">navigation</a>. The top bar has two menus:</p>
        <ul>
          <li><strong>+</strong> &mdash; <strong>Add to List</strong> (save the cache to an <a href="lists.html#offline">offline list</a>), <strong>Watch</strong> (add it to your geocaching.com watchlist) and <strong>Ignore</strong>. Items you&rsquo;ve already applied switch to their Remove counterparts.</li>
          <li><strong>&#8943;</strong> &mdash; the actions below.</li>
        </ul>
        <table>
          <thead><tr><th>&#8943; menu</th><th>What it does</th></tr></thead>
          <tbody>
            <tr><td>Refresh</td><td>Re-download the cache&rsquo;s data.</td></tr>
            <tr><td>Log a trackable</td><td>Log a Travel Bug / geocoin against this cache.</td></tr>
            <tr><td>Highlight</td><td>Set (or edit/remove) the cache&rsquo;s <a href="search.html#highlights">color highlight</a>.</td></tr>
            <tr><td>Add Waypoint</td><td>Create a user <a href="waypoints.html">waypoint</a> (incl. projection).</td></tr>
            <tr><td>Share</td><td>Share the cache via the iOS share sheet.</td></tr>
            <tr><td>Export GPX</td><td>Export the cache to a <a href="import-export.html">GPX</a> file.</td></tr>
            <tr><td>Find Caches Near This</td><td>Search for caches around this one.</td></tr>
            <tr><td>View on geocaching.com</td><td>Open the listing in the browser.</td></tr>
          </tbody>
        </table>
        <p>Extra items appear when they apply: <strong>Edit</strong> / <strong>Delete</strong> for offline caches (on caches saved in several lists, Delete lets you remove it from this list or from all), <strong>Load Full Cache</strong> for Basic members (who get lite data by default), <strong>Add to Calendar</strong> for events, and <strong>Download Cartridge</strong> for Wherigo caches.</p>

        <h2 id="create-offline-geocache">Creating an offline geocache</h2>
        <p>Cachly can also create a cache entry from scratch &mdash; useful for hides you&rsquo;re planning, caches from other listing sites, or waypoint-style targets you want to treat as a full cache. Choose <span class="ui-path">Create Offline Geocache</span> from an offline list&rsquo;s <strong>&#8943;</strong> menu, or from the menu of a <a href="map.html">dropped pin</a> to start it at that spot. The new cache is stored in the offline list like any other, so you can navigate to it, add waypoints and log it.</p>
        <p>The editor covers everything a real listing has:</p>
        <ul>
          <li><strong>Details</strong> &mdash; cache name, cache code, who placed it, the <strong>Placed Date</strong>, and a <strong>Found</strong> toggle.</li>
          <li><strong>Description</strong> &mdash; free-form listing text, plus a hint.</li>
          <li><strong>Coordinates</strong> &mdash; the standard <strong>DDM picker</strong> with the same <a href="#corrected-coordinates">coordinate-format menu</a> (DDM, Decimal Degrees, DMS, Plain Text, Current Location, Copy, Paste).</li>
          <li><strong>Type</strong> &mdash; pick any cache type.</li>
          <li><strong>Difficulty</strong> and <strong>Terrain</strong> &mdash; sliders from 1.0 to 5.0.</li>
          <li><strong>Size</strong> &mdash; the container size.</li>
          <li><strong>Options</strong> &mdash; <strong>Available</strong>, <strong>Archived</strong> and <strong>Premium</strong> toggles, plus state and country.</li>
        </ul>
        <p>Tap <strong>Save</strong> to add the cache to the list; you can <strong>Edit</strong> it later from its detail screen&rsquo;s &#8943; menu.</p>

        <div class="callout tip">
          <span class="callout-icon" aria-hidden="true">&#9989;</span>
          <div class="callout-body">Ready to record your visit? Everything about logging &mdash; including logging for several accounts at once &mdash; is on the <a href="logging.html">Logging a Find</a> page.</div>
        </div>
""")

page("logging", "Logging a Find",
     "How to log a geocache in Cachly: log types, multi-user logging, drafts and field notes, templates, favorite points, photos and corrected coordinates.",
     "Logging a Find", "Logging a Find",
     "Logging records your visit to a cache. Cachly lets you log a single find quickly, log for several accounts at once, save drafts for later, reuse text templates, attach photos, and award a favorite point.",
"""        <h2 id="log-screen">The Log Geocache screen</h2>
        <p>From a cache&rsquo;s <a href="geocache-details.html">details</a>, start a log to open the <strong>Log Geocache</strong> screen. Top to bottom it contains:</p>
        <ul>
          <li><strong>Send Log Now</strong> &mdash; a switch controlling whether the log posts immediately or is <a href="#send-now">saved for later</a>.</li>
          <li><strong>Date</strong> and <strong>time</strong> &mdash; tap either to change when the find happened (they default to right now).</li>
          <li><strong>Log Type</strong> &mdash; opens the <a href="#log-types">type picker</a>. A status line underneath confirms what will happen: <em>Your log will be sent now</em>, or <em>Your log will be saved and you can send it later from the Pending Logs</em>.</li>
          <li><strong>A section per signed-in user</strong> &mdash; each account gets its own <strong>Message</strong>, <strong>Favorite Cache</strong> toggle, <strong>Save as Draft</strong> toggle and <strong>Trackables</strong> row (see <a href="#multi-user">multi-user logging</a>). The Trackables row selects which of that account&rsquo;s <a href="trackables.html">trackables</a> are dropped or visited with the log.</li>
        </ul>

        <h2 id="log-types">Choosing a log type</h2>
        <p>Tap <strong>Log Type</strong> and pick one:</p>
        <ul>
          <li><strong>Found it</strong> &mdash; you found the cache.</li>
          <li><strong>Didn&rsquo;t find it</strong> (DNF) &mdash; you looked but came up empty.</li>
          <li><strong>Write note</strong> &mdash; a comment without claiming a find.</li>
          <li><strong>Owner Attention Requested</strong> &mdash; the cache needs maintenance from its owner.</li>
          <li><strong>Reviewer Attention Requested</strong> &mdash; flag a serious problem to a community reviewer.</li>
        </ul>
        <p>Cachly picks a sensible default type for you: on a <strong>webcam</strong> cache a Found It becomes <strong>Webcam Photo Taken</strong>; on a <strong>future event</strong> it defaults to <strong>Will Attend</strong> and on a past one to <strong>Attended</strong>; and <strong>Owner Maintenance</strong> is offered only on caches you own.</p>

        <h2 id="send-now">Send now, or save for later</h2>
        <p>At the top of the log screen is the <strong>Send Log Now</strong> switch:</p>
        <ul>
          <li><strong>On</strong> (the default) &mdash; the action button reads <strong>Send</strong> and posts your log to Geocaching.com right away.</li>
          <li><strong>Off</strong> &mdash; the button becomes <strong>Save</strong> and your log is kept as a <a href="logs.html#pending">pending log</a> to upload later.</li>
        </ul>
        <p>If you tap Send while you&rsquo;re offline, Cachly notices and offers to save the log as pending instead of failing. Likewise, if you cancel a log you&rsquo;ve started, it offers to <strong>Save as Pending</strong> rather than lose your write-up. Editing a pending log reopens this same screen, and pending logs can be submitted or exported in bulk from the Logs tab &mdash; see <a href="logs.html#pending">Pending logs</a>.</p>

        <h2 id="multi-user">Multi-user logging <span class="pro-badge">PRO</span></h2>
        <p>Cachly can log a single cache under multiple geocaching.com accounts at once &mdash; see the dedicated <a href="multi-user-logging.html">Multi-User Logging</a> page.</p>

        <h2 id="message-editor">Writing the message</h2>
        <p>Tap <strong>Message</strong> to open the log editor. A counter tracks your length against the <strong>5,000-character</strong> limit, and a <strong>Write / Preview</strong> switch lets you check how formatting will look before you post. From the editor you can also:</p>
        <ul>
          <li><strong>Attach photos</strong> &mdash; the image button offers <strong>Take Photo</strong>, <strong>Choose From Library</strong> and <strong>Personal Note Photos</strong>; images upload with your log.</li>
          <li><strong>Insert a template</strong> &mdash; drop in one of your saved <a href="#templates">text templates</a>, or jump to <strong>Edit Text Templates</strong>. A <strong>Clear Message Text</strong> option starts you over.</li>
          <li><strong>Insert keywords</strong> &mdash; pick placeholder keywords from the keywords picker instead of typing them by hand; Cachly replaces them with real values when the log is posted.</li>
          <li><strong>Draft with AI</strong> &mdash; the <strong>sparkle</strong> button opens <a href="intelligence.html">Cachly Intelligence</a>, which can write a log for you using Apple Intelligence, Claude, ChatGPT or Gemini &mdash; you then edit and post it.</li>
        </ul>

        <h2 id="templates">Log templates</h2>
        <p>If you write similar logs often, save <strong>text templates</strong> and drop them into a log with one tap. Templates can include keyword placeholders that Cachly fills in (such as the find count or date), so each log still feels personal. Manage them in <span class="ui-path">Settings &rsaquo; Templates</span> or via <strong>Edit Text Templates</strong> in the message editor.</p>
        <p>Each template can be given a <strong>log type</strong>: when you create a log matching that type, the template&rsquo;s text is <strong>inserted automatically</strong> &mdash; a Found It template for finds, a DNF template for the days that don&rsquo;t go so well. In multi-user logging, each account&rsquo;s own templates are applied to its message.</p>

        <h2 id="drafts">Drafts vs. pending logs</h2>
        <p>Cachly has two ways to hold a log you&rsquo;re not posting as a finished log &mdash; they sound similar but work differently:</p>
        <ul>
          <li><strong>Drafts</strong> (field notes) &mdash; turn on <strong>Save as Draft</strong> and the log is saved to <strong>Geocaching.com as a Draft</strong>. Drafts sync to the website and across your devices, and you can finish them later in Cachly or on the site. The first time you use it, Cachly explains what a Draft is.</li>
          <li><strong>Pending logs</strong> &mdash; turning <a href="#send-now">Send Log Now</a> off (or saving when offline) keeps a finished log <strong>on your device</strong>, ready to upload. Pending logs upload when you reconnect, and can be edited, bulk-submitted or exported from the Logs tab. See <a href="logs.html#pending">Pending logs</a>.</li>
        </ul>

        <h2 id="extras">Photos, favorites &amp; corrected coordinates</h2>
        <ul>
          <li><strong>Photos</strong> &mdash; attach images to your log from the <a href="#message-editor">message editor</a>.</li>
          <li><strong>Favorite point</strong> &mdash; if you&rsquo;ve found it and have points available, turn on <strong>Favorite Cache</strong> to award one to a great cache. (On certain cache types, such as events, the option is hidden because it doesn&rsquo;t apply.)</li>
          <li><strong>Trackables</strong> &mdash; the Trackables row logs drops and visits for the trackables you&rsquo;re carrying; <a href="trackables.html#auto-visit">auto-visit</a> can handle this automatically.</li>
          <li><strong>Corrected coordinates</strong> &mdash; update the cache&rsquo;s coordinates (for solved puzzles or owner adjustments) as part of the flow. See <a href="waypoints.html">Waypoints &amp; Coordinates</a>.</li>
        </ul>

        <div class="callout tip">
          <span class="callout-icon" aria-hidden="true">&#9881;</span>
          <div class="callout-body">Set your logging defaults &mdash; default log type, favorite prompts, draft behavior and more &mdash; in <span class="ui-path">Settings &rsaquo; Logs</span> so the compose screen opens the way you like it.</div>
        </div>
""")

page("logs", "Logs, Drafts & History",
     "The Logs tab in Cachly: pending logs awaiting upload, submission errors, saved drafts and your logging history.",
     "Logs, Drafts &amp; History", "Logs, Drafts &amp; History",
     "The Logs tab is mission control for everything you&rsquo;ve written: logs waiting to upload, ones that hit an error, your saved drafts, and your full logging history.",
"""        <h2 id="logs-tab">The Logs tab</h2>
        <p>The <strong>Logs</strong> tab lists the logs you&rsquo;ve written, newest first. Each row shows the <strong>cache name</strong>, the <strong>log type</strong> (Found It, DNF, Write Note&hellip;), the <strong>date and time</strong>, any badges your log earned (such as <strong>Great Story</strong> or <strong>Helpful</strong>), and a <strong>photo count</strong> when images are attached. You can <strong>sort</strong> (by date, cache, type) and <strong>filter</strong> (by log type or date range) to find a past log quickly &mdash; useful for revisiting a write-up or checking what you logged on a busy caching day. Tap the <strong>profile icon</strong> to open the cacher, the <strong>cache name</strong> to open its details, and green underlined <strong>coordinates</strong> in a log to copy them or navigate.</p>

        <h2 id="log-menu">Per-log menu</h2>
        <p>The <strong>&#8943;</strong> button on each log entry offers: <strong>Share</strong>, <strong>Translate</strong> the text, <strong>Copy cache code</strong>, <strong>Add images</strong>, <strong>Edit</strong> and <strong>Delete</strong>.</p>
        <p>When you delete a log on a cache <strong>you own</strong>, Geocaching.com requires a reason &mdash; Cachly prompts you for one and sends it to the log&rsquo;s author. Deleting your own log on someone else&rsquo;s cache just asks you to confirm.</p>

        <h2 id="pending">Pending logs</h2>
        <p><strong>Pending logs</strong> are finished logs stored <strong>on your device</strong>, queued to send to Geocaching.com. A log lands here when you compose it with <a href="logging.html#send-now">Send Log Now</a> turned <strong>off</strong>, or when you post without connectivity &mdash; deep in a forest, abroad without data, or in airplane mode. This is what makes confident offline logging possible: write now, sync later.</p>
        <p>Find them under <span class="ui-path">More &rsaquo; Pending Geocache Logs</span> (the More screen shows a count next to the entry, so you can see at a glance whether anything is waiting). Each pending log lists the cache name, the date and time you wrote it, and the GC code. When you&rsquo;re back online, tap <strong>Submit All Logs</strong> to upload everything at once, or post logs individually.</p>
        <p>Tap a pending log&rsquo;s <strong>&#8943;</strong> button for its actions:</p>
        <ul>
          <li><strong>Post Log</strong> &mdash; submit this one log to Geocaching.com now.</li>
          <li><strong>Edit</strong> &mdash; reopen the full compose screen: change the date, log type, message, favorite point, Save as Draft or trackables, exactly as when you first wrote it.</li>
          <li><strong>View Geocache</strong> &mdash; open the cache&rsquo;s details.</li>
          <li><strong>Delete</strong> &mdash; discard the pending log.</li>
        </ul>

        <h2 id="pending-menu">Managing pending logs</h2>
        <p>The <strong>&#8943;</strong> menu at the top of the Pending Logs screen works on the whole queue:</p>
        <ul>
          <li><strong>Select Logs</strong> &mdash; enter select mode with a checkbox per log, then <strong>submit</strong> or <strong>delete</strong> just the selected ones in bulk. Handy after a group day when some logs are ready and others still need a sentence or two.</li>
          <li><strong>Export .txt File</strong> &mdash; export your pending logs as a field-notes text file, a useful backup before a bulk submit (or for importing elsewhere).</li>
          <li><strong>Delete All Pending Logs</strong> &mdash; clear the entire queue after confirming.</li>
        </ul>

        <div class="callout tip">
          <span class="callout-icon" aria-hidden="true">&#128246;</span>
          <div class="callout-body">Caching somewhere without coverage? Leave <a href="logging.html#send-now">Send Log Now</a> off and log every find on the spot &mdash; your write-ups queue up as pending logs, and one tap on <strong>Submit All Logs</strong> posts the whole day once you&rsquo;re back in signal.</div>
        </div>

        <h2 id="errors">Submission errors</h2>
        <p>If a log can&rsquo;t be posted (a network problem, an expired session, or a server rejection), it appears under <strong>pending log errors</strong> with the reason. From there you can review, fix and retry it rather than losing your write-up.</p>

        <div class="callout warning">
          <span class="callout-icon" aria-hidden="true">&#9888;</span>
          <div class="callout-body">If errors mention authorization, your Geocaching.com session may have expired &mdash; re-sign in from your <a href="profile.html">profile</a>, then retry the pending logs.</div>
        </div>

        <h2 id="drafts">Drafts</h2>
        <p><strong>Drafts</strong> (field notes) are logs you started but haven&rsquo;t posted. Open one to finish writing, change the type or date, then post or keep saving.</p>
        <p><strong>Online Drafts</strong> (<span class="ui-path">More &rsaquo; Online Drafts</span>) are drafts stored on geocaching.com &mdash; they <strong>sync across your devices and the website</strong>. Edit a draft&rsquo;s message (with keyword and <a href="logging.html#templates">template</a> support), add photos with the green <strong>+</strong> above the keyboard, then submit it as a full log via the &#8943; menu &rarr; <strong>Post Log</strong>.</p>

        <div class="callout note">
          <span class="callout-icon" aria-hidden="true">&#128221;</span>
          <div class="callout-body">Drafts live on <strong>geocaching.com</strong> and follow you everywhere; pending logs live on <strong>this device</strong> until uploaded. The full comparison is in <a href="logging.html#drafts">Drafts vs. pending logs</a>.</div>
        </div>

        <h2 id="history">History</h2>
        <p><span class="ui-path">More &rsaquo; History</span> lists the caches you&rsquo;ve <strong>recently viewed</strong>, so you can jump back to one without searching again. Search the list to narrow it down, tap a cache to reopen its details, or use <strong>Clear</strong> to wipe the history.</p>
""")

page("waypoints", "Waypoints & Coordinates",
     "Waypoints and coordinate entry in Cachly: user and cache waypoints, the coordinate picker, formats (DDM/DMS/decimal), coordinate projection, and saving locations.",
     "Waypoints &amp; Coordinates", "Waypoints &amp; Coordinates",
     "Waypoints are extra points tied to a cache &mdash; parking, trailheads, puzzle stages and your own additions. This page covers entering coordinates, the formats Cachly supports, and projecting a new coordinate from a bearing and distance.",
"""        <h2 id="kinds">Cache vs. user waypoints</h2>
        <ul>
          <li><strong>Cache waypoints</strong> come from the listing &mdash; parking, trailhead, reference points, and the stages of multi-caches.</li>
          <li><strong>User waypoints</strong> are ones you add yourself: a solved puzzle final, a better parking spot, or where you actually found the container.</li>
        </ul>
        <p>Add a user waypoint from a cache&rsquo;s <a href="geocache-details.html#waypoints">Waypoints</a> section (toggle <strong>User</strong>/<strong>Cache</strong> at the top, then tap <strong>+</strong>), then enter its coordinates. The <strong>&#8943;</strong> menu next to any waypoint offers <strong>Duplicate</strong>, <strong>Translate with Google</strong>, <strong>Copy Waypoint Text</strong> and <strong>Copy Coordinates</strong>.</p>

        <h2 id="formats">Coordinate formats</h2>
        <figure class="shot" style="float:right;margin:0 0 12px 18px"><img loading="lazy" src="assets/screenshots/coord-format-menu.png" alt="The coordinate picker with its format menu open" width="248"><figcaption>The coordinate picker&rsquo;s &#8943; menu: five input formats plus Current Location, Copy and Paste.</figcaption></figure>
        <p>The same point can be written several ways. Cachly&rsquo;s coordinate picker offers <strong>five</strong> input formats, switchable any time from the <strong>&#8943;</strong> menu &mdash; your choice is remembered for next time:</p>
        <table>
          <thead><tr><th>Format</th><th>Example</th><th>Notes</th></tr></thead>
          <tbody>
            <tr><td><strong>Degrees Decimal Minutes (DDM)</strong></td><td><code>N 45&deg; 54.595&rsquo;</code></td><td>The geocaching standard, used by Geocaching.com and GPS units. Cachly&rsquo;s default. Type the degrees, then the decimal minutes (to 1/1000).</td></tr>
            <tr><td>Decimal Degrees (DD)</td><td><code>45.90992</code></td><td>A single signed number per axis; compact and used by many web mapping tools.</td></tr>
            <tr><td>Degrees Minutes Seconds (DMS)</td><td><code>N 45&deg; 54&rsquo; 35.70&rdquo;</code></td><td>Common on traditional maps. Seconds go to 1/100.</td></tr>
            <tr><td>DDM Picker</td><td>spinning wheels</td><td>The classic scroll-wheel entry for degrees, whole minutes and decimal minutes &mdash; tactile, no keyboard.</td></tr>
            <tr><td>Plain Text</td><td>paste anything</td><td>One free-text field: paste a coordinate in almost any format (DDM, DMS or DD) and Cachly parses it. The baseline value is shown beneath for comparison, and unreadable text is flagged in red.</td></tr>
          </tbody>
        </table>
        <p>Your default display format is also set in <a href="settings.html">Settings</a>.</p>

        <h2 id="entering">Entering coordinates</h2>
        <p>The picker keeps entry fast and unambiguous. In the standard DDM layout you set the hemisphere (N/S, E/W) with a tap, type the whole <strong>degrees</strong>, then type the <strong>decimal minutes</strong> yourself &mdash; so the decimal point lands exactly where you mean it. As soon as you change a value from where it started, a red <strong>Updated</strong> badge appears next to the format label so you can see at a glance that you&rsquo;ve edited the coordinate. The <strong>&#8943;</strong> menu offers <strong>Reset Coordinates</strong>, which returns every field to the value the picker opened with. If you don&rsquo;t touch anything, saving keeps the original coordinate at full precision &mdash; it isn&rsquo;t round-tripped through the display format.</p>

        <div class="callout tip">
          <span class="callout-icon" aria-hidden="true">&#128203;</span>
          <div class="callout-body">The picker accepts both a period and a comma as the decimal separator, so it works naturally with locale keyboards. When you paste into Plain Text, Cachly reads the geocaching DDM standard first so a loosely-formatted paste doesn&rsquo;t get misread.</div>
        </div>

        <h2 id="projection">Coordinate projection</h2>
        <p>Many puzzle and multi-caches give you a starting point plus a <strong>bearing</strong> and <strong>distance</strong> (&ldquo;go 120&deg; for 80&nbsp;m&rdquo;). Cachly&rsquo;s <strong>projection</strong> tool calculates the destination for you. It takes exactly three inputs:</p>
        <ol>
          <li>A <strong>starting coordinate</strong> &mdash; the current waypoint or your location.</li>
          <li>A <strong>direction</strong> in degrees relative to North.</li>
          <li>A <strong>distance</strong> with a selectable unit: meters, kilometers, feet or miles.</li>
        </ol>
        <p>Cachly shows the resulting coordinate so you can review it before tapping <strong>Done</strong> to apply it as a waypoint.</p>

        <div class="screen-fig">
<pre>
  Project Waypoint
  &#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;
  Start     N 45 54.595  W 122 29.070
  Direction [ 120 ] &deg;
  Distance  [ 80 ]  [ Meters &#9662; ]
  &#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;
  Result    N 45 54.618  W 122 29.014   [Done]
</pre>
          <div class="screen-cap">Projection: start point + direction + distance &rarr; calculated coordinate.</div>
        </div>

        <h2 id="save-location">Saving a location</h2>
        <p>Cachly can <strong>save locations</strong> &mdash; coordinates you want to keep handy (a parking spot, a campsite, a search center). Saved locations can be reused as search centers or starting points for projection.</p>
""")

page("trackables", "Trackables",
     "Travel Bugs and geocoins in Cachly: inventory and owned, grab/drop/discover/visit, travel history, the TB scanner and auto-visit.",
     "Trackables", "Trackables",
     "Trackables are Travel Bugs and geocoins that move from cache to cache. The Trackables tab manages the ones in your inventory and the ones you own, and lets you log their movements.",
"""        <h2 id="inventory-owned">Inventory &amp; owned</h2>
        <p>The Trackables tab has two views, switched at the top:</p>
        <ul>
          <li><strong>Inventory</strong> &mdash; trackables you&rsquo;re currently carrying (you grabbed or retrieved them).</li>
          <li><strong>Owned</strong> &mdash; trackables you released into the wild, so you can follow their journeys.</li>
        </ul>
        <p>Sort by <strong>Date of Last Log</strong> or <strong>Trackable Name</strong> with the sort icon, and find a specific item by entering its <strong>TB code</strong> or <strong>tracking number</strong> &mdash; or by scanning its <strong>QR code</strong>. Tap any trackable for a detailed view where you can log activities or see a map of its movement history.</p>

        <h2 id="trackable-detail">Trackable detail</h2>
        <p>Tapping a trackable opens its detail screen &mdash; name, type, who it was last seen with, release date and distance traveled &mdash; with sections for <strong>Description</strong>, <strong>Goal</strong>, <strong>Logs</strong>, <strong>Images</strong> and <strong>Additional Information</strong>. The top-right <strong>&#8943;</strong> menu offers <strong>View on geocaching.com</strong>.</p>

        <h2 id="logging-trackables">Logging a trackable</h2>
        <p>From the detail screen, tap <strong>Log Trackable</strong>. The log screen has a <strong>Send Log Now</strong> toggle (on = upload to geocaching.com immediately; off = save to <a href="logs.html#pending">pending logs</a>), a date, a <strong>Message</strong>, and a <strong>Log Type</strong>. The available actions depend on whether the trackable is in your inventory:</p>
        <table>
          <thead><tr><th>Action</th><th>Meaning</th></tr></thead>
          <tbody>
            <tr><td><strong>Discover</strong> / <strong>Grab</strong> / <strong>Retrieve</strong></td><td>For a trackable you don&rsquo;t hold: note that you saw it, or take it into your inventory.</td></tr>
            <tr><td><strong>Dropped Off in Cache</strong></td><td>Place a held trackable into a cache &mdash; it leaves your inventory.</td></tr>
            <tr><td><strong>Visited Cache</strong></td><td>A held trackable traveled with you to a cache without being dropped.</td></tr>
            <tr><td><strong>Write Note</strong></td><td>A comment without changing the trackable&rsquo;s location.</td></tr>
            <tr><td><strong>Mark as Missing</strong></td><td>Flag a trackable that&rsquo;s no longer where it should be.</td></tr>
          </tbody>
        </table>

        <h2 id="travel-history">Travel history</h2>
        <p>Each trackable has a <strong>travel list</strong> showing where it&rsquo;s been. You can view a trackable&rsquo;s journey on the map using the <a href="map.html#view-types">Trackable Travels</a> view type to see the path it has taken.</p>

        <h2 id="tb-scanner">TB Scanner</h2>
        <p>The built-in <strong>TB Scanner</strong> reads a trackable&rsquo;s code so you can log it quickly without typing &mdash; handy at events where you&rsquo;re discovering many trackables.</p>

        <h2 id="auto-visit">Auto-visit</h2>
        <p>With <strong>auto-visit</strong> (enabled in <a href="settings.html">Settings &rsaquo; Trackables</a>), the trackables you choose from your inventory are automatically marked as visiting the caches you log &mdash; so a Travel Bug riding along racks up mileage without per-cache logging. It applies to <strong>Found It</strong>, <strong>Attended</strong> and <strong>Webcam Photo Taken</strong> logs.</p>

        <div class="callout warning">
          <span class="callout-icon" aria-hidden="true">&#9888;</span>
          <div class="callout-body"><strong>Trackable visit limits.</strong> Since October&nbsp;1, 2025, Geocaching HQ caps trackable visits across all partner apps at <strong>20 per 15 minutes</strong> and <strong>600 per 25 hours</strong>, and bulk-visit has been discontinued. These limits apply to every app, not just Cachly.</div>
        </div>
""")

# ===========================================================================
# Organize & Search
# ===========================================================================

page("lists", "Lists & Offline Sets",
     "Bookmark lists, custom lists and offline sets in Cachly: create lists, add and remove caches, and download caches for offline use.",
     "Lists &amp; Offline Sets", "Lists &amp; Offline Sets",
     "Lists keep caches organized; offline sets take it further by downloading caches (and their photos) to your device so you can cache with no signal.",
"""        <h2 id="kinds-of-lists">Kinds of lists</h2>
        <p>The Lists tab is split into three segments across the top:</p>
        <ul>
          <li><strong>Offline</strong> (the default) &mdash; lists whose caches are downloaded to your device for full offline access. Each row shows the cache count, the list name and when it was created.</li>
          <li><strong>Online</strong> &mdash; the bookmark lists stored on your geocaching.com account, including your <strong>Ignore List</strong>, each with its cache count and a per-row &hellip; menu. Online lists require a geocaching.com Premium membership and stay in sync with the service.</li>
          <li><strong>Trips</strong> (the car icon) &mdash; trip lists for planning a route of caches, e.g. &ldquo;Trip To Seattle&rdquo;.</li>
        </ul>
        <p>Swipe left on any list row to <strong>Delete</strong> it.</p>

        <h2 id="create">Creating a list</h2>
        <p>Tap <strong>+</strong> at the top of the Lists tab. For an offline list you give it a <strong>title</strong> and can enable <strong>Show in CarPlay</strong>, which makes the list browsable from your car&rsquo;s screen in <a href="carplay.html">CarPlay</a> <span class="pro-badge">PRO</span>. An online list is created with a title and optional description and is saved straight to your geocaching.com account.</p>

        <h2 id="adding-caches">Adding caches to a list</h2>
        <p>There are two main ways to fill a list:</p>
        <ul>
          <li><strong>One cache at a time</strong> &mdash; on a cache&rsquo;s <a href="geocache-details.html">detail screen</a>, tap the <strong>+</strong> button and choose <span class="ui-path">Add to List</span> (the same menu offers Watch and Ignore).</li>
          <li><strong>In bulk from the map</strong> &mdash; open the map&rsquo;s &hellip; menu, choose <span class="ui-path">Add to List</span>, then pick the scope: <strong>All Caches</strong>, <strong>Visible Caches</strong> or <strong>Highlighted Caches</strong>.</li>
        </ul>
        <p>Either way, you then pick the destination list and land on a confirmation screen showing how many geocaches will be saved offline, with two options: <strong>Download Images</strong> (store the caches&rsquo; photos too) and <strong>Show in CarPlay</strong>.</p>

        <h2 id="offline">Offline sets</h2>
        <p>An <strong>offline set</strong> stores cache information locally &mdash; descriptions, hints, logs, waypoints and (on demand) <strong>photos</strong> &mdash; so everything is available with no internet, perfect for trips without signal. There are three ways to create one:</p>
        <ul>
          <li>Add <a href="search.html">search results</a> from the Live tab.</li>
          <li>Import an existing online list or <a href="import-export.html#pocket-queries">pocket query</a> from geocaching.com.</li>
          <li>Import a <a href="import-export.html">GPX file</a> received by email or cloud storage.</li>
        </ul>
        <p>Browse an offline set on the map using the <a href="map.html#view-types">Offline Lists</a> view type.</p>

        <div class="callout tip">
          <span class="callout-icon" aria-hidden="true">&#128246;</span>
          <div class="callout-body">Pair offline sets with <a href="offline-maps.html">offline maps</a> <span class="pro-badge">PRO</span> for a completely offline experience &mdash; ideal for remote trails, travel and poor coverage.</div>
        </div>

        <h2 id="map-and-list-modes">Map mode and List mode</h2>
        <p>Opening an offline list gives you the same two views as the Live tab. <strong>Map mode</strong> shows the list&rsquo;s caches as pins with the full map toolset, scoped to just that list. <strong>List mode</strong> shows a cache-count heading and one row per cache with its distance, D/T, size and GC code.</p>
        <p>In list mode, the sort button (up/down arrows) opens the same sort sheet as the live cache list: choose <strong>Ascending</strong> or <strong>Descending</strong>, then a sort type &mdash; Date Found, Date Last Found, Date Placed, Difficulty, Distance, FTF, Favorite Count, Favorite Percentage, Found, GC Code, Highlight Color and more.</p>

        <h2 id="manage">Managing an offline list</h2>
        <p>In map mode, the &hellip; menu at the top right manages the whole list:</p>
        <ul>
          <li><strong>Create Offline Geocache</strong> &mdash; add a cache of your own to the list.</li>
          <li><strong>Add to List</strong> &mdash; copy caches into another list (All / Visible / Highlighted Caches).</li>
          <li><strong>Update Caches</strong> &mdash; refresh the stored cache data from geocaching.com.</li>
          <li><strong>Download Cache Images</strong> &mdash; fetch photos for caches that were saved without them.</li>
          <li><strong>Highlight</strong> &mdash; apply a <a href="search.html#highlights">highlight color</a> to the caches.</li>
          <li><strong>Export GPX</strong> &mdash; <a href="import-export.html">export</a> the caches as a GPX file.</li>
          <li><strong>Delete Visible Caches</strong> &mdash; remove the currently visible caches from the list.</li>
        </ul>

        <h2 id="membership">List membership</h2>
        <p>At the bottom of a cache&rsquo;s <a href="geocache-details.html">detail screen</a>, <strong>List Membership</strong> shows when the cache was last saved offline and which offline lists contain it. When a cache is in several lists you can use <strong>Edit</strong> (or swipe left) to remove it from specific lists while keeping it in the one you opened it from. This applies to caches stored offline.</p>

        <h2 id="filter-offline">Filtering offline lists</h2>
        <p>Offline lists have their own filtering system, far deeper than live search: tap the <strong>filter</strong> button in list view to stack multiple filters, invert them, and save whole sets as templates. The walkthrough and the complete table of filter options are on <a href="search.html#offline-filters">Search &amp; Filters</a>.</p>
""")

page("search", "Search & Filters",
     "Finding caches in Cachly: advanced search, filters, filter and search templates, highlights, sorting, counties and search history.",
     "Search &amp; Filters", "Search &amp; Filters",
     "Cachly&rsquo;s search and filtering tools let you zero in on exactly the caches you want &mdash; by difficulty, terrain, type, attributes and location &mdash; and save those criteria for reuse.",
"""        <h2 id="advanced-search">Live search &amp; filter options</h2>
        <p>The search field on the Live tab accepts a <strong>location</strong>, <strong>GC codes</strong> or <strong>coordinates</strong>, and the clock icon beside it re-runs a recent search (see <a href="#history">search history</a>). Results can be shown on the <a href="map.html#view-types">map</a> or as a list, sorted (see <a href="#sorting">below</a>), and saved to a <a href="lists.html">list</a> or <a href="lists.html#offline">offline set</a>.</p>
        <p>Tapping the <strong>filter</strong> button on the Live tab opens <strong>Live Search Filtering</strong>, which refines what the geocaching.com API returns. At the top, a <strong>Disable Filtering</strong> master toggle turns all live filtering off without changing your individual options &mdash; handy for a quick unfiltered look. The options:</p>
        <ul>
          <li><strong>Search by Cache Name</strong> &mdash; find caches by name within a 100-mile radius of the map center.</li>
          <li><strong>Exclusions</strong> &mdash; checkboxes for <strong>Exclude My Finds</strong>, <strong>Exclude My Hides</strong>, <strong>Exclude Corrected Coordinates</strong>, <strong>Has Corrected Coordinates</strong> and <strong>Exclude Adventures Stages</strong>.</li>
          <li><strong>Usernames</strong> &mdash; hidden by / not hidden by / found by / not found by specific username(s).</li>
          <li><strong>Cache types &amp; attributes</strong> &mdash; limit results to particular cache types, container sizes and attributes.</li>
          <li><strong>Difficulty</strong> and <strong>Terrain</strong> &mdash; range sliders from 1.0 to 5.0.</li>
          <li><strong>Search Radius</strong> &mdash; how far from the search point to look.</li>
          <li><strong>Favorites Minimum</strong> &mdash; only caches with at least this many favorite points.</li>
          <li><strong>Cache Placed Date</strong> and <strong>Cache Published Date</strong> &mdash; start and end date ranges.</li>
          <li><strong>Sorting</strong> &mdash; how the API returns results (Cache Name, Difficulty, Distance, Favorites, Found Date, Placed Date, Size or Terrain, ascending or descending; the default is distance ascending). This is separate from <a href="#sorting">list sorting</a>.</li>
          <li><strong>Other</strong> &mdash; Enabled Only, Exclude Enabled, Premium Only, Exclude Premium, Has Cache Note, Exclude Cache Note, <strong>Use Map Bounds in Search</strong> (limit results to the visible screen area) and Ignore Map Location.</li>
          <li><strong>Limit to State, Province or Country</strong> &mdash; restrict results geographically with the States/Provinces and Country pickers.</li>
        </ul>
        <p>A <strong>Templates</strong> section at the bottom shows the <strong>Current Template</strong> and offers <strong>Save New Template</strong> &mdash; a search template saves the entire filter configuration above so you can reapply it in one tap (see <a href="#templates">templates</a>). The <span class="ui-path">Reset</span> button returns everything to defaults.</p>

        <h2 id="filtering">Filtering</h2>
        <p>Where search <em>fetches</em> caches, <strong>filtering</strong> narrows what you&rsquo;re already looking at &mdash; live map results, a list, or an <a href="lists.html#offline">offline set</a>. Filters apply in real time, and the filter icon shows solid when constraints are active. Live search filtering (above) and <a href="#offline-filters">offline list filters</a> are two separate systems with their own options and templates.</p>

        <h2 id="filter-types">How offline filters match</h2>
        <p>Offline filtering is far more extensive than live search. Each filter belongs to a kind that sets how you configure it and how a cache is matched:</p>
        <table>
          <thead><tr><th>Kind</th><th>How it matches</th></tr></thead>
          <tbody>
            <tr><td><strong>Text</strong></td><td>A text field with a matching mode: <strong>Contains</strong>, <strong>Begins with</strong>, <strong>Ends with</strong>, <strong>Matches (Regex)</strong>, or <strong>Contains Multiple</strong>.</td></tr>
            <tr><td><strong>Number</strong></td><td>A numeric comparison (less than, less than or equal to, greater than, greater than or equal to, equal to, not equal to &mdash; or a range). Difficulty and Terrain accept decimals.</td></tr>
            <tr><td><strong>Multi-select</strong></td><td>Pick one or more values; a cache passes if it matches <strong>any</strong> selected value.</td></tr>
            <tr><td><strong>Yes / No</strong></td><td>A true/false condition (e.g. is archived, has images).</td></tr>
            <tr><td><strong>Date</strong></td><td>Match against a date, such as when the cache was placed, found or downloaded.</td></tr>
            <tr><td><strong>List</strong></td><td>Membership in one or more other offline lists.</td></tr>
          </tbody>
        </table>
        <p>Most filters can also be <strong>inverted</strong> (match the opposite), and you can combine as many as you like.</p>

        <h2 id="offline-filters">Offline list filters</h2>
        <p>Offline lists have their own stacked-filter system, separate from live search filtering. In an offline list&rsquo;s <a href="lists.html#map-and-list-modes">list view</a>, tap the <strong>filter</strong> button to open it. At the top, a <strong>Disable Filters</strong> toggle switches all filtering off without losing your setup; below it, <strong>List Filters</strong> holds the filters themselves and <strong>Filters Template</strong> saves and reloads whole filter sets (see <a href="#templates">templates</a>).</p>
        <p>Tap <span class="ui-path">Add Filter</span> to create a filter:</p>
        <ul>
          <li><strong>Filter Type</strong> &mdash; choose from the (searchable) list of filter types below.</li>
          <li><strong>Filter Details</strong> &mdash; the type-specific options. For example, an Attributes filter lets you pick attributes and set the <strong>Logic</strong> to <strong>AND</strong> or <strong>OR</strong>; a text filter takes a search term and matching mode; a number filter takes a comparison.</li>
          <li><strong>Advanced &rsaquo; Invert Filter</strong> &mdash; uses the reverse of the options chosen: if you filter to show only Traditional caches, inverting instead shows everything <em>except</em> Traditional caches.</li>
        </ul>
        <p>Filters <strong>stack</strong> &mdash; add as many as you like and they apply together, so you can build queries like &ldquo;Traditional caches, D/T under 3, with favorite points, not found by me&rdquo;.</p>
        <p>The complete set of filter types:</p>
        <table>
          <thead><tr><th>Filter</th><th>Kind</th><th>Matches</th></tr></thead>
          <tbody>
            <tr><td>Name Text</td><td>Text</td><td>The cache name.</td></tr>
            <tr><td>GC Code Text</td><td>Text</td><td>The GC code.</td></tr>
            <tr><td>Owner Text</td><td>Text</td><td>The cache owner&rsquo;s name.</td></tr>
            <tr><td>Placed By Text</td><td>Text</td><td>The &ldquo;placed by&rdquo; name.</td></tr>
            <tr><td>Description Text</td><td>Text</td><td>Text within the listing description.</td></tr>
            <tr><td>Hint Text</td><td>Text</td><td>Text within the hint.</td></tr>
            <tr><td>Log Text</td><td>Text</td><td>Text within stored logs.</td></tr>
            <tr><td>Personal Note Text</td><td>Text</td><td>Text within your personal note.</td></tr>
            <tr><td>Image Text</td><td>Text</td><td>Text in image captions/descriptions.</td></tr>
            <tr><td>Found By Username</td><td>Text</td><td>A specific finder&rsquo;s username.</td></tr>
            <tr><td>Location &ndash; Country Text</td><td>Text</td><td>The cache&rsquo;s country.</td></tr>
            <tr><td>Location &ndash; State Text</td><td>Text</td><td>The cache&rsquo;s state/province.</td></tr>
            <tr><td>County</td><td>Text</td><td>The cache&rsquo;s county.</td></tr>
            <tr><td>Difficulty</td><td>Number</td><td>Difficulty rating (decimal).</td></tr>
            <tr><td>Terrain</td><td>Number</td><td>Terrain rating (decimal).</td></tr>
            <tr><td>Favorite Count</td><td>Number</td><td>Number of favorite points.</td></tr>
            <tr><td>Favorite Percentage</td><td>Number</td><td>Favorite-point percentage.</td></tr>
            <tr><td>Distance</td><td>Number</td><td>Distance from you.</td></tr>
            <tr><td>Find Count</td><td>Number</td><td>Total times the cache has been found.</td></tr>
            <tr><td>Size</td><td>Multi-select</td><td>Container size(s).</td></tr>
            <tr><td>Type</td><td>Multi-select</td><td>Cache type(s).</td></tr>
            <tr><td>Log Type</td><td>Multi-select</td><td>Log type(s) on the cache.</td></tr>
            <tr><td>Highlight Color</td><td>Multi-select</td><td><a href="#highlights">Highlight</a> color(s).</td></tr>
            <tr><td>Attributes</td><td>Multi-select</td><td>Specific cache attribute(s), with AND/OR logic.</td></tr>
            <tr><td>Date Placed</td><td>Date</td><td>When the cache was placed.</td></tr>
            <tr><td>Date Published</td><td>Date</td><td>When the cache was published.</td></tr>
            <tr><td>Date Found By Me</td><td>Date</td><td>When you found it.</td></tr>
            <tr><td>Date Last Found</td><td>Date</td><td>When it was most recently found.</td></tr>
            <tr><td>Date Downloaded</td><td>Date</td><td>When you downloaded it offline.</td></tr>
            <tr><td>Date Last Updated</td><td>Date</td><td>When its data was last refreshed.</td></tr>
            <tr><td>Date Hidden &ndash; Year / Month / Day</td><td>Date</td><td>The hidden date by year, month or day.</td></tr>
            <tr><td>Is Archived</td><td>Yes/No</td><td>Cache is archived.</td></tr>
            <tr><td>Is Available</td><td>Yes/No</td><td>Cache is active/available.</td></tr>
            <tr><td>Is Premium</td><td>Yes/No</td><td>Premium-member-only cache.</td></tr>
            <tr><td>Is Highlighted</td><td>Yes/No</td><td>Has any highlight color.</td></tr>
            <tr><td>Is Found By Me</td><td>Yes/No</td><td>You&rsquo;ve found it.</td></tr>
            <tr><td>Is DNF By Me</td><td>Yes/No</td><td>You&rsquo;ve logged a DNF.</td></tr>
            <tr><td>DNFs in Last Logs</td><td>Yes/No</td><td>The cache&rsquo;s most recent stored logs include a run of DNFs &mdash; you choose how many DNFs to look for in how many recent logs (up to 25 each; the default is 5 DNFs in the last 5 logs). Only logs stored offline are checked, matching what you see on the cache&rsquo;s logs screen.</td></tr>
            <tr><td>Is Event Ended</td><td>Yes/No</td><td>The event&rsquo;s end date has passed. Set it to No (or invert it) to hide past events from a list. Events without a stored end date &mdash; such as some GPX imports &mdash; are never considered ended.</td></tr>
            <tr><td>Is Owned By Me</td><td>Yes/No</td><td>You own (hid) it.</td></tr>
            <tr><td>Is Favorite</td><td>Yes/No</td><td>You awarded it a favorite point.</td></tr>
            <tr><td>Is Lonely</td><td>Yes/No</td><td>Not found in a long time.</td></tr>
            <tr><td>Is Created Offline</td><td>Yes/No</td><td>A cache you created locally in Cachly.</td></tr>
            <tr><td>Is FTF Available <span class="pro-badge">PREMIUM</span></td><td>Yes/No</td><td>No found logs yet (first-to-find); shown for geocaching.com Premium members.</td></tr>
            <tr><td>Has Corrected Coordinates</td><td>Yes/No</td><td>Has corrected coordinates set.</td></tr>
            <tr><td>Has Trackables</td><td>Yes/No</td><td>Currently holds trackables.</td></tr>
            <tr><td>Has Personal Note</td><td>Yes/No</td><td>Has a personal note.</td></tr>
            <tr><td>Has Images</td><td>Yes/No</td><td>Has images.</td></tr>
            <tr><td>Has Personal Note Images</td><td>Yes/No</td><td>Has photos attached to a personal note.</td></tr>
            <tr><td>Has Waypoints</td><td>Yes/No</td><td>Has waypoints.</td></tr>
            <tr><td>Has Attributes</td><td>Yes/No</td><td>Has any attributes.</td></tr>
            <tr><td>Has Logs</td><td>Yes/No</td><td>Has stored logs.</td></tr>
            <tr><td>Has Description</td><td>Yes/No</td><td>Has a description.</td></tr>
            <tr><td>Has Hint</td><td>Yes/No</td><td>Has a hint.</td></tr>
            <tr><td>Has Solution Checker</td><td>Yes/No</td><td>Has a geocaching.com solution checker.</td></tr>
            <tr><td>In Other List</td><td>Yes/No</td><td>Belongs to another offline list.</td></tr>
            <tr><td>In Selected Lists</td><td>List</td><td>Belongs to specific offline lists you choose.</td></tr>
          </tbody>
        </table>
        <div class="callout tip">
          <span class="callout-icon" aria-hidden="true">&#128161;</span>
          <div class="callout-body">Save a combination you use often as a <a href="#templates">filter template</a> so it&rsquo;s one tap away on any offline list.</div>
        </div>

        <h2 id="templates">Filter &amp; search templates</h2>
        <p>Both filtering systems let you save your configuration as a reusable <strong>template</strong> and apply or clear it in one tap &mdash; no reconfiguring each time. In each case the Templates section shows the <strong>Current Template</strong> (tap to load a saved one) and <strong>Save New Template</strong> (name and save the current setup). The two kinds are separate, and they behave differently when it comes to syncing:</p>
        <ul>
          <li><strong>Live search templates</strong> &mdash; save the entire Live Search Filtering configuration; <strong>synced via iCloud</strong> across your devices (both iCloud and iCloud Drive must be enabled).</li>
          <li><strong>Offline list filter templates</strong> &mdash; save a stacked filter set that can be applied to any offline list; stored <strong>locally on the device only</strong>, so they won&rsquo;t appear on your other devices.</li>
        </ul>

        <h2 id="highlights">Highlights</h2>
        <p><strong>Highlighting</strong> marks caches with color &mdash; from the cache details, the Live tab, offline map lists and long-press menus. There are <strong>20 colors</strong>, shown as colored bars across interface elements, and you can rename the color labels to suit your workflow (e.g. &ldquo;challenge candidates&rdquo;, &ldquo;revisit&rdquo;). Highlights are stored in <strong>iCloud</strong>, so a deleted cache keeps its highlight when reloaded; if devices get out of sync, use <span class="ui-path">Settings &rsaquo; Highlighting &rsaquo; Manually Sync Highlights</span>.</p>

        <h2 id="sorting">Sorting</h2>
        <p>The sort button (up/down arrows) in any cache list &mdash; live results or an offline list &mdash; opens a sort sheet: choose a <strong>Direction</strong> (Ascending or Descending), then a <strong>Sort Type</strong>: Date Found, Date Last Found, Date Placed, Difficulty, Distance, FTF, Favorite Count, Favorite Percentage, Found, GC Code, Highlight Color, name, size, premium status, trackable count and more. Trackables have their own sort options too. This local sorting is separate from the live filter&rsquo;s <a href="#advanced-search">API Sorting</a> option, which controls the order caches come back from geocaching.com.</p>

        <h2 id="cache-actions">Cache actions (long-press)</h2>
        <p>Long-press a cache in any list or search result for a quick-action menu (with a preview of the cache):</p>
        <ul>
          <li><strong>Edit Highlight</strong> / <strong>Remove Highlight</strong> &mdash; set or clear its color.</li>
          <li><strong>Add to List</strong> &mdash; add it to an offline or online list.</li>
          <li><strong>Watch</strong> / <strong>Ignore</strong> &mdash; add to your geocaching.com watch or ignore list.</li>
          <li><strong>Navigate to Cache</strong> and <strong>Show on Map</strong>.</li>
          <li><strong>Copy Cache Code</strong> / <strong>Copy Coordinates</strong>.</li>
          <li><strong>Delete</strong> &mdash; remove it (offline caches).</li>
        </ul>

        <h2 id="history">Search history</h2>
        <figure class="shot" style="float:right;margin:0 0 12px 18px"><img loading="lazy" src="assets/screenshots/search-history.png" alt="The search history list with recent coordinate and GC-code searches" width="248"><figcaption>Recent searches &mdash; tap any entry to run it again.</figcaption></figure>
        <p>Cachly remembers recent searches so you can re-run one without rebuilding it &mdash; tap the clock icon next to the Live tab&rsquo;s search field to pick from your history, or clear it from the same screen.</p>
""")

page("challenge-tools", "Challenge Tools",
     "Cachly's challenge-caching tools: Counties / Regions and DeLorme Grid tracking with map views.",
     "Challenge Tools", "Challenge Tools",
     "Chasing challenge caches? Cachly tracks your progress county by county and DeLorme page by page \u2014 with maps that show exactly where you still need a find.",
"""        <h2 id="counties">Counties / Regions <span class="pro-badge">PRO</span></h2>
        <p>For county-challenge cachers, <strong>Counties / Regions</strong> tracks your finds at the county level. The screen starts empty until you <strong>Import Data</strong>; choose a source: <strong>Offline List</strong>, <strong>Dropbox</strong>, <strong>Google Drive</strong>, <strong>Files/iCloud</strong> or <strong>Other</strong>. Once imported you get a country-level progress header (say, <em>948 of 3144</em>) above a row per state or region, each showing how many of its counties you&rsquo;ve found. Open a state for its county list &mdash; each county with your find count &mdash; or tap <strong>View All</strong> to see the state as a map: <strong>found counties shaded green, missing ones red</strong>. Tap a green county to open its panel and view the geocaches you found there, right on the map. The &hellip; menu lets you <span class="ui-path">Import Data</span> again or <span class="ui-path">Delete Current Data</span>, and you can filter any offline list by <strong>County</strong> (see the <a href="#offline-filters">filter table</a>).</p>
        <div class="callout note">
          <span class="callout-icon" aria-hidden="true">&#8505;</span>
          <div class="callout-body">Not seeing your caches? Tap the <span class="ui-path">Why don&rsquo;t I see my caches?</span> button on the screen for help &mdash; county tracking only counts caches whose data you&rsquo;ve imported.</div>
        </div>

        <h2 id="delorme-grid">DeLorme Grid <span class="pro-badge">PRO</span></h2>
        <p>The <strong>DeLorme Grid</strong> tracks your finds by DeLorme atlas grid page, for grid-challenge caching. It works just like Counties / Regions: import caches first (same source choices), then browse per-state atlas pages with find counts, or <strong>View All</strong> to see the page grid drawn over the state map &mdash; green pages found, red still needed. Tapping a green page shows the geocaches you&rsquo;ve found on it.</p>

""")

page("dt-grid", "D/T Grid",
     "Cachly's D/T grid: your finds across the 81 Difficulty/Terrain combinations, for Fizzy-style challenge caches.",
     "D/T Grid", "D/T Grid",
     "Every find plotted on the 9\u00d79 Difficulty/Terrain matrix \u2014 see which of the 81 combinations you still need, and search for caches that fill the gaps.",
"""        <h2 id="the-grid">The grid</h2>
        <p>The <strong>D/T Statistics</strong> grid plots your finds on the 9&times;9 <strong>Difficulty/Terrain matrix</strong> &mdash; a must for Fizzy-style challenge caches. Below the grid you&rsquo;ll see your loop progress (percent complete and combinations remaining), total finds, unique D/T combinations out of 81, and your average difficulty and terrain. Tap any cell to <strong>search for caches with that D/T combination</strong> and fill the gaps.</p>
""")

page("profile", "Profile & Social",
     "Your Cachly profile and social features: stats, friends and requests, souvenirs, the notification center and API usage.",
     "Profile &amp; Social", "Profile &amp; Social",
     "The profile area gathers your geocaching identity &mdash; your stats and finds, your friends, your souvenirs, notifications, and a look at your API usage.",
"""        <h2 id="profile">Your profile &amp; stats</h2>
        <p>Tap your name at the top of the <strong>More</strong> tab to open your <strong>profile</strong> &mdash; your geocaching identity in one screen, pulled from Geocaching.com. Your avatar and username sit at the top, with a <strong>PREMIUM</strong> badge if you hold a premium membership, followed by a <strong>Found Cache Types</strong> chart breaking your finds down by cache type. In between, rows drill into every part of your record:</p>
        <ul>
          <li><strong>Finds</strong> &mdash; opens a <strong>map of everything you&rsquo;ve found</strong>, so you can see your caching footprint at a glance.</li>
          <li><strong>Hides</strong> &mdash; the caches you own.</li>
          <li><strong>Logs</strong> &mdash; your log history.</li>
          <li><strong>Trackables</strong> &mdash; the trackables <em>you own</em>, grouped by type (Travel Bug Dog Tags, geocoins and so on) with a count for each.</li>
          <li><strong>Favorites</strong> &mdash; your favorite points, shown as remaining/awarded.</li>
          <li><strong>Souvenirs</strong> &mdash; your earned <a href="#souvenirs">souvenirs</a>.</li>
          <li><strong>Lists</strong> &mdash; your geocaching.com lists.</li>
          <li><strong>Gallery</strong> &mdash; every photo you&rsquo;ve attached to a log, grouped by date.</li>
          <li><strong>geocaching.com Profile</strong> and <strong>Project-GC Stats</strong> &mdash; open your full web profile and Project-GC statistics.</li>
        </ul>
        <p>From here you can also re-authenticate if your Geocaching.com session expires.</p>

        <h2 id="friends">Friends</h2>
        <p><span class="ui-path">More &rsaquo; Friends</span> lists your geocaching.com friends with their find counts; tap one to open their profile, and use the <strong>Friends / Requests</strong> switch at the top to review and accept pending friend requests. Because of privacy rules, friends only appear if they&rsquo;ve <strong>authorized sharing</strong> &mdash; both you and each friend must check &ldquo;Allow Authorized Developer applications&hellip;&rdquo; under <a href="https://www.geocaching.com/account/settings/authorizations">geocaching.com &rsaquo; Authorizations</a>. Cachly explains this with a prompt the first time you open Friends, and offers a shortcut to view or manage your authorizations. If you don&rsquo;t see everyone, that authorization is usually why.</p>

        <h2 id="contact">Phone, text or message a cacher</h2>
        <p>From a user profile, a friend, or a log author, you can <strong>phone</strong>, send a <strong>geocaching.com message</strong>, or <strong>text</strong> them. Phone/text require the cacher&rsquo;s caching name to be stored in the <strong>Company</strong> or <strong>Nickname</strong> field of an iOS contact (matched case-insensitively); this needs Contacts permission. Email works for any profile.</p>

        <h2 id="message-center">Message Center</h2>
        <p><span class="ui-path">More &rsaquo; Message Center</span> opens geocaching.com&rsquo;s messaging system right inside Cachly, so you can read and reply to messages from other cachers without leaving the app.</p>

        <h2 id="souvenirs">Souvenirs</h2>
        <p><strong>Souvenirs</strong> are the virtual badges Geocaching.com awards for finds in particular places or during events. Cachly lists the souvenirs you&rsquo;ve earned with the date each was awarded; tap one for its artwork and details.</p>

        <h2 id="notifications">Notification center</h2>
        <p>The <strong>notification center</strong> collects activity relevant to you in one place.</p>

        <h2 id="dt-grid">D/T Grid</h2>
        <p><span class="ui-path">More &rsaquo; D/T Grid</span> shows a <strong>9&times;9 Difficulty/Terrain matrix</strong> of your finds. See the dedicated <a href="dt-grid.html">D/T Grid</a> page.</p>

        <h2 id="usage">Usage &amp; storage</h2>
        <p>If you&rsquo;re ever wondering why Cachly is using so much space &mdash; or how much API allowance you have left &mdash; <span class="ui-path">More &rsaquo; Usage</span> is the answer. It has three parts:</p>
        <ul>
          <li><strong>Storage</strong> &mdash; how much space <strong>Cache Images</strong>, <strong>Offline Maps</strong>, the <strong>Database</strong> and <strong>Backups</strong> occupy. The rows are tappable for cleanup: delete all images, delete offline maps, or delete backups to reclaim space.</li>
          <li><strong>Database Objects</strong> &mdash; counts of what&rsquo;s stored on the device: geocaches, logs, waypoints, trackables, photos, attributes, users and state/county regions.</li>
          <li><strong>API Limits</strong> &mdash; Geocaching.com limits how many caches apps can request per period, with separate quotas for <strong>lite</strong> (basic) and <strong>full</strong> geocache data. Cachly shows how many of each you have <strong>remaining</strong> and the <strong>time until the count resets</strong> &mdash; useful if you do heavy searching or large downloads and want to pace yourself.</li>
        </ul>

        <div class="callout note">
          <span class="callout-icon" aria-hidden="true">&#8505;</span>
          <div class="callout-body">If you hit a usage limit, Cachly will let you know; waiting for the limit window to reset restores access. Premium membership generally provides a larger allowance.</div>
        </div>
""")

# ===========================================================================
# Offline & Data
# ===========================================================================

page("offline-maps", "Offline Maps & Downloads",
     "Offline maps and downloads in Cachly: MapLibre vector maps, MBTiles, DeLorme, downloading regions and managing downloads.",
     "Offline Maps &amp; Downloads", "Offline Maps &amp; Downloads",
     "Offline maps let the base map render with no connection &mdash; the other half of caching off-grid (the first half being <a href=\"lists.html#offline\">offline cache sets</a>). Most offline map capabilities are part of <a href=\"cachly-pro.html\">Cachly Pro</a>.",
"""        <h2 id="pro-offline-maps">Pro Offline Maps <span class="pro-badge">PRO</span></h2>
        <p>Cachly Pro&rsquo;s offline maps are <strong>worldwide vector maps</strong> built from OpenStreetMap data and optimized for readability. Download them via the map-layers icon or <span class="ui-path">Settings &rsaquo; Cachly Pro &rsaquo; Download Offline Maps</span>. Maps update <strong>weekly</strong>. Features include:</p>
        <ul>
          <li><strong>Contours &amp; hillshades</strong> as supplementary downloads, switching with your metric/imperial units.</li>
          <li>Customizable <strong>layer visibility</strong> &mdash; trails, 3D buildings, points of interest &mdash; and 3D map rendering.</li>
          <li><strong>County lines &amp; names</strong> for US states and comparable international regions.</li>
          <li><strong>Trail symbols &amp; colors</strong> from OpenStreetMap, plus an optional bold scheme matching UK Ordnance Survey styling.</li>
        </ul>

        <h2 id="offline-search">Offline map searching <span class="pro-badge">PRO</span></h2>
        <p>When an offline map is active on the Live tab, Cachly can search map features <strong>completely offline</strong>, within your currently visible screen area &mdash; zoom to frame your target region first. Toggle it on under <span class="ui-path">Settings</span>; enable <strong>Allows Partial Words</strong> so searching &ldquo;water&rdquo; matches waterfall and waterway. For structured point-of-interest queries by OpenStreetMap tag (parking, drinking water, bus stops&hellip;), see <a href="osm-poi.html">OSM POI Search</a>.</p>

        <h2 id="downloading">Downloading a region</h2>
        <p>Choose a region to download; Cachly fetches it in the background (a background session keeps large downloads going even if you leave the app). The <strong>Downloads</strong> screen shows progress and manages what you&rsquo;ve saved.</p>

        <div class="callout tip">
          <span class="callout-icon" aria-hidden="true">&#128246;</span>
          <div class="callout-body">Download over Wi-Fi before heading out, and pair maps with an <a href="lists.html#offline">offline cache set</a> so both the map <em>and</em> the cache data are on your device.</div>
        </div>

        <h2 id="custom-tiles">Custom tile URLs</h2>
        <p>Beyond the built-in sources, Cachly can load tiles from <strong>any tile server</strong> &mdash; specialist commercial maps or free ones (many free servers require your own API key). Open the <a href="map.html#map-sources">Map Types</a> panel, scroll to <strong>Custom Tile URLs</strong> and tap <strong>Add Custom Tile URL</strong>.</p>
        <p>On the <strong>Tile URL Details</strong> screen, give the source a name and enter its URL template in z/x/y format &mdash; for example <code>https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png</code>:</p>
        <ul>
          <li><code>{z}</code>, <code>{x}</code>, <code>{y}</code> &mdash; zoom level and tile coordinates (required).</li>
          <li><code>{s}</code> &mdash; rotates across the server&rsquo;s subdomains.</li>
          <li><code>{q}</code> or <code>{quadtree}</code> &mdash; for servers that address tiles with a quadtree key instead of z/x/y.</li>
        </ul>
        <p>Under <strong>Geometry</strong>, enable <strong>TMS / Flipped Geometry</strong> for servers whose y-axis runs the other way (TMS layout). A <strong>Presets</strong> section offers ready-made configurations &mdash; such as <strong>UK OS Maps</strong> &mdash; so common services need no manual setup. Saved sources appear in the Map Types panel like any other map, and can be edited or removed later.</p>
        <p>Other formats Cachly handles include <strong>MBTiles</strong> (with local tile search) and <strong>DeLorme</strong> <span class="pro-badge">PRO</span>.</p>

""")

page("import-export", "Import & Export",
     "Moving cache data in and out of Cachly: GPX import and export, pocket queries from Geocaching.com, and managing imported files.",
     "Import &amp; Export", "Import &amp; Export",
     "Cachly speaks <strong>GPX</strong>, the standard geocaching exchange format, and integrates pocket queries &mdash; so you can bring caches in from other tools and take your data with you.",
"""        <h2 id="gpx-import">Importing GPX</h2>
        <p><strong>Import from GPX</strong> brings caches into Cachly from a <code>.gpx</code> or <code>.zip</code> file (Cachly unzips automatically) &mdash; a pocket query, or an export from another app or website. Cachly uses a streaming parser so even very large files import efficiently, and you choose an existing <a href="lists.html#offline">offline list</a> or create a new one on import. You can bring a file in from:</p>
        <ul>
          <li><strong>Email</strong> &mdash; download the attachment, long-press it, Share &rarr; Cachly.</li>
          <li><strong>Dropbox / Google Drive</strong> &mdash; from the app (&#8943; &rarr; Share/Open in &rarr; Cachly) or via the iOS <strong>Files</strong> app.</li>
          <li><strong>AirDrop</strong> &mdash; send a GPX/zip to Cachly from another device or a Mac.</li>
          <li>Any app offering an iOS <strong>Share</strong> option for a GPX file.</li>
        </ul>

        <h2 id="pocket-queries">Pocket queries</h2>
        <p><strong>Pocket Queries</strong> are saved searches you set up on Geocaching.com (a premium-membership feature) that the service runs for you. Cachly can <strong>download</strong> your ready pocket queries directly and load them in &mdash; a fast way to bring a curated set of caches onto your device.</p>

        <div class="callout note">
          <span class="callout-icon" aria-hidden="true">&#8505;</span>
          <div class="callout-body">Pocket queries are created and scheduled on Geocaching.com and require premium membership. Cachly downloads the results once they&rsquo;re generated.</div>
        </div>

        <h2 id="gpx-export">Exporting GPX</h2>
        <p><strong>Export GPX</strong> writes caches back out to a <code>.gpx</code> file &mdash; available from the <a href="map.html">Live tab</a>, an <a href="lists.html#offline">offline list</a>, or a cache&rsquo;s <a href="geocache-details.html">details</a>. Choose the scope (<strong>All</strong>, <strong>Visible</strong>, or <strong>Highlighted</strong> caches) and what to include:</p>
        <ul>
          <li><strong>Include Logs</strong> &mdash; stored cache logs.</li>
          <li><strong>Include Waypoints</strong> &mdash; all associated waypoints.</li>
          <li><strong>Include GSAK Extensions</strong> &mdash; GSAK-specific data (needed for favorite-point tracking).</li>
          <li><strong>Include Private Data</strong> &mdash; sensitive info such as solved-puzzle coordinates and personal notes (handy for team caching).</li>
        </ul>
        <p>Cachly also writes your <a href="search.html#highlights">highlight colors</a> into the GPX using its own tags, so a cache you export and later re-import into Cachly keeps the color you gave it.</p>
        <p>Exports can be shared device-to-device over <strong>AirDrop</strong> with no internet &mdash; the recipient picks an app and an offline list to receive the caches.</p>

        <h2 id="my-finds-gpx">My Finds GPX</h2>
        <p>For <a href="challenge-tools.html#counties">Counties/Regions</a> and DeLorme Grid <span class="pro-badge">PRO</span>, import a <strong>My Finds</strong> pocket query GPX (geocaching.com &rsaquo; Premium Tools &rsaquo; Build pocket queries &rsaquo; My Finds) via the <strong>Import Data</strong> button. After the first import, new finds logged in Cachly auto-register. Note: Adventure Lab finds aren&rsquo;t included in GPX files.</p>

        <h2 id="imported-files">Managing imported files</h2>
        <p>The <strong>Imported Files</strong> screen lists files you&rsquo;ve brought in, so you can re-import or remove them. You can also receive GPX files from other apps via the iOS share sheet and open them straight into Cachly.</p>
""")

page("sync-backup", "Sync & Backup",
     "Keeping Cachly data safe and in sync: iCloud sync across devices, cloud backups and restore, and Dropbox/Google Drive integration.",
     "Sync &amp; Backup", "Sync &amp; Backup",
     "Cachly can sync your data across your devices and back it up to the cloud, so a new phone or a reinstall doesn&rsquo;t mean starting over.",
"""        <h2 id="icloud-sync">iCloud sync</h2>
        <p>With <strong>iCloud sync</strong> enabled, Cachly keeps your data in step across the iPhone and iPad signed into the same Apple&nbsp;ID &mdash; so lists, settings and more follow you from device to device.</p>

        <h2 id="backups">Backups &amp; restore</h2>
        <p>Cachly can create <strong>backups</strong> of your data to the cloud. The <strong>Backups</strong> screen lists your backups so you can restore one &mdash; invaluable when moving to a new device or recovering after a reinstall. You can browse the underlying iCloud documents from the <strong>iCloud files</strong> screen.</p>

        <h2 id="database-file">Backing up the database file</h2>
        <p>For a full manual copy, the database file <code>Cachly.sqlite</code> holds all your offline lists and pending logs (but <em>not</em> settings). Grab it two ways:</p>
        <ul>
          <li><strong>Files app:</strong> <span class="ui-path">Browse &rsaquo; On My iPhone &rsaquo; Cachly</span>, long-press <code>Cachly.sqlite</code> and Share (e.g. AirDrop to a computer).</li>
          <li><strong>Finder / iTunes File Sharing:</strong> connect the device, select it, choose <strong>File Sharing &rsaquo; Cachly</strong>, select <code>Cachly.sqlite</code> and Save.</li>
        </ul>
        <p>To <strong>restore</strong>, add your saved <code>Cachly.sqlite</code> back via File Sharing (Add), confirming the overwrite.</p>

        <div class="callout tip">
          <span class="callout-icon" aria-hidden="true">&#128190;</span>
          <div class="callout-body">Make a backup before a big change &mdash; like a major offline-map migration or clearing space &mdash; so you can roll back if needed.</div>
        </div>

        <h2 id="cloud-services">Dropbox &amp; Google Drive</h2>
        <p>Cachly also integrates with <strong>Dropbox</strong> and <strong>Google Drive</strong>, letting you move files (such as GPX) to and from those services for import/export workflows. See <a href="import-export.html">Import &amp; Export</a>.</p>
""")

# ===========================================================================
# Smart Features
# ===========================================================================

page("intelligence", "Cachly Intelligence",
     "Cachly Intelligence: AI-assisted log writing with Apple Intelligence, Claude, ChatGPT and Google Gemini, with writing prompts, a prompt editor and a model picker.",
     "Cachly Intelligence", "Cachly Intelligence",
     "Cachly Intelligence helps you write better logs faster and read caches in any language, using on-device or cloud AI. You stay in control: it drafts, you edit and post.",
"""        <h2 id="what-it-does">What it does</h2>
        <p>When you&rsquo;re <a href="logging.html">logging a find</a>, Cachly Intelligence can draft a log for you &mdash; turning a few notes (or just the cache&rsquo;s context) into a friendly, well-written log you then tweak and submit. It&rsquo;s designed to beat the blank-page problem, not to post on your behalf.</p>

        <div class="callout pro">
          <span class="callout-icon" aria-hidden="true">&#11088;</span>
          <div class="callout-body">Cachly Intelligence is a <a href="cachly-pro.html">Cachly Pro</a> feature, and it&rsquo;s off until you turn it on in <span class="ui-path">Settings &rsaquo; Cachly Pro</span>.</div>
        </div>

        <h2 id="setup">Turning it on</h2>
        <p>Everything lives at the top of <span class="ui-path">Settings &rsaquo; Cachly Pro</span>, in the <strong>Cachly Intelligence</strong> section:</p>
        <ol>
          <li>Switch on <strong>Enable Cachly Intelligence</strong>.</li>
          <li>Tap <strong>AI Provider</strong> and choose who does the thinking. <strong>Apple Intelligence</strong> works immediately, entirely on-device. For <strong>Claude</strong>, <strong>ChatGPT</strong> or <strong>Gemini</strong>, tap the provider to add your own API key first &mdash; until then the row shows <em>API key not set</em>.</li>
          <li>Optionally open the three prompt rows below (<a href="#prompts">Log Summary, Description Summary, Log Writing</a>) and tailor them to your taste &mdash; each is fully editable.</li>
        </ol>
        <p>Once enabled, a <strong>sparkle</strong> button appears in the places Cachly Intelligence can help: a cache&rsquo;s description, its logs list, and the log message editor.</p>

        <div class="callout danger">
          <span class="callout-icon" aria-hidden="true">&#9888;&#65039;</span>
          <div class="callout-body"><strong>Apple Intelligence is only available on the iPhone&nbsp;15&nbsp;Pro and newer devices</strong> (and requires iOS&nbsp;26). On older iPhones, choose Claude, ChatGPT or Gemini with your own API key instead.</div>
        </div>

        <h2 id="summaries">AI summaries</h2>
        <p>Beyond drafting logs, Cachly Intelligence can <strong>summarize</strong> for you. On a cache&rsquo;s <a href="geocache-details.html#logs-photos">Logs</a> screen and on its <a href="geocache-details.html#description">description</a>, tap the <strong>sparkle</strong> button (bottom right): a <strong>Cachly Intelligence</strong> sheet slides up with a concise summary &mdash; how the cache has been doing, common tips from finders, or the gist of a long pirate-themed backstory &mdash; without reading a wall of text.</p>
        <div class="callout tip">
          <span class="callout-icon" aria-hidden="true">&#127760;</span>
          <div class="callout-body"><strong>Summaries translate, too.</strong> Caching abroad? Summarize a cache&rsquo;s German (or French, Japanese&hellip;) logs and description and the summary comes back <strong>in English &mdash; or whatever your device language is</strong>. No more pasting logs into a translator to figure out if a cache is findable.</div>
        </div>

        <p>In <a href="carplay.html">CarPlay</a>, Cachly Intelligence goes hands-free: it can summarize a cache&rsquo;s logs and description <strong>by voice</strong>, reading the summary aloud so you get the gist while driving.</p>

        <h2 id="models">Choosing a model</h2>
        <p>Cachly supports multiple AI providers, selectable under <span class="ui-path">Settings &rsaquo; Cachly Pro &rsaquo; AI Provider</span>:</p>
        <table>
          <thead><tr><th>Provider</th><th>Notes</th></tr></thead>
          <tbody>
            <tr><td><strong>Apple Intelligence</strong></td><td>On-device AI &mdash; private and offline-capable. Requires iOS 26 and an iPhone 15&nbsp;Pro or newer.</td></tr>
            <tr><td><strong>Claude</strong> (Anthropic)</td><td>Cloud model via the Claude API.</td></tr>
            <tr><td><strong>ChatGPT</strong> (OpenAI)</td><td>Cloud model via the OpenAI API.</td></tr>
            <tr><td><strong>Google Gemini</strong></td><td>Cloud model via Google.</td></tr>
          </tbody>
        </table>

        <div class="callout note">
          <span class="callout-icon" aria-hidden="true">&#8505;</span>
          <div class="callout-body">Cloud providers (Claude, ChatGPT, Gemini) send your prompt to that service and may require your own API key or account. Apple Intelligence runs on-device where supported. Choose the option that matches your privacy preference.</div>
        </div>

        <h2 id="prompts">Writing prompts &amp; the prompt editor</h2>
        <p>Every Cachly Intelligence feature is driven by a prompt you can see and change. <span class="ui-path">Settings &rsaquo; Cachly Pro</span> has three, and <strong>all three are fully user-editable</strong>:</p>
        <ul>
          <li><strong>Log Summary Prompt</strong> &mdash; shapes how a cache&rsquo;s logs are summarized; the logs are appended to the end of your prompt.</li>
          <li><strong>Description Summary Prompt</strong> &mdash; shapes description summaries the same way.</li>
          <li><strong>Log Writing Prompt</strong> &mdash; shapes generated logs; the cache&rsquo;s info and your notes are appended to it.</li>
        </ul>
        <p>Edit them to match your voice &mdash; always mention the trail, keep it short, write in your language &mdash; and the AI&rsquo;s output follows.</p>

        <h2 id="writing-a-log">Writing a log with AI</h2>
        <p>In the <a href="logging.html#message-editor">log message editor</a>, tap the <strong>sparkle</strong> button and describe what you want to say (<em>&ldquo;Found it quickly, thank the owner, mention the nice park setting&rdquo;</em>). Tap <strong>Generate</strong> and a <strong>Preview</strong> of the drafted log appears &mdash; <strong>Insert</strong> it into your log, or <strong>Try Again</strong> for a different draft. Nothing is added until you choose Insert.</p>

        <h2 id="privacy">Privacy &amp; control</h2>
        <p>Generated text is always a <strong>draft</strong>: nothing is posted until you review and submit it. You decide which provider to use, and you can edit or discard any suggestion.</p>
""")

# ===========================================================================
# Settings & Platforms
# ===========================================================================

page("settings", "Settings",
     "Cachly settings: coordinate format, units, map options and sources, custom map URLs, themes and dark mode, navigation app, logging, proximity sounds and tracking.",
     "Settings", "Settings",
     "Settings (in the <strong>More</strong> tab) is where you tailor Cachly to how you cache. The screen is <strong>searchable</strong> &mdash; type in the search box at the top to jump to an option by name &mdash; and is organized into the categories below.",
"""        <h2 id="categories">How Settings is organized</h2>
        <p>The Settings root screen lists twelve categories: <strong>Cachly Pro</strong>, <strong>Users</strong>, <strong>General</strong>, <strong>Map Options &amp; Navigation</strong>, <strong>Caches &amp; Waypoints</strong>, <strong>Logs</strong>, <strong>Templates</strong>, <strong>Proximity Alert</strong>, <strong>Trackables</strong>, <strong>Highlighting</strong>, <strong>Imports &amp; Pocket Queries</strong> and <strong>Dark Mode</strong>. Each is covered below.</p>
        <p>Beneath the categories are <strong>Manage Subscriptions</strong> (opens your Apple&nbsp;ID subscription management) and <strong>Restore Purchases</strong>, which re-activates a <a href="cachly-pro.html#restore">Cachly Pro</a> subscription after a reinstall or on a new device.</p>

        <h2 id="cachly-pro">Cachly Pro <span class="pro-badge">PRO</span></h2>
        <p>Everything tied to your <a href="cachly-pro.html">Pro subscription</a> lives here, grouped by feature:</p>
        <ul>
          <li><strong>Cachly Intelligence</strong> &mdash; enable AI features, pick the <strong>AI Provider</strong> (Apple Intelligence, Claude, ChatGPT, Gemini), and edit the <strong>Log Summary</strong>, <strong>Description Summary</strong> and <strong>Log Writing</strong> prompts. See <a href="intelligence.html">Cachly Intelligence</a>.</li>
          <li><strong>Pro Offline Maps</strong> &mdash; <strong>Download Offline Maps</strong>, <strong>Layer Options</strong>, <strong>Offline Searching</strong> (search map features within the screen bounds) and <strong>Counties &amp; Regions</strong>. See <a href="offline-maps.html">Offline Maps</a>.</li>
          <li><strong>Automatically Add Finds</strong> &mdash; add finds made in Cachly to your <strong>Counties</strong> and <strong>DeLorme</strong> challenge maps automatically.</li>
          <li><strong>Automatically Load Caches</strong> &mdash; <strong>Use Auto Load Caches</strong> loads new caches as you move around the live map, with toggles for <strong>Adventure Labs</strong> and their <strong>stages</strong>.</li>
          <li><strong>CarPlay</strong> &mdash; microphone and speech-recognition permissions used for <a href="carplay.html">voice logging in the car</a>.</li>
          <li><strong>Project GC</strong> &mdash; enter your <strong>User Token</strong> and <strong>User ID</strong> (from project-gc.com/User/Settings) to enable Project&nbsp;GC features.</li>
        </ul>

        <h2 id="users">Users</h2>
        <div class="callout note">
          <span class="callout-icon" aria-hidden="true">&#8505;</span>
          <div class="callout-body"><strong>New in Cachly 8:</strong> Settings has a Users category supporting multiple geocaching.com accounts.</div>
        </div>
        <p>Your <strong>Primary User</strong> is the account used for all aspects of Cachly, including searching for caches. You can add <strong>additional users</strong> here so a group caching together can log finds under several accounts at once &mdash; see <a href="logging.html#multi-user">multi-user logging</a>. If an added account&rsquo;s session expires, return to <span class="ui-path">Settings &rsaquo; Users</span> to sign it in again.</p>

        <h2 id="general">General</h2>
        <p>App-wide preferences, from units to power use:</p>
        <ul>
          <li><strong>Measurement</strong> &mdash; switch between <strong>Metric</strong> and imperial units.</li>
          <li><strong>iPhone Rotation Lock</strong> &mdash; All Orientations, Portrait or Landscape (iPhone only).</li>
          <li><strong>TB Scanner</strong> &mdash; <strong>Automatic Scanning</strong> reads trackable codes without tapping the capture button.</li>
          <li><strong>Offline Lists</strong> &mdash; allow (or hide) the <strong>Delete All</strong> option.</li>
          <li><strong>Power &amp; Battery</strong> &mdash; <strong>High Power Mode</strong> improves GPS accuracy when moving between screens at the cost of battery.</li>
          <li><strong>Default Coordinate Format</strong> &mdash; the format used when copying coordinates: DDM (N&nbsp;47&deg;&nbsp;38.938&rsquo;), decimal degrees, UTM, <strong>Copy Presented Format</strong>, or <strong>Use Coordinate Picker</strong> to choose each time. See <a href="waypoints.html#formats">coordinate formats</a>.</li>
          <li><strong>Sorting</strong> &mdash; <strong>Re-sort on Location Updates</strong> keeps distance-sorted lists in order as you move.</li>
          <li><strong>Other</strong> &mdash; <strong>Decode Hint</strong> (auto-decrypt ROT13 hints) and <strong>Delete Offline Upvote Counts</strong>.</li>
        </ul>

        <h2 id="map-options">Map Options &amp; Navigation</h2>
        <p>Controls how <a href="map.html">the map</a> behaves and which app handles driving directions:</p>
        <ul>
          <li><strong>Map behavior</strong> &mdash; <strong>Automatic Search on Start</strong>, <strong>Show Cache Radius</strong>, <strong>Prevent Map Rotation</strong> / <strong>Prevent Map Tilt</strong>, <strong>Fit to Map</strong> (zoom to fit all caches and waypoints) and <strong>Clear Map On Refresh</strong> (turn off to keep previous searches on the map).</li>
          <li><strong>Number of Maps</strong> &mdash; how many recently used maps appear when you long-press the map-layers button.</li>
          <li><strong>Zoom In While Navigating</strong> &mdash; in follow / follow-heading mode, automatically zoom in as you close on the target.</li>
          <li><strong>Displayed Map Type</strong> &mdash; the map type used across all map screens; also see <a href="map.html#sync-position">Sync Live &amp; Offline Map Position</a>.</li>
          <li><strong>World Landcover and Hillshades</strong> <span class="pro-badge">PRO</span> &mdash; <strong>Landcover</strong> and <strong>Hillshades</strong> layers for Pro maps (small bandwidth use, online only), plus <strong>Tile URLs 2x Size</strong> for easier-to-read custom tiles.</li>
          <li><strong>Map API Keys</strong> &mdash; some map sources need a free key, e.g. <strong>Open Cycle &amp; Thunderforest</strong>.</li>
          <li><strong>Navigation</strong> &mdash; choose the external navigation app used for driving directions from the <a href="map.html">Navigate to Cache</a> screen.</li>
        </ul>

        <h2 id="caches-waypoints">Caches &amp; Waypoints</h2>
        <p>How caches and <a href="waypoints.html">waypoints</a> look and load:</p>
        <ul>
          <li><strong>Pin Design</strong> &mdash; three pin styles, plus <strong>Show Favorite Points</strong> to display the favorite count on pins above a minimum you set.</li>
          <li><strong>Live Search</strong> &mdash; <strong>Full Cache Data</strong> (description, hint, logs, waypoints, attributes) and how many caches each live-search request loads.</li>
          <li><strong>Clustering</strong> &mdash; <strong>Use Clustering</strong> with a <strong>Cluster Threshold</strong> and <strong>Max Zoom Level</strong>; reduces memory use when many caches are on the map.</li>
          <li><strong>Ignore Corrected Coordinates</strong> &mdash; show caches at their original rather than corrected coordinates.</li>
          <li><strong>Waypoints</strong> &mdash; <strong>Show All Waypoints</strong> on the map, filterable by type (requires Full Cache Data for live caches).</li>
          <li><strong>Lonely Caches</strong> &mdash; mark caches unfound for a set <strong>Number of Days</strong> with a clock icon.</li>
          <li><strong>Did Not Find (DNF)</strong> &mdash; <strong>Clear Pending DNF on Map</strong> and <strong>Show Cache Type on Map</strong> alongside the DNF marker.</li>
          <li><strong>Found But Not Logged</strong> &mdash; <strong>Clear All Checkmarks</strong>, and the <strong>FTF Indicator</strong> that flags caches nobody has found yet.</li>
        </ul>

        <h2 id="logs">Logs</h2>
        <p>Defaults for <a href="logging.html">writing logs</a>:</p>
        <ul>
          <li><strong>Logging Defaults</strong> &mdash; choose whether new logs default to <strong>Send Log Now</strong> or <strong>Save as Draft</strong>, and set the default <strong>Log Type</strong>.</li>
          <li><strong>Display</strong> &mdash; <strong>Recent Logs Use Smilies</strong> shows smiley/frown icons instead of colored dots in cache details.</li>
        </ul>

        <h2 id="templates">Templates</h2>
        <p>Create reusable <a href="logging.html#templates">text templates</a> for your logs here &mdash; boilerplate like a thank-you line or your team sign-off. Templates can be inserted while writing a log or applied automatically by log type.</p>

        <h2 id="proximity">Proximity Alert</h2>
        <p>Cachly can play an audio alert and post a notification as you near a cache, so your phone can stay pocketed on the approach:</p>
        <ul>
          <li><strong>Enable Proximity Alert</strong> &mdash; separately for the <strong>Live</strong> tab, <strong>Offline Lists</strong> and <strong>Navigate to Cache</strong>.</li>
          <li><strong>Proximity Distance</strong> &mdash; the trigger radius (in feet).</li>
          <li><strong>Proximity Centering</strong> &mdash; center the radius on your <strong>Current User Location</strong> or the <strong>Current Target</strong> (used when navigating to a cache).</li>
          <li><strong>Options</strong> &mdash; <strong>Include My Finds</strong>, <strong>Include My Hides</strong>, <strong>Hint in Notification</strong>, and <strong>Notify For All Caches</strong> (alert for nearby caches, not just the target).</li>
          <li><strong>Notification Sound</strong> &mdash; pick the alert sound.</li>
        </ul>
        <div class="callout tip">
          <span class="callout-icon" aria-hidden="true">&#128276;</span>
          <div class="callout-body">Proximity alerts need <strong>location</strong> and <strong>notification</strong> permissions. The Permissions section at the bottom of this screen shows their status; grant anything missing in iOS Settings.</div>
        </div>

        <h2 id="trackables">Trackables</h2>
        <p><strong>Automatically Visit</strong> lets <a href="trackables.html#auto-visit">trackables in your inventory</a> be visited with each cache log: turn on <strong>Enable Auto-Visit</strong> and pick which trackables under <strong>Auto-Visit Trackables</strong>. Applies to Found It and Attended log types.</p>

        <h2 id="highlighting">Highlighting</h2>
        <p>Maintenance tools for <a href="search.html#highlights">cache highlights</a>:</p>
        <ul>
          <li><strong>Manually Sync Highlights</strong> &mdash; fix highlights that got out of sync on offline lists after changes on another device.</li>
          <li><strong>Remove By Color</strong> / <strong>Remove All Highlights</strong> &mdash; clear highlights, across all devices.</li>
          <li><strong>Restore Caches From Highlights</strong> and <strong>Edit Highlight Color Labels</strong> &mdash; rebuild caches from your highlight records and rename what each color means.</li>
        </ul>

        <h2 id="imports-pocket-queries">Imports &amp; Pocket Queries</h2>
        <p>Controls for <a href="import-export.html">GPX imports and pocket queries</a>:</p>
        <ul>
          <li><strong>Lock Corrected Coordinates</strong> / <strong>Lock Found Status</strong> &mdash; prevent imported GPX data from being overwritten when caches update.</li>
          <li><strong>GSAK</strong> &mdash; <strong>User Flag Sets Highlight</strong> highlights caches whose GSAK user flag is set.</li>
          <li><strong>Adventure Lab</strong> &mdash; <strong>Show Import Icon</strong> distinguishes imported Adventure Labs from API-loaded ones.</li>
          <li><strong>Pocket Queries</strong> &mdash; <strong>Import Using Full Data</strong> brings in personal notes and corrected coordinates; turn it off for a faster GPX-only import.</li>
        </ul>

        <h2 id="dark-mode">Dark Mode</h2>
        <p>By default Cachly follows the iOS appearance. Two toggles let you opt out independently: <strong>Dark Interface Styles</strong> controls whether the app&rsquo;s interface goes dark when iOS is in dark mode, and <strong>Dark Map Styles</strong> does the same for the maps &mdash; so you can keep a light map under a dark interface, or vice versa.</p>
""")

page("apple-watch", "Apple Watch",
     "Cachly on Apple Watch: nearby caches, filters, full cache details, map and compass navigation, and logging finds right from your wrist.",
     "Apple Watch", "Cachly on Apple Watch",
     "Cachly&rsquo;s Apple Watch app puts the essentials on your wrist &mdash; find nearby caches, read the details and hint, follow the map or compass to ground zero, and log the find &mdash; without reaching for your phone.",
"""        <h2 id="overview">What the Watch app does</h2>
        <p>The Watch app syncs with your iPhone and focuses on the in-the-field essentials:</p>
        <ul>
          <li><strong>Nearby caches</strong> &mdash; a searchable, filterable list of caches around you.</li>
          <li><strong>Cache details</strong> &mdash; distance, D/T, size, favorite points, description, hint, logs, attributes, waypoints and photos.</li>
          <li><strong>Map &amp; compass navigation</strong> &mdash; distance and direction to the selected cache.</li>
          <li><strong>Quick logging</strong> &mdash; log a find (or save a draft) with dictation or Scribble.</li>
          <li><strong>Lists</strong> &mdash; browse your offline and online lists.</li>
        </ul>

        <div class="callout tip">
          <span class="callout-icon" aria-hidden="true">&#8986;</span>
          <div class="callout-body">For caches in an <a href="lists.html#offline">offline set</a>, the Watch can show details without needing the iPhone to be online.</div>
        </div>

        <h2 id="home-screen">Home screen &amp; complications</h2>
        <p>Add Cachly as a <strong>complication</strong> on your watch face for one-tap launching &mdash; the green Cachly pin appears right on the face. The app&rsquo;s home screen offers the ways in:</p>
        <ul>
          <li><strong>Nearby</strong> &mdash; loads geocaches around your current location.</li>
          <li><strong>Current</strong> &mdash; the cache you&rsquo;re currently (or were last) viewing on your iPhone.</li>
          <li><strong>Lists</strong> &mdash; your offline and online cache lists.</li>
          <li><strong>Saved</strong> &mdash; caches stored directly on the watch with the <span class="ui-path">&hellip; &rsaquo; Save</span> action (if you haven&rsquo;t saved any yet, Cachly tells you).</li>
        </ul>

        <div class="shots">
          <figure class="shot"><img loading="lazy" src="assets/screenshots/watch-complication.png" alt="Add the Cachly complication to your watch face for one-tap launching." width="248"><figcaption>Add the Cachly complication to your watch face for one-tap launching.</figcaption></figure>
          <figure class="shot"><img loading="lazy" src="assets/screenshots/watch-home.png" alt="The home screen: Nearby, Current, Lists  and Saved below." width="248"><figcaption>The home screen: Nearby, Current, Lists &mdash; and Saved below.</figcaption></figure>
        </div>

        <h2 id="nearby">Nearby search &amp; filters</h2>
        <p><strong>Nearby</strong> lists the caches around you as cards showing the cache name and type, GC code, a <strong>PREM</strong> badge for premium-only caches, distance, favorite points, and the D/T ratings and container size. <strong>Search</strong> re-runs the search at your current position; <strong>Filter</strong> narrows the results:</p>
        <ul>
          <li><strong>Finds / Hides</strong> &mdash; toggles to include or exclude your finds and your hides.</li>
          <li><strong>Difficulty &amp; Terrain</strong> &mdash; minimum and maximum ratings with stepper controls (1.0&ndash;5.0).</li>
          <li><strong>Cache Size</strong> &mdash; tick the container sizes to include (Micro, Small, Medium, Large&hellip;).</li>
          <li><strong>Cache Type</strong> &mdash; tick cache types individually or use <strong>Toggle All</strong>.</li>
          <li><strong>Reset</strong> &mdash; back to the defaults.</li>
        </ul>

        <div class="shots">
          <figure class="shot"><img loading="lazy" src="assets/screenshots/watch-nearby.png" alt="Nearby results as cards: name, GC code, premium badge, distance, favorite points and D/T/size." width="248"><figcaption>Nearby results as cards: name, GC code, premium badge, distance, favorite points and D/T/size.</figcaption></figure>
          <figure class="shot"><img loading="lazy" src="assets/screenshots/watch-filter.png" alt="Filters: your finds and hides, difficulty and terrain ranges, sizes and types." width="248"><figcaption>Filters: your finds and hides, difficulty and terrain ranges, sizes and types.</figcaption></figure>
          <figure class="shot"><img loading="lazy" src="assets/screenshots/watch-filter-types.png" alt="Cache types can be toggled individually or all at once." width="248"><figcaption>Cache types can be toggled individually or all at once.</figcaption></figure>
        </div>

        <h2 id="cache-details">Cache details</h2>
        <p>Tap a cache to open its details: name, GC code, premium status, the date it was placed, distance, favorite points, and its difficulty, terrain and size. Scroll on for the full set of sections &mdash; <strong>Description</strong>, <strong>Hint</strong>, <strong>Logs</strong>, <strong>Attributes</strong>, <strong>Waypoints</strong> (including your own, like a parking waypoint), <strong>Photos</strong> and your <strong>Personal Note</strong> &mdash; each opening full-screen for reading on the small display.</p>
        <p>Below the details, <strong>Log Cache</strong> starts a log (see <a href="#logging-on-watch">logging</a>), and the <strong>&hellip;</strong> button offers <strong>View Map</strong>, <strong>Compass</strong> and <strong>Save</strong> (store the cache on the watch).</p>

        <div class="shots">
          <figure class="shot"><img loading="lazy" src="assets/screenshots/watch-cache-details.png" alt="Cache details: name, GC code, premium status, distance and D/T/size." width="248"><figcaption>Cache details: name, GC code, premium status, distance and D/T/size.</figcaption></figure>
          <figure class="shot"><img loading="lazy" src="assets/screenshots/watch-cache-sections.png" alt="Scroll for the full sections: Description, Hint, Logs and more." width="248"><figcaption>Scroll for the full sections: Description, Hint, Logs and more.</figcaption></figure>
          <figure class="shot"><img loading="lazy" src="assets/screenshots/watch-photos.png" alt="The caches photo gallery on your wrist." width="248"><figcaption>The cache&rsquo;s photo gallery on your wrist.</figcaption></figure>
          <figure class="shot"><img loading="lazy" src="assets/screenshots/watch-actions.png" alt="The  menu: View Map, Compass, or Save the cache to the watch." width="248"><figcaption>The &hellip; menu: View Map, Compass, or Save the cache to the watch.</figcaption></figure>
        </div>

        <h2 id="navigation">Map &amp; compass navigation</h2>
        <p><strong>View Map</strong> shows the cache and its waypoints as pins around your position, with the remaining distance at the top. <strong>Compass</strong> gives you a classic navigation dial: distance to go, bearing (e.g. 162&deg; S), and the current GPS accuracy, with a red needle pointing at the cache.</p>

        <div class="shots">
          <figure class="shot"><img loading="lazy" src="assets/screenshots/watch-map.png" alt="View Map: the cache and waypoints as pins around you, distance up top." width="248"><figcaption>View Map: the cache and waypoints as pins around you, distance up top.</figcaption></figure>
          <figure class="shot"><img loading="lazy" src="assets/screenshots/watch-compass.png" alt="The compass dial: distance, bearing and GPS accuracy." width="248"><figcaption>The compass dial: distance, bearing and GPS accuracy.</figcaption></figure>
        </div>

        <h2 id="compass">Why the compass needs you to move (older watches)</h2>
        <p>On <strong>Apple Watch Series 5 and later</strong>, Cachly shows a true compass that updates as you turn, even standing still. <strong>Earlier models have no compass sensor</strong>, so Cachly derives heading from GPS course &mdash; which only works while you&rsquo;re moving. If your compass won&rsquo;t update while stationary, that&rsquo;s the hardware; a Series 5 or newer resolves it.</p>

        <h2 id="logging-on-watch">Logging from the Watch</h2>
        <p>Tap <strong>Log Cache</strong> on a cache&rsquo;s details to log it right on the watch:</p>
        <ul>
          <li><strong>Send Now / Draft</strong> &mdash; submit the log immediately, or save it as a draft to finish on your iPhone later.</li>
          <li><strong>Log type</strong> &mdash; e.g. Found It.</li>
          <li><strong>Message</strong> &mdash; compose your log text with dictation or Scribble.</li>
          <li><strong>Send</strong> &mdash; off it goes.</li>
        </ul>

        <div class="shots">
          <figure class="shot"><img loading="lazy" src="assets/screenshots/watch-log.png" alt="Logging: Send Now or save a Draft, pick the log type" width="248"><figcaption>Logging: Send Now or save a Draft, pick the log type&hellip;</figcaption></figure>
          <figure class="shot"><img loading="lazy" src="assets/screenshots/watch-log-message.png" alt="and write the log with dictation or Scribble." width="248"><figcaption>&hellip;and write the log with dictation or Scribble.</figcaption></figure>
        </div>
        <p>The log syncs back through your iPhone and follows the same <a href="logs.html#pending">pending/upload</a> flow as logs written on the phone.</p>

        <h2 id="watch-lists">Lists on the Watch</h2>
        <p>The <strong>Lists</strong> screen splits into <strong>Offline Lists</strong> (from your iPhone) and <strong>Online Lists</strong> (from geocaching.com), mirroring the <a href="lists.html">Lists tab</a> on the phone.</p>

        <div class="shots">
          <figure class="shot"><img loading="lazy" src="assets/screenshots/watch-lists.png" alt="Lists: offline lists from your iPhone, online lists from geocaching.com." width="248"><figcaption>Lists: offline lists from your iPhone, online lists from geocaching.com.</figcaption></figure>
        </div>
""")

# CarPlay page content is based on the help.cachly.com article (article 131),
# reformatted to site conventions.
page("carplay", "CarPlay",
     "Cachly's CarPlay integration: search, navigate to and voice-log geocaches from your vehicle's dashboard. A Cachly Pro feature.",
     "CarPlay", "Cachly on CarPlay",
     "Cachly's CarPlay integration brings the full geocaching experience to your vehicle's dashboard, allowing you to search for caches, navigate to them, and even log your finds &mdash; all while keeping your eyes on the road.",
"""        <figure class="article-img"><img loading="lazy" src="assets/help-images/carplay-01.jpg" alt="CarPlay screenshot"></figure>

        <div class="callout pro">
          <span class="callout-icon" aria-hidden="true">&#11088;</span>
          <div class="callout-body">CarPlay is a <a href="cachly-pro.html">Cachly Pro</a> feature and requires an active Cachly Pro subscription.</div>
        </div>

        <h2 id="getting-started">Getting started</h2>
        <p>When you connect your iPhone to a CarPlay-compatible vehicle, Cachly will appear on your CarPlay dashboard. Simply tap the Cachly icon to launch the app.</p>
        <figure class="article-img"><img loading="lazy" src="assets/help-images/carplay-02.jpg" alt="CarPlay screenshot"></figure>
        <p>Upon first launch, you&rsquo;ll see the main map view centered on your current location. The map will automatically begin loading nearby geocaches if you have an active internet connection.</p>

        <h3>Requirements</h3>
        <ul>
          <li>iPhone with iOS 14 or later</li>
          <li>CarPlay-compatible vehicle or head unit</li>
          <li>Active Cachly Pro subscription</li>
          <li>Internet connection (for live cache searching) or pre-downloaded Trips (for offline use)</li>
        </ul>

        <h3>Cachly icon not showing in CarPlay</h3>
        <p>Cachly should be added automatically to CarPlay, but if you are not seeing the Cachly icon go to <span class="ui-path">iOS Settings &rsaquo; General &rsaquo; CarPlay</span> and choose your car. Next go to <strong>Apps</strong>, scroll to the bottom and <strong>add Cachly</strong> as an included app.</p>
        <figure class="article-img"><img loading="lazy" src="assets/help-images/carplay-03.png" alt="CarPlay screenshot"></figure>

        <h2 id="carplay-map">The CarPlay map</h2>
        <p>The CarPlay map is your primary interface for discovering geocaches while driving. It displays geocache locations as pins with icons indicating the cache type and cache titles at higher zoom levels.</p>
        <figure class="article-img"><img loading="lazy" src="assets/help-images/carplay-04.jpg" alt="CarPlay screenshot"></figure>

        <h3>Map controls</h3>
        <p>The map includes several control buttons:</p>
        <table>
          <thead><tr><th>Button</th><th>Function</th></tr></thead>
          <tbody>
            <tr><td><strong>+</strong></td><td>Zoom in one level (see below for screenshots)</td></tr>
            <tr><td><strong>&minus;</strong></td><td>Zoom out one level (see below for screenshots)</td></tr>
            <tr><td><strong>Location Arrow</strong></td><td>Center map on your current location</td></tr>
            <tr><td><strong>Cache Count</strong></td><td>Shows number of visible caches (displays &ldquo;10+&rdquo; when more than 10)</td></tr>
            <tr><td><strong>Panning</strong></td><td>Shows the CarPlay panning interface (see below for screenshots)</td></tr>
            <tr><td><strong>X clear</strong></td><td>Clears caches from a loaded trip</td></tr>
          </tbody>
        </table>

        <h3>Understanding the map display</h3>
        <ul>
          <li><strong>Cache Pins</strong> &mdash; each geocache appears as a pin with an icon representing its cache type (Traditional, Multi, Mystery, etc.)
            <ul>
              <li>Favorites: cache pins will show favorites count for caches that have 10 or more favorite points.</li>
            </ul></li>
          <li><strong>Cache Labels</strong> &mdash; when zoomed in sufficiently (zoom level 14+), cache names appear next to their pins</li>
          <li><strong>Your Location</strong> &mdash; a blue dot shows your current position when the map is not following your location, and a direction-of-travel icon when it is.</li>
        </ul>

        <h3>Zoom in/out and panning the map</h3>
        <ul>
          <li>Most CarPlay systems only support panning and zooming by using the UI buttons.</li>
          <li>Some new CarPlay systems on iOS 26 support zoom and rotating by pinching and zooming.</li>
        </ul>
        <figure class="article-img"><img loading="lazy" src="assets/help-images/carplay-05.jpg" alt="CarPlay screenshot"></figure>
        <figure class="article-img"><img loading="lazy" src="assets/help-images/carplay-06.jpg" alt="CarPlay screenshot"></figure>

        <h3>Map behavior</h3>
        <ul>
          <li>The map automatically refreshes and loads new caches as you drive</li>
          <li>Caches load when you&rsquo;re zoomed in to at least level 12</li>
          <li>If you&rsquo;re zoomed out too far, you&rsquo;ll see a message asking you to zoom in</li>
        </ul>

        <h2 id="browsing">Browsing geocaches</h2>

        <h3>Viewing the cache list</h3>
        <p>Tap the <strong>cache count button</strong> (showing the number of visible caches) to open a list view of all geocaches currently on the map.</p>
        <figure class="article-img"><img loading="lazy" src="assets/help-images/carplay-07.jpg" alt="CarPlay screenshot"></figure>
        <p>Each cache in the list displays:</p>
        <ul>
          <li><strong>Cache Name</strong> &mdash; the title of the geocache</li>
          <li><strong>Distance</strong> &mdash; how far the cache is from your current location</li>
          <li><strong>D/T Rating</strong> &mdash; Difficulty and Terrain ratings</li>
          <li><strong>Size</strong> &mdash; container size (Micro, Small, Regular, Large, etc.)</li>
          <li><strong>GC Code</strong> &mdash; the unique geocache identifier</li>
          <li><strong>Favorite Points</strong> &mdash; shown with a heart symbol (&#9829;&#65038;)</li>
          <li><strong>Highlight Color</strong> &mdash; if you&rsquo;ve assigned a highlight color to the cache, it appears as a colored circle</li>
        </ul>
        <figure class="article-img"><img loading="lazy" src="assets/help-images/carplay-08.jpg" alt="CarPlay screenshot"></figure>

        <h3>Viewing cache details</h3>
        <p>Tap any cache in the list to view its details:</p>
        <ul>
          <li><strong>Difficulty/Terrain/Size</strong> &mdash; core cache attributes</li>
          <li><strong>Favorite Points</strong> &mdash; community rating</li>
          <li><strong>GC Code</strong> &mdash; for reference</li>
          <li><strong>Placed By</strong> &mdash; cache owner&rsquo;s username</li>
          <li><strong>Placement Date</strong> &mdash; when the cache was published</li>
          <li><strong>Distance</strong> &mdash; live-updating distance from your location</li>
        </ul>
        <p>From the details screen, you can:</p>
        <ul>
          <li><strong>Navigate</strong> &mdash; start navigation to this cache</li>
          <li><strong>Log Cache</strong> &mdash; record your find using voice</li>
          <li><strong>Hint</strong> &mdash; view the cache hint (if available)</li>
        </ul>
        <figure class="article-img"><img loading="lazy" src="assets/help-images/carplay-09.jpg" alt="CarPlay screenshot"></figure>

        <div class="callout warning">
          <span class="callout-icon" aria-hidden="true">&#9888;&#65039;</span>
          <div class="callout-body"><strong>You cannot tap directly on cache pins on the map.</strong> To interact with a geocache, you must use the cache list button. Tap the cache count button to open the list, then select the cache you want to view or navigate to. <strong>This is a limitation of CarPlay itself, imposed by Apple.</strong></div>
        </div>

        <h2 id="intelligence-summaries">Cachly Intelligence summaries</h2>
        <p>With <a href="intelligence.html">Cachly Intelligence</a> enabled, the cache details screen gains a <strong>sparkle</strong> button in the top bar. Tap it and choose <strong>Summarize Description</strong> or <strong>Summarize Logs</strong> &mdash; Cachly generates a concise <a href="intelligence.html#summaries">AI summary</a> and <strong>reads it aloud</strong>, so you get the gist of a long description or the latest finder activity without taking your eyes off the road.</p>
        <div class="callout tip">
          <span class="callout-icon" aria-hidden="true">&#10024;</span>
          <div class="callout-body">The sparkle button appears once Cachly Intelligence is turned on in <span class="ui-path">Settings &rsaquo; Cachly Pro</span> on your iPhone and an <a href="intelligence.html#setup">AI provider</a> is set up.</div>
        </div>

        <h2 id="trips">Using Trips (offline lists)</h2>
        <p>Trips are offline lists you&rsquo;ve created and saved offline in the Cachly iOS app. They allow you to browse and navigate to geocaches without an internet connection.</p>
        <figure class="article-img"><img loading="lazy" src="assets/help-images/carplay-10.jpg" alt="CarPlay screenshot"></figure>

        <h3>Setting up Trips for CarPlay</h3>
        <p>Before your Trips appear in CarPlay, you must enable them in the iOS app:</p>
        <ol>
          <li>Open Cachly on your iPhone</li>
          <li>Tap the Trips tab (car icon) in the Lists section of Cachly</li>
          <li>Tap <strong>+</strong> to create a new Trip list</li>
          <li>Copy or add caches from the Live tab or other offline lists</li>
          <li>Optionally, arrange the sort order of your lists</li>
        </ol>

        <h3>Browsing Trips in CarPlay</h3>
        <figure class="article-img"><img loading="lazy" src="assets/help-images/carplay-11.jpg" alt="CarPlay screenshot"></figure>
        <ol>
          <li>From the main map, access the menu by tapping the <strong>trips menu button</strong></li>
          <li>Browse your available offline lists</li>
          <li>Each Trip shows:
            <ol>
              <li>List name</li>
              <li>Number of geocaches</li>
              <li>Last updated date</li>
            </ol></li>
          <li>Tap a Trip to view its caches</li>
          <li>Select the <strong>Show on Map</strong> icon to display all caches from that Trip on the map</li>
        </ol>
        <figure class="article-img"><img loading="lazy" src="assets/help-images/carplay-12.jpg" alt="CarPlay screenshot"></figure>

        <h3>Custom sorting</h3>
        <p>You can sort caches within a Trip two ways:</p>
        <ul>
          <li><strong>By Distance</strong> &mdash; caches sorted by proximity to your current location (default)</li>
          <li><strong>Custom Order</strong> &mdash; respects the manual sort order you&rsquo;ve set in the iOS app</li>
        </ul>
        <p>To change sorting, go to <span class="ui-path">Settings &rsaquo; Sorting</span> in CarPlay.</p>

        <h2 id="navigation">Navigating to geocaches</h2>
        <p>Cachly supports multiple navigation options to guide you to geocaches.</p>
        <figure class="article-img"><img loading="lazy" src="assets/help-images/carplay-13.jpg" alt="CarPlay screenshot"></figure>

        <h3>Starting navigation</h3>
        <ol>
          <li>Select a geocache from the list or cache details</li>
          <li>Tap <strong>Navigate</strong></li>
          <li>Choose your preferred navigation app (if not set as default)</li>
        </ol>

        <h3>Navigation apps</h3>
        <p>Cachly supports the following navigation options:</p>
        <ol>
          <li><strong>Pro Offline Maps</strong> &mdash; Cachly&rsquo;s built-in navigation using downloaded offline maps</li>
          <li><strong>Apple Maps</strong> &mdash; opens Apple Maps with directions</li>
          <li><strong>Google Maps</strong> &mdash; opens Google Maps (must be installed)</li>
          <li><strong>Waze</strong> &mdash; opens Waze (must be installed)</li>
          <li><strong>TomTom Go</strong> &mdash; opens TomTom Go (must be installed)</li>
        </ol>
        <p>You can set your default navigation app in <span class="ui-path">Settings &rsaquo; Navigation</span>. The first time you navigate, Cachly shows the full list of options; after that it uses your saved default.</p>

        <h3>During navigation using Pro Offline Maps</h3>
        <p>When navigating to a geocache using offline maps:</p>
        <ul>
          <li>A navigation line shows the direct route to the cache</li>
          <li>The map tracks both your location and the destination</li>
          <li>An information panel shows the cache name and details</li>
          <li>You can log the cache or proceed to the next cache in your route</li>
          <li><strong>The geocache will show on your iOS device</strong></li>
        </ul>

        <h3>Starting navigation from iPhone</h3>
        <p>You can start navigation from the Cachly iOS app while connected to CarPlay:</p>
        <ol>
          <li>Open a geocache in the iOS app and browse to the navigate screen</li>
          <li>Tap the action <strong>&hellip;</strong> button and choose <strong>Pro Offline Maps</strong></li>
          <li>CarPlay will automatically begin navigating to that cache</li>
        </ol>

        <h2 id="routes">Multiple cache routes</h2>
        <p>Plan a geocaching route with multiple stops directly from CarPlay.</p>

        <h3>Creating a route</h3>
        <ol>
          <li>Open the cache list (tap the cache count button)</li>
          <li>Tap the <strong>route button</strong> to enter selection mode</li>
          <li>Tap each cache you want to include in your route (checkmarks appear)</li>
          <li>Tap the navigate button to start your route</li>
        </ol>
        <figure class="article-img"><img loading="lazy" src="assets/help-images/carplay-14.jpg" alt="CarPlay screenshot"></figure>

        <h3>Following a multiple cache route using Pro Offline Maps</h3>
        <p>During multiple cache navigation:</p>
        <ul>
          <li>The screen shows which cache you&rsquo;re navigating to (e.g., &ldquo;1 of 5&rdquo;)</li>
          <li>After arriving at or logging a cache, tap <strong>Next</strong> to proceed to the next cache</li>
          <li>The route automatically cycles back to the first cache when you reach the end</li>
          <li>You can log each cache as you visit it</li>
        </ul>

        <h2 id="voice-logging">Voice logging</h2>
        <p>Log your geocache finds hands-free using voice recognition &mdash; perfect for when you&rsquo;re back in the car after finding a cache.</p>
        <figure class="article-img"><img loading="lazy" src="assets/help-images/carplay-15.jpg" alt="CarPlay screenshot"></figure>

        <h3>How to log a cache</h3>
        <ol>
          <li>While viewing a cache or navigating, tap <strong>Log Cache</strong></li>
          <li>Select your log type:
            <ul>
              <li><strong>Found It</strong> &mdash; you found the cache</li>
              <li><strong>DNF</strong> &mdash; Did Not Find</li>
              <li><strong>Write Note</strong> &mdash; add a note without logging a find</li>
              <li><strong>Attended</strong> &mdash; for Event caches</li>
              <li><strong>Will Attend</strong> &mdash; for upcoming Event caches</li>
              <li><strong>Webcam Photo Taken</strong> &mdash; for Webcam caches</li>
            </ul></li>
          <li>Speak your log message when prompted</li>
          <li>Review your message (tap <strong>Review Message</strong> to hear it read back)</li>
          <li>Tap <strong>Send Log</strong> to submit or <strong>Save Log</strong> to save as a draft</li>
        </ol>

        <h3>Voice settings</h3>
        <p>Customize voice logging in <span class="ui-path">Settings &rsaquo; Voice</span>:</p>
        <ul>
          <li><strong>Include Voice Before Template</strong> &mdash; adds your spoken text before any log template you&rsquo;ve set up in the iOS app</li>
          <li><strong>Skip Voice Input</strong> &mdash; quickly log without speaking (uses your template only)</li>
        </ul>

        <h3>Log templates</h3>
        <p>CarPlay respects the log templates you&rsquo;ve configured in the iOS Cachly app. Your voice message can be combined with these templates for consistent, detailed logs.</p>

        <h3>Offline logging</h3>
        <p>If you don&rsquo;t have an internet connection when logging:</p>
        <ul>
          <li>Your log is automatically saved as a draft (Field Note)</li>
          <li>Sync your drafts when you&rsquo;re back online using the iOS app</li>
        </ul>

        <h2 id="proximity-alerts">Proximity alerts</h2>
        <p>Cachly can alert you when you&rsquo;re approaching a geocache while driving.</p>
        <figure class="article-img"><img loading="lazy" src="assets/help-images/carplay-16.jpg" alt="CarPlay screenshot"></figure>

        <h3>How alerts work</h3>
        <ul>
          <li>When you come within <strong>300 meters</strong> of a geocache, an alert appears</li>
          <li>The alert shows the cache name, type, and basic details</li>
          <li>You can dismiss the alert or tap to navigate</li>
          <li>Alerts only trigger while your vehicle is moving</li>
        </ul>

        <h3>Alert settings</h3>
        <p>Configure alerts in <span class="ui-path">Settings &rsaquo; Alerts</span>:</p>
        <ul>
          <li><strong>Show Upcoming Alert</strong> &mdash; enable or disable proximity alerts</li>
          <li><strong>Alert Only Favorited 2+</strong> &mdash; only show alerts for caches with 2 or more favorite points (helps focus on higher-quality caches)</li>
        </ul>

        <h3>Alert limitations</h3>
        <p>Alerts will NOT appear:</p>
        <ul>
          <li>For caches you&rsquo;ve already found</li>
          <li>For caches you own</li>
          <li>For a cache you&rsquo;ve already been alerted about during this session</li>
          <li>While actively navigating to a cache</li>
          <li>When your vehicle is stationary</li>
        </ul>

        <h2 id="offline-maps">Offline maps</h2>
        <p>Use downloaded vector maps for navigation without an internet connection.</p>
        <figure class="article-img"><img loading="lazy" src="assets/help-images/carplay-17.jpg" alt="CarPlay screenshot"></figure>

        <h3>Setting up offline maps</h3>
        <ol>
          <li>Download offline maps in the Cachly iOS app first</li>
          <li>In CarPlay, tap the <strong>maps icon</strong> on the top left of the map screen</li>
          <li>Select the offline map you want to use</li>
          <li>The map will update to use your selected offline map</li>
        </ol>
        <figure class="article-img"><img loading="lazy" src="assets/help-images/carplay-18.jpg" alt="CarPlay screenshot"></figure>

        <h3>Offline map display</h3>
        <ul>
          <li>Shows map name and country/region</li>
          <li>Use the list to switch between downloaded maps</li>
          <li>Pro Offline Maps navigation uses these downloaded maps</li>
        </ul>

        <h2 id="settings">CarPlay settings</h2>
        <p>Access settings from the main menu to customize your CarPlay experience.</p>
        <figure class="article-img"><img loading="lazy" src="assets/help-images/carplay-19.jpg" alt="CarPlay screenshot"></figure>
        <table>
          <thead><tr><th>Section</th><th>Options</th></tr></thead>
          <tbody>
            <tr><td><strong>Filtering</strong></td><td><strong>Use Filter Options From iPhone</strong> &mdash; sync filters with your iOS app settings. <strong>Exclude My Finds</strong> &mdash; hide caches you&rsquo;ve already found. <strong>Exclude My Hides</strong> &mdash; hide caches you own.</td></tr>
            <tr><td><strong>Voice</strong></td><td><strong>Include Voice Before Template</strong> &mdash; prepend voice input to your log template. <strong>Skip Voice Input</strong> &mdash; log without voice recording.</td></tr>
            <tr><td><strong>Navigation</strong></td><td><strong>Pro Offline Maps</strong> &mdash; use Cachly&rsquo;s built-in navigation. <strong>Apple Maps</strong> &mdash; use Apple Maps for navigation. <strong>Google Maps</strong> &mdash; use Google Maps (if installed). <strong>Waze</strong> &mdash; use Waze (if installed). <strong>TomTom Go</strong> &mdash; use TomTom Go (if installed).</td></tr>
            <tr><td><strong>Map Options</strong></td><td><strong>Map Orientation</strong> &mdash; <strong>North Up</strong> keeps north at the top, <strong>Follow Course</strong> rotates the map to your direction of travel. <strong>Show Compass</strong> &mdash; show a compass on the map. <strong>Show Speed and Altitude</strong> &mdash; show a live speed and altitude readout on the map. <strong>Map Style</strong> &mdash; <strong>Automatic</strong>, <strong>Light</strong> or <strong>Dark</strong>; this also switches the whole CarPlay interface between light and dark appearance.</td></tr>
            <tr><td><strong>Alerts</strong></td><td><strong>Show Upcoming Alert</strong> &mdash; enable proximity alerts. <strong>Alert Only Favorited 2+</strong> &mdash; only alert for highly-favorited caches.</td></tr>
            <tr><td><strong>Pin Type</strong></td><td><strong>Pin Type 1, 2, or 3</strong> &mdash; choose your preferred visual style for cache pins.</td></tr>
            <tr><td><strong>Sorting</strong></td><td><strong>Distance</strong> &mdash; sort caches by distance from you. <strong>Custom</strong> &mdash; use your manual sort order from the iOS app.</td></tr>
          </tbody>
        </table>

        <h2 id="ios-integration">Integration with the iOS app</h2>
        <p>CarPlay works seamlessly with the Cachly iOS app on your iPhone.</p>

        <h3>Trips synchronization</h3>
        <ul>
          <li>Create and manage Trips in the iOS app</li>
          <li>Arrange Trip order in the iOS app to control CarPlay display order</li>
          <li>Download caches for offline access before your trip</li>
        </ul>

        <h3>Custom sort order</h3>
        <p>To use custom sorting in CarPlay:</p>
        <ol>
          <li>Open an offline list in the iOS app</li>
          <li>View the offline trip, choose the <strong>sorting icon on the lists screen</strong>, then choose <strong>Custom</strong> in sort types and manually arrange caches in your preferred order</li>
          <li>In CarPlay, go to <span class="ui-path">Settings &rsaquo; Sorting</span> and select <strong>Custom</strong></li>
          <li>Your caches will now appear in the order you set</li>
        </ol>

        <h3>Filter synchronization</h3>
        <p>Enable <strong>Use Filter Options From iPhone</strong> in CarPlay Settings to apply your iOS app&rsquo;s filter settings when searching for live caches.</p>

        <h3>Navigation handoff</h3>
        <ul>
          <li>Start navigation in CarPlay using offline maps, and the iOS app knows which cache you&rsquo;re heading to</li>
          <li>Start navigation in the iOS app using the CarPlay option</li>
        </ul>

        <h3>Log synchronization</h3>
        <ul>
          <li>Logs submitted from CarPlay appear in your iOS app&rsquo;s log history</li>
          <li>Pending logs saved in CarPlay sync to your Pending Logs on iOS</li>
          <li>Log templates from the iOS app are used in CarPlay</li>
        </ul>

        <h2 id="limitations">Limitations</h2>
        <p>Understanding CarPlay&rsquo;s limitations helps you get the most from the feature.</p>

        <h3>Map interaction</h3>
        <ul>
          <li><strong>Cannot tap on cache pins</strong> &mdash; you must use the cache list to select and interact with geocaches. <strong>This is a limitation of CarPlay itself, imposed by Apple.</strong></li>
          <li><strong>Labels only visible when zoomed in</strong> &mdash; cache names appear at zoom level 14 and higher</li>
          <li><strong>Maximum 200 caches on live map</strong> &mdash; oldest caches are removed when this limit is exceeded</li>
        </ul>

        <h3>Cache loading</h3>
        <ul>
          <li><strong>Minimum zoom level required</strong> &mdash; caches only load at zoom level 12 or higher</li>
          <li><strong>Maximum 100 caches per search</strong> &mdash; API limits restrict how many caches load per request</li>
          <li><strong>Internet required for live search</strong> &mdash; use Trips for offline access</li>
          <li><strong>Adventure Labs</strong> are not currently loaded on the live map</li>
        </ul>

        <h3>Voice logging</h3>
        <ul>
          <li><strong>Requires permissions</strong> &mdash; speech recognition and microphone permissions must be granted in iOS Settings</li>
          <li><strong>On-device only</strong> &mdash; speech recognition happens on your device (not sent to servers)</li>
          <li><strong>May need iOS app setup</strong> &mdash; grant permissions in the iOS app before using in CarPlay</li>
        </ul>

        <h3>Navigation</h3>
        <ul>
          <li><strong>Third-party apps must be installed</strong> &mdash; Google Maps, Waze and TomTom Go only appear if installed on your iPhone</li>
          <li><strong>Offline navigation requires downloaded maps</strong> &mdash; Pro Offline Maps needs pre-downloaded map regions</li>
        </ul>

        <h3>General</h3>
        <ul>
          <li><strong>Cachly Pro required</strong> &mdash; CarPlay features require an active Cachly Pro subscription</li>
          <li><strong>Pagination limits</strong> &mdash; lists show a maximum number of items per page (varies by vehicle); use Load More to see additional items</li>
          <li><strong>No cache descriptions</strong> &mdash; full cache descriptions are not available in CarPlay for safety reasons</li>
        </ul>

        <h2 id="troubleshooting">Troubleshooting</h2>

        <h3>CarPlay not showing Cachly</h3>
        <ul>
          <li>Ensure you have an active Cachly Pro subscription</li>
          <li>Check that CarPlay is enabled for Cachly in <span class="ui-path">iPhone Settings &rsaquo; General &rsaquo; CarPlay</span></li>
          <li>Try disconnecting and reconnecting your iPhone</li>
        </ul>

        <h3>Caches not loading</h3>
        <ul>
          <li>Verify you have an internet connection</li>
          <li>Zoom in to at least level 12 on the map</li>
          <li>Check that your filters aren&rsquo;t excluding all caches</li>
          <li>Try disabling &ldquo;Exclude My Finds&rdquo; temporarily</li>
        </ul>

        <h3>Voice logging not working</h3>
        <ul>
          <li>Open the Cachly iOS app</li>
          <li>Go to <span class="ui-path">More &rsaquo; Settings &rsaquo; Cachly Pro</span></li>
          <li>Ensure Speech Recognition is enabled</li>
          <li>Ensure Microphone access is enabled</li>
        </ul>

        <h3>Trips not appearing</h3>
        <ul>
          <li>Open the Cachly iOS app</li>
          <li>Ensure that you have added offline trips</li>
        </ul>

        <h3>Navigation app not available</h3>
        <ul>
          <li>Google Maps, Waze and TomTom Go only appear if installed on your iPhone</li>
          <li>Install the desired app from the App Store</li>
        </ul>

        <h3>Proximity alerts not triggering</h3>
        <ul>
          <li>Ensure &ldquo;Show Upcoming Alert&rdquo; is enabled in Settings</li>
          <li>Alerts only work while moving (not when stationary)</li>
          <li>Check that you haven&rsquo;t already been alerted for that cache</li>
          <li>Alerts don&rsquo;t appear during active navigation</li>
        </ul>
""")

page("ipad", "iPad",
     "Cachly on iPad: the adaptive split-view layout, multitasking and large-screen workflows.",
     "iPad", "Cachly on iPad",
     "Cachly adapts to the bigger iPad screen with a sidebar and split views instead of a bottom tab bar &mdash; the same features, arranged to take advantage of the space.",
"""        <h2 id="ipad">iPad layout</h2>
        <p>On iPad, Cachly uses an <strong>adaptive split-view layout</strong>: a list or sidebar alongside the map or detail view, so you can see a cache&rsquo;s details and its position at the same time. It also supports iPadOS multitasking, so you can run Cachly beside another app.</p>

        <div class="callout tip">
          <span class="callout-icon" aria-hidden="true">&#128421;</span>
          <div class="callout-body">With <a href="sync-backup.html#icloud-sync">iCloud sync</a> on, lists and data you set up on iPad are ready on your iPhone in the field.</div>
        </div>

        <h2 id="same-features">Everything else is the same</h2>
        <p>The capabilities described throughout this guide &mdash; <a href="map.html">the map</a>, <a href="logging.html">logging</a>, <a href="search.html">search</a>, <a href="offline-maps.html">offline maps</a> and more &mdash; are all present on iPad, just laid out for the larger display.</p>
""")

# ===========================================================================
# Reference & Help
# ===========================================================================

page("faq", "FAQ & Troubleshooting",
     "Answers to common Cachly questions: login problems, GPS accuracy, missing caches, the geocaching.com API, sending a crash log, and more.",
     "FAQ &amp; Troubleshooting", "FAQ &amp; Troubleshooting",
     "Answers to the questions cachers ask most often &mdash; from sign-in trouble to GPS accuracy &mdash; drawn from the Cachly help site.",
"""        <h2 id="about-cachly">About Cachly</h2>
        <h3>Is Cachly the same as geocaching.com?</h3>
        <p>No &mdash; Cachly is an official <strong>partner app</strong> of Geocaching.com / Geocaching HQ. It signs you in through the geocaching.com login page and reads data through the official Geocaching API, made possible by Premium memberships.</p>
        <h3>Is there an Android version?</h3>
        <p>No. Cachly is iOS-only (iPhone, iPad, iPod touch, Apple Watch) and there are no plans for an Android version.</p>
        <h3>What is the geocaching.com API?</h3>
        <p>An API is a defined way for software to communicate. Cachly can only show the data the Geocaching API exposes &mdash; some information on the website isn&rsquo;t available through the API and therefore can&rsquo;t appear in Cachly.</p>
        <h3>Which version of Cachly do I have?</h3>
        <p>Tap <span class="ui-path">More &rsaquo; About Cachly</span> and scroll to the bottom &mdash; the version is shown there.</p>
        <h3>Does Cachly support CarPlay?</h3>
        <p>Yes &mdash; CarPlay arrived in version 8.1 and is part of <a href="cachly-pro.html">Cachly Pro</a>. See <a href="carplay.html">CarPlay</a>.</p>

        <h2 id="login">Sign-in &amp; account</h2>
        <h3>I can&rsquo;t log in, but the website works</h3>
        <p>If your username contains an apostrophe, iOS &ldquo;smart quotes&rdquo; may substitute a curly quote that breaks login. Press &amp; hold the apostrophe key and pick the straight quote, or turn off <span class="ui-path">iOS Settings &rsaquo; General &rsaquo; Keyboard &rsaquo; Smart Punctuation</span>.</p>
        <h3>&ldquo;Opted-out user&rdquo; error</h3>
        <p>Geocaching.com has a privacy option that blocks sharing your data with authorized developer apps like Cachly. It must be <strong>unchecked</strong> at <a href="https://www.geocaching.com/account/settings/authorizations#developer">geocaching.com &rsaquo; Authorizations</a>.</p>
        <h3>I didn&rsquo;t get my confirmation email</h3>
        <p>Check spam/junk, and confirm you typed your address correctly at sign-up (re-register if not). You can also <a href="https://www.geocaching.com/v/send.aspx">resend the validation email</a>.</p>

        <h2 id="finding">Finding &amp; accuracy</h2>
        <h3>Why isn&rsquo;t Cachly showing all caches on the Live tab?</h3>
        <p>A filter is probably active &mdash; the funnel icon is solid and &ldquo;Filtering On&rdquo; shows at the top. Tap the funnel and choose <strong>Reset</strong>. Note that Basic members see a limited set of caches (a geocaching.com restriction &mdash; see <a href="getting-started.html#membership">membership</a>).</p>
        <h3>Why does my GPS accuracy seem poor?</h3>
        <p>Cachly uses the highest accuracy level available to apps (the very top level is reserved for turn-by-turn nav apps on power). Compare with Apple/Google Maps &mdash; reported accuracy should be similar. Accuracy depends on your device&rsquo;s GPS and surroundings.</p>
        <h3>Open geocache links in Safari instead of the Geocaching app</h3>
        <p>Long-press a geocache link and choose <strong>Open in Safari</strong>; iOS remembers the choice. To revert, repeat and choose Open in &ldquo;Geocaching&rdquo;.</p>
        <h3>Add a just-published cache from its email</h3>
        <p>Long-press the link in the publish email, <strong>Copy</strong> it, then paste it into the Live tab search field to open the cache and add it to a list.</p>

        <h2 id="support">Support</h2>
        <h3>How do I send a crash log?</h3>
        <p>Open <span class="ui-path">iOS Settings &rsaquo; Privacy &amp; Security &rsaquo; Analytics &amp; Improvements &rsaquo; Analytics Data</span>, find the <strong>Cachly</strong> entry for the relevant time, tap Share, and email it to <a href="mailto:support@cach.ly">support@cach.ly</a>.</p>
""")

page("whats-new", "What's New in 8.x",
     "What's new in Cachly 8.x: Cachly Pro, CarPlay, Counties/Regions, DeLorme Grid, Auto Load Map, multi-user logging, and the 8.0 feature list.",
     "What&rsquo;s New in 8.x", "What&rsquo;s New in 8.x",
     "Highlights of the Cachly 8.x release line. Many of the headline additions are part of <a href=\"cachly-pro.html\">Cachly Pro</a>.",
"""        <h2 id="pro">Cachly Pro (8.0+)</h2>
        <p>Version 8.0 introduced <a href="cachly-pro.html">Cachly Pro</a>, a premium subscription. Its features rolled out across 8.x:</p>
        <ul>
          <li><strong>Pro Offline Maps</strong> &mdash; worldwide OpenStreetMap vector maps with contours, trails and offline search.</li>
          <li><strong>Counties / Regions</strong> and <strong>DeLorme Grid</strong> &mdash; visual found/not-found tracking by region.</li>
          <li><strong>Auto Load Map</strong> &mdash; caches load as you pan the live map (long-press the reload icon, or enable in Settings &rsaquo; Cachly Pro).</li>
          <li><strong>CarPlay</strong> &mdash; added in 8.1. See <a href="carplay.html">CarPlay</a>.</li>
          <li><strong>Multiple User Logging</strong> &mdash; added in 8.2 (log under several accounts at once).</li>
        </ul>

        <h2 id="non-pro">New for everyone</h2>
        <ul>
          <li><strong>Online Drafts</strong> &mdash; view, edit and submit drafts in-app; they sync to geocaching.com and across devices.</li>
          <li><strong>Rebuilt <a href="waypoints.html#formats">coordinate picker</a></strong> &mdash; five input formats (DDM, DD, DMS, the classic wheel picker and a Plain Text paste field), an &ldquo;Updated&rdquo; badge and one-tap Reset.</li>
          <li><strong><a href="map.html#sync-position">Sync Live &amp; Offline Map Position</a></strong> &mdash; keep the live map and an offline list&rsquo;s map at the same place and zoom.</li>
          <li><strong>Highlights in GPX</strong> &mdash; your <a href="search.html#highlights">highlight colors</a> now round-trip through GPX <a href="import-export.html">import and export</a>, and GPX import is much faster.</li>
          <li><strong>Wherigo download</strong> &mdash; download a cartridge from a Wherigo cache via the &#8943; button (needs the Wherigo app installed).</li>
          <li><strong>Account deletion</strong>, three coordinate copy formats, a larger profile with find count, and a built-in &ldquo;What&rsquo;s New&rdquo; feed.</li>
        </ul>

        <h2 id="other-8-0">Other 8.0 improvements</h2>
        <ul>
          <li><strong>Maps:</strong> toggle trail colors/symbols, share cache location, better place search, Mapy.cz navigation, searchable state/country picker, more proximity-alert sounds, long-press the funnel to toggle filtering, adjustable live-search radius, Adventure Lab owned/found icons, indicator for ignored corrected coordinates, a cancel option on reload.</li>
          <li><strong>Logs:</strong> favorite-heart indicator in My Logs, cache-type icon in place of the avatar, &ldquo;Great story&rdquo;/&ldquo;Helpful&rdquo; shown on your own logs, military-time date keywords, trackable-log keyword support.</li>
          <li><strong>Offline lists:</strong> county-based filtering, pre-populated county lists, the Generate Counties tool (Pro), and removing caches across multiple lists.</li>
          <li><strong>Importing:</strong> Dropbox/Google Drive via the Files app, append-to-personal-note option, Groundspeak personal-note support.</li>
          <li><strong>Apple Watch:</strong> strike-through for archived/disabled caches and infographic complications.</li>
        </ul>

        <div class="callout note">
          <span class="callout-icon" aria-hidden="true">&#8505;</span>
          <div class="callout-body">Cachly Pro is separate from a geocaching.com Premium membership and doesn&rsquo;t change cache-type access or daily cache limits. See the <a href="cachly-pro.html">Cachly Pro</a> page.</div>
        </div>
""")

# ===========================================================================
# Screenshots injected at the top of pages
# ===========================================================================

def esc(s):
    return html.escape(s, quote=True) if s else ""

# Real screenshots captured from the running app (iPhone 17 Pro, iOS 26.2).
SCREENSHOTS = {
    "getting-started": [("01-login.png", "The login screen &mdash; sign in with your geocaching.com account, sign up, or skip to explore.")],
    "interface": [("06-more.png", "The More tab gathers your profile, pending logs, drafts, history, settings, downloads and more.")],
    "map": [('live-map.png', 'The live map with cache pins, favorite-count badges and the right-side tool stack.'),
            ('map-cache-callout.png', 'Tapping a pin shows the cache callout &mdash; name, distance, favorite count, D/T, size and GC code.'),
            ('dropped-pin-menu.png', 'The dropped-pin menu &mdash; create an offline geocache, save the location, navigate, or copy coordinates.'),
            ('map-layers.png', 'The Map Types panel with the Pro Offline Maps download and Apple &amp; Google styles.'),
            ('saved-locations.png', 'Saved Locations under More &mdash; each row keeps a named spot with its coordinates.')],
    "geocache-details": [('cache-details.png', 'The geocache detail screen: header, coordinates and distance, section rows, and the pinned Log Geocache and navigate buttons.'),
            ('cache-details-more-menu.png', "The detail screen's options menu with Refresh, Log a trackable, Highlight, Add Waypoint, Share, Export GPX and more."),
            ('personal-note-add-image.png', 'Attaching a photo to a personal note with the + button; images are stored in iCloud and sync across your devices.'),
            ('corrected-coords-picker.png', 'The Corrected Coordinates editor with the Is Corrected toggle, DDM picker, presets and coordinate tools.'),
            ('cache-additional-info.png', 'The Additional Information screen listing found dates, county, elevation, status flags, type and date hidden.'),
            ('create-geocache.png', 'The Create Offline Geocache editor with details, description and a DDM coordinate picker.')],
    "waypoints": [("24-waypoints.png", "A cache&rsquo;s waypoints, with the User/Cache toggle and each waypoint&rsquo;s coordinates.")],
    "lists": [('lists-main.png', 'The Lists tab on its Offline segment, with the Offline/Online/Trips control and your offline lists.'),
            ('lists-online.png', 'The Online segment &mdash; your geocaching.com bookmark lists, including the Ignore List, with cache counts.'),
            ('lists-trips.png', 'The Trips segment holds trip lists for planning a route of caches.'),
            ('add-to-list-options.png', 'Confirming an Add to List &mdash; how many geocaches will be saved offline, plus Download Images and Show in CarPlay.'),
            ('offline-list-listview.png', 'An offline list in List mode &mdash; sortable cache rows with distance, D/T, size and GC code.'),
            ('offline-list-manage-menu.png', 'The offline list &hellip; menu &mdash; update caches, download images, highlight, export GPX and more.')],
    "trackables": [("31-trackables.png", "The Trackables tab &mdash; your inventory of Travel Bugs and geocoins (Inventory/Owned toggle, TB scanner)."),
                   ("41-trackable-detail.png", "A trackable&rsquo;s detail screen, with Description, Goal, Logs, Images and a Log Trackable button.")],
    "logs": [('logs-main.png', 'The Logs tab: your logs in chronological order with type, date, badges and photo counts.'),
            ('pending-geocache-logs.png', 'Pending Geocache Logs holding a saved log that is ready to upload.'),
            ('pending-logs-menu.png', 'The Pending Logs menu with Select Logs, Export .txt File and Delete All Pending Logs.'),
            ('pending-log-row-menu.png', "A pending log's menu: Post Log, Edit, View Geocache and Delete."),
            ('pending-log-detail.png', 'Editing a pending log reopens the full compose screen with date, type, message and options.')],
    "profile": [('profile-main.png', 'Your profile with premium badge, stat rows and the Found Cache Types chart.'),
            ('profile-gallery.png', 'The Gallery collects photos from your logs, grouped by date.'),
            ('friends.png', 'The Friends list shows your geocaching.com friends with their find counts.'),
            ('usage.png', 'The Usage screen breaks down storage, database objects and API limits.')],
    "logging": [('log-compose.png', 'The Log Geocache screen with Send Log Now, date and time, Log Type, and a per-user section with Message, Favorite Cache, Save as Draft and Trackables.'),
            ('log-type-picker.png', "The Log Type picker: Found it, Didn't find it, Write note, Reviewer Attention Requested and Owner Attention Requested."),
            ('log-message-editor.png', 'The log message editor with its 5,000-character counter and the Cachly Intelligence sparkle button.')],
    "search": [('filters-main.png', 'Live Search Filtering &mdash; the Disable Filtering master toggle, name search, exclusion checkboxes and cache types.'),
            ('filters-3.png', 'The bottom of the live filter screen &mdash; API Sorting, Other toggles, and the Templates section with Current Template and Save New Template.'),
            ('offline-filter.png', 'An offline list&rsquo;s filter screen &mdash; Disable Filters, stackable List Filters and the Filters Template section.'),
            ('offline-filter-types.png', 'The Filter Type picker when adding an offline list filter &mdash; dozens of types from Attributes to Distance and beyond.'),
            ('offline-filter-config.png', 'Configuring a filter &mdash; type-specific Filter Details with AND/OR logic, plus the Advanced Invert Filter option.'),
            ('search-template-list.png', 'Search templates save a whole live-filter configuration for reuse.')],
    "dt-grid": [('dt-grid.png', 'The D/T grid: your finds across all 81 Difficulty/Terrain combinations.')],
    "challenge-tools": [('counties-regions.png', 'Counties / Regions (Pro): per-state progress toward finding a cache in every county.'),
            ('counties-map.png', 'View All shows the state map with found counties in green and missing ones in red.'),
            ('counties-detail.png', 'Tapping a green county opens its panel with the geocaches you found there.'),
            ('delorme-map.png', 'The DeLorme Grid draws atlas pages over the state &mdash; tap a green page to see your finds there.'),],
    "settings": [('settings-main.png', 'The Settings root screen with its twelve categories plus Manage Subscriptions and Restore Purchases.'),
            ('settings-users.png', 'The Users category, new in Cachly 8, showing the Primary User account used for searching.'),
            ('settings-general.png', 'General settings covering measurement units, rotation lock, TB scanner, power mode and coordinate format.'),
            ('settings-map-options.png', 'Map Options & Navigation settings such as cache radius, map rotation and tilt locks, and Fit to Map.'),
            ('settings-caches-waypoints.png', 'Caches & Waypoints settings for pin design, favorite points on pins, live-search data and clustering.'),
            ('settings-proximity.png', 'Proximity Alert settings with per-context enable toggles, trigger distance and centering options.')],
    "offline-maps": [('custom-tile-url-add.png', 'Adding a custom tile source &mdash; URL template in z/x/y format, TMS geometry option and presets like UK OS Maps.')],
    "multi-user-logging": [('settings-users.png', 'Settings &rsaquo; Users &mdash; the Primary User, additional users for logging, and the Multi-User Logging toggle.'),
            ('settings-users-menu.png', 'Each user&rsquo;s menu: Set as Primary, Text Templates, Auto-Visit Trackables, Delete.'),
            ('log-compose-multi-2.png', 'The log screen with an Other Users section listing every added account.'),
            ('log-compose-multi-expanded.png', 'Expanding a user reveals their own Message, Favorite Cache, Save as Draft and Trackables.')],
    "intelligence": [('intelligence-settings.png', 'Cachly Intelligence settings &mdash; the enable toggle, AI Provider, and the three editable prompts.'),
            ('intelligence-ai-provider.png', 'The AI Provider picker: on-device Apple Intelligence, or Claude, ChatGPT and Gemini with your own API key.'),
            ('intelligence-log-summary.png', 'A one-tap summary of a cache&rsquo;s recent logs, generated on-device.'),
            ('intelligence-description-summary.png', 'The same sparkle button on a description condenses a long listing into a quick read.'),
            ('intelligence-log-writing.png', 'Log writing: describe what you want to say&hellip;'),
            ('intelligence-log-writing-result.png', '&hellip;and Cachly Intelligence drafts the log &mdash; Insert it, or Try Again.')],
}

def render_shots(page_id):
    shots = SCREENSHOTS.get(page_id)
    if not shots:
        return ""
    figs = []
    for fname, cap in shots:
        figs.append(
            f'<figure class="shot"><img loading="lazy" src="assets/screenshots/{fname}" '
            f'alt="{esc(cap)}" width="248"><figcaption>{cap}</figcaption></figure>')
    return '<div class="shots">\n' + "\n".join(figs) + '\n</div>\n'



# Prepend real screenshots to the top of each page that has them.
for p in PAGES:
    sh = render_shots(p["id"])
    if sh:
        p["body"] = sh + "\n" + p["body"]




# ===========================================================================
# Static JSON API (api/v1/) — machine-readable articles + search corpus.
# Consumed by the site's ⌘K search (docs.js) and available to the app.
# ===========================================================================
import hashlib
from html.parser import HTMLParser as _HTMLParser

class _SectionText(_HTMLParser):
    """Split a page body into sections at h2 anchors, collecting plain text
    (figures/captions excluded — screenshots are listed separately)."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.sections = [{"anchor": None, "heading": None, "parts": []}]
        self._skip = 0
        self._in_h2 = False
        self._h2 = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("figure", "script", "style"):
            self._skip += 1
        elif tag == "h2":
            self._in_h2, self._h2 = True, []
            self.sections.append({"anchor": a.get("id"), "heading": None, "parts": []})
    def handle_endtag(self, tag):
        if tag in ("figure", "script", "style") and self._skip:
            self._skip -= 1
        elif tag == "h2":
            self._in_h2 = False
            self.sections[-1]["heading"] = re.sub(r"\s+", " ", "".join(self._h2)).strip()
    def handle_data(self, data):
        if self._skip:
            return
        (self._h2 if self._in_h2 else self.sections[-1]["parts"]).append(data)

def _plain(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s or ""))).strip()

# Nav group per page id, parsed from docs.js so the API can't drift from the sidebar.
_groups = {}
_docsjs = open(os.path.join(DOCS, "assets", "docs.js"), encoding="utf-8").read()
for _g in re.finditer(r'title:\s*"([^"]+)",\s*items:\s*\[(.*?)\]', _docsjs, re.S):
    for _pid in re.findall(r'id:\s*"([^"]+)"', _g.group(2)):
        _groups[_pid] = _g.group(1)

_api_dir = os.path.join(DOCS, "api", "v1")
os.makedirs(os.path.join(_api_dir, "articles"), exist_ok=True)
_articles, _entries = [], []
for p in PAGES:
    pid, title = p["id"], html.unescape(p["title"])
    group = _groups.get(pid, "Documentation")
    lead = _plain(p["lead"])
    parser = _SectionText(); parser.feed(p["body"])
    secs = [{"anchor": s["anchor"], "heading": s["heading"],
             "text": re.sub(r"\s+", " ", " ".join(s["parts"])).strip()}
            for s in parser.sections if s["heading"] or "".join(s["parts"]).strip()]
    shots = [{"file": f, "caption": _plain(c)} for f, c in SCREENSHOTS.get(pid, [])]
    _articles.append({"id": pid, "title": title, "section": group,
                      "url": pid + ".html", "lead": lead})
    with open(os.path.join(_api_dir, "articles", pid + ".json"), "w", encoding="utf-8") as _f:
        json.dump({"id": pid, "title": title, "section": group, "url": pid + ".html",
                   "lead": lead, "sections": secs, "screenshots": shots},
                  _f, ensure_ascii=False, indent=1)
    _entries.append({"title": title, "section": group, "href": pid + ".html", "text": lead})
    for s in secs:
        if s["anchor"]:
            _entries.append({"title": title, "heading": s["heading"], "section": group,
                             "href": pid + ".html#" + s["anchor"], "text": s["text"][:400]})

_corpus = json.dumps({"entries": _entries}, ensure_ascii=False)
_hash = hashlib.sha1(_corpus.encode()).hexdigest()[:10]
open(os.path.join(_api_dir, "search.json"), "w", encoding="utf-8").write(_corpus)
with open(os.path.join(_api_dir, "index.json"), "w", encoding="utf-8") as _f:
    json.dump({"version": 1, "hash": _hash, "articles": _articles}, _f,
              ensure_ascii=False, indent=1)
print(f"API: {len(_articles)} articles, {len(_entries)} search entries ({_hash})")

# ===========================================================================
# Write files
# ===========================================================================

def seo_block(p):
    """Canonical + Open Graph/Twitter meta + JSON-LD for one page."""
    url = f"{BASE_URL}/{p['id']}.html"
    title_txt = html.unescape(p["title"])
    desc_txt = html.unescape(p["desc"])
    crumb_txt = html.unescape(_plain(p["crumb"]))
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "TechArticle",
                "headline": title_txt,
                "description": desc_txt,
                "url": url,
                "inLanguage": "en",
                "isPartOf": {
                    "@type": "WebSite",
                    "name": "Cachly User Guide",
                    "url": BASE_URL + "/",
                },
                "about": {
                    "@type": "MobileApplication",
                    "name": "Cachly",
                    "operatingSystem": "iOS",
                    "url": "https://www.cachly.com/",
                },
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Docs",
                     "item": BASE_URL + "/"},
                    {"@type": "ListItem", "position": 2, "name": crumb_txt,
                     "item": url},
                ],
            },
        ],
    }
    lines = [
        f'  <link rel="canonical" href="{url}">',
        f'  <meta property="og:title" content="{esc(title_txt)} — Cachly Documentation">',
        f'  <meta property="og:description" content="{esc(desc_txt)}">',
        f'  <meta property="og:url" content="{url}">',
        '  <meta property="og:site_name" content="Cachly User Guide">',
        '  <meta property="og:type" content="article">',
        f'  <meta property="og:image" content="{BASE_URL}/assets/logo.png">',
        '  <meta name="twitter:card" content="summary">',
        '  <script type="application/ld+json">',
        json.dumps(ld, ensure_ascii=False, indent=1),
        "  </script>",
    ]
    return "\n".join(lines)

count = 0
for p in PAGES:
    out = os.path.join(DOCS, p["id"] + ".html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(SHELL.format(seo=seo_block(p), **p))
    count += 1

# sitemap.xml + robots.txt (index.html is hand-maintained but still listed).
_urls = [BASE_URL + "/"] + [f"{BASE_URL}/{p['id']}.html" for p in PAGES]
with open(os.path.join(DOCS, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in _urls:
        f.write(f"  <url><loc>{u}</loc></url>\n")
    f.write("</urlset>\n")


print(f"Generated {count} pages in {DOCS} (+ sitemap.xml)")
for p in PAGES:
    print("  -", p["id"] + ".html")
