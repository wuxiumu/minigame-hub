#!/usr/bin/env python3
"""把 games/*.md 游戏档案构建成 blog/*.html 博客页（霓虹游乐场风格）。

用法：在仓库根目录执行  python3 tools/build_blog.py
产物：blog/index.html（文章列表）+ blog/<slug>.html（每篇文章页）
"""
import re
from pathlib import Path

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent.parent
GAMES_DIR = ROOT / "games"
BLOG_DIR = ROOT / "blog"
SITE = "https://wuxiumu.github.io/minigame-hub"

md = MarkdownIt("commonmark", {"html": True}).enable("table")


def parse_meta(text: str, slug: str) -> dict:
    title_m = re.search(r"^#\s+(.+)$", text, re.M)
    date_m = re.search(r"收录日期：\s*([0-9-]+)", text)
    score_m = re.search(r"\*\*总分\*\*\s*\|\s*\*\*(\d+)", text)
    comment_m = re.search(r"## 一句话点评\s*\n+(.+)", text)
    score = int(score_m.group(1)) if score_m else 0
    grade = "A" if score >= 16 else "B" if score >= 13 else "C" if score >= 10 else "D"
    return {
        "slug": slug,
        "title": title_m.group(1).strip() if title_m else slug,
        "date": date_m.group(1) if date_m else "",
        "score": score,
        "grade": grade,
        "comment": comment_m.group(1).strip() if comment_m else "",
        "github": f"https://github.com/wuxiumu/minigame-hub/blob/main/games/{slug}.md",
    }


def render_body(text: str) -> str:
    # 去掉首个一级标题（页面头已展示）
    text = re.sub(r"^#\s+.+\n", "", text, count=1)
    body = md.render(text)
    # 外链新窗口打开
    body = body.replace('<a href="http', '<a target="_blank" rel="noopener" href="http')
    return body


