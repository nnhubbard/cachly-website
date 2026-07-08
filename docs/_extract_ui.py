#!/usr/bin/env python3
"""
Extract a UI reference from Cachly's storyboards.

Parses each scene and pulls out the controls a user actually sees and taps:
bar-button items, buttons, segmented controls, switches, sliders, text fields,
search bars, and static table rows/sections — together with the action selector
or segue each is wired to (i.e. "what the control does"). Tags each screen with a
documentation "area" so the docs generator can place it.

Outputs:
  assets/ui-reference.json   structured screen + control data
  assets/ui-search-index.js  window.CACHLY_UI_INDEX for the ⌘K search

Build-time tool. Re-run after storyboard changes:  python3 _extract_ui.py
"""
import json, os, re
import xml.etree.ElementTree as ET

DOCS = os.path.dirname(os.path.abspath(__file__))
REPO = "/Users/nnhubbard/Documents/Cachly"  # Cachly Xcode source; docs now live outside it

SOURCES = [
    ("ios",   os.path.join(REPO, "Cachly/Base.lproj/Main.storyboard")),
    ("watch", os.path.join(REPO, "Cachly Watch App/Base.lproj/Interface.storyboard")),
]

CONTROLLER_TAGS = {
    "viewController", "tableViewController", "collectionViewController",
    "navigationController", "tabBarController", "pageViewController",
    "splitViewController", "glkViewController", "avPlayerViewController",
    "hostingController", "controller",  # "controller" = WatchKit interface controller
}

# Internal / developer / container screens to keep out of user docs.
EXCLUDE = {
    "ZSSDebugTableView", "ZSSDebugFileList", "ZSSMapboxLayersDebug",
    "ZSSCoreDataStartMigration", "ZSSCoreDataMigration", "ZSSStartMigrationSteps",
    "ZSSMacMasterLeftNavigation", "ZSSMacMasterSplitViewController", "ZSSMacSidebar",
    "ZSSOSMTags", "ZSSTabBarController", "ZSSMasterNavigationController",
}

