from PIL import Image, ImageDraw, ImageFont
import os

def criar_icone(size, path):
    img = Image.new('RGB', (size, size), '#0a0a1a')
    draw = ImageDraw.Draw(img)
    # fundo circular vermelho
    m = size // 10
    draw.ellipse([m, m, size-m, size-m], fill='#c0000a')
    # faixa
    cy = size // 2
    h = size // 12
    draw.rectangle([size//6, cy-h, size*5//6, cy+h], fill='#f5f5f5')
    # letra O
    fs = size // 3
    draw.text((size//2, size//2), 'O', fill='#0a0a1a', anchor='mm')
    img.save(path)
    print(f"Icone {size}x{size} criado")

try:
    criar_icone(192, '/home/claude/olivia-app/icon-192.png')
    criar_icone(512, '/home/claude/olivia-app/icon-512.png')
except Exception as e:
    print(f"PIL nao disponivel: {e}")
    # cria PNGs minimos validos via bytes
    import struct, zlib

    def png_minimal(size, path):
        def chunk(t, d):
            c = struct.pack('>I', len(d)) + t + d
            return c + struct.pack('>I', zlib.crc32(c[4:]) & 0xffffffff)
        
        sig = b'\x89PNG\r\n\x1a\n'
        ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0))
        
        # pixels vermelhos simples
        row = b'\x00' + b'\xc0\x00\x0a' * size
        raw = row * size
        idat = chunk(b'IDAT', zlib.compress(raw))
        iend = chunk(b'IEND', b'')
        
        with open(path, 'wb') as f:
            f.write(sig + ihdr + idat + iend)
        print(f"PNG {size}x{size} criado")
    
    png_minimal(192, '/home/claude/olivia-app/icon-192.png')
    png_minimal(512, '/home/claude/olivia-app/icon-512.png')
