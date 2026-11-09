#!/usr/bin/env python3
"""Monta o PDF de entrega ao cliente a partir de um manifesto JSON + PNGs.

Uso (raiz do MCPs):

  python3 scripts/montar-pdf-entrega-cliente.py \\
    --chamado "chamados/08112026222201 - operatta - gedore - Atualizações Gedore 06.11" \\
    --ambiente local \\
    --manifest evidencia/entrega-local/manifest.json

O manifesto é relativo à pasta do chamado (ou path absoluto).
Requer: reportlab + pillow (instala num venv se faltarem).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import venv
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VENV_DIR = Path("/tmp/mcps-entrega-pdf-venv")


def ensure_deps() -> Path:
    """Devolve o interpretador com reportlab+pillow."""
    py = VENV_DIR / "bin" / "python"
    if not py.exists():
        venv.create(VENV_DIR, with_pip=True)
        subprocess.check_call(
            [str(py), "-m", "pip", "install", "-q", "reportlab", "pillow"],
        )
    else:
        try:
            subprocess.check_call(
                [str(py), "-c", "import reportlab,PIL"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            subprocess.check_call(
                [str(py), "-m", "pip", "install", "-q", "reportlab", "pillow"],
            )
    return py


MANIFEST_SCHEMA_HINT = """
{
  "titulo": "Atualizações Gedore — 06/11",
  "subtitulo": "Relatório de entrega com evidências de teste",
  "cliente": "Gedore",
  "produto": "Operatta",
  "chamado": "08112026222201",
  "ambiente": "local",
  "url_base": "http://localhost:5173",
  "resumo_intro": "Texto curto para a capa…",
  "entregas": [
    {"id": "1", "titulo": "Admin redefine senha", "status": "Entregue"}
  ],
  "contexto": ["Bullet opcional…"],
  "nao_mudou": ["Bullet opcional…"],
  "secoes": [
    {
      "titulo": "Entrega 1 — …",
      "pedido": "O que o cliente pediu.",
      "como_ficou": "O que foi implementado.",
      "evidencia_nota": "O que a figura mostra.",
      "figura": "a1-users-nova-senha.png",
      "legenda": "Figura 1 — …"
    }
  ],
  "resumo_cliente": ["Bullet final…"],
  "referencias": [
    ["Item", "Detalhe"],
    ["Chamado", "0811…"]
  ],
  "rodape": "Operatta · Atualizações Gedore 06.11 · Entrega"
}
""".strip()


def resolve_chamado(raw: str) -> Path:
    p = Path(raw)
    if not p.is_absolute():
        p = (ROOT / p).resolve()
    if not p.is_dir():
        raise SystemExit(f"Pasta do chamado não encontrada: {p}")
    return p


def sanitize_filename(text: str) -> str:
    import unicodedata

    # ASCII-ish names travel better in e-mail / Windows
    norm = unicodedata.normalize("NFKD", text.strip())
    ascii_text = "".join(ch for ch in norm if not unicodedata.combining(ch))
    out = []
    for ch in ascii_text:
        if ch.isalnum() or ch in ".-_":
            out.append(ch)
        elif ch in " /":
            out.append("-")
    s = "".join(out).strip("-")
    while "--" in s:
        s = s.replace("--", "-")
    return s or "Entrega"


def build_pdf(chamado_dir: Path, ambiente: str, manifest_path: Path, out_path: Path | None) -> Path:
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    evid_dir = manifest_path.parent

    # Lazy imports after deps
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.colors import HexColor, white
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Image,
        PageBreak,
        Table,
        TableStyle,
        HRFlowable,
    )
    from PIL import Image as PILImage

    BLUE = HexColor("#1e4d8c")
    LIGHT = HexColor("#f4f7fb")
    ACCENT = HexColor("#2563eb")
    MUTED = HexColor("#475569")
    OK = HexColor("#15803d")
    FAIL = HexColor("#b91c1c")
    BORDER = HexColor("#cbd5e1")

    def fit_img(name: str, max_w=170 * mm, max_h=95 * mm):
        if not name:
            return None
        p = evid_dir / name
        if not p.exists():
            raise SystemExit(f"Figura em falta: {p}")
        with PILImage.open(p) as im:
            w, h = im.size
        ratio = min(max_w / w, max_h / h)
        return Image(str(p), width=w * ratio, height=h * ratio)

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=26,
            textColor=BLUE,
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverSub",
            fontName="Helvetica",
            fontSize=12,
            leading=16,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H1",
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=BLUE,
            spaceBefore=10,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H2",
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=HexColor("#0f172a"),
            spaceBefore=8,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            textColor=HexColor("#1e293b"),
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Caption",
            fontName="Helvetica-Oblique",
            fontSize=8.5,
            leading=11,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceBefore=3,
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Meta",
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=MUTED,
            alignment=TA_CENTER,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BulletBody",
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            textColor=HexColor("#1e293b"),
            leftIndent=8,
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Small",
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=MUTED,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Ok",
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=12,
            textColor=OK,
        )
    )

    story = []
    produto = data.get("produto") or "Produto"
    cliente = data.get("cliente") or "Cliente"
    titulo = data.get("titulo") or "Entrega"
    subtitulo = data.get("subtitulo") or "Relatório de entrega com evidências de teste"
    amb = (data.get("ambiente") or ambiente).upper()
    chamado_id = data.get("chamado") or chamado_dir.name.split(" - ")[0]
    url_base = data.get("url_base") or ""

    story.append(Spacer(1, 28 * mm))
    story.append(Paragraph(produto, styles["CoverTitle"]))
    story.append(Paragraph(titulo, styles["CoverTitle"]))
    story.append(Spacer(1, 4 * mm))
    story.append(
        HRFlowable(
            width="60%",
            thickness=1.5,
            color=ACCENT,
            spaceBefore=2,
            spaceAfter=10,
            hAlign="CENTER",
        )
    )
    story.append(Paragraph(subtitulo, styles["CoverSub"]))
    story.append(
        Paragraph(
            f"Cliente: <b>{cliente}</b> &nbsp;·&nbsp; Produto: <b>{produto}</b> &nbsp;·&nbsp; Ambiente: <b>{amb}</b>",
            styles["Meta"],
        )
    )
    if url_base:
        story.append(Paragraph(f"Alvo: {url_base}", styles["Meta"]))
    story.append(
        Paragraph(
            f"Data: {datetime.now().strftime('%d/%m/%Y')} &nbsp;·&nbsp; Chamado: {chamado_id}",
            styles["Meta"],
        )
    )
    story.append(Spacer(1, 12 * mm))

    entregas = data.get("entregas") or []
    if entregas:
        rows = [["#", "Entrega", "Status"]]
        for e in entregas:
            rows.append([str(e.get("id", "")), e.get("titulo", ""), e.get("status", "")])
        t = Table(rows, colWidths=[12 * mm, 120 * mm, 28 * mm])
        style_cmds = [
            ("BACKGROUND", (0, 0), (-1, 0), BLUE),
            ("TEXTCOLOR", (0, 0), (-1, 0), white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8.5),
            ("ALIGN", (0, 0), (0, -1), "CENTER"),
            ("ALIGN", (2, 0), (2, -1), "CENTER"),
            ("BACKGROUND", (0, 1), (-1, -1), LIGHT),
            ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ]
        for i, e in enumerate(entregas, start=1):
            st = (e.get("status") or "").lower()
            color = OK if "entreg" in st or st in {"ok", "passou", "sim"} else (
                FAIL if any(x in st for x in ("falh", "não", "nao", "bloque")) else MUTED
            )
            style_cmds.append(("TEXTCOLOR", (2, i), (2, i), color))
            style_cmds.append(("FONTNAME", (2, i), (2, i), "Helvetica-Bold"))
        t.setStyle(TableStyle(style_cmds))
        story.append(t)
        story.append(Spacer(1, 8 * mm))

    if data.get("resumo_intro"):
        story.append(Paragraph(data["resumo_intro"], styles["Body"]))

    story.append(PageBreak())

    # Contexto
    story.append(Paragraph("1. Contexto e objetivo", styles["H1"]))
    for b in data.get("contexto") or []:
        story.append(Paragraph(f"• {b}", styles["BulletBody"]))
    if data.get("nao_mudou"):
        story.append(Paragraph("O que não mudou", styles["H2"]))
        for b in data["nao_mudou"]:
            story.append(Paragraph(f"• {b}", styles["BulletBody"]))

    # Secções de evidência
    for idx, sec in enumerate(data.get("secoes") or [], start=1):
        story.append(PageBreak())
        story.append(Paragraph(sec.get("titulo") or f"Entrega {idx}", styles["H1"]))
        if sec.get("pedido"):
            story.append(Paragraph(f"<b>Pedido:</b> {sec['pedido']}", styles["Body"]))
        if sec.get("como_ficou"):
            story.append(Paragraph(f"<b>Como ficou:</b> {sec['como_ficou']}", styles["Body"]))
        if sec.get("evidencia_nota"):
            story.append(Paragraph(f"<b>Evidência:</b> {sec['evidencia_nota']}", styles["Ok"]))
        fig = fit_img(sec.get("figura") or "", max_h=100 * mm)
        if fig:
            story.append(fig)
            story.append(Paragraph(sec.get("legenda") or f"Figura {idx}", styles["Caption"]))

    # Resumo
    story.append(PageBreak())
    story.append(Paragraph("Resumo para o cliente", styles["H1"]))
    for b in data.get("resumo_cliente") or []:
        story.append(Paragraph(f"• {b}", styles["BulletBody"]))

    refs = data.get("referencias") or []
    if refs:
        story.append(Spacer(1, 6 * mm))
        story.append(Paragraph("Referências", styles["H1"]))
        tm = Table(refs, colWidths=[40 * mm, 120 * mm])
        tm.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), BLUE),
                    ("TEXTCOLOR", (0, 0), (-1, 0), white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                    ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                    ("BACKGROUND", (0, 1), (-1, -1), LIGHT),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        story.append(tm)

    story.append(Spacer(1, 10 * mm))
    story.append(HRFlowable(width="100%", thickness=0.6, color=BORDER, spaceBefore=4, spaceAfter=8))
    story.append(
        Paragraph(
            data.get("nota_final")
            or (
                "Documento preparado para envio ao cliente. As capturas foram feitas no ambiente indicado; "
                "não inclui segredos nem dumps técnicos."
            ),
            styles["Small"],
        )
    )

    rodape = data.get("rodape") or f"{produto} · {titulo} · Entrega"

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.4)
        canvas.line(18 * mm, 12 * mm, A4[0] - 18 * mm, 12 * mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(18 * mm, 7 * mm, rodape[:90])
        canvas.drawRightString(A4[0] - 18 * mm, 7 * mm, f"{doc.page}")
        canvas.restoreState()

    if out_path is None:
        # Derive from chamado folder name: "<NUM> - <emp> - <cli> - <assunto>"
        parts = [p.strip() for p in chamado_dir.name.split(" - ", 3)]
        assunto = parts[3] if len(parts) == 4 else titulo
        out_name = f"{sanitize_filename(assunto)}-Entrega-{amb}.pdf"
        out_path = chamado_dir / out_name

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=14 * mm,
        bottomMargin=16 * mm,
        title=f"{titulo} — Entrega ({amb})",
        author=f"{produto}",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return out_path


def main() -> None:
    ap = argparse.ArgumentParser(description="Monta PDF de entrega ao cliente a partir do manifesto.")
    ap.add_argument("--chamado", required=True, help="Pasta do chamado (relativa ao MCPs ou absoluta)")
    ap.add_argument("--ambiente", required=True, choices=["local", "dev", "hml", "prd"])
    ap.add_argument("--manifest", required=True, help="Path do manifest.json (relativo ao chamado ou absoluto)")
    ap.add_argument("--out", default=None, help="Path de saída do PDF (opcional)")
    ap.add_argument("--schema", action="store_true", help="Imprime exemplo de manifesto e sai")
    args = ap.parse_args()

    if args.schema:
        print(MANIFEST_SCHEMA_HINT)
        return

    chamado_dir = resolve_chamado(args.chamado)
    manifest = Path(args.manifest)
    if not manifest.is_absolute():
        manifest = (chamado_dir / manifest).resolve()
    if not manifest.is_file():
        raise SystemExit(f"Manifesto não encontrado: {manifest}")

    out = Path(args.out).resolve() if args.out else None

    py = ensure_deps()
    # Re-exec under venv so imports work even if system python is PEP 668
    if Path(sys.executable).resolve() != py.resolve():
        cmd = [str(py), str(Path(__file__).resolve()), *sys.argv[1:]]
        raise SystemExit(subprocess.call(cmd))

    pdf = build_pdf(chamado_dir, args.ambiente, manifest, out)
    print(f"PDF: {pdf}")
    print(f"size_kb: {round(pdf.stat().st_size / 1024, 1)}")


if __name__ == "__main__":
    main()