# Map each screen class to a documentation page id. Anything not listed (and any
# ZSSWK* watch screen) is still included on the All-Screens reference page.
AREA = {
    "ZSSLogin": "getting-started",
    "ZSSMore": "interface",
    "ZSSMasterMap": "map", "ZSSMapTrackingSettings": "map", "ZSSSaveLocation": "map",
    "ZSSGeocacheDetails": "geocache-details", "ZSSGeocacheDescriptionDetails": "geocache-details",
    "ZSSSolutionChecker": "geocache-details", "ZSSPhotoAttributes": "geocache-details",
    "ZSSUpdateCacheNote": "geocache-details", "ZSSCreateGeocache": "geocache-details",
    "ZSSLogGeocache": "logging", "ZSSLogGeocacheMessage": "logging", "ZSSLogDraftEdit": "logging",
    "ZSSLogs": "logs", "ZSSPendingLogs": "logs", "ZSSHistory": "logs",
    "ZSSProjectWaypoint": "waypoints", "ZSSCreateUserWaypoint": "waypoints", "ZSSWaypoints": "waypoints",
    "ZSSTrackables": "trackables", "ZSSTrackablesDetails": "trackables",
    "ZSSLogTrackable": "trackables", "ZSSTBScanner": "trackables",
    "ZSSLists": "lists", "ZSSListsCreate": "lists", "ZSSOfflineList": "lists",
    "ZSSOfflineListCreate": "lists", "ZSSOfflineListCreateOnly": "lists",
    "ZSSAdvancedSearch": "search", "ZSSAdvancedSearchStateCountry": "search",
    "ZSSAdvancedSearchTemplateCreate": "search", "ZSSFiltering": "search",
    "ZSSFilteringDetails": "search", "ZSSFilteringGenericListing": "search",
    "ZSSFilterTemplateCreate": "search", "ZSSFilterTypeSelection": "search",
    "ZSSSortCaches": "search", "ZSSHighlightSettings": "search",
    "ZSSCounties": "challenge-tools", "ZSSCountiesImport": "challenge-tools",
    "ZSSUserProfile": "profile", "ZSSFriends": "profile", "ZSSUsage": "profile",
    "ZSSVectorOfflineFiles2": "offline-maps", "ZSSOfflineMapLayerPOI": "offline-maps",
    "ZSSThunderforestAPIKey": "offline-maps",
    "ZSSImportFromGPX": "import-export", "ZSSExportGPX": "import-export",
    "ZSSSettings": "settings", "ZSSSettingsMapOptions": "settings",
    "ZSSSettingsMapOptionCustomURL": "settings", "ZSSSettingsTextOption": "settings",
    "ZSSDocs": "settings", "ZSSPrivacy": "settings", "ZSSBasicMemberPrompt": "cachly-pro",
    "ZSSTrackingSaveActivity": "map", "ZSSTrackingActivityList": "map",
    "ZSSSaveLocationList": "map",
    # additional screens
    "ZSSAboutCachly": "settings", "ZSSOpenSourceAttribution": "settings",
    "ZSSDocsArticleViewer": "settings", "ZSSProximitySounds": "settings",
    "ZSSSettingsLogTypes": "settings",
    "ZSSAdvancedSearchTemplateList": "search", "ZSSCountiesDetail": "challenge-tools",
    "ZSSFilterOfflineLists": "search", "ZSSFilterTemplateList": "search",
    "ZSSFilteringAttributes": "search", "ZSSFilteringCacheTypes": "search",
    "ZSSFilteringContainerSize": "search", "ZSSFilteringHighlightColors": "search",
    "ZSSFilteringLogTypes": "search", "ZSSHighlightEdit": "search",
    "ZSSHighlightPicker": "search", "ZSSSearchHistory": "search",
    "ZSSBackupsList": "sync-backup", "ZSSiCloudUbiquityFiles": "sync-backup",
    "ZSSCreateGeocacheCacheType": "geocache-details",
    "ZSSCreateGeocacheContainerType": "geocache-details",
    "ZSSGeocacheAdditionalDetails": "geocache-details",
    "ZSSGeocacheAttributes": "geocache-details", "ZSSPhotoGallery": "geocache-details",
    "ZSSUsersFavoritedCache": "geocache-details",
    "ZSSEditLog": "logs", "ZSSLogDrafts": "logs", "ZSSLogFiltering": "logs",
    "ZSSLogsSorting": "logs",
    "ZSSEditLogTypes": "logging", "ZSSLogGeocacheTypes": "logging",
    "ZSSLogKeywordsPicker": "logging", "ZSSTextTemplateCreateEdit": "logging",
    "ZSSTextTemplateList": "logging", "ZSSTextTemplateLogTypes": "logging",
    "ZSSDownloads": "offline-maps", "ZSSMBTilesSearchResults": "offline-maps",
    "ZSSVectorOfflineMigration": "offline-maps",
    "ZSSDownloadGeocacheProgress": "lists", "ZSSListMembership": "lists",
    "ZSSImportedFiles": "import-export", "ZSSPocketQueries": "import-export",
    "ZSSIAPPro": "cachly-pro", "ZSSIAPViewController": "cachly-pro",
    "ZSSNotificationCenter": "profile", "ZSSSouvenirDetails": "profile",
    "ZSSSouvenirsList": "profile", "ZSSUsageTypes": "profile",
    "ZSSUserProfileTrackablesList": "profile",
    "ZSSSortTrackables": "trackables", "ZSSTrackablesAddDetails": "trackables",
    "ZSSTrackablesAdditionalDetails": "trackables", "ZSSTrackablesAutoVisit": "trackables",
    "ZSSTrackablesLogType": "trackables", "ZSSTrackablesMyInventory": "trackables",
    "ZSSTrackablesTravelList": "trackables", "ZSSTrackablesTravelListList": "trackables",
}


def humanize_selector(sel):
    if not sel:
        return None
    name = sel.split(":")[0]
    # strip chained leading verbs that add no meaning (didChange…, onTap…, etc.)
    prev = None
    while prev != name:
        prev = name
        name = re.sub(r"^(did|on|handle|user|tap|press|toggle|change|update|set)(?=[A-Z])",
                      "", name, flags=re.I)
    # strip trailing widget words
    name = re.sub(r"(Tapped|Pressed|Action|Clicked|Button|Switch|Changed|Toggled|Cell|Tap)$", "", name)
    words = re.sub(r"(?<!^)(?=[A-Z])", " ", name).strip()
    if not words:
        return None
    return words[:1].upper() + words[1:]


