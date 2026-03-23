"""Write the new editor.html — run once then delete."""
content = r'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Éditeur — 3D Masterclass Syllabus</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
    body { font-family:'Inter',sans-serif; background-color:#f8f1e0; color:#4a3426;
        background-image:url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%234a3426' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E"); }
    ::-webkit-scrollbar{width:8px;height:8px}::-webkit-scrollbar-track{background:#f8f1e0}::-webkit-scrollbar-thumb{background:#cfa848;border-radius:4px;border:2px solid #f8f1e0}::-webkit-scrollbar-thumb:hover{background:#4a3426}
    @keyframes fadeSlideIn{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
    .animate-fade-slide{animation:fadeSlideIn 0.4s ease-out}
    .banner-gradient{background:linear-gradient(180deg,#e0d1bc 0%,#eaddcf 50%,rgba(248,241,224,0) 100%);border-radius:1rem;padding:2rem 2rem 2.5rem 2rem;margin:0 0 1.5rem 0}
    [contenteditable]{cursor:text;transition:outline .12s,background-color .12s;border-radius:5px}
    [contenteditable]:hover{outline:1.5px dashed rgba(207,168,72,.7);outline-offset:4px}
    [contenteditable]:focus{outline:2px solid #cfa848 !important;outline-offset:4px;background-color:rgba(207,168,72,.04)}
    .del-btn{opacity:0;transition:opacity .15s}.hover-group:hover .del-btn{opacity:1}
    .tool-input{display:none;padding:4px 10px;border-radius:6px;border:1.5px dashed #cfa848;background:rgba(207,168,72,.06);font-size:.875rem;color:#4a3426;outline:none;width:110px;font-family:'Inter',sans-serif}
    .tool-input:focus{border-style:solid;background:rgba(207,168,72,.1)}
    .meta-input{background:transparent;border:none;border-bottom:1.5px solid rgba(207,168,72,.4);outline:none;color:rgba(74,52,38,.55);font-family:'Inter',sans-serif;font-size:.875rem;transition:border-color .15s}
    .meta-input:focus{border-bottom-color:#cfa848;color:#4a3426}
    .spill{display:inline-flex;align-items:center;gap:5px;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:700;border:1px solid;transition:all .2s}
    .s-idle{background:rgba(207,168,72,.12);color:#cfa848;border-color:rgba(207,168,72,.45)}
    .s-dirty{background:rgba(207,168,72,.15);color:#b8922e;border-color:#b8922e}
    .s-saving{background:rgba(207,168,72,.15);color:#cfa848;border-color:#cfa848}
    .s-saved{background:rgba(61,148,100,.12);color:#3d9464;border-color:#3d9464}
    .s-error{background:rgba(224,90,78,.12);color:#e05a4e;border-color:#e05a4e}
    /* resize handle on left-column cards */
    .v-resize{display:flex;justify-content:center;align-items:center;height:12px;cursor:ns-resize;color:rgba(207,168,72,.5);user-select:none;margin-top:4px}
    .v-resize:hover{color:#cfa848}
    /* color picker popover */
    #colorPop{position:fixed;z-index:9999;background:#fff;border:1px solid #eaddcf;border-radius:12px;padding:10px 12px;box-shadow:0 8px 32px rgba(74,52,38,.18);display:none;align-items:center;gap:8px;flex-wrap:wrap;width:220px}
    #colorPop.visible{display:flex}
    .cp-swatch{width:22px;height:22px;border-radius:50%;border:2px solid transparent;cursor:pointer;transition:transform .1s,border-color .1s;flex-shrink:0}
    .cp-swatch:hover{transform:scale(1.2);border-color:#cfa848}
    #cpNative{width:28px;height:28px;border:none;border-radius:50%;padding:0;cursor:pointer;background:none;overflow:hidden;flex-shrink:0}
    #cpNative::-webkit-color-swatch-wrapper{padding:0}
    #cpNative::-webkit-color-swatch{border-radius:50%;border:2px solid #eaddcf}
    .cp-reset{font-size:10px;font-weight:700;color:#4a3426;background:#f8f1e0;border:1px solid #eaddcf;border-radius:6px;padding:2px 7px;cursor:pointer;white-space:nowrap}
    .cp-reset:hover{border-color:#cfa848;color:#cfa848}
    /* left-col card that is color-target for its background */
    .left-card{position:relative}
    .card-color-btn{position:absolute;top:8px;right:8px;width:20px;height:20px;border-radius:50%;border:1.5px solid rgba(207,168,72,.4);background:#f8f1e0;cursor:pointer;display:flex;align-items:center;justify-content:center;opacity:0;transition:opacity .15s}
    .left-card:hover .card-color-btn{opacity:1}
</style>
<script>tailwind.config={theme:{extend:{}}}</script>
</head>
<body class="bg-[#f8f1e0] text-[#4a3426] min-h-screen">

<!-- COLOR PICKER POPOVER (global, appended to body) -->
<div id="colorPop">
    <span id="cpLabel" style="font-size:11px;font-weight:700;color:#4a3426;width:100%;margin-bottom:2px">Couleur</span>
    <span class="cp-swatch" style="background:#4a3426" data-c="#4a3426"></span>
    <span class="cp-swatch" style="background:#cfa848" data-c="#cfa848"></span>
    <span class="cp-swatch" style="background:#5d4231" data-c="#5d4231"></span>
    <span class="cp-swatch" style="background:#e05a4e" data-c="#e05a4e"></span>
    <span class="cp-swatch" style="background:#3d9464" data-c="#3d9464"></span>
    <span class="cp-swatch" style="background:#2e6db4" data-c="#2e6db4"></span>
    <span class="cp-swatch" style="background:#f8f1e0" data-c="#f8f1e0;border:1px solid #eaddcf"></span>
    <input type="color" id="cpNative" value="#4a3426" title="Couleur personnalisée">
    <button class="cp-reset" id="cpReset">Réinitialiser</button>
</div>

<!-- NAVBAR -->
<header class="sticky top-0 z-50 bg-[#4a3426] border-b-4 border-[#cfa848] shadow-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div class="flex items-center gap-3">
            <div class="bg-[#cfa848] p-2 rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#4a3426" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.29 7 12 12 20.71 7"/><line x1="12" y1="22" x2="12" y2="12"/></svg>
            </div>
            <div>
                <h1 class="text-[#f8f1e0] font-bold text-lg leading-none">3D Masterclass</h1>
                <span class="text-xs text-[#cfa848] font-bold tracking-wider uppercase">Éditeur de Syllabus</span>
            </div>
        </div>
        <div class="flex items-center gap-4">
            <span id="saveStatus" class="spill s-idle">Chargement…</span>
            <button onclick="saveAll()" class="flex items-center gap-2 px-4 py-2 rounded-lg bg-[#cfa848] hover:bg-[#b8922e] transition-all duration-200 border border-[#b8922e] shadow-[0_3px_0_rgb(140,100,20)] hover:shadow-none hover:translate-y-0.5 text-sm text-[#4a3426] font-bold">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
                Sauvegarder
            </button>
            <a href="index.html" target="_blank" class="flex items-center gap-2 px-3 py-1 rounded-full bg-[#3a2418] border border-[#cfa848]/30 text-sm text-[#f8f1e0] font-medium hover:border-[#cfa848] transition-colors" style="text-decoration:none;">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                Voir le syllabus
            </a>
        </div>
    </div>
</header>

<main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="grid grid-cols-1 md:grid-cols-12 gap-8">
        <!-- Sidebar -->
        <aside class="md:col-span-4 lg:col-span-3 space-y-4">
            <div class="flex items-center justify-between mb-4 px-1">
                <h2 class="text-[#4a3426]/60 text-sm font-bold uppercase tracking-wider">Timeline</h2>
                <span id="module-counter" class="text-xs bg-[#eaddcf] text-[#4a3426] font-medium px-2 py-0.5 rounded-full border border-[#cfa848]/20">–/–</span>
            </div>
            <button id="scroll-up-btn" onclick="paginateModules(-1)" class="w-full hidden flex justify-center items-center py-2 rounded-xl border border-[#eaddcf] bg-white hover:bg-[#fdf7ec] hover:border-[#cfa848] text-[#4a3426]/40 hover:text-[#cfa848] transition-all shadow-sm">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m18 15-6-6-6 6"/></svg>
            </button>
            <div id="module-list" class="space-y-3"></div>
            <button id="scroll-down-btn" onclick="paginateModules(1)" class="w-full flex justify-center items-center py-2 rounded-xl border border-[#eaddcf] bg-white hover:bg-[#fdf7ec] hover:border-[#cfa848] text-[#4a3426]/40 hover:text-[#cfa848] transition-all shadow-sm">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
            </button>
            <button onclick="addModule()" class="w-full flex justify-center items-center gap-2 py-2.5 rounded-xl border-2 border-dashed border-[#cfa848]/30 text-[#4a3426]/40 hover:border-[#cfa848] hover:text-[#cfa848] transition-all text-sm font-medium mt-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                Nouveau module
            </button>
        </aside>

        <!-- Main white card -->
        <section class="md:col-span-8 lg:col-span-9">
            <div class="bg-white border border-[#eaddcf] rounded-3xl p-6 md:p-8 min-h-[800px] shadow-[0_20px_40px_-10px_rgba(74,52,38,0.1)] relative overflow-hidden">
                <div class="absolute top-0 right-0 -mr-20 -mt-20 w-96 h-96 bg-[#cfa848]/5 rounded-full blur-3xl pointer-events-none"></div>
                <div class="absolute bottom-0 left-0 -ml-20 -mb-20 w-64 h-64 bg-[#4a3426]/5 rounded-full blur-3xl pointer-events-none"></div>
                <div id="module-detail" class="relative z-10">
                    <div class="flex flex-col items-center justify-center h-64 text-[#4a3426]/30 gap-3">
                        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" style="opacity:.25"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                        <p class="text-sm">Sélectionnez un module dans la timeline pour l'éditer</p>
                    </div>
                </div>
            </div>
            <footer class="mt-8 text-center text-[#4a3426]/40 text-sm">
                <p>Éditeur — modifications sauvegardées directement dans <strong>index.html</strong></p>
            </footer>
        </section>
    </div>
</main>

<script>
// ════ ICONS ══════════════════════════════════════════════════════════════════
const ICONS={
box:`<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.29 7 12 12 20.71 7"/><line x1="12" y1="22" x2="12" y2="12"/></svg>`,
palette:`<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="13.5" cy="6.5" r=".5" fill="currentColor"/><circle cx="17.5" cy="10.5" r=".5" fill="currentColor"/><circle cx="8.5" cy="7.5" r=".5" fill="currentColor"/><circle cx="6.5" cy="12.5" r=".5" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/></svg>`,
repeat:`<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m17 2 4 4-4 4"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></svg>`,
layers:`<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>`,
briefcase:`<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="7" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>`,
shirt:`<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.38 3.46 16 2a4 4 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.34 2.23l.58 3.57a1 1 0 0 0 .99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.57a2 2 0 0 0-1.34-2.23z"/></svg>`,
user:`<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`,
scanFace:`<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><path d="M9 9h.01"/><path d="M15 9h.01"/></svg>`,
cpu:`<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/></svg>`,
chevronRight:`<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>`,
penTool:`<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15.707 21.293a1 1 0 0 1-1.414 0l-1.586-1.586a1 1 0 0 1 0-1.414l5.586-5.586a1 1 0 0 1 1.414 0l1.586 1.586a1 1 0 0 1 0 1.414z"/><path d="m18 13-1.375-6.874a1 1 0 0 0-.746-.776L3.235 2.028a1 1 0 0 0-1.207 1.207L5.35 15.879a1 1 0 0 0 .776.746L13 18"/><path d="m2.3 2.3 7.286 7.286"/><circle cx="11" cy="11" r="2"/></svg>`,
trophy:`<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>`,
checkCircle:`<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>`,
calendar:`<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/><path d="m9 16 2 2 4-4"/></svg>`,
trash:`<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="m19 6-.867 13.142A2 2 0 0 1 16.138 21H7.862a2 2 0 0 1-1.995-1.858L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>`,
upload:`<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>`,
gripLines:`<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/></svg>`,
paintBucket:`<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m19 11-8-8-8.5 8.5a5.5 5.5 0 0 0 7.78 7.78L19 11"/><path d="m5 2 5 5"/><path d="M2 13h15"/><path d="M22 20a2 2 0 1 1-4 0c0-1.6 1.7-2.4 2-4 .3 1.6 2 2.4 2 4z"/></svg>`
};

function getModuleIcon(cat,title){
    if(title.includes('Cloth')||title.includes('Marvelous'))return ICONS.shirt;
    if(title.includes('Anatomy'))return ICONS.user;
    if(title.includes('Scan'))return ICONS.scanFace;
    if(title.includes('IA'))return ICONS.cpu;
    switch(cat){case'modeling':return ICONS.box;case'texturing':return ICONS.palette;case'workflow':return ICONS.repeat;case'specialized':return ICONS.layers;case'career':return ICONS.briefcase;default:return ICONS.box;}
}

// ════ STATE ══════════════════════════════════════════════════════════════════
let modules=[], currentId=null, dirty=false, moduleListStart=0;
const MODULES_PER_PAGE=4;

// ════ COLOR PICKER ═══════════════════════════════════════════════════════════
// colorTarget: { el, key } where key is a dot-path like 'title', 'objective', 'extra.0.bg', etc.
let colorTarget = null;

function initColorPicker(){
    const pop = document.getElementById('colorPop');
    // Swatches
    pop.querySelectorAll('.cp-swatch').forEach(sw=>{
        sw.addEventListener('click',()=>applyColor(sw.dataset.c));
    });
    // Native picker
    const native = document.getElementById('cpNative');
    native.addEventListener('input',()=>applyColor(native.value));
    // Reset
    document.getElementById('cpReset').addEventListener('click',()=>applyColor(null));
    // Close on outside click
    document.addEventListener('mousedown', e=>{
        if(!pop.contains(e.target) && !e.target.closest('[data-cp-key]') && !e.target.closest('.card-color-btn')){
            hideColorPicker();
        }
    });
}

function showColorPicker(e, el, key, label, property){
    e.stopPropagation();
    colorTarget = {el, key, property: property||'color'};
    const pop = document.getElementById('colorPop');
    pop.querySelector('#cpLabel').textContent = label||'Couleur';
    const rect = el.getBoundingClientRect();
    const pw=220, ph=80;
    let left = rect.left;
    let top  = rect.bottom + 8;
    if(left+pw > window.innerWidth) left = window.innerWidth - pw - 8;
    if(top+ph  > window.innerHeight) top = rect.top - ph - 8;
    pop.style.left = left+'px';
    pop.style.top  = top+'px';
    pop.classList.add('visible');
    // Sync native input to current color
    const m = getModule(currentId);
    const cur = m?.colors?.[key];
    if(cur){ document.getElementById('cpNative').value = cur; }
}

function hideColorPicker(){ document.getElementById('colorPop').classList.remove('visible'); colorTarget=null; }

function applyColor(color){
    if(!colorTarget) return;
    const m = getModule(currentId); if(!m) return;
    m.colors = m.colors||{};
    if(color===null){ delete m.colors[colorTarget.key]; }
    else { m.colors[colorTarget.key]=color; }
    // Apply inline to live element
    if(colorTarget.el){
        if(color===null){ colorTarget.el.style.removeProperty(colorTarget.property); }
        else { colorTarget.el.style.setProperty(colorTarget.property, color); }
    }
    markDirty();
    // Don't re-render — just update the live element
}

function getC(m, key, fallback){
    return (m.colors&&m.colors[key]) ? m.colors[key] : (fallback||'');
}

// ════ INIT ═══════════════════════════════════════════════════════════════════
async function init(){
    initColorPicker();
    initResizer();
    try{
        const res=await fetch('/api/modules');
        modules=await res.json();
        renderModuleList();
        if(modules.length>0)selectModule(modules[0].id);
        setStatus('idle','Prêt');
    }catch(e){setStatus('error','Erreur serveur');console.error(e);}
}

// ════ HELPERS ════════════════════════════════════════════════════════════════
function escHtml(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');}
function escAttr(s){return escHtml(s);}
function getModule(id){return modules.find(m=>m.id===id);}
function markDirty(){if(!dirty){dirty=true;setStatus('dirty','Non sauvegardé');}}
function setStatus(t,txt){const el=document.getElementById('saveStatus');el.className='spill s-'+t;el.textContent=txt;}
function pastePlain(e){e.preventDefault();document.execCommand('insertText',false,(e.clipboardData||window.clipboardData).getData('text/plain'));}
function stopEnter(e){if(e.key==='Enter'){e.preventDefault();e.target.blur();}}

// color-button helper  (returns html for a small paint-bucket icon button)
function cpBtn(key, label, property){
    property=property||'color';
    return `<button class="card-color-btn" title="Couleur ${label}" onclick="showColorPicker(event,this.previousElementSibling||this.parentElement,'${key}','${label}','${property}')" style="position:absolute;top:8px;right:8px;width:20px;height:20px;border-radius:50%;border:1.5px solid rgba(207,168,72,.4);background:#f8f1e0;cursor:pointer;display:flex;align-items:center;justify-content:center;opacity:inherit;">${ICONS.paintBucket}</button>`;
}

// ════ SIDEBAR ════════════════════════════════════════════════════════════════
function renderModuleList(){
    const c=document.getElementById('module-list');
    c.innerHTML=modules.slice(moduleListStart,moduleListStart+MODULES_PER_PAGE).map(m=>{
        const a=m.id===currentId;
        return`<button onclick="selectModule(${m.id})" class="w-full text-left p-4 rounded-xl border transition-all duration-300 group flex items-center justify-between ${a?'bg-[#4a3426] border-[#cfa848] shadow-[0_4px_0_rgba(207,168,72,0.3)]':'bg-white border-[#eaddcf] hover:border-[#cfa848] hover:bg-[#fdf7ec] shadow-sm'}">
            <div class="flex items-center gap-4"><div class="p-3 rounded-lg ${a?'bg-[#cfa848] text-[#4a3426]':'bg-[#eaddcf] text-[#4a3426] group-hover:bg-[#cfa848]/30 transition-colors'}">${getModuleIcon(m.category,m.title)}</div>
            <div><span class="text-xs font-bold uppercase tracking-wider ${a?'text-[#cfa848]':'text-[#4a3426]/50'}">Semaine ${m.week}</span>
            <h3 class="font-semibold text-base leading-tight ${a?'text-[#f8f1e0]':'text-[#4a3426]'}">${escHtml(m.title)}</h3></div></div>
            <span class="transition-transform ${a?'text-[#cfa848]':'text-[#4a3426]/30 opacity-0 group-hover:opacity-100'}">${ICONS.chevronRight}</span></button>`;
    }).join('');
    updatePaginationButtons();
}
function paginateModules(dir){const ns=moduleListStart+dir*MODULES_PER_PAGE;if(ns<0||ns>=modules.length)return;moduleListStart=ns;renderModuleList();}
function updatePaginationButtons(){
    const up=document.getElementById('scroll-up-btn'),dn=document.getElementById('scroll-down-btn'),ct=document.getElementById('module-counter');
    if(up)up.classList.toggle('hidden',moduleListStart===0);
    if(dn)dn.classList.toggle('hidden',moduleListStart+MODULES_PER_PAGE>=modules.length);
    if(ct)ct.textContent=`${Math.min(moduleListStart+MODULES_PER_PAGE,modules.length)}/${modules.length}`;
}
function selectModule(id){
    const idx=modules.findIndex(m=>m.id===id);if(idx<0)return;
    if(idx<moduleListStart)moduleListStart=idx;
    else if(idx>=moduleListStart+MODULES_PER_PAGE)moduleListStart=idx-MODULES_PER_PAGE+1;
    currentId=id;hideColorPicker();renderModuleList();renderModuleDetail();
    window.scrollTo({top:0,behavior:'smooth'});
}

// ════ RESIZER ════════════════════════════════════════════════════════════════
let _rz = null;
function initResizer(){
    document.addEventListener('mousemove',e=>{
        if(!_rz)return;
        const dy=e.clientY-_rz.y0;
        const nh=Math.max(60,_rz.h0+dy);
        _rz.el.style.minHeight=nh+'px';
        _rz.y0=e.clientY;_rz.h0=nh;
    });
    document.addEventListener('mouseup',()=>{
        if(!_rz)return;
        // persist height in model
        const m=getModule(currentId);if(m){
            m.heights=m.heights||{};
            m.heights[_rz.key]=_rz.el.style.minHeight;
            markDirty();
        }
        _rz=null;
        document.body.style.userSelect='';
        document.body.style.cursor='';
    });
}
function startResize(e,el,key){
    e.preventDefault();
    document.body.style.userSelect='none';
    document.body.style.cursor='ns-resize';
    _rz={el,key,y0:e.clientY,h0:el.offsetHeight};
}

// ════ MODULE DETAIL ═══════════════════════════════════════════════════════════
function renderModuleDetail(){
    const m=getModule(currentId);if(!m)return;
    m.colors=m.colors||{};m.heights=m.heights||{};m.extraBlocks=m.extraBlocks||[];
    const container=document.getElementById('module-detail');

    const toolsHtml=(m.tools||[]).map((t,i)=>`
        <span class="hover-group flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-[#eaddcf] border border-[#cfa848]/30 text-[#4a3426] text-sm font-medium">
            <span class="text-[#cfa848]">${ICONS.penTool}</span>${escHtml(t)}
            <button class="del-btn ml-0.5 w-4 h-4 flex items-center justify-center rounded-full text-[#4a3426]/40 hover:text-[#e05a4e] hover:bg-[#e05a4e]/10 text-sm leading-none transition-colors" onclick="removeTool(${i})">×</button>
        </span>`).join('');

    const delHtml=(m.deliverables||[]).map((d,i)=>`
        <li class="hover-group flex items-start gap-3 text-sm text-[#5d4231]">
            <div class="mt-2 w-1.5 h-1.5 rounded-full bg-[#cfa848] shrink-0"></div>
            <span contenteditable="true" class="flex-1" data-cp-key="del${i}"
                style="${getC(m,'del'+i)?'color:'+getC(m,'del'+i):''}"
                onblur="updateDeliverable(${i},this.innerText.trim())"
                oninput="markDirty()" onkeydown="stopEnter(event)" onpaste="pastePlain(event)">${escHtml(d)}</span>
            <button class="del-btn ml-auto flex items-center gap-0.5 px-1.5 py-0.5 rounded text-[#4a3426]/25 hover:text-[#cfa848] text-xs" title="Couleur" onclick="showColorPicker(event,this.previousElementSibling,'del${i}','Livrable ${i+1}','color')">${ICONS.paintBucket}</button>
            <button class="del-btn shrink-0 w-4 h-4 rounded-full bg-[#f8f1e0] border border-[#eaddcf] hover:border-[#e05a4e] text-[#4a3426]/30 hover:text-[#e05a4e] flex items-center justify-center text-xs transition-all mt-0.5" onclick="removeDeliverable(${i})">×</button>
        </li>`).join('');

    const schedHtml=(m.schedule||[]).map((day,di)=>{
        const tsHtml=(day.tasks||[]).map((t,ti)=>`
            <li class="hover-group flex items-start gap-2 text-[#5d4231] text-sm">
                <span class="mt-1.5 w-1 h-1 bg-[#cfa848]/60 rounded-full shrink-0"></span>
                <span contenteditable="true" class="flex-1" data-cp-key="task${di}_${ti}"
                    style="${getC(m,'task'+di+'_'+ti)?'color:'+getC(m,'task'+di+'_'+ti):''}"
                    onblur="updateTask(${di},${ti},this.innerText.trim())"
                    oninput="markDirty()" onkeydown="stopEnter(event)" onpaste="pastePlain(event)">${escHtml(t)}</span>
                <button class="del-btn flex items-center gap-0.5 px-1.5 py-0.5 rounded text-[#4a3426]/25 hover:text-[#cfa848] text-xs" onclick="showColorPicker(event,this.previousElementSibling,'task${di}_${ti}','Tâche','color')">${ICONS.paintBucket}</button>
                <button class="del-btn shrink-0 w-4 h-4 rounded-full bg-[#fdf7ec] border border-[#eaddcf] hover:border-[#e05a4e] text-[#4a3426]/30 hover:text-[#e05a4e] flex items-center justify-center text-xs transition-all" onclick="removeTask(${di},${ti})">×</button>
            </li>`).join('');
        const dayBg=getC(m,'dayBg'+di)?'background:'+getC(m,'dayBg'+di)+';':'';
        return`
        <div class="hover-group bg-[#fdf7ec] border border-[#eaddcf] rounded-xl overflow-hidden hover:border-[#cfa848] transition-colors shadow-sm" style="${dayBg}">
            <div class="p-4 flex flex-col md:flex-row md:items-start gap-4">
                <div class="flex-shrink-0 w-16 h-16 bg-white rounded-lg flex flex-col items-center justify-center border border-[#eaddcf] hover:border-[#cfa848] transition-colors shadow-sm">
                    <span class="text-xs text-[#4a3426]/40 uppercase font-bold">Jour</span>
                    <span class="text-2xl font-bold text-[#4a3426]">${day.day}</span>
                </div>
                <div class="flex-grow min-w-0">
                    <div class="flex items-center gap-2 mb-2">
                        <h3 contenteditable="true" class="font-bold text-[#4a3426] border-l-2 border-[#cfa848] pl-2 flex-1" data-cp-key="dayTitle${di}"
                            style="${getC(m,'dayTitle'+di)?'color:'+getC(m,'dayTitle'+di):''}"
                            onblur="updateDayTitle(${di},this.innerText.trim())"
                            oninput="markDirty()" onkeydown="stopEnter(event)" onpaste="pastePlain(event)">${escHtml(day.title)}</h3>
                        <button class="del-btn flex items-center gap-0.5 px-1.5 py-0.5 rounded text-[#4a3426]/25 hover:text-[#cfa848] text-xs" onclick="showColorPicker(event,this.previousElementSibling,'dayTitle${di}','Titre jour','color')">${ICONS.paintBucket}</button>
                        <button class="del-btn flex items-center gap-0.5 px-1.5 py-0.5 rounded text-[#4a3426]/25 hover:text-[#cfa848] text-xs" onclick="showColorPicker(event,this.parentElement.parentElement.parentElement.parentElement,'dayBg${di}','Fond carte jour','background-color')">${ICONS.paintBucket} <span style="font-size:9px">bg</span></button>
                        <button class="del-btn shrink-0 w-5 h-5 rounded-full bg-[#f8f1e0] border border-[#eaddcf] hover:border-[#e05a4e] text-[#4a3426]/30 hover:text-[#e05a4e] flex items-center justify-center text-xs transition-all" onclick="removeDay(${di})">×</button>
                    </div>
                    <ul class="grid grid-cols-1 gap-2">${tsHtml}</ul>
                    <button onclick="addTask(${di})" class="mt-2 flex items-center gap-1.5 text-xs text-[#4a3426]/30 hover:text-[#cfa848] transition-colors font-medium">
                        <span class="w-3.5 h-3.5 rounded-full border border-dashed border-current flex items-center justify-center leading-none">+</span>Tâche
                    </button>
                </div>
            </div>
        </div>`;
    }).join('');

    // Extra left-column blocks
    const extraHtml=(m.extraBlocks||[]).map((blk,bi)=>{
        const bgC=getC(m,'extraBg'+bi)||'#f8f1e0';
        const textC=getC(m,'extraText'+bi)||'#5d4231';
        const h=m.heights?.['extraCard'+bi]||'';
        return`
        <div class="left-card bg-[#f8f1e0] p-6 rounded-2xl border border-[#eaddcf] shadow-sm relative" id="extraCard${bi}" style="background:${bgC};${h?'min-height:'+h:''}" >
            <div class="flex items-center gap-3 mb-3">
                <span contenteditable="true" class="font-black text-xl text-[#4a3426] flex-1" data-cp-key="extraTitle${bi}"
                    style="${getC(m,'extraTitle'+bi)?'color:'+getC(m,'extraTitle'+bi):''}"
                    onblur="updateExtraTitle(${bi},this.innerText.trim())"
                    oninput="markDirty()" onkeydown="stopEnter(event)" onpaste="pastePlain(event)">${escHtml(blk.title)}</span>
                <!-- color buttons always visible on left-card hover -->
                <button class="del-btn flex items-center gap-0.5 px-1.5 py-0.5 rounded text-[#4a3426]/30 hover:text-[#cfa848] text-xs" onclick="showColorPicker(event,this,'extraTitle${bi}','Titre bloc','color')">${ICONS.paintBucket}</button>
                <button class="del-btn flex items-center gap-0.5 px-1.5 py-0.5 rounded text-[#4a3426]/30 hover:text-[#cfa848] text-xs" onclick="showColorPickerBg(event,document.getElementById('extraCard${bi}'),'extraBg${bi}')" title="Fond">${ICONS.paintBucket}<span style="font-size:9px">bg</span></button>
                <button class="del-btn flex items-center gap-0.5 px-1.5 py-0.5 rounded text-[#4a3426]/30 hover:text-[#e05a4e] text-xs" onclick="removeExtraBlock(${bi})">×</button>
            </div>
            <p contenteditable="true" class="text-sm leading-relaxed" data-cp-key="extraBody${bi}"
                style="outline:none;min-height:2em;color:${textC}"
                onblur="updateExtraBody(${bi},this.innerText.trim())"
                oninput="markDirty()" onpaste="pastePlain(event)">${escHtml(blk.body)}</p>
            <button class="del-btn flex items-center gap-0.5 px-1.5 py-0.5 rounded text-[#4a3426]/30 hover:text-[#cfa848] text-xs mt-2" onclick="showColorPicker(event,this.previousElementSibling,'extraBody${bi}','Texte bloc','color')">${ICONS.paintBucket} texte</button>
            <!-- vertical resize handle -->
            <div class="v-resize" onmousedown="startResize(event,this.parentElement,'extraCard${bi}')" title="Redimensionner">${ICONS.gripLines}</div>
        </div>`;
    }).join('');

    // Rendus
    const rc=(m.rendus||[]).length;
    const rendusCards=rc===0
        ?`<div class="col-span-3 flex items-center justify-center h-28 border-2 border-dashed border-[#cfa848]/30 rounded-xl text-[#4a3426]/30 text-sm">Aucun rendu — importez des images ci-dessus</div>`
        :(m.rendus||[]).map((r,i)=>`
            <div class="hover-group relative overflow-hidden rounded-xl border-2 bg-white shadow-lg ${i<3?'border-[#4a3426]':'border-[#eaddcf]'}">
                ${i<3?'<div class="absolute top-2 left-2 z-10 px-2 py-0.5 bg-[#cfa848] rounded-full text-[#4a3426] text-xs font-black uppercase tracking-wider shadow-sm">Affiché</div>':''}
                <div class="aspect-square overflow-hidden bg-[#eaddcf]"><img src="${escAttr(r.image)}" alt="${escAttr(r.student)}" class="w-full h-full object-cover"></div>
                <div class="p-3">
                    <span contenteditable="true" class="block text-sm font-semibold text-[#4a3426]"
                        onblur="updateRenduStudent(${i},this.innerText.trim())"
                        oninput="markDirty()" onkeydown="stopEnter(event)" onpaste="pastePlain(event)">${escHtml(r.student)}</span>
                    <p class="text-xs text-[#4a3426]/30 mt-0.5 truncate">${escHtml(r.image)}</p>
                </div>
                <button onclick="removeRendu(${i})" class="del-btn absolute top-2 right-2 w-7 h-7 rounded-full bg-[#e05a4e] text-white flex items-center justify-center font-bold shadow-md" title="Supprimer">×</button>
            </div>`).join('');

    const titleStyle=getC(m,'title')?`color:${getC(m,'title')};`:'';
    const descStyle=getC(m,'description')?`color:${getC(m,'description')};`:'';
    const objStyle=getC(m,'objective')?`color:${getC(m,'objective')};`:'';
    const objBg=getC(m,'objectiveBg')||'#f8f1e0';
    const delBg=getC(m,'deliverablesBg')||'#f8f1e0';
    const objH=m.heights?.objectiveCard||'';
    const delH=m.heights?.deliverablesCard||'';

    container.innerHTML=`
    <div class="animate-fade-slide p-1">
        <div class="flex justify-end mb-1">
            <button onclick="deleteCurrentModule()" class="flex items-center gap-1.5 px-3 py-1 rounded-lg border border-[#eaddcf] text-[#4a3426]/25 hover:border-[#e05a4e]/50 hover:text-[#e05a4e] text-xs font-medium transition-all">${ICONS.trash} Supprimer ce module</button>
        </div>

        <div class="banner-gradient mb-8">
            <div class="flex items-center gap-2 mb-3 flex-wrap">
                <span class="px-3 py-1 bg-[#cfa848]/15 text-[#4a3426] rounded-full text-xs font-bold uppercase tracking-widest border border-[#cfa848]/30">Module ${m.id}</span>
                <span class="text-[#4a3426]/40 text-sm font-medium">| Semaine</span>
                <input type="number" value="${m.week}" min="1" max="52" class="meta-input w-10 text-center" oninput="updateField('week',parseInt(this.value)||${m.week});renderModuleList();">
                <select class="meta-input ml-2 cursor-pointer" onchange="updateField('category',this.value);renderModuleList();">
                    ${['modeling','texturing','workflow','specialized','career','sculpting','rigging','animation','cloth','lookdev'].map(c=>`<option value="${c}"${m.category===c?' selected':''}>${c.charAt(0).toUpperCase()+c.slice(1)}</option>`).join('')}
                </select>
            </div>
            <div class="hover-group relative inline-block w-full">
                <h1 contenteditable="true" data-cp-key="title"
                    class="text-4xl md:text-5xl font-black text-[#4a3426] mb-4" style="line-height:1.2;outline:none;${titleStyle}"
                    onblur="updateField('title',this.innerText.trim());renderModuleList();"
                    oninput="markDirty()" onkeydown="stopEnter(event)" onpaste="pastePlain(event)">${escHtml(m.title)}</h1>
                <button class="del-btn absolute -right-2 top-0 flex items-center gap-0.5 px-1.5 py-0.5 rounded text-[#4a3426]/25 hover:text-[#cfa848] text-xs" onclick="showColorPicker(event,this.previousElementSibling,'title','Titre','color')">${ICONS.paintBucket}</button>
            </div>
            <div class="hover-group relative">
                <p contenteditable="true" data-cp-key="description"
                    class="text-lg text-[#5d4231] max-w-2xl leading-relaxed" style="outline:none;${descStyle}"
                    onblur="updateField('description',this.innerText.trim())"
                    oninput="markDirty()" onpaste="pastePlain(event)">${escHtml(m.description)}</p>
                <button class="del-btn absolute -right-2 top-0 flex items-center gap-0.5 px-1.5 py-0.5 rounded text-[#4a3426]/25 hover:text-[#cfa848] text-xs" onclick="showColorPicker(event,this.previousElementSibling,'description','Description','color')">${ICONS.paintBucket}</button>
            </div>
            <div class="flex flex-wrap gap-2 mt-5 items-center">
                ${toolsHtml}
                <button id="addToolBtn" onclick="showToolInput()" class="flex items-center gap-1.5 px-3 py-1.5 rounded-md border border-dashed border-[#cfa848]/50 text-[#4a3426]/40 text-sm font-medium hover:bg-[#eaddcf] hover:text-[#4a3426] hover:border-[#cfa848] transition-all">+ Outil</button>
                <input type="text" id="toolInput" class="tool-input" placeholder="Ex: ZBrush" onblur="commitTool(this)" onkeydown="handleToolKey(event,this)">
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- LEFT COLUMN -->
            <div class="lg:col-span-1 space-y-6" id="leftCol">

                <!-- Objectif card -->
                <div class="left-card p-6 rounded-2xl border border-[#eaddcf] shadow-sm relative" id="objectiveCard" style="background:${objBg};${objH?'min-height:'+objH:''}">
                    <div class="flex items-center gap-3 mb-4 text-[#cfa848]">${ICONS.trophy}
                        <h2 class="font-black text-xl text-[#4a3426] flex-1">Objectif</h2>
                        <button class="del-btn flex items-center gap-0.5 px-1.5 py-0.5 rounded text-[#4a3426]/25 hover:text-[#cfa848] text-xs" onclick="showColorPickerBg(event,document.getElementById('objectiveCard'),'objectiveBg')" title="Fond">${ICONS.paintBucket}<span style="font-size:9px">bg</span></button>
                    </div>
                    <p contenteditable="true" data-cp-key="objective"
                        class="text-[#5d4231] text-sm leading-relaxed" style="outline:none;min-height:2em;${objStyle}"
                        onblur="updateField('objective',this.innerText.trim())"
                        oninput="markDirty()" onpaste="pastePlain(event)">${escHtml(m.objective)}</p>
                    <button class="del-btn flex items-center gap-0.5 px-1.5 py-0.5 rounded text-[#4a3426]/25 hover:text-[#cfa848] text-xs mt-2" onclick="showColorPicker(event,this.previousElementSibling,'objective','Objectif','color')">${ICONS.paintBucket} texte</button>
                    <div class="v-resize" onmousedown="startResize(event,document.getElementById('objectiveCard'),'objectiveCard')" title="Redimensionner">${ICONS.gripLines}</div>
                </div>

                <!-- Livrables card -->
                <div class="left-card p-6 rounded-2xl border border-[#eaddcf] shadow-sm relative" id="deliverablesCard" style="background:${delBg};${delH?'min-height:'+delH:''}">
                    <div class="flex items-center gap-3 mb-4 text-[#cfa848]">${ICONS.checkCircle}
                        <h2 class="font-black text-xl text-[#4a3426] flex-1">Livrables</h2>
                        <button class="del-btn flex items-center gap-0.5 px-1.5 py-0.5 rounded text-[#4a3426]/25 hover:text-[#cfa848] text-xs" onclick="showColorPickerBg(event,document.getElementById('deliverablesCard'),'deliverablesBg')" title="Fond">${ICONS.paintBucket}<span style="font-size:9px">bg</span></button>
                    </div>
                    <ul class="space-y-3">${delHtml}</ul>
                    <button onclick="addDeliverable()" class="mt-4 flex items-center gap-2 text-sm text-[#4a3426]/40 hover:text-[#cfa848] transition-colors font-medium">
                        <span class="w-4 h-4 rounded-full border border-dashed border-current flex items-center justify-center text-xs font-bold leading-none">+</span>Ajouter un livrable
                    </button>
                    <div class="v-resize" onmousedown="startResize(event,document.getElementById('deliverablesCard'),'deliverablesCard')" title="Redimensionner">${ICONS.gripLines}</div>
                </div>

                <!-- Extra blocks -->
                ${extraHtml}

                <!-- Add block button -->
                <button onclick="addExtraBlock()" class="w-full flex justify-center items-center gap-2 py-2.5 rounded-xl border-2 border-dashed border-[#cfa848]/30 text-[#4a3426]/40 hover:border-[#cfa848] hover:text-[#cfa848] transition-all text-sm font-medium">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                    Ajouter un bloc
                </button>
            </div>

            <!-- RIGHT COLUMN -->
            <div class="lg:col-span-2">
                <div class="flex items-center gap-3 mb-6"><span class="text-[#cfa848]">${ICONS.calendar}</span><h2 class="text-2xl font-black text-[#4a3426]">Planning de la semaine</h2></div>
                <div class="space-y-4">${schedHtml}</div>
                <button onclick="addDay()" class="mt-4 w-full py-3 border-2 border-dashed border-[#cfa848]/30 rounded-xl text-[#4a3426]/40 hover:border-[#cfa848] hover:text-[#cfa848] transition-all text-sm font-medium">+ Ajouter un jour</button>
            </div>
        </div>

        <!-- Rendus -->
        <div class="mt-10">
            <div class="banner-gradient">
                <div class="flex items-start justify-between gap-4 flex-wrap">
                    <div>
                        <h2 class="text-4xl md:text-5xl font-black text-[#4a3426] mb-3" style="line-height:1.2;">Rendu Étudiants</h2>
                        <p class="text-lg text-[#5d4231] font-light">${rc} rendu(s) — les 3 premiers s'affichent directement.</p>
                    </div>
                    <label for="uploadInput" class="cursor-pointer flex items-center gap-2 px-4 py-2 rounded-lg bg-[#4a3426] hover:bg-[#3a2418] text-[#f8f1e0] text-sm font-bold border-2 border-[#cfa848]/40 hover:border-[#cfa848] transition-all self-start mt-1">
                        ${ICONS.upload} Importer images
                    </label>
                    <input type="file" id="uploadInput" multiple accept="image/*" style="display:none" onchange="handleUpload(this)">
                </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">${rendusCards}</div>
        </div>
    </div>`;
}

// background-color variant of the color picker (targets element bg)
function showColorPickerBg(e, el, key){
    e.stopPropagation();
    const m=getModule(currentId);if(!m)return;
    colorTarget={el,key,property:'background-color'};
    const pop=document.getElementById('colorPop');
    pop.querySelector('#cpLabel').textContent='Fond';
    const rect=e.target.getBoundingClientRect(),pw=220,ph=80;
    let left=rect.left,top=rect.bottom+8;
    if(left+pw>window.innerWidth)left=window.innerWidth-pw-8;
    if(top+ph>window.innerHeight)top=rect.top-ph-8;
    pop.style.left=left+'px';pop.style.top=top+'px';
    pop.classList.add('visible');
    const cur=m.colors?.[key];
    if(cur)document.getElementById('cpNative').value=cur;
}

// ════ FIELD UPDATERS ══════════════════════════════════════════════════════════
function updateField(f,v){const m=getModule(currentId);if(m){m[f]=v;markDirty();}}
function updateDeliverable(i,v){const m=getModule(currentId);if(m?.deliverables)m.deliverables[i]=v,markDirty();}
function updateDayTitle(di,v){const m=getModule(currentId);if(m?.schedule?.[di])m.schedule[di].title=v,markDirty();}
function updateTask(di,ti,v){const m=getModule(currentId);if(m?.schedule?.[di]?.tasks)m.schedule[di].tasks[ti]=v,markDirty();}
function updateRenduStudent(i,v){const m=getModule(currentId);if(m?.rendus?.[i])m.rendus[i].student=v,markDirty();}
function updateExtraTitle(bi,v){const m=getModule(currentId);if(m?.extraBlocks?.[bi])m.extraBlocks[bi].title=v,markDirty();}
function updateExtraBody(bi,v){const m=getModule(currentId);if(m?.extraBlocks?.[bi])m.extraBlocks[bi].body=v,markDirty();}

// ════ DELIVERABLES ════════════════════════════════════════════════════════════
function addDeliverable(){const m=getModule(currentId);if(!m)return;(m.deliverables=m.deliverables||[]).push('Nouveau livrable');renderModuleDetail();markDirty();}
function removeDeliverable(i){const m=getModule(currentId);if(!m)return;m.deliverables.splice(i,1);renderModuleDetail();markDirty();}

// ════ TOOLS ═══════════════════════════════════════════════════════════════════
function removeTool(i){const m=getModule(currentId);if(!m)return;m.tools.splice(i,1);renderModuleDetail();markDirty();}
function showToolInput(){const i=document.getElementById('toolInput');if(!i)return;i.style.display='inline-block';i.value='';i.focus();document.getElementById('addToolBtn').style.display='none';}
function commitTool(inp){const v=inp.value.trim();inp.style.display='none';const b=document.getElementById('addToolBtn');if(b)b.style.display='';if(!v||!currentId)return;const m=getModule(currentId);(m.tools=m.tools||[]).push(v);renderModuleDetail();markDirty();}
function handleToolKey(e,inp){if(e.key==='Enter'){e.preventDefault();commitTool(inp);}if(e.key==='Escape'){inp.style.display='none';const b=document.getElementById('addToolBtn');if(b)b.style.display='';}}

// ════ SCHEDULE ════════════════════════════════════════════════════════════════
function addDay(){const m=getModule(currentId);if(!m)return;m.schedule=m.schedule||[];const n=m.schedule.length>0?Math.max(...m.schedule.map(d=>d.day))+1:1;m.schedule.push({day:n,title:'Nouveau jour',tasks:[]});renderModuleDetail();markDirty();}
function removeDay(di){const m=getModule(currentId);if(!m)return;m.schedule.splice(di,1);renderModuleDetail();markDirty();}
function addTask(di){const m=getModule(currentId);if(!m)return;(m.schedule[di].tasks=m.schedule[di].tasks||[]).push('Nouvelle tâche');renderModuleDetail();markDirty();}
function removeTask(di,ti){const m=getModule(currentId);if(!m)return;m.schedule[di].tasks.splice(ti,1);renderModuleDetail();markDirty();}

// ════ EXTRA BLOCKS ════════════════════════════════════════════════════════════
function addExtraBlock(){const m=getModule(currentId);if(!m)return;(m.extraBlocks=m.extraBlocks||[]).push({title:'Nouveau bloc',body:''});renderModuleDetail();markDirty();}
function removeExtraBlock(bi){const m=getModule(currentId);if(!m)return;m.extraBlocks.splice(bi,1);// also clean colors/heights for this block
Object.keys(m.colors||{}).filter(k=>k.startsWith('extra')&&k.includes(bi)).forEach(k=>delete m.colors[k]);
Object.keys(m.heights||{}).filter(k=>k.includes('extraCard'+bi)).forEach(k=>delete m.heights[k]);
renderModuleDetail();markDirty();}

// ════ RENDUS ══════════════════════════════════════════════════════════════════
function removeRendu(i){const m=getModule(currentId);if(!m)return;m.rendus.splice(i,1);renderModuleDetail();markDirty();}
async function handleUpload(input){
    const m=getModule(currentId);if(!m)return;m.rendus=m.rendus||[];
    const files=Array.from(input.files);if(!files.length)return;
    setStatus('saving',`Envoi de ${files.length} image(s)…`);
    for(const file of files){
        const fd=new FormData();fd.append('moduleId',String(currentId));fd.append('file',file,file.name);
        try{const res=await fetch('/api/upload',{method:'POST',body:fd});const d=await res.json();if(d.ok)m.rendus.push({student:file.name.replace(/\.[^.]+$/,'').replace(/[-_]/g,' '),image:d.path});}catch(e){console.error(e);}
    }
    renderModuleDetail();markDirty();input.value='';
}

// ════ ADD / DELETE MODULE ═════════════════════════════════════════════════════
function addModule(){
    const newId=modules.length>0?Math.max(...modules.map(m=>m.id))+1:1;
    const newWeek=modules.length>0?Math.max(...modules.map(m=>m.week))+1:1;
    modules.push({id:newId,week:newWeek,title:'Nouveau module',category:'modeling',description:'',objective:'',tools:[],deliverables:[],schedule:[],rendus:[],extraBlocks:[],colors:{},heights:{}});
    moduleListStart=Math.max(0,modules.length-MODULES_PER_PAGE);
    renderModuleList();selectModule(newId);markDirty();
}
function deleteCurrentModule(){
    if(!confirm('Supprimer ce module ?'))return;
    const idx=modules.findIndex(m=>m.id===currentId);
    modules.splice(idx,1);currentId=null;dirty=true;
    moduleListStart=Math.max(0,Math.min(moduleListStart,modules.length-MODULES_PER_PAGE));
    if(moduleListStart<0)moduleListStart=0;
    renderModuleList();
    if(modules.length>0)selectModule(modules[Math.max(0,idx-1)].id);
    else document.getElementById('module-detail').innerHTML='<div class="flex items-center justify-center h-64 text-[#4a3426]/30 text-sm">Aucun module.</div>';
}

// ════ SAVE ════════════════════════════════════════════════════════════════════
async function saveAll(){
    setStatus('saving','Sauvegarde…');
    try{
        const res=await fetch('/api/modules',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(modules)});
        const d=await res.json();
        if(d.ok){dirty=false;setStatus('saved','Sauvegardé ✓');}else setStatus('error',d.error||'Erreur');
    }catch(e){setStatus('error','Erreur réseau');console.error(e);}
}

window.addEventListener('beforeunload',e=>{if(dirty){e.preventDefault();e.returnValue='';}});
init();
</script>
</body>
</html>
'''
open('editor.html','w',encoding='utf-8').write(content)
print('ok', len(content))
