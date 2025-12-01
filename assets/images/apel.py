import math
import cairo

# -------------------------------------------------
# Surface maker
# -------------------------------------------------
def make_surface(filename, w=600, h=600):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)

    # Background transparan (tidak perlu paint apapun)
    # ARGB32 secara default transparan jika tidak di-paint

    return surface, ctx


# -------------------------------------------------
# Draw perfected apple
# -------------------------------------------------
def draw_apple(ctx, cx, cy, scale=1.0):
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(scale, scale)

    # ---------------------------------------
    # BAYANGAN BAWAH APEL
    # ---------------------------------------
    ctx.save()
    ctx.translate(0, 155)
    ctx.scale(1.0, 0.3)
    
    grad_shadow = cairo.RadialGradient(0, 0, 20, 0, 0, 120)
    grad_shadow.add_color_stop_rgba(0, 0, 0, 0, 0.3)
    grad_shadow.add_color_stop_rgba(1, 0, 0, 0, 0)
    
    ctx.set_source(grad_shadow)
    ctx.arc(0, 0, 120, 0, 2 * math.pi)
    ctx.fill()
    ctx.restore()

    # ---------------------------------------
    # BADAN APEL (bentuk lebih natural)
    # ---------------------------------------
    ctx.set_line_width(16)
    ctx.set_line_join(cairo.LineJoin.ROUND)

    # Bentuk apel yang lebih realistis
    ctx.move_to(0, 140)
    ctx.curve_to(-145, 135, -165, -15, -65, -88)
    ctx.curve_to(-25, -135, 25, -135, 65, -88)
    ctx.curve_to(165, -15, 145, 135, 0, 140)

    # Gradient warna apel lebih kompleks
    grad = cairo.RadialGradient(-40, -20, 30, 0, 20, 220)
    grad.add_color_stop_rgb(0, 1.0, 0.35, 0.35)
    grad.add_color_stop_rgb(0.4, 0.95, 0.15, 0.15)
    grad.add_color_stop_rgb(1, 0.70, 0.05, 0.05)

    ctx.set_source(grad)
    ctx.fill_preserve()

    # Outline hitam
    ctx.set_source_rgb(0, 0, 0)
    ctx.stroke()

    # ---------------------------------------
    # CEKUNGAN ATAS (tempat batang)
    # ---------------------------------------
    ctx.save()
    grad_indent = cairo.RadialGradient(0, -95, 5, 0, -95, 25)
    grad_indent.add_color_stop_rgba(0, 0, 0, 0, 0.4)
    grad_indent.add_color_stop_rgba(1, 0, 0, 0, 0)
    
    ctx.set_source(grad_indent)
    ctx.arc(0, -95, 25, 0, 2 * math.pi)
    ctx.fill()
    ctx.restore()

    # ---------------------------------------
    # BATANG (lebih 3D dengan gradient)
    # ---------------------------------------
    ctx.set_line_width(22)
    
    # Shadow batang
    ctx.set_source_rgba(0.15, 0.08, 0.02, 0.5)
    ctx.move_to(5, -98)
    ctx.curve_to(18, -155, -5, -158, 5, -98)
    ctx.stroke()
    
    # Batang utama dengan gradient
    grad_stem = cairo.LinearGradient(-5, -100, 5, -100)
    grad_stem.add_color_stop_rgb(0, 0.25, 0.15, 0.05)
    grad_stem.add_color_stop_rgb(0.5, 0.45, 0.25, 0.10)
    grad_stem.add_color_stop_rgb(1, 0.30, 0.18, 0.06)
    
    ctx.set_source(grad_stem)
    ctx.move_to(0, -100)
    ctx.curve_to(12, -158, -8, -160, 0, -100)
    ctx.stroke()

    # Highlight batang
    ctx.set_line_width(6)
    ctx.set_source_rgba(0.6, 0.4, 0.2, 0.6)
    ctx.move_to(-3, -105)
    ctx.line_to(-4, -145)
    ctx.stroke()

    # ---------------------------------------
    # DAUN (lebih detail dengan tekstur)
    # ---------------------------------------
    ctx.save()
    ctx.translate(48, -125)
    ctx.rotate(-math.radians(18))

    # Shadow daun
    ctx.set_source_rgba(0, 0.2, 0, 0.3)
    ctx.move_to(2, 2)
    ctx.curve_to(72, -28, 112, 2, 92, 42)
    ctx.curve_to(62, 22, 32, 32, 2, 2)
    ctx.fill()

    # Daun utama
    ctx.move_to(0, 0)
    ctx.curve_to(70, -30, 110, 0, 90, 40)
    ctx.curve_to(60, 20, 30, 30, 0, 0)

    leaf = cairo.LinearGradient(0, -10, 90, 50)
    leaf.add_color_stop_rgb(0, 0.15, 0.85, 0.25)
    leaf.add_color_stop_rgb(0.5, 0.08, 0.70, 0.18)
    leaf.add_color_stop_rgb(1, 0.05, 0.50, 0.12)

    ctx.set_source(leaf)
    ctx.fill_preserve()

    # Outline daun
    ctx.set_line_width(8)
    ctx.set_source_rgb(0.02, 0.30, 0.05)
    ctx.stroke()

    # Urat tengah daun
    ctx.set_line_width(5)
    ctx.set_source_rgba(0.05, 0.45, 0.10, 0.8)
    ctx.move_to(5, 2)
    ctx.curve_to(35, 10, 60, 18, 80, 22)
    ctx.stroke()

    # Urat samping kiri atas
    ctx.set_line_width(2.5)
    ctx.set_source_rgba(0.05, 0.40, 0.10, 0.6)
    ctx.move_to(30, 8)
    ctx.curve_to(25, -5, 35, -15, 45, -18)
    ctx.stroke()

    # Urat samping kiri bawah
    ctx.move_to(45, 14)
    ctx.curve_to(40, 22, 42, 28, 52, 30)
    ctx.stroke()

    # Urat samping kanan atas
    ctx.move_to(60, 18)
    ctx.curve_to(68, 10, 78, 8, 88, 12)
    ctx.stroke()

    # Urat samping kanan bawah
    ctx.move_to(68, 21)
    ctx.curve_to(72, 28, 76, 32, 82, 32)
    ctx.stroke()

    # Highlight daun
    ctx.set_source_rgba(1, 1, 1, 0.25)
    ctx.move_to(15, -5)
    ctx.curve_to(50, -20, 80, -10, 75, 5)
    ctx.curve_to(50, 0, 30, 5, 15, -5)
    ctx.fill()

    ctx.restore()

    # ---------------------------------------
    # TEKSTUR HALUS PADA APEL (titik-titik kecil)
    # ---------------------------------------
    ctx.set_source_rgba(0.5, 0.1, 0.1, 0.15)
    import random
    random.seed(42)
    for _ in range(80):
        x = random.uniform(-120, 120)
        y = random.uniform(-80, 120)
        # Cek apakah titik dalam area apel
        if x*x/140**2 + (y-20)**2/140**2 < 0.8:
            ctx.arc(x, y, random.uniform(1, 2.5), 0, 2 * math.pi)
            ctx.fill()

    ctx.restore()


# -------------------------------------------------
# SAVE PNG
# -------------------------------------------------
surface, ctx = make_surface("apel.png")
draw_apple(ctx, 300, 330, 1.3)
surface.write_to_png("apel.png")