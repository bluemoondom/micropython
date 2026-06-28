from machine import Pin, SPI, PWM
import framebuf
import time
import math
from rp2040lcd import QMI8658

DC   = 8
CS   = 9
SCK  = 10
MOSI = 11
RST  = 12
BL   = 25

class LCD_1inch28(framebuf.FrameBuffer):
    def __init__(self):
        self.width  = 240
        self.height = 240
        self.cs  = Pin(CS,  Pin.OUT)
        self.rst = Pin(RST, Pin.OUT)
        self.cs(1)
        self.spi = SPI(1, 100_000_000, polarity=0, phase=0,
                       sck=Pin(SCK), mosi=Pin(MOSI), miso=None)
        self.dc = Pin(DC, Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(240 * 240 * 2)
        super().__init__(self.buffer, 240, 240, framebuf.RGB565)
        self.init_display()
        self.fill(0)
        self.show()
        self.pwm = PWM(Pin(BL))
        self.pwm.freq(5000)

    def write_cmd(self, cmd):
        self.cs(1); self.dc(0); self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1); self.dc(1); self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def set_bl_pwm(self, duty):
        self.pwm.duty_u16(duty)

    def init_display(self):
        self.rst(1); time.sleep(0.01)
        self.rst(0); time.sleep(0.01)
        self.rst(1); time.sleep(0.05)
        self.write_cmd(0xEF)
        self.write_cmd(0xEB); self.write_data(0x14)
        self.write_cmd(0xFE); self.write_cmd(0xEF)
        self.write_cmd(0xEB); self.write_data(0x14)
        self.write_cmd(0x84); self.write_data(0x40)
        self.write_cmd(0x85); self.write_data(0xFF)
        self.write_cmd(0x86); self.write_data(0xFF)
        self.write_cmd(0x87); self.write_data(0xFF)
        self.write_cmd(0x88); self.write_data(0x0A)
        self.write_cmd(0x89); self.write_data(0x21)
        self.write_cmd(0x8A); self.write_data(0x00)
        self.write_cmd(0x8B); self.write_data(0x80)
        self.write_cmd(0x8C); self.write_data(0x01)
        self.write_cmd(0x8D); self.write_data(0x01)
        self.write_cmd(0x8E); self.write_data(0xFF)
        self.write_cmd(0x8F); self.write_data(0xFF)
        self.write_cmd(0xB6); self.write_data(0x00); self.write_data(0x20)
        self.write_cmd(0x36); self.write_data(0x98)
        self.write_cmd(0x3A); self.write_data(0x05)
        self.write_cmd(0x90)
        self.write_data(0x08); self.write_data(0x08)
        self.write_data(0x08); self.write_data(0x08)
        self.write_cmd(0xBD); self.write_data(0x06)
        self.write_cmd(0xBC); self.write_data(0x00)
        self.write_cmd(0xFF)
        self.write_data(0x60); self.write_data(0x01); self.write_data(0x04)
        self.write_cmd(0xC3); self.write_data(0x13)
        self.write_cmd(0xC4); self.write_data(0x13)
        self.write_cmd(0xC9); self.write_data(0x22)
        self.write_cmd(0xBE); self.write_data(0x11)
        self.write_cmd(0xE1); self.write_data(0x10); self.write_data(0x0E)
        self.write_cmd(0xDF)
        self.write_data(0x21); self.write_data(0x0c); self.write_data(0x02)
        self.write_cmd(0xF0)
        self.write_data(0x45); self.write_data(0x09); self.write_data(0x08)
        self.write_data(0x08); self.write_data(0x26); self.write_data(0x2A)
        self.write_cmd(0xF1)
        self.write_data(0x43); self.write_data(0x70); self.write_data(0x72)
        self.write_data(0x36); self.write_data(0x37); self.write_data(0x6F)
        self.write_cmd(0xF2)
        self.write_data(0x45); self.write_data(0x09); self.write_data(0x08)
        self.write_data(0x08); self.write_data(0x26); self.write_data(0x2A)
        self.write_cmd(0xF3)
        self.write_data(0x43); self.write_data(0x70); self.write_data(0x72)
        self.write_data(0x36); self.write_data(0x37); self.write_data(0x6F)
        self.write_cmd(0xED); self.write_data(0x1B); self.write_data(0x0B)
        self.write_cmd(0xAE); self.write_data(0x77)
        self.write_cmd(0xCD); self.write_data(0x63)
        self.write_cmd(0x70)
        self.write_data(0x07); self.write_data(0x07); self.write_data(0x04)
        self.write_data(0x0E); self.write_data(0x0F); self.write_data(0x09)
        self.write_data(0x07); self.write_data(0x08); self.write_data(0x03)
        self.write_cmd(0xE8); self.write_data(0x34)
        self.write_cmd(0x62)
        self.write_data(0x18); self.write_data(0x0D); self.write_data(0x71)
        self.write_data(0xED); self.write_data(0x70); self.write_data(0x70)
        self.write_data(0x18); self.write_data(0x0F); self.write_data(0x71)
        self.write_data(0xEF); self.write_data(0x70); self.write_data(0x70)
        self.write_cmd(0x63)
        self.write_data(0x18); self.write_data(0x11); self.write_data(0x71)
        self.write_data(0xF1); self.write_data(0x70); self.write_data(0x70)
        self.write_data(0x18); self.write_data(0x13); self.write_data(0x71)
        self.write_data(0xF3); self.write_data(0x70); self.write_data(0x70)
        self.write_cmd(0x64)
        self.write_data(0x28); self.write_data(0x29); self.write_data(0xF1)
        self.write_data(0x01); self.write_data(0xF1); self.write_data(0x00)
        self.write_data(0x07)
        self.write_cmd(0x66)
        self.write_data(0x3C); self.write_data(0x00); self.write_data(0xCD)
        self.write_data(0x67); self.write_data(0x45); self.write_data(0x45)
        self.write_data(0x10); self.write_data(0x00); self.write_data(0x00)
        self.write_data(0x00)
        self.write_cmd(0x67)
        self.write_data(0x00); self.write_data(0x3C); self.write_data(0x00)
        self.write_data(0x00); self.write_data(0x00); self.write_data(0x01)
        self.write_data(0x54); self.write_data(0x10); self.write_data(0x32)
        self.write_data(0x98)
        self.write_cmd(0x74)
        self.write_data(0x10); self.write_data(0x85); self.write_data(0x80)
        self.write_data(0x00); self.write_data(0x00); self.write_data(0x4E)
        self.write_data(0x00)
        self.write_cmd(0x98); self.write_data(0x3e); self.write_data(0x07)
        self.write_cmd(0x35)
        self.write_cmd(0x21)
        self.write_cmd(0x11); time.sleep(0.12)
        self.write_cmd(0x29); time.sleep(0.02)
        self.write_cmd(0x21); self.write_cmd(0x11); self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00); self.write_data(0x00)
        self.write_data(0x00); self.write_data(0xef)
        self.write_cmd(0x2B)
        self.write_data(0x00); self.write_data(0x00)
        self.write_data(0x00); self.write_data(0xEF)
        self.write_cmd(0x2C)
        self.cs(1); self.dc(1); self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)

