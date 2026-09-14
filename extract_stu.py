#!/usr/bin/env python3
"""
Extraction des sections de programme depuis un fichier projet
Schneider Electric EcoStruxure Control Expert (.STU / .ZEF).

Produit, dans un dossier au nom du .stu, les fichiers suivants :

  <nom>/
    st/NN_<section_ou_programme>.st   Code source Structured Text
    sfc/NN_<programme>.sfc.xml        XML brut du grafcet (source Schneider)
    sfc/NN_<programme>.txt            Grafcet lisible en texte
    sfc/NN_<programme>.tex            Grafcet rendu en TikZ (LaTeX standalone)
    README.md                         Inventaire des sections extraites

Usage :
    python3 extract_stu.py <fichier.STU> [dossier_sortie]
"""

from __future__ import annotations

import re
import shutil
import sys
import tempfile
import zipfile
from collections import defaultdict
from pathlib import Path


KNOWN_PROGRAM_NAMES: list[bytes] = [
    b'GEMMA', b'GMMA_PRE',
    b'GRAPHE', b'GRAPHEPOST',
    b'F1_PRODUCTIONNORMAL', b'F1_PRODUCTIONNORMALPOST',
    b'A1_POST', b'A5_POST', b'A6_SFC', b'SFA6_SFC',
    b'D1_POST', b'D2_POST',
    b'READETHIPROBOT', b'YWRITEETHIPROBOT', b'WRITEQTOR',
    b'READHMI', b'WRITESCREEN',
    b'GM_MOUVEMENT', b'GM_POWER',
    b'TIMER', b'TIMER2',
    b'MAIN',
    b'F1_EVAL_PRISEDEPOSE', b'F1_EVAL_PRISEDEPOSEPOST',
    b'F1_PRISEDEPOSE', b'PRISEDEPOSE',
]

MAX_PROGRAM_LOOKBACK = 400_000
MAX_BLOCK_SIZE = 250_000
ASPBO_LOOKBACK = 400
SECTION_META_MAX_DIST = 5000


# ---------------------------------------------------------------------------
# Archivage et recherche de blocs encodés en UTF-16-LE dans la base binaire
# ---------------------------------------------------------------------------

def extract_archive(stu_path: Path) -> Path:
    tmp = Path(tempfile.mkdtemp(prefix='stu_extract_'))
    with zipfile.ZipFile(stu_path) as zf:
        zf.extractall(tmp)
    return tmp


def iter_utf16_blocks(data: bytes, start_tag: str, end_tag: str):
    start_enc = start_tag.encode('utf-16-le')
    end_enc = end_tag.encode('utf-16-le')
    pos = 0
    while True:
        p = data.find(start_enc, pos)
        if p < 0:
            return
        end_p = data.find(end_enc, p, p + MAX_BLOCK_SIZE)
        if end_p >= 0:
            chunk = data[p:end_p + len(end_enc)]
            pos_next = end_p + len(end_enc)
        else:
            chunk = data[p:p + MAX_BLOCK_SIZE]
            pos_next = p + 2
        yield p, chunk.decode('utf-16-le', errors='replace')
        pos = pos_next


def clean_printable_ascii(text: str) -> str:
    return ''.join(c for c in text if (32 <= ord(c) <= 126) or c in '\n\r\t')


def find_nearest_program(data: bytes, pos: int) -> str:
    best_name = 'unknown'
    best_pos = -1
    low = max(0, pos - MAX_PROGRAM_LOOKBACK)
    for name in KNOWN_PROGRAM_NAMES:
        p = data.rfind(name, low, pos)
        if p > best_pos:
            best_pos = p
            best_name = name.decode()
    return best_name


def find_section_id(data: bytes, pos: int) -> str:
    window = data[max(0, pos - ASPBO_LOOKBACK):pos]
    text_u16 = window.decode('utf-16-le', errors='replace')
    matches = re.findall(r'Aspbo\d+o[A-Z0-9]+\$[UX]', text_u16)
    if matches:
        return matches[-1]
    matches_ascii = re.findall(rb'Aspbo\d+o[A-Z0-9]+\$[UX]', window)
    if matches_ascii:
        return matches_ascii[-1].decode()
    return ''


