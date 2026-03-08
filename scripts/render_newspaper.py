#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / 'templates'
PORTAL_TEMPLATE = (TEMPLATES / 'portal.html.tpl').read_text(encoding='utf-8')
PROJECT_TEMPLATE = (TEMPLATES / 'project.html.tpl').read_text(encoding='utf-8')
SITE_INDEX = ROOT / 'site' / 'index.html'
PORTAL_DATA = ROOT / 'site' / 'data' / 'portal-index.json'


def latest_for_project(editions, slug):
    items = [e for e in editions if e['projectSlug'] == slug]
    items.sort(key=lambda x: x.get('publishedAt', ''), reverse=True)
    return items


def render_portal(projects, editions, generated_at):
    cards = []
    portal_projects = {}
    for project in projects:
        items = latest_for_project(editions, project['slug'])
        latest = items[0] if items else None
        count_text = f"{len(items)} 版" if items else '暂无版次'
        latest_text = f"最新：{latest['title']}" if latest else '最新：暂时还没有归档版次'
        cards.append(
            f'<a class="project-card" href="/projects/{project["slug"]}/index.html">'
            f'<div class="card-top"><span>Project</span><span>{count_text}</span></div>'
            f'<h2>{escape(project["label"])}</h2>'
            f'<p>{escape(project["description"])}</p>'
            f'<div class="card-meta"><span>{escape(latest_text)}</span><span>进入项目长页</span></div>'
            f'</a>'
        )
        portal_projects[project['slug']] = {
            'label': project['label'],
            'description': project['description'],
            'items': [
                {
                    'name': Path(e['htmlUrl']).name,
                    'title': e['title'],
                    'rawTitle': e['rawTitle'],
                    'summary': e['summary'],
                    'url': e['htmlUrl'],
                    'updatedAt': e['updatedAt'],
                    'size': e['size'],
                    'density': e['density'],
                    'densityLabel': e['densityLabel'],
                }
                for e in items
            ],
            'aggregateUrl': f'/projects/{project["slug"]}/index.html',
            'info': {
                'summary': project['summary'],
                'stage': project['stage'],
                'blockers': project['blockers'],
                'updated': project['updatedAt'].replace('T', ' ')[:16],
                'next': project['next'],
            },
        }
    html = (
        PORTAL_TEMPLATE.replace('{{title}}', 'OpenClaw Newspaper Projects')
        .replace('{{heading}}', '项目列表')
        .replace('{{dek}}', '首页现在只保留项目层切换与入口，不再展示项目内容概览、头版工作台或项目内版次预览。进入项目后，直接在项目单页里连续向下阅读全部版次。')
        .replace('{{cards}}', ''.join(cards))
        .replace('{{generatedAt}}', generated_at)
    )
    SITE_INDEX.write_text(html, encoding='utf-8')
    PORTAL_DATA.write_text(json.dumps({'generatedAt': generated_at, 'projects': portal_projects}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def render_project(project, projects, editions):
    items = latest_for_project(editions, project['slug'])
    switches = []
    for p in projects:
        cls = 'project-switch is-active' if p['slug'] == project['slug'] else 'project-switch'
        switches.append(f'<a class="{cls}" href="/projects/{p["slug"]}/index.html">{escape(p["label"])}</a>')

    edition_links = []
    edition_sections = []
    for idx, item in enumerate(items, start=1):
        density_name = '头版' if item['density'] == 'longform' else '快报'
        edition_links.append(
            f'<a class="side-link" href="#edition-{idx}"><small>{density_name} · 第 {idx:02d} 版</small><b>{escape(item["title"])}</b><span>{escape(item["publishedAt"].replace("T", " ")[:16])}</span></a>'
        )
        edition_sections.append(
            f'<section class="edition edition-{escape(item["density"])}" id="edition-{idx}">'
            f'<div class="edition-head"><div class="edition-meta"><small>{density_name} · 第 {idx:02d} 版</small><b>{escape(item["title"])}</b><span>{escape(item["publishedAt"].replace("T", " ")[:16])}</span></div>'
            f'<p>{escape(item["summary"])}</p></div>'
            f'<iframe class="edition-frame" src="{escape(item["htmlUrl"])}" loading="lazy" title="{escape(item["title"])}" data-edition-density="{escape(item["density"])}"></iframe>'
            f'</section>'
        )

    hero = items[0] if items else None
    hero_title = f'{hero["title"]}已经挂进报纸系统，直接去读最新版就行。' if hero else '这个项目位还没有报纸版次。'
    hero_summary = hero['summary'] if hero else project['summary']
    hero_links = []
    if hero:
        hero_links.append('<a class="preview-link is-strong" href="#edition-1">直达最新版</a>')
    hero_links.append('<a class="preview-link" href="/site/index.html">项目门户</a>')

    html = PROJECT_TEMPLATE
    replacements = {
        '{{projectLabel}}': escape(project['label']),
        '{{projectSwitches}}': ''.join(switches),
        '{{projectSummary}}': escape(project['summary']),
        '{{projectStage}}': escape(project['stage']),
        '{{editionCount}}': str(len(items)),
        '{{projectUpdated}}': escape(project['updatedAt'].replace('T', ' ')[:16]),
        '{{projectBlockers}}': escape(project['blockers']),
        '{{projectNext}}': escape(project['next']),
        '{{editionLinks}}': ''.join(edition_links),
        '{{heroTitle}}': escape(hero_title),
        '{{heroSummary}}': escape(hero_summary),
        '{{heroLinks}}': ''.join(hero_links),
        '{{editionSections}}': ''.join(edition_sections),
    }
    for old, new in replacements.items():
        html = html.replace(old, new)
    (ROOT / 'projects' / project['slug'] / 'index.html').write_text(html, encoding='utf-8')


def run_render(projects_path: str | Path, editions_path: str | Path):
    projects_json = json.loads(Path(projects_path).read_text(encoding='utf-8'))
    editions_json = json.loads(Path(editions_path).read_text(encoding='utf-8'))
    projects = projects_json['projects']
    editions = editions_json['editions']
    generated_at = projects_json.get('generatedAt') or editions_json.get('generatedAt') or 'unknown'
    render_portal(projects, editions, generated_at)
    for project in projects:
        render_project(project, projects, editions)
    return len(projects)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--projects', default=str(ROOT / 'data' / 'source' / 'projects.json'))
    parser.add_argument('--editions', default=str(ROOT / 'data' / 'source' / 'editions.json'))
    args = parser.parse_args()
    count = run_render(args.projects, args.editions)
    print(f'rendered portal and {count} project pages')


if __name__ == '__main__':
    main()