STYLE = """
  * { margin: 0; padding: 0; box-sizing: border-box; }
  :root {
    --bg: #0d0817; --panel: rgba(26, 16, 48, .72); --line: rgba(167, 139, 250, .16);
    --text: #f1ecff; --muted: #a89ec9;
    --pink: #ff2d9b; --cyan: #22d3ee; --yellow: #fde047; --green: #4ade80; --purple: #a855f7;
  }
  body {
    background:
      radial-gradient(900px 500px at 15% -5%, rgba(168, 85, 247, .22), transparent 60%),
      radial-gradient(800px 500px at 90% 10%, rgba(255, 45, 155, .16), transparent 60%),
      var(--bg);
    color: var(--text);
    font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", -apple-system, "Segoe UI", sans-serif;
    min-height: 100vh; line-height: 1.7;
  }
  a { color: var(--cyan); }
  .topbar {
    max-width: 900px; margin: 0 auto; padding: 18px 20px;
    display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap;
  }
  .logo { display: flex; align-items: center; gap: 10px; text-decoration: none; color: var(--text); font-size: 18px; font-weight: 800; }
  .logo-dot { width: 12px; height: 12px; border-radius: 4px; background: linear-gradient(135deg, var(--pink), var(--cyan)); box-shadow: 0 0 12px rgba(255,45,155,.8); }
  .nav { display: flex; gap: 8px; flex-wrap: wrap; }
  .nav a {
    font-size: 13px; color: var(--muted); text-decoration: none;
    border: 1px solid var(--line); border-radius: 999px; padding: 5px 14px; transition: .15s;
  }
  .nav a:hover, .nav a.on { color: var(--cyan); border-color: rgba(34,211,238,.5); box-shadow: 0 0 14px rgba(34,211,238,.25); }
  .page { max-width: 900px; margin: 0 auto; padding: 10px 20px 60px; }

  /* 列表页 */
  .blog-head { text-align: center; padding: 26px 0 30px; }
  .blog-head h1 {
    font-size: clamp(30px, 6vw, 44px); font-weight: 900; letter-spacing: 3px; color: #fff;
    text-shadow: 0 0 6px #fff, 0 0 18px var(--pink), 0 0 42px var(--pink), 0 0 90px #c026d3;
  }
  .blog-head .en { margin-top: 8px; font-size: 14px; font-weight: 800; letter-spacing: 6px; color: transparent; -webkit-text-stroke: 1px rgba(34,211,238,.85); }
  .blog-head p { margin-top: 12px; color: var(--muted); font-size: 14px; }
  .post-list { list-style: none; display: grid; gap: 14px; }
  .post-item {
    position: relative; display: flex; align-items: center; gap: 16px;
    padding: 18px 22px 18px 26px;
    background: var(--panel); border: 1px solid var(--line); border-radius: 16px;
    text-decoration: none; color: inherit; transition: .15s;
    backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
  }
  .post-item::before { content: ""; position: absolute; left: 0; top: 14px; bottom: 14px; border-left: 2px dashed rgba(167,139,250,.35); }
  .post-item:hover { transform: translateY(-2px); border-color: rgba(255,45,155,.4); box-shadow: 0 0 22px rgba(255,45,155,.15); }
  .grade-badge {
    width: 48px; height: 48px; border-radius: 13px; display: grid; place-items: center;
    font-size: 21px; font-weight: 900; flex: none;
  }
  .grade-A { color: var(--green); background: rgba(74,222,128,.1); border: 1px solid rgba(74,222,128,.45); text-shadow: 0 0 12px rgba(74,222,128,.7); }
  .grade-B { color: var(--cyan); background: rgba(34,211,238,.1); border: 1px solid rgba(34,211,238,.45); text-shadow: 0 0 12px rgba(34,211,238,.7); }
  .grade-C { color: var(--yellow); background: rgba(253,224,71,.1); border: 1px solid rgba(253,224,71,.4); }
  .grade-D { color: var(--pink); background: rgba(255,45,155,.1); border: 1px solid rgba(255,45,155,.4); }
  .post-main { flex: 1; min-width: 0; }
  .post-title { font-size: 17px; font-weight: 800; display: flex; align-items: baseline; gap: 10px; flex-wrap: wrap; }
  .post-score { font-size: 12px; font-weight: 700; color: var(--yellow); background: rgba(253,224,71,.08); border: 1px solid rgba(253,224,71,.3); border-radius: 999px; padding: 1px 10px; }
  .post-comment { font-size: 13px; color: var(--text); margin-top: 3px; }
  .post-date { font-size: 12px; color: var(--muted); margin-top: 3px; }
  .post-arrow { color: var(--muted); font-size: 17px; flex: none; }
  .post-item:hover .post-arrow { color: var(--pink); }

  /* 文章页 */
  .article {
    background: var(--panel); border: 1px solid var(--line); border-radius: 22px;
    padding: clamp(22px, 5vw, 44px);
    backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
    box-shadow: 0 20px 50px rgba(0,0,0,.35);
  }
  .article-head { border-bottom: 1px solid var(--line); padding-bottom: 20px; margin-bottom: 24px; }
  .article-head h1 { font-size: clamp(26px, 5vw, 36px); font-weight: 900; letter-spacing: 1px; line-height: 1.3; }
  .article-meta { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 14px; align-items: center; }
  .chip {
    font-size: 12px; color: var(--muted); border: 1px solid var(--line);
    border-radius: 999px; padding: 3px 12px; background: rgba(13,8,23,.6);
  }
  .chip.grade { font-weight: 900; font-size: 13px; }
  .article-body h2 {
    font-size: 20px; font-weight: 800; margin: 30px 0 12px;
    display: flex; align-items: center; gap: 10px;
  }
  .article-body h2::before { content: ""; width: 4px; height: 18px; border-radius: 2px; background: linear-gradient(180deg, var(--pink), var(--cyan)); flex: none; }
  .article-body h3 { font-size: 16px; margin: 22px 0 10px; color: var(--cyan); }
  .article-body p { margin: 10px 0; }
  .article-body ul, .article-body ol { padding-left: 24px; margin: 10px 0; }
  .article-body li { margin: 6px 0; }
  .article-body li::marker { color: var(--pink); }
  .article-body strong { color: var(--yellow); }
  .article-body a { text-decoration: none; border-bottom: 1px dashed rgba(34,211,238,.5); }
  .article-body a:hover { text-shadow: 0 0 10px rgba(34,211,238,.6); }
  .article-body blockquote {
    border-left: 3px solid var(--purple); background: rgba(168,85,247,.08);
    padding: 10px 16px; border-radius: 0 10px 10px 0; color: var(--muted); margin: 14px 0;
  }
  .article-body table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px; }
  .article-body th, .article-body td { border: 1px solid var(--line); padding: 9px 12px; text-align: left; }
  .article-body th { background: rgba(168,85,247,.12); color: var(--cyan); font-weight: 700; }
  .article-body tr:nth-child(even) td { background: rgba(255,255,255,.02); }
  .article-body code { background: rgba(13,8,23,.8); border: 1px solid var(--line); border-radius: 6px; padding: 1px 7px; font-size: 13px; }
  .article-foot { margin-top: 34px; padding-top: 20px; border-top: 1px solid var(--line); display: flex; gap: 10px; flex-wrap: wrap; }
  .btn {
    display: inline-flex; align-items: center; gap: 6px; text-decoration: none;
    font-size: 14px; font-weight: 700; padding: 10px 20px; border-radius: 999px; transition: .15s;
  }
  .btn-primary { background: linear-gradient(135deg, var(--pink), var(--purple)); color: #fff; box-shadow: 0 0 18px rgba(255,45,155,.4); }
  .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 0 30px rgba(255,45,155,.65); }
  .btn-ghost { border: 1.5px solid rgba(34,211,238,.5); color: var(--cyan); }
  .btn-ghost:hover { transform: translateY(-2px); box-shadow: 0 0 18px rgba(34,211,238,.3); }
  .site-footer { text-align: center; color: var(--muted); font-size: 13px; padding: 30px 20px 40px; }
  .site-footer a { color: var(--muted); }
"""


