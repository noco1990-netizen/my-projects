#!/usr/bin/env python3
"""
背景除去 → 白背景合成スクリプト
使い方: python remove_bg.py 画像1.jpg 画像2.jpg ...
出力: 元ファイル名_white.jpg として保存される
"""
import sys
from pathlib import Path
from rembg import remove
from PIL import Image


def convert_to_white_bg(input_path: str) -> str:
    input_path = Path(input_path)
    output_path = input_path.parent / f"{input_path.stem}_white.jpg"

    print(f"処理中: {input_path.name} ...", end=" ", flush=True)

    with open(input_path, "rb") as f:
        img_data = f.read()

    # 背景除去（RGBA画像として返される）
    removed = remove(img_data)

    # PIL で白背景に合成
    foreground = Image.open(__import__("io").BytesIO(removed)).convert("RGBA")
    background = Image.new("RGBA", foreground.size, (255, 255, 255, 255))
    composite = Image.alpha_composite(background, foreground).convert("RGB")
    composite.save(str(output_path), "JPEG", quality=95)

    print(f"完了 → {output_path.name}")
    return str(output_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python remove_bg.py 画像1.jpg [画像2.jpg ...]")
        sys.exit(1)

    for path in sys.argv[1:]:
        if not Path(path).exists():
            print(f"ファイルが見つかりません: {path}")
            continue
        try:
            convert_to_white_bg(path)
        except Exception as e:
            print(f"エラー ({path}): {e}")