def safe_filename(s: str) -> str:
    return re.sub(r'[^A-Za-z0-9._-]', '_', s) or 'unknown'


# ---------------------------------------------------------------------------
# Résolution nom de section → code ST
# ---------------------------------------------------------------------------

def find_section_metadata_positions(data: bytes, names: set[str]) -> list[tuple[int, str]]:
    """Positions où un nom de section apparaît en tant qu'en-tête (hors XML).

    Chaque section (Trans_1, Timer, TrD1D2…) est référencée deux fois dans la base :
    - dans le XML du grafcet sous la forme <sectionName>NOM</sectionName>
    - en tant qu'en-tête de la section elle-même, juste avant son code ST
    """
    results: list[tuple[int, str]] = []
    # Tri par longueur décroissante pour que les noms imbriqués (Timer ⊂ Timer2)
    # soient filtrés via la vérification du caractère suivant.
    for name in sorted(names, key=len, reverse=True):
        u16 = name.encode('utf-16-le')
        for m in re.finditer(re.escape(u16), data):
            pos = m.start()
            end = pos + len(u16)
            # Évite de matcher Timer dans Timer2
            if end + 2 <= len(data):
                try:
                    next_ch = data[end:end + 2].decode('utf-16-le')
                    if next_ch and (next_ch.isalnum() or next_ch == '_'):
                        continue
                except UnicodeDecodeError:
                    pass
            # Écarte les références XML (<sectionName>...</...>, <variableName>...)
            prefix = data[max(0, pos - 40):pos].decode('utf-16-le', errors='replace')
            if 'sectionName' in prefix or 'variableName' in prefix:
                continue
            results.append((pos, name))
    results.sort()
    return results


def resolve_section_names(data: bytes, st_blocks: list[dict], candidate_names: set[str]) -> None:
    """Annote chaque bloc ST avec le nom de section dont l'en-tête le précède (proximité)."""
    meta = find_section_metadata_positions(data, candidate_names)
    for st in st_blocks:
        best: tuple[int, str] | None = None
        for meta_pos, meta_name in meta:
            if meta_pos > st['pos']:
                break
            dist = st['pos'] - meta_pos
            if dist > SECTION_META_MAX_DIST:
                continue
            if best is None or dist < best[0]:
                best = (dist, meta_name)
        st['section_name'] = best[1] if best else None


def _step_before_transition(chart: dict, t: dict) -> str | None:
    """Nom de l'étape qui précède (sur la même colonne) cette transition."""
    tx, ty = t['x'], t['y']
    candidates = [s for s in chart['steps']
                  if s.get('x') == tx and s.get('y') is not None and s['y'] < ty]
    if not candidates:
        return None
    return max(candidates, key=lambda s: s['y'])['name']