def topbar(active: str) -> str:
    return f"""
  <div class="topbar">
    <a class="logo" href="../index.html"><span class="logo-dot"></span><span>minigame-hub</span></a>
    <nav class="nav">
      <a href="../index.html">🎰 游戏厅</a>
      <a href="index.html"{' class="on"' if active else ""}>🎟️ 博客</a>
      <a href="https://github.com/wuxiumu/minigame-hub" target="_blank" rel="noopener">GitHub ↗</a>
    </nav>
  </div>"""


def article_page(meta: dict, body_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{meta['title']} · 游戏评测 | 迷你游戏厅博客</title>
<meta name="description" content="{meta['comment'] or meta['title'] + ' 游戏评测档案'}">
<link rel="canonical" href="{SITE}/blog/{meta['slug']}.html">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<meta property="og:type" content="article">
<meta property="og:title" content="{meta['title']} · 游戏评测 | 迷你游戏厅博客">
<meta property="og:description" content="{meta['comment']}">
<meta property="og:url" content="{SITE}/blog/{meta['slug']}.html">
<meta property="og:image" content="{SITE}/assets/og-image.png">
<style>{STYLE}</style>
</head>
<body>
{topbar(False)}
<main class="page">
  <article class="article">
    <header class="article-head">
      <h1>{meta['title']}</h1>
      <div class="article-meta">
        <span class="chip grade grade-{meta['grade']}">{meta['grade']} 级 · {meta['score']} 分</span>
        <span class="chip">收录于 {meta['date']}</span>
      </div>
    </header>
    <div class="article-body">
{body_html}
    </div>
    <footer class="article-foot">
      <a class="btn btn-primary" href="index.html">🎟️ 更多评测</a>
      <a class="btn btn-ghost" href="../index.html#games-section">🕹️ 去玩自研游戏</a>
      <a class="btn btn-ghost" href="{meta['github']}" target="_blank" rel="noopener">GitHub 原文 ↗</a>
    </footer>
  </article>
</main>
<footer class="site-footer">迷你游戏厅 minigame-hub · 收集好游戏，也做自己的游戏</footer>
</body>
</html>
"""


def index_page(metas: list) -> str:
    items = "\n".join(
        f"""    <li><a class="post-item" href="{m['slug']}.html">
      <span class="grade-badge grade-{m['grade']}">{m['grade']}</span>
      <span class="post-main">
        <span class="post-title">{m['title']}<span class="post-score">{m['score']} 分</span></span>
        <span class="post-comment">“{m['comment']}”</span>
        <span class="post-date">收录于 {m['date']}</span>
      </span>
      <span class="post-arrow">→</span>
    </a></li>"""
        for m in metas
    )
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>游戏博客 · 评测与拆解 | 迷你游戏厅 minigame-hub</title>
<meta name="description" content="迷你游戏厅游戏博客：AI 制作小游戏深度评测、玩法拆解与自研借鉴笔记。">
<link rel="canonical" href="{SITE}/blog/">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:title" content="游戏博客 · 评测与拆解 | 迷你游戏厅">
<meta property="og:description" content="AI 制作小游戏深度评测、玩法拆解与自研借鉴笔记。">
<meta property="og:url" content="{SITE}/blog/">
<meta property="og:image" content="{SITE}/assets/og-image.png">
<style>{STYLE}</style>
</head>
<body>
{topbar(True)}
<main class="page">
  <div class="blog-head">
    <h1>游戏博客</h1>
    <p class="en">GAME REVIEWS</p>
    <p>收录游戏的深度评测 · 玩法拆解 · 自研借鉴笔记，共 {len(metas)} 篇</p>
  </div>
  <ul class="post-list">
{items}
  </ul>
</main>
<footer class="site-footer">迷你游戏厅 minigame-hub · 收集好游戏，也做自己的游戏</footer>
</body>
</html>
"""


def main():
    BLOG_DIR.mkdir(exist_ok=True)
    metas = []
    for f in sorted(GAMES_DIR.glob("*.md")):
        if f.name.startswith("_"):
            continue
        text = f.read_text(encoding="utf-8")
        meta = parse_meta(text, f.stem)
        (BLOG_DIR / f"{meta['slug']}.html").write_text(
            article_page(meta, render_body(text)), encoding="utf-8"
        )
        metas.append(meta)
        print(f"built blog/{meta['slug']}.html  [{meta['grade']} {meta['score']}] {meta['title']}")
    metas.sort(key=lambda m: m["score"], reverse=True)
    (BLOG_DIR / "index.html").write_text(index_page(metas), encoding="utf-8")
    print(f"built blog/index.html  共 {len(metas)} 篇")


if __name__ == "__main__":
    main()
