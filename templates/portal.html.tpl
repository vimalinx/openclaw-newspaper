<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{{title}}</title>
<style>
:root{--paper:#f5f1e8;--ink:#171717;--muted:#666;--rule:#1f1f1f;--accent:#7f1111;--sans:"Inter","PingFang SC","Noto Sans CJK SC",sans-serif;--serif:"Source Han Serif SC","Songti SC","STSong",serif;}
*{box-sizing:border-box;}body{margin:0;background:#ddd6c8;color:var(--ink);font-family:var(--serif);}a{color:inherit}
.page{max-width:1360px;margin:18px auto;background:var(--paper);border:1px solid rgba(0,0,0,.18);box-shadow:0 12px 36px rgba(0,0,0,.18);padding:20px 24px 26px;}
.masthead{border-bottom:4px double var(--rule);padding-bottom:10px;margin-bottom:20px;display:grid;grid-template-columns:minmax(0,1.4fr) minmax(260px,.8fr);gap:18px;}
.topline{font:10px/1.35 var(--sans);letter-spacing:.09em;text-transform:uppercase;color:var(--muted);margin-bottom:6px;}h1{margin:0;font-size:clamp(34px,4.8vw,58px);line-height:.94;}.dek{margin-top:8px;font-size:16px;line-height:1.58;max-width:920px;}
.hero-meta{display:grid;gap:10px;align-content:start;}.hero-chip{background:rgba(255,255,255,.56);padding:12px 14px;}.hero-chip small{display:block;font:11px/1.4 var(--sans);color:var(--muted);margin-bottom:4px;}.hero-chip b{display:block;font:700 14px/1.45 var(--sans);}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;}.project-card{display:block;color:inherit;text-decoration:none;background:linear-gradient(180deg, rgba(255,255,255,.44), rgba(255,255,255,.20));box-shadow:0 10px 24px rgba(0,0,0,.06);padding:20px 20px 18px;}
.card-top,.card-meta{display:flex;justify-content:space-between;gap:12px;font:11px/1.4 var(--sans);color:var(--muted);text-transform:uppercase;letter-spacing:.06em;}.project-card h2{margin:12px 0 10px;font-size:clamp(26px,3vw,40px);line-height:1.02;}.project-card p{margin:0 0 14px;font:14px/1.66 var(--sans);color:#2b251f;}.footer{margin-top:18px;padding-top:10px;border-top:3px double var(--rule);font:10px/1.5 var(--sans);color:var(--muted);}
@media (max-width: 980px){.masthead{grid-template-columns:1fr;} .grid{grid-template-columns:1fr;}}
</style>
</head>
<body>
<main class="page">
<header class="masthead">
  <div>
    <div class="topline">OpenClaw Newspaper Portal</div>
    <h1>{{heading}}</h1>
    <div class="dek">{{dek}}</div>
  </div>
  <div class="hero-meta">
    <div class="hero-chip"><small>当前模式</small><b>首页选项目，项目页直接读报</b></div>
    <div class="hero-chip"><small>导航结构</small><b>顶栏切项目 · 左栏看项目摘要 · 右栏看版次目录</b></div>
  </div>
</header>
<section class="grid">{{cards}}</section>
<footer class="footer">Generated {{generatedAt}}</footer>
</main>
</body>
</html>