def derive_title(cls):
    base = re.sub(r"^ZSS(WK)?", "", cls)
    base = re.sub(r"(TableViewController|ViewController|Controller)$", "", base)
    base = re.sub(r"\d+$", "", base)  # drop version suffixes (Files2 -> Files)
    # split camelCase but keep acronym runs intact (GPX, POI, URL, API stay whole)
    words = re.sub(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", " ", base).strip()
    return words or cls


def first_action(el):
    conns = el.find("connections")
    if conns is None:
        return None
    for action in conns.findall("action"):
        if action.get("selector"):
            return action.get("selector")
    return None


def first_segue_dest(el):
    conns = el.find("connections")
    if conns is None:
        return None
    for seg in conns.findall("segue"):
        return seg.get("destination")
    return None


def button_title(el):
    if el.get("title"):
        return el.get("title").strip()
    for st in el.findall("state"):
        if st.get("key") == "normal" and st.get("title"):
            return st.get("title").strip()
    cfg = el.find("buttonConfiguration")
    if cfg is not None and cfg.get("title"):
        return cfg.get("title").strip()
    return None


def segmented_titles(el):
    segs = el.find("segments")
    if segs is None:
        return []
    return [s.get("title").strip() for s in segs.findall("segment") if s.get("title")]


def parse_storyboard(platform, path):
    if not os.path.exists(path):
        return []
    root = ET.parse(path).getroot()

    # id -> human label, for resolving segue destinations
    id_label = {}
    for obj in root.iter():
        oid = obj.get("id")
        if oid and (obj.get("customClass") or obj.get("storyboardIdentifier")):
            cc = obj.get("customClass")
            id_label[oid] = derive_title(cc) if cc else obj.get("storyboardIdentifier")

    screens = []
    for sc in root.findall(".//scene"):
        objects = sc.find("objects")
        if objects is None:
            continue
        controller = None
        for child in objects:
            if child.tag in CONTROLLER_TAGS and child.get("sceneMemberID") == "viewController":
                controller = child; break
        if controller is None:
            for child in objects:
                if child.tag in CONTROLLER_TAGS:
                    controller = child; break
        if controller is None:
            continue

        cls = controller.get("customClass")
        if not cls or cls in EXCLUDE:
            continue
        sid = controller.get("storyboardIdentifier")

        title = controller.get("title")
        navitem = controller.find(".//navigationItem")
        if navitem is not None and navitem.get("title"):
            title = navitem.get("title")
        derived = False
        if not title:
            title = derive_title(cls); derived = True

        controls, seen = [], set()

        def add(kind, label, action=None, detail=None):
            label = (label or "").strip()
            key = (kind, label, action, detail)
            if key in seen:
                return
            seen.add(key)
            controls.append({"kind": kind, "label": label, "action": action, "detail": detail})

        def detail_for(el):
            dest = first_segue_dest(el)
            return ("Opens " + id_label[dest]) if dest and dest in id_label else None

        for bbi in controller.iter("barButtonItem"):
            label = bbi.get("title")
            if not label and bbi.get("systemItem"):
                si = bbi.get("systemItem"); label = si[:1].upper() + si[1:]
            sel = first_action(bbi); h = humanize_selector(sel)
            if not label:
                label = h or "(icon)"; h = None
            add("Bar button", label, h, detail_for(bbi))

        for b in controller.iter("button"):
            t = button_title(b); sel = first_action(b); h = humanize_selector(sel)
            det = detail_for(b)
            if t:
                add("Button", t, h, det)
            elif h or det:
                add("Button", h or "Button", None if h else h, det)

        for s in controller.iter("segmentedControl"):
            titles = segmented_titles(s)
            if titles:
                add("Segmented control", " / ".join(titles), humanize_selector(first_action(s)))

        for s in controller.iter("switch"):
            t = s.get("title"); h = humanize_selector(first_action(s))
            if t:
                add("Switch", t, h)
            else:
                add("Switch", h or "Toggle", None)

        for s in controller.iter("slider"):
            add("Slider", humanize_selector(first_action(s)) or "Slider", None)

        for tf in controller.iter("textField"):
            if tf.get("placeholder"):
                add("Text field", tf.get("placeholder"), None)

        for sb in controller.iter("searchBar"):
            add("Search bar", sb.get("placeholder") or "Search", None)

        for sec in controller.iter("tableViewSection"):
            if sec.get("headerTitle"):
                add("Section", sec.get("headerTitle"), None, "header")
            if sec.get("footerTitle"):
                add("Section", sec.get("footerTitle"), None, "footer")

        for cell in controller.iter("tableViewCell"):
            det = detail_for(cell)
            labels = [lb.get("text").strip() for lb in cell.iter("label")
                      if lb.get("text") and lb.get("text").strip()]
            if labels and det:
                add("Row", labels[0], None, det)

        screens.append({
            "platform": platform, "class": cls, "storyboardID": sid,
            "title": title, "titleDerived": derived,
            "area": "apple-watch" if platform == "watch" else AREA.get(cls),
            "controls": controls,
        })
    return screens


SRC_DIRS = [
    os.path.join(REPO, "Cachly", "Classes"),
    os.path.join(REPO, "CarPlay"),
    os.path.join(REPO, "Cachly"),
]

def find_source(cls):
    for d in SRC_DIRS:
        for ext in (".m", ".mm", ".swift"):
            p = os.path.join(d, cls + ext)
            if os.path.exists(p):
                return p
    return None


def parse_code(path, cls):
    """Best-effort extraction of programmatic controls from an Obj-C/Swift VC."""
    txt = open(path, encoding="utf-8", errors="ignore").read()
    swift = path.endswith(".swift")
    title = None
    controls = []  # (kind, label, selector|None)

    if swift:
        # Only trust a code title when there's a single assignment — VCs that
        # re-title themselves per mode (e.g. the map) would otherwise mislabel.
        tmatches = re.findall(r'self\.(?:navigationItem\.)?title\s*=\s*(?:NSLocalizedString\(\s*)?"([^"]+)"', txt)
        if len(set(tmatches)) == 1:
            title = tmatches[0].strip()
        for m in re.finditer(r'UIBarButtonItem\(\s*title:\s*(?:NSLocalizedString\(\s*)?"([^"]+)"[\s\S]{0,200}?action:\s*#selector\(([^)\s]+)', txt):
            controls.append(("Bar button", m.group(1).strip(), m.group(2)))
        for m in re.finditer(r'UIBarButtonItem\(\s*barButtonSystemItem:\s*\.(\w+)[\s\S]{0,200}?action:\s*#selector\(([^)\s]+)', txt):
            controls.append(("Bar button", m.group(1)[:1].upper() + m.group(1)[1:], m.group(2)))
        for m in re.finditer(r'UIAlertAction\(\s*title:\s*(?:NSLocalizedString\(\s*)?"([^"]+)"', txt):
            controls.append(("Menu option", m.group(1).strip(), None))
        for m in re.finditer(r'UIAction\(\s*title:\s*(?:NSLocalizedString\(\s*)?"([^"]+)"', txt):
            controls.append(("Menu option", m.group(1).strip(), None))
        for m in re.finditer(r'\.setTitle\(\s*(?:NSLocalizedString\(\s*)?"([^"]+)"', txt):
            controls.append(("Button", m.group(1).strip(), None))
    else:  # Objective-C
        tmatches = re.findall(r'self\.(?:navigationItem\.)?title\s*=\s*(?:NSLocalizedString\(\s*)?@"([^"]+)"', txt)
        if len(set(tmatches)) == 1:
            title = tmatches[0].strip()
        for m in re.finditer(r'initWithTitle:\s*(?:NSLocalizedString\(\s*)?@"([^"]+)"[\s\S]{0,200}?action:@selector\((\w+)\)', txt):
            controls.append(("Bar button", m.group(1).strip(), m.group(2)))
        for m in re.finditer(r'initWithBarButtonSystemItem:UIBarButtonSystemItem(\w+)[\s\S]{0,200}?action:@selector\((\w+)\)', txt):
            controls.append(("Bar button", m.group(1), m.group(2)))
        for m in re.finditer(r'actionWithTitle:\s*(?:NSLocalizedString\(\s*)?@"([^"]+)"', txt):
            controls.append(("Menu option", m.group(1).strip(), None))
        for m in re.finditer(r'setTitle:\s*(?:NSLocalizedString\(\s*)?@"([^"]+)"', txt):
            controls.append(("Button", m.group(1).strip(), None))
        segs = [m.group(1).strip() for m in
                re.finditer(r'insertSegmentWithTitle:\s*(?:NSLocalizedString\(\s*)?@"([^"]+)"', txt)]
        if segs:
            controls.append(("Segmented control", " / ".join(dict.fromkeys(segs)), None))

    # drop empties and obvious non-labels
    clean = []
    for k, label, sel in controls:
        if not label or label.strip() in ("", " "):
            continue
        if "debug" in label.lower():
            continue
        clean.append((k, label, sel))
    return title, clean


def main():
    screens = []
    for platform, path in SOURCES:
        screens.extend(parse_storyboard(platform, path))

    # merge dup classes
    merged = {}
    for s in screens:
        k = (s["platform"], s["class"])
        if k in merged:
            ex = merged[k]
            have = {(c["kind"], c["label"], c["action"], c["detail"]) for c in ex["controls"]}
            for c in s["controls"]:
                if (c["kind"], c["label"], c["action"], c["detail"]) not in have:
                    ex["controls"].append(c)
        else:
            merged[k] = s

    # ---- Augment from source code (programmatic UI) -----------------------
    code_added = 0
    target_classes = set(AREA.keys()) | {s["class"] for s in screens if s["platform"] == "ios"}
    for cls in sorted(target_classes):
        if cls in EXCLUDE:
            continue
        path = find_source(cls)
        if not path:
            continue
        title, ctrls = parse_code(path, cls)
        if not title and not ctrls:
            continue
        key = ("ios", cls)
        screen = merged.get(key)
        if screen is None:
            if AREA.get(cls) is None:
                continue  # only add code-only screens that we can place
            # Code titles are unreliable (VCs re-title per mode), so use the
            # class-derived name rather than a possibly mode-specific string.
            screen = {"platform": "ios", "class": cls, "storyboardID": None,
                      "title": derive_title(cls), "titleDerived": True,
                      "area": AREA.get(cls), "controls": []}
            merged[key] = screen
        have = {(c["kind"], c["label"], c["action"], c["detail"]) for c in screen["controls"]}
        for kind, label, sel in ctrls:
            act = humanize_selector(sel) if sel else None
            k2 = (kind, label, act, None)
            if k2 in have:
                continue
            have.add(k2)
            screen["controls"].append({"kind": kind, "label": label, "action": act,
                                       "detail": None, "source": "code"})
            code_added += 1

    # Clean titles for a few screens whose derived/code name reads poorly.
    TITLE_OVERRIDE = {
        "ZSSMasterMap": "Map", "ZSSMore": "More",
        "ZSSIAPPro": "Upgrade to Cachly Pro", "ZSSIAPViewController": "In-App Purchase",
        "ZSSMBTilesSearchResults": "MBTiles Search Results",
        "ZSSiCloudUbiquityFiles": "iCloud Files",
    }
    for s in merged.values():
        if s["class"] in TITLE_OVERRIDE:
            s["title"] = TITLE_OVERRIDE[s["class"]]

    # Drop any developer/debug controls that slipped through either pass.
    for s in merged.values():
        s["controls"] = [c for c in s["controls"]
                         if "debug" not in (c["label"] or "").lower()
                         and "debug" not in (c["action"] or "").lower()]

    screens = sorted(merged.values(), key=lambda s: (s["platform"], (s["title"] or s["class"]).lower()))

    json.dump(screens, open(os.path.join(DOCS, "assets", "ui-reference.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    # NOTE: the screen search index (assets/ui-search-index.js) is written by
    # _generate.py so its anchors match the generated page anchors exactly.

    ctrl = sum(len(s["controls"]) for s in screens)
    ios = sum(1 for s in screens if s["platform"] == "ios")
    watch = sum(1 for s in screens if s["platform"] == "watch")
    mapped = sum(1 for s in screens if s["area"])
    print(f"Extracted {len(screens)} screens ({ios} iOS, {watch} Watch), {ctrl} controls.")
    print(f"  Added from source code: {code_added} controls")
    print(f"  Mapped to a page: {mapped} · unmapped (reference-only): {len(screens) - mapped}")


if __name__ == "__main__":
    main()
