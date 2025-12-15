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
    kpis = load_kpis(os.path.join(screenshots_dir, 'kpis.json'))

    c = canvas.Canvas(out_path, pagesize=A4)
    width, height = A4

    margin = 20 * mm
    x = margin
    y = height - margin

    # Title
    c.setFont('Helvetica-Bold', 18)
    c.drawString(x, y, 'Superstore — Executive Summary')
    y -= 10 * mm

    # KPIs
    c.setFont('Helvetica-Bold', 12)
    c.drawString(x, y, 'Key KPIs')
    y -= 6 * mm
    c.setFont('Helvetica', 10)
    keys = [
        ('Total sales', 'total_sales'),
        ('Total profit', 'total_profit'),
        ('Average discount', 'avg_discount'),
        ('Avg profit per order', 'avg_profit_per_order'),
    ]
    for label, key in keys:
        val = kpis.get(key, '—')
        if isinstance(val, float):
            if 'discount' in key:
                display = f"{val:.1%}"
            else:
                display = f"{val:,.2f}"
        else:
            display = str(val)
        c.drawString(x + 4 * mm, y, f"• {label}: {display}")
        y -= 5 * mm

    y -= 3 * mm

    # Top insights
    c.setFont('Helvetica-Bold', 12)
    c.drawString(x, y, 'Top Insights')
    y -= 6 * mm
    c.setFont('Helvetica', 10)
    top_regions = kpis.get('top_3_regions_by_profit', [])
    if top_regions:
        c.drawString(x + 4 * mm, y, f"• Top regions by profit: {', '.join(top_regions)}")
        y -= 5 * mm
    disc_thresh = kpis.get('discount_threshold_loss')
    if disc_thresh is not None:
        c.drawString(x + 4 * mm, y, f"• Discount threshold where avg profit -> negative: {disc_thresh:.0%}")
        y -= 5 * mm
    top_customers = kpis.get('top_10_customers_by_profit', [])
    if top_customers:
        sample = ', '.join(top_customers[:5]) + (', ...' if len(top_customers) > 5 else '')
        c.drawString(x + 4 * mm, y, f"• Top customers: {sample}")
        y -= 5 * mm

    # Draw images on right half
    img_x = width / 2 + 10 * mm
    img_y = height - margin - 10 * mm
    img_w = (width - margin - img_x) - 10 * mm
    img_h = 50 * mm

    images = ['profit_by_region.png', 'discount_vs_profit.png', 'top_customers.png']
    cur_y = img_y
    for im in images:
        path = os.path.join(screenshots_dir, im)
        draw_image(c, path, img_x, cur_y, img_w, img_h)
        cur_y -= img_h + 6 * mm

    # Footer / contact
    c.setFont('Helvetica-Oblique', 9)
    c.drawString(margin, 15 * mm, 'Author: Abhinav Verma — https://github.com/Abhinav-TheAnalyst')
    c.save()


if __name__ == '__main__':
    out = os.path.join('reports', 'superstore_summary.pdf')
    screenshots = os.path.join('dashboard', 'screenshots')
    os.makedirs('reports', exist_ok=True)
    make_pdf(out, screenshots)
    print('WROTE:', out)
