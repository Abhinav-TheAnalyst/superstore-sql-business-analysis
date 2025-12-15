from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import utils
import json
import os


def draw_image(c, path, x, y, max_width, max_height):
    if not os.path.exists(path):
        return
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    ratio = min(max_width / iw, max_height / ih)
    w = iw * ratio
    h = ih * ratio
    c.drawImage(path, x, y - h, width=w, height=h)


def load_kpis(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def make_pdf(out_path, screenshots_dir):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas
    from reportlab.lib import utils
    from reportlab.lib.colors import HexColor
    import json
    import os


    def draw_image(c, path, x, y, max_width, max_height):
        if not os.path.exists(path):
            return
        img = utils.ImageReader(path)
        iw, ih = img.getSize()
        ratio = min(max_width / iw, max_height / ih)
        w = iw * ratio
        h = ih * ratio
        # center image horizontally within the max_width
        c.drawImage(path, x + (max_width - w) / 2, y - h, width=w, height=h, preserveAspectRatio=True, mask='auto')


    def load_kpis(path):
        if not os.path.exists(path):
            return {}
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)


    def fmt_money(v):
        try:
            return f"{v:,.2f}"
        except Exception:
            return str(v)


    def fmt_pct(v):
        try:
            return f"{v:.1%}"
        except Exception:
            return str(v)


    def make_pdf(out_path, screenshots_dir):
        kpis = load_kpis(os.path.join(screenshots_dir, 'kpis.json'))

        c = canvas.Canvas(out_path, pagesize=A4)
        width, height = A4

        margin = 18 * mm
        content_width = width - 2 * margin

        # Header bar
        header_h = 18 * mm
        c.setFillColor(HexColor('#0B6E4F'))
        c.rect(0, height - header_h, width, header_h, stroke=0, fill=1)
        c.setFillColor(HexColor('#FFFFFF'))
        c.setFont('Helvetica-Bold', 16)
        c.drawString(margin, height - header_h + 5 * mm, 'Superstore — Executive Summary')

        # Subtitle
        c.setFont('Helvetica', 9)
        c.drawString(width - margin - 150 * mm, height - header_h + 6 * mm, 'One-page summary — generated automatically')

        # KPI cards (three across)
        kpi_y = height - header_h - 10 * mm
        card_h = 20 * mm
        gap = 6 * mm
        card_w = (content_width - 2 * gap) / 3
        keys = [
            ('Total sales', 'total_sales'),
            ('Total profit', 'total_profit'),
            ('Average discount', 'avg_discount'),
        ]
        x0 = margin
        for label, key in keys:
            c.setFillColor(HexColor('#F4F6F5'))
            c.roundRect(x0, kpi_y - card_h, card_w, card_h, 3 * mm, fill=1, stroke=0)
            c.setFillColor(HexColor('#0B6E4F'))
            c.setFont('Helvetica-Bold', 10)
            c.drawString(x0 + 4 * mm, kpi_y - 6 * mm, label)
            val = kpis.get(key, '—')
            c.setFont('Helvetica-Bold', 12)
            if isinstance(val, float):
                display = fmt_pct(val) if 'discount' in key else fmt_money(val)
            else:
                display = str(val)
            c.drawRightString(x0 + card_w - 4 * mm, kpi_y - 8 * mm, display)
            x0 += card_w + gap

        # Body: left column summary bullets, right column images
        body_top = kpi_y - card_h - 8 * mm
        left_x = margin
        left_w = content_width * 0.45
        right_x = margin + left_w + 8 * mm
        right_w = content_width - left_w - 8 * mm

        # Summary bullets
        c.setFillColor(HexColor('#000000'))
        c.setFont('Helvetica-Bold', 11)
        c.drawString(left_x, body_top, 'Key insights')
        c.setFont('Helvetica', 10)
        y = body_top - 6 * mm
        bullets = []
        top_regions = kpis.get('top_3_regions_by_profit', [])
        if top_regions:
            bullets.append(f"Top regions by profit: {', '.join(top_regions)}")
        avg_disc = kpis.get('avg_discount')
        if avg_disc is not None:
            bullets.append(f"Average discount: {fmt_pct(avg_disc)}; threshold for negative avg profit ≈ {fmt_pct(kpis.get('discount_threshold_loss', 0))}")
        top_customers = kpis.get('top_10_customers_by_profit', [])
        if top_customers:
            bullets.append('Top customers: ' + ', '.join(top_customers[:5]) + (', ...' if len(top_customers) > 5 else ''))
        bullets.append('Action: tighten high discounts, prioritize top customers, focus merchandising on top products.')

        for b in bullets:
            c.drawString(left_x + 4 * mm, y, '• ' + b)
            y -= 6 * mm

        # Draw a light box around left summary
        box_bottom = y - 4 * mm
        c.setStrokeColor(HexColor('#E6EAE8'))
        c.rect(left_x - 2 * mm, box_bottom, left_w + 4 * mm, body_top - box_bottom, stroke=1, fill=0)

        # Images on right
        img_h = (body_top - box_bottom - 6 * mm) / 3
        imgs = ['profit_by_region.png', 'discount_vs_profit.png', 'top_customers.png']
        img_y = body_top
        for im in imgs:
            path = os.path.join(screenshots_dir, im)
            draw_image(c, path, right_x, img_y, right_w, img_h)
            img_y -= img_h + 6 * mm

        # Footer: contact and note
        c.setFont('Helvetica-Oblique', 8)
        c.setFillColor(HexColor('#666666'))
        c.drawString(margin, 12 * mm, 'Author: Abhinav Verma — https://github.com/Abhinav-TheAnalyst')
        c.save()


    if __name__ == '__main__':
        out = os.path.join('reports', 'superstore_summary.pdf')
        screenshots = os.path.join('dashboard', 'screenshots')
        os.makedirs('reports', exist_ok=True)
        make_pdf(out, screenshots)
        print('WROTE:', out)