def colour(R, G, B):
    return (((G & 0b00011100) << 3) + ((B & 0b11111000) >> 3) << 8) \
           + (R & 0b11111000) + ((G & 0b11100000) >> 5)

C_BLACK  = colour(0,   0,   0  )
C_FACE   = colour(8,   10,  15 )
C_EYE_BG = colour(3,   20,  22 )
C_RIM    = colour(0,   155, 148)
C_PUPIL  = colour(0,   200, 195)
C_SHINE  = colour(215, 255, 253)
C_LID    = colour(5,   6,   12 )

def _dx(row, h, r):
    if r <= 0:
        return 0
    if row < r:
        dy = r - row
    elif row >= h - r:
        dy = row - (h - r - 1)
    else:
        return 0
    sq = r * r - dy * dy
    return r - int(math.sqrt(sq)) if sq >= 0 else r


def filled_rrect(x, y, w, h, r, col):
    r = min(r, w // 2, h // 2)
    for row in range(h):
        d = _dx(row, h, r)
        lw = w - 2 * d
        if lw > 0:
            LCD.hline(x + d, y + row, lw, col)


def filled_circle(cx, cy, r, col):
    for dy in range(-r, r + 1):
        a = int(math.sqrt(max(0, r * r - dy * dy)))
        if a > 0:
            LCD.hline(cx - a, cy + dy, 2 * a, col)


def rim_rrect(x, y, w, h, r, col, t=2):
    r  = min(r, w // 2, h // 2)
    ri = max(0, r - t)
    for row in range(h):
        d_out = _dx(row, h, r)
        d_in  = _dx(row, h, ri)

        ol = x + d_out
        or_ = x + w - d_out
        il = x + d_in  + t
        ir = x + w - d_in - t

        if il >= ir:
            lw = or_ - ol
            if lw > 0:
                LCD.hline(ol, y + row, lw, col)
        else:

            lw = il - ol
            if lw > 0:
                LCD.hline(ol, y + row, lw, col)

            lw = or_ - ir
            if lw > 0:
                LCD.hline(ir, y + row, lw, col)


EYE_W  = 80
EYE_H  = 58
EYE_RR = 14
EYE_CY = 120
EYE_LX = 72
EYE_RX = 168

FACE_X = EYE_LX - EYE_W // 2 - 2
FACE_Y = EYE_CY - EYE_H // 2 - 2
FACE_W = (EYE_RX + EYE_W // 2 + 2) - FACE_X
FACE_H = EYE_H + 4


def draw_eye(cx, cy, open_frac, angry_frac, is_left):
    eh = max(4, int(EYE_H * open_frac))
    ey = cy - eh // 2
    ex = cx - EYE_W // 2
    r  = min(EYE_RR, EYE_W // 2, eh // 2)

    filled_rrect(ex, ey, EYE_W, eh, r, C_EYE_BG)

    if open_frac > 0.10:
        pw = EYE_W * 38 // 100
        ph = max(4, eh * 68 // 100)
        px = cx - pw // 2
        py = cy - ph // 2
        pr = min(pw // 2, 8)
        filled_rrect(px, py, pw, ph, pr, C_PUPIL)

        sr = max(2, pw * 22 // 100)
        filled_circle(px + pw * 38 // 100, py + ph * 30 // 100, sr, C_SHINE)

    if angry_frac > 0.02 and eh > 6:
        lid_h = int(eh * 0.52 * angry_frac)
        for row in range(lid_h):
            f       = row / max(1, lid_h - 1)
            d_edge  = _dx(row, eh, r)
            inner_w = EYE_W - 2 * d_edge
            w_lid   = int(inner_w * (1.0 - f * 0.50))
            if is_left:
                x0 = ex + d_edge
            else:
                x0 = ex + d_edge + (inner_w - w_lid)
            if w_lid > 0:
                LCD.hline(x0, ey + row, w_lid, C_LID)

    rim_rrect(ex, ey, EYE_W, eh, r, C_RIM, t=2)


def draw_eyes(open_frac, angry_frac):
    filled_rrect(FACE_X, FACE_Y, FACE_W, FACE_H, 0, C_FACE)
    draw_eye(EYE_LX, EYE_CY, open_frac, angry_frac, True)
    draw_eye(EYE_RX, EYE_CY, open_frac, angry_frac, False)


class _RNG:
    def __init__(self): self._s = 54321
    def randint(self, a, b):
        self._s = (self._s * 1664525 + 1013904223) & 0xFFFFFFFF
        return a + self._s % (b - a + 1)

_rng = _RNG()

blink_phase  = 0
next_blink   = _rng.randint(120, 320)
blink_timer  = 0
angry_level  = 0.0
prev_xyz     = [0.0, 0.0, 0.0]
shake_smooth = 0.0
BLINK_STEPS  = 6


def step_animation(shake_intensity):
    global blink_phase, blink_timer, next_blink, angry_level

    target = min(1.0, shake_intensity * 2.5)
    if target > angry_level:
        angry_level = min(1.0, angry_level + 0.18)
    else:
        angry_level = max(0.0, angry_level - 0.04)

    blink_timer += 1
    if blink_phase == 0:
        if blink_timer >= next_blink and angry_level < 0.25:
            blink_phase = 1
            blink_timer = 0
            next_blink = _rng.randint(120, 320)
    elif blink_phase <= BLINK_STEPS * 2:
        blink_phase += 1
        if blink_phase > BLINK_STEPS * 2:
            blink_phase = 0

    if blink_phase == 0:
        open_frac = 1.0
    elif blink_phase <= BLINK_STEPS:
        open_frac = 1.0 - blink_phase / BLINK_STEPS
    else:
        open_frac = (blink_phase - BLINK_STEPS) / BLINK_STEPS

    return open_frac, angry_level


LCD = LCD_1inch28()
LCD.set_bl_pwm(65535)
LCD.fill(C_BLACK)
LCD.show()

qmi8658 = QMI8658()

while True:
    xyz = qmi8658.Read_XYZ()

    dx = abs(xyz[0] - prev_xyz[0])
    dy = abs(xyz[1] - prev_xyz[1])
    dz = abs(xyz[2] - prev_xyz[2])
    shake_raw    = min(1.0, (dx + dy + dz) * 2.5)
    shake_smooth = shake_smooth * 0.65 + shake_raw * 0.35
    prev_xyz     = list(xyz)

    open_frac, angry_frac = step_animation(shake_smooth)
    draw_eyes(open_frac, angry_frac)
    LCD.show()