def resolve_sections_for_chart(chart: dict, sfc_pos: int,
                               st_blocks: list[dict]) -> dict[str, str]:
    """Associe chaque section référencée par un grafcet à un code ST.

    Stratégies combinées :
    1. Correspondance sémantique : si la transition quitte l'étape S, on cherche un
       ST mentionnant S.t ; les conditions initiales du grafcet (après l'étape
       initiale) sont rapprochées d'un ST mentionnant une variable d'entrée.
    2. Le ST retenu est celui dont la position est la plus proche de celle
       du grafcet dans la base binaire (un programme regroupe ses blocs).
    """
    result: dict[str, str] = {}
    used: set[int] = set()  # positions des ST déjà attribués (pour éviter les doublons)

    # Étape initiale (pour repérer les transitions « d'entrée »)
    init_names = {s['name'] for s in chart['steps'] if s['type'] == 'initialStep'}

    transitions = [t for t in chart['transitions'] if t.get('section')]
    # On traite en priorité les transitions les plus spécifiques (celles qui
    # quittent une étape connue) puis les autres
    def specificity(t):
        prev = _step_before_transition(chart, t)
        return 0 if prev and prev not in init_names else 1
    transitions.sort(key=specificity)

    for t in transitions:
        name = t['section']
        if name in result:
            continue
        prev_step = _step_before_transition(chart, t)

        def score(st):
            s = st['src']
            # Exclure les ST déjà retenus (pour les sections à noms identiques dans
            # plusieurs programmes, comme Timer/Timer2 dans F1 et A1_POST)
            if st['pos'] in used:
                return None
            match = 0
            # Critère 1 : ST mentionne l'étape source
            if prev_step and re.search(rf'\b{re.escape(prev_step)}\.t\b', s):
                match += 100
            elif prev_step and prev_step not in init_names and prev_step in s:
                match += 20
            # Critère 2 : pour les transitions nommées TrXY, le ST mentionne X
            m = re.fullmatch(r'Tr([A-Z]\d?)([A-Z]\d?)', name)
            if m:
                src_step, dst_step = m.group(1), m.group(2)
                if re.search(rf'\b{src_step}\.t\b', s):
                    match += 50
                # TrD2A5 typiquement : passage de diagnostic → évacuation, condition complexe
                if src_step == 'D2' and 'Reset' in s and 'Stop' in s:
                    match += 80
                if src_step == 'D1' and 'Power' in s and 'Reset' not in s:
                    match += 80
                if src_step == 'A1' and ('xDefaut' in s or 'Defaut' in s):
                    match += 80
            # Critère 3 : transitions d'entrée -> guichet/variables capteurs
            if prev_step in init_names and 'guichet' in s:
                match += 30
                # Différencie Trans_1 (NOT nixDgt) et Trans_2 (nixDgt)
                if name.endswith('_1') and 'NOT' in s:
                    match += 20
                if name.endswith('_2') and 'NOT' not in s and 'Dgt' in s:
                    match += 20
            # Critère 4 : proximité positionnelle dans la base binaire
            dist = abs(st['pos'] - sfc_pos)
            match += max(0, 50 - dist // 5000)
            return match

        scored = [(score(st), st) for st in st_blocks]
        scored = [(s, st) for s, st in scored if s is not None and s > 0]
        if not scored:
            continue
        scored.sort(key=lambda x: -x[0])
        best_score, best_st = scored[0]
        result[name] = best_st['src']
        used.add(best_st['pos'])

    return result


# ---------------------------------------------------------------------------
# Grafcet (SFC) : analyse tolérante + inférence de positions manquantes
# ---------------------------------------------------------------------------

_STEP_RE = re.compile(
    r'<step\s+stepType="(?P<type>\w+)"\s+stepName="(?P<name>[^"]*)"\s+stepID="(?P<id>[^"]*)"'
    r'(?:[^<]*<objPosition\s+posX="(?P<x>[^"]*)"\s+posY="(?P<y>[^"]*)"\s*/>)?',
    re.DOTALL)
_TRANS_RE = re.compile(
    r'<transition>\s*<objPosition\s+posX="(?P<x>[^"]*)"\s+posY="(?P<y>[^"]*)"\s*/>\s*'
    r'<transitionCondition\s+invertLogic="(?P<inv>[^"]*)"\s*>(?P<cond>.*?)</transitionCondition>',
    re.DOTALL)
_ALT_RE = re.compile(
    r'<(?P<tag>altBranch|altJoint)\s+width="(?P<w>[^"]*)"[^>]*>\s*'
    r'<objPosition\s+posX="(?P<x>[^"]*)"\s+posY="(?P<y>[^"]*)"\s*/>',
    re.DOTALL)
_LINK_RE = re.compile(r'<linkSFC>(?P<body>.*?)</linkSFC>', re.DOTALL)
_LINK_SRC_RE = re.compile(
    r'<directedLinkSource\s+objectType="(?P<t>[^"]*)"\s*>\s*'
    r'<objPosition\s+posX="(?P<x>[^"]*)"\s+posY="(?P<y>[^"]*)"\s*/>', re.DOTALL)
_LINK_DST_RE = re.compile(
    r'<directedLinkDestination\s+objectType="(?P<t>[^"]*)"\s*>\s*'
    r'<objPosition\s+posX="(?P<x>[^"]*)"\s+posY="(?P<y>[^"]*)"\s*/>', re.DOTALL)
_GRID_RE = re.compile(
    r'<gridObjPosition\s+posX="(?P<x>[^"]*)"\s+posY="(?P<y>[^"]*)"\s*/>')


def parse_sfc(xml_text: str) -> dict | None:
    chart: dict = {'steps': [], 'transitions': [], 'branches': [], 'links': []}

    for m in _STEP_RE.finditer(xml_text):
        chart['steps'].append({
            'type': m['type'], 'name': m['name'], 'id': m['id'],
            'x': float(m['x']) if m['x'] is not None else None,
            'y': float(m['y']) if m['y'] is not None else None,
            'inferred': False,
        })

    for m in _TRANS_RE.finditer(xml_text):
        cond = m['cond']
        section = re.search(r'<sectionName>([^<]*)</sectionName>', cond)
        var = re.search(r'<variableName>([^<]*)</variableName>', cond)
        chart['transitions'].append({
            'x': float(m['x']), 'y': float(m['y']),
            'section': section.group(1) if section else None,
            'variable': var.group(1) if var else None,
            'invert': m['inv'] == 'true',
        })

    for m in _ALT_RE.finditer(xml_text):
        chart['branches'].append({
            'kind': 'alt_open' if m['tag'] == 'altBranch' else 'alt_close',
            'width': int(m['w']),
            'x': float(m['x']), 'y': float(m['y']),
        })

    for link_match in _LINK_RE.finditer(xml_text):
        body = link_match['body']
        src = _LINK_SRC_RE.search(body)
        dst = _LINK_DST_RE.search(body)
        if not (src and dst):
            continue
        grid = [(float(g['x']), float(g['y'])) for g in _GRID_RE.finditer(body)]
        chart['links'].append({
            'src_type': src['t'], 'src_x': float(src['x']), 'src_y': float(src['y']),
            'dst_type': dst['t'], 'dst_x': float(dst['x']), 'dst_y': float(dst['y']),
            'grid': grid,
        })

    if not chart['steps'] and not chart['transitions']:
        return None
    return chart


def infer_missing_step_positions(chart: dict) -> None:
    """Déduit la position d'une étape manquante à partir des transitions voisines.

    Stratégie : si une transition porte le nom `Tr<autre><etape>` ou `Tr<etape><autre>`,
    elle borde l'étape par le haut ou le bas. L'étape se place entre les deux.
    """
    for step in chart['steps']:
        if step['x'] is not None and step['y'] is not None:
            continue
        name = step['name']
        if not name:
            continue

        before: tuple[float, float] | None = None  # transition vers cette étape
        after: tuple[float, float] | None = None   # transition au départ de cette étape

        esc = re.escape(name)
        for t in chart['transitions']:
            sect = t.get('section')
            if not sect:
                continue
            if re.fullmatch(rf'Tr(.+?){esc}', sect):
                before = (t['x'], t['y'])
            elif re.fullmatch(rf'Tr{esc}(.+)', sect):
                after = (t['x'], t['y'])

        if before and after:
            step['x'], step['y'] = before[0], (before[1] + after[1]) / 2.0
        elif before:
            step['x'], step['y'] = before[0], before[1] + 1.0
        elif after:
            step['x'], step['y'] = after[0], after[1] - 1.0
        else:
            continue
        step['inferred'] = True


# ---------------------------------------------------------------------------
# Rendu texte
# ---------------------------------------------------------------------------

def _pos_str(obj: dict) -> str:
    if obj.get('x') is None or obj.get('y') is None:
        return 'pos=(?,?)'
    tag = ' *' if obj.get('inferred') else ''
    return f"pos=({obj['x']:.1f},{obj['y']:.1f}){tag}"


def sfc_to_text(chart: dict, name: str, section_map: dict[str, str] | None = None) -> str:
    section_map = section_map or {}
    lines = [f'Grafcet : {name}', '=' * 60, '']

    lines.append('ÉTAPES')
    steps_sorted = sorted(chart['steps'],
                          key=lambda z: (z['y'] if z['y'] is not None else 1e9,
                                         z['x'] if z['x'] is not None else 1e9))
    for s in steps_sorted:
        mark = '(*)' if s['type'] == 'initialStep' else '   '
        lines.append(f"  {mark} {s['name']:<15}  id={s['id']:<8}  {_pos_str(s)}")

    lines += ['', 'TRANSITIONS']
    for t in sorted(chart['transitions'], key=lambda z: (z['y'], z['x'])):
        kind = 'section' if t['section'] else 'variable'
        marker = '¬' if t['invert'] else ' '
        label = t['section'] or t['variable'] or '?'
        extra = ''
        if t['section'] and t['section'] in section_map:
            resolved = section_map[t['section']].replace('\n', ' ').strip()
            extra = f'   →  {resolved}'
        lines.append(f"  {_pos_str(t)}  [{kind}] {marker}{label}{extra}")

    if chart['branches']:
        lines += ['', 'DIVERGENCES / CONVERGENCES']
        for b in chart['branches']:
            lines.append(f"  {b['kind']:<9} {_pos_str(b)}  largeur={b['width']}")

    if chart['links']:
        lines += ['', 'LIAISONS (sauts / retours)']
        for l in chart['links']:
            lines.append(f"  {l['src_type']}({l['src_x']:.1f},{l['src_y']:.1f}) "
                         f"→ {l['dst_type']}({l['dst_x']:.1f},{l['dst_y']:.1f})")
    if section_map:
        lines += ['', 'RÉSOLUTION DES SECTIONS DE TRANSITION']
        for sect_name, src in sorted(section_map.items()):
            lines.append(f"  {sect_name} :  {src.replace(chr(10), ' ')}")
    return '\n'.join(lines) + '\n'


# ---------------------------------------------------------------------------
# Rendu TikZ
# ---------------------------------------------------------------------------

def _escape_tex(s: str) -> str:
    repl = {
        '\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$',
        '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}',
        '~': r'\textasciitilde{}', '^': r'\textasciicircum{}',
    }
    out = ''.join(repl.get(c, c) for c in s)
    out = out.replace('>=', r'$\geq$').replace('<=', r'$\leq$')
    return out


def _format_transition_label(t: dict, section_map: dict[str, str]) -> str:
    if t['variable']:
        raw = t['variable']
    elif t['section']:
        resolved = section_map.get(t['section'])
        if resolved:
            # Compactage : une seule ligne + espaces condensés
            raw = re.sub(r'\s+', ' ', resolved).strip()
        else:
            raw = t['section']
    else:
        raw = '?'
    tex = _escape_tex(raw)
    if t.get('invert'):
        tex = r'$\overline{\mbox{' + tex + r'}}$'
    return tex


def sfc_to_tikz(chart: dict, name: str, section_map: dict[str, str] | None = None) -> str:
    section_map = section_map or {}

    hdr = (
        r'\documentclass[tikz,border=5mm]{standalone}' + '\n'
        r'\usepackage{tikz}' + '\n'
        r'\usetikzlibrary{arrows.meta,positioning}' + '\n'
        r'\begin{document}' + '\n'
        f'% Grafcet : {name}\n'
        r'\begin{tikzpicture}[' + '\n'
        r'  sfcstep/.style   = {draw, fill=white, rounded corners=1pt,'
        r' minimum width=18mm, minimum height=8mm, inner sep=2pt,'
        r' font=\small},' + '\n'
        r'  sfcinit/.style   = {draw, double, fill=white, rounded corners=1pt,'
        r' minimum width=18mm, minimum height=8mm, inner sep=2pt,'
        r' font=\small},' + '\n'
        r'  sfctrans/.style  = {draw, fill=white, line width=0.8pt,'
        r' minimum width=8mm, minimum height=1.2mm, inner sep=0pt},' + '\n'
        r'  sfcbranch/.style = {line width=1.4pt},' + '\n'
        r'  sfclink/.style   = {->, >=Stealth, line width=0.7pt},' + '\n'
        r'  x=18mm, y=-14mm,' + '\n'
        r']' + '\n'
    )
    draws: list[str] = []
    nodes: list[str] = []

    placed_steps = [s for s in chart['steps']
                    if s['x'] is not None and s['y'] is not None]
    placed_trans = chart['transitions']

    # Détermine la colonne à laquelle appartient chaque transition en OU,
    # afin de choisir le côté du libellé (droite pour la colonne la plus à gauche,
    # gauche pour les suivantes) — évite le chevauchement des étiquettes.
    columns_used = sorted({t['x'] for t in placed_trans})
    left_x = columns_used[0] if columns_used else 0.0
    right_x = columns_used[-1] if columns_used else 0.0

    # Les barres de divergence / convergence OU sont au niveau y des transitions.
    # Pour ne pas chevaucher ces transitions, on décale chaque barre de ±0.35 unit.
    branch_y_offset_by_kind = {'alt_open': -0.35, 'alt_close': +0.35}

    # 1) Liaisons verticales implicites entre objets d'une même colonne.
    #    On relie chaque paire y_i -> y_{i+1} SAUF lorsque la branche de divergence
    #    ajoute un segment au-dessus/au-dessous de la transition concernée.
    branch_by_y = {b['y']: b['kind'] for b in chart['branches']}
    by_column: dict[float, list[float]] = defaultdict(list)
    for s in placed_steps:
        by_column[s['x']].append(s['y'])
    for t in placed_trans:
        by_column[t['x']].append(t['y'])
    for x, ys in by_column.items():
        ys = sorted(set(ys))
        for y1, y2 in zip(ys, ys[1:]):
            # Si y1 ou y2 correspond à une transition en divergence/convergence,
            # on raccourcit le trait pour laisser la place à la barre.
            y_start, y_end = y1, y2
            if branch_by_y.get(y1) == 'alt_open':
                y_start = y1 - 0.35  # barre alt_open au-dessus → décale le départ
            if branch_by_y.get(y2) == 'alt_close':
                y_end = y2 + 0.35    # barre alt_close en dessous → décale l'arrivée
            draws.append(f"  \\draw ({x:.2f},{y_start:.2f}) -- ({x:.2f},{y_end:.2f});")

    # 2) Divergences / convergences : barre horizontale double, décalée en y
    for b in chart['branches']:
        w = max(b['width'], 1)
        offset = branch_y_offset_by_kind.get(b['kind'], 0.0)
        y = b['y'] + offset
        x0, x1 = b['x'] - 0.5 * w, b['x'] + 0.5 * w
        draws.append(f"  \\draw[sfcbranch] ({x0:.2f},{y-0.03:.2f}) -- ({x1:.2f},{y-0.03:.2f});")
        draws.append(f"  \\draw[sfcbranch] ({x0:.2f},{y+0.03:.2f}) -- ({x1:.2f},{y+0.03:.2f});")
        # Petits embranchements de la barre vers chaque colonne utilisée en OU
        for col in columns_used:
            if x0 - 0.01 <= col <= x1 + 0.01:
                if b['kind'] == 'alt_open':
                    draws.append(f"  \\draw ({col:.2f},{b['y']+offset+0.03:.2f}) -- ({col:.2f},{b['y']:.2f});")
                else:
                    draws.append(f"  \\draw ({col:.2f},{b['y']:.2f}) -- ({col:.2f},{b['y']+offset-0.03:.2f});")

    # 3) Liaisons explicites (sauts / retours)
    for l in chart['links']:
        path = [f"({l['src_x']:.2f},{l['src_y']:.2f})"]
        path += [f"({gx:.2f},{gy:.2f})" for gx, gy in l['grid']]
        path += [f"({l['dst_x']:.2f},{l['dst_y']:.2f})"]
        draws.append(r"  \draw[sfclink] " + ' -- '.join(path) + ';')

    # 4) Étapes (dessinées par-dessus les traits grâce à fill=white)
    for s in placed_steps:
        style = 'sfcinit' if s['type'] == 'initialStep' else 'sfcstep'
        nid = f"s{s['id']}" if s['id'] else safe_filename(s['name'])
        label = _escape_tex(s['name'])
        if s.get('inferred'):
            label = label + r'\,\scriptsize(*)'
        nodes.append(f"  \\node[{style}] ({nid}) at ({s['x']:.2f},{s['y']:.2f}) {{{label}}};")

    # 5) Transitions : le libellé va à droite pour la colonne la plus à gauche,
    #    à gauche pour toute autre colonne (évite le chevauchement en divergence OU).
    for i, t in enumerate(placed_trans):
        tex = _format_transition_label(t, section_map)
        side = 'right' if t['x'] == left_x else 'left'
        nodes.append(f"  \\node[sfctrans,label={{{side}:\\footnotesize {tex}}}] "
                     f"(t{i}) at ({t['x']:.2f},{t['y']:.2f}) {{}};")

    body = hdr + '\n'.join(draws) + '\n' + '\n'.join(nodes) + '\n'
    # Légende pour les étapes inférées
    if any(s.get('inferred') for s in placed_steps):
        body += (r'  \node[anchor=north west, font=\scriptsize, align=left]'
                 r' at (current bounding box.south west)'
                 r' {(*)~position reconstruite par inférence};' + '\n')
    body += r'\end{tikzpicture}' + '\n' + r'\end{document}' + '\n'
    return body


# ---------------------------------------------------------------------------
# Pipeline principal
# ---------------------------------------------------------------------------

def extract(stu_path: Path, out_dir: Path) -> None:
    print(f'→ {stu_path.name}  =>  {out_dir}')
    out_dir.mkdir(parents=True, exist_ok=True)

    tmp = extract_archive(stu_path)
    try:
        asprog = tmp / 'ASPROG.db'
        if not asprog.exists():
            sys.exit(f'Erreur : ASPROG.db introuvable dans {stu_path}')
        data = asprog.read_bytes()

        # ---- Passe 1 : collecte des blocs ST bruts ---------------------
        st_blocks: list[dict] = []
        for pos, text in iter_utf16_blocks(data, '<STExchangeFile>', '</STExchangeFile>'):
            text = clean_printable_ascii(text)
            m = re.search(r'<STSource>(.*?)</STSource>', text, re.DOTALL)
            if not m:
                continue
            src = (m.group(1)
                   .replace('&gt;', '>').replace('&lt;', '<')
                   .replace('&amp;', '&').strip())
            st_blocks.append({
                'pos': pos,
                'src': src,
                'prog': find_nearest_program(data, pos),
                'sid': find_section_id(data, pos),
                'section_name': None,
            })

        # ---- Passe 2 : analyse des grafcets ----------------------------
        sfc_entries: list[dict] = []
        for pos, text in iter_utf16_blocks(data, '<SFCExchangeFile>', '</SFCExchangeFile>'):
            clean = clean_printable_ascii(text)
            chart = parse_sfc(clean)
            if chart is None:
                continue
            infer_missing_step_positions(chart)
            sfc_entries.append({
                'pos': pos,
                'xml': clean,
                'chart': chart,
                'prog': find_nearest_program(data, pos),
                'sid': find_section_id(data, pos),
            })

        # ---- Résolution des noms de section référencés par les grafcets -----
        candidate_names = {t['section'] for e in sfc_entries
                           for t in e['chart']['transitions'] if t['section']}
        # Première passe : proximité des en-têtes binaires (annote les ST)
        resolve_section_names(data, st_blocks, candidate_names)
        # Seconde passe : par grafcet, appariement sémantique + proximité
        for e in sfc_entries:
            e['section_map'] = resolve_sections_for_chart(
                e['chart'], e['pos'], st_blocks)

        # ---- Écriture des ST ------------------------------------------
        st_dir = out_dir / 'st'
        st_dir.mkdir(exist_ok=True)
        for idx, st in enumerate(st_blocks, 1):
            tag = (safe_filename(st['section_name']) if st['section_name']
                   else safe_filename(st['sid']) if st['sid']
                   else safe_filename(st['prog']))
            fname = f'{idx:02d}_{tag}.st'
            header = [
                f'(* Section        : {st["section_name"] or "?"}',
                f'   Id interne     : {st["sid"] or "?"}',
                f'   Programme      : {st["prog"]}',
                f'   Offset binaire : {st["pos"]} *)',
                '',
            ]
            (st_dir / fname).write_text('\n'.join(header) + st['src'] + '\n', encoding='utf-8')
        print(f'   ST  : {len(st_blocks):2d} section(s) -> st/')

        # ---- Écriture des grafcets ------------------------------------
        sfc_dir = out_dir / 'sfc'
        sfc_dir.mkdir(exist_ok=True)
        for idx, e in enumerate(sfc_entries, 1):
            tag = safe_filename(e['sid']) if e['sid'] else safe_filename(e['prog'])
            base = f'{idx:02d}_{tag}'
            label = f"{e['prog']} ({e['sid']})" if e['sid'] else e['prog']

            (sfc_dir / f'{base}.sfc.xml').write_text(e['xml'], encoding='utf-8')
            (sfc_dir / f'{base}.txt').write_text(
                sfc_to_text(e['chart'], label, e['section_map']), encoding='utf-8')
            (sfc_dir / f'{base}.tex').write_text(
                sfc_to_tikz(e['chart'], label, e['section_map']), encoding='utf-8')
        print(f'   SFC : {len(sfc_entries):2d} grafcet(s) -> sfc/')

        # ---- Résumé ----------------------------------------------------
        readme = out_dir / 'README.md'
        with readme.open('w', encoding='utf-8') as f:
            f.write(f'# Extraction de `{stu_path.name}`\n\n')
            f.write(f'Source : `{stu_path}`\n\n')

            f.write('## Sections Structured Text\n\n')
            if st_blocks:
                f.write('| # | Fichier | Section | Aspbo | Prog. voisin | Aperçu |\n')
                f.write('|---|---------|---------|-------|--------------|--------|\n')
                for idx, st in enumerate(st_blocks, 1):
                    tag = (safe_filename(st['section_name']) if st['section_name']
                           else safe_filename(st['sid']) if st['sid']
                           else safe_filename(st['prog']))
                    fn = f'{idx:02d}_{tag}.st'
                    preview = st['src'].splitlines()[0][:55].replace('|', r'\|')
                    f.write(f"| {idx:02d} | `st/{fn}` | `{st['section_name'] or '-'}` "
                            f"| `{st['sid'] or '-'}` | `{st['prog']}` | `{preview}` |\n")
            else:
                f.write('_Aucune section ST détectée._\n')

            f.write('\n## Grafcets\n\n')
            if sfc_entries:
                f.write('| # | Fichier | Aspbo | Prog. voisin | Étapes | Transitions |\n')
                f.write('|---|---------|-------|--------------|--------|-------------|\n')
                for idx, e in enumerate(sfc_entries, 1):
                    tag = safe_filename(e['sid']) if e['sid'] else safe_filename(e['prog'])
                    base = f'{idx:02d}_{tag}'
                    f.write(f"| {idx:02d} | `sfc/{base}.*` | `{e['sid'] or '-'}` "
                            f"| `{e['prog']}` | {len(e['chart']['steps'])} "
                            f"| {len(e['chart']['transitions'])} |\n")
            else:
                f.write('_Aucun grafcet détecté._\n')
        print(f'   Résumé -> {readme}')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(f'Usage : {sys.argv[0]} <fichier.STU> [dossier_sortie]')
    stu_path = Path(sys.argv[1]).resolve()
    if not stu_path.exists():
        sys.exit(f'Erreur : {stu_path} introuvable')
    out_dir = (Path(sys.argv[2]) if len(sys.argv) > 2
               else Path.cwd() / stu_path.stem).resolve()
    extract(stu_path, out_dir)


if __name__ == '__main__':
    main()
