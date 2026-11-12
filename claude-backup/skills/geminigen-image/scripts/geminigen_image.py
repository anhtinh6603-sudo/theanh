#!/usr/bin/env python3
import argparse, json, subprocess, time, uuid
from pathlib import Path
from urllib.request import Request, urlopen

ENV_PATH = Path.home() / '.meta-ads' / '.env'
OUT_DIR = Path('/home/openclaw/.openclaw/workspace/.openclaw/generated-images')
API_URL = 'https://api.geminigen.ai/uapi/v1/generate_image'


def load_env():
    data = {}
    for line in ENV_PATH.read_text().splitlines():
        if '=' in line:
            k, v = line.split('=', 1)
            data[k.strip()] = v.strip()
    return data


def fetch_history(api_key, uuid_value):
    cmd = [
        'curl', '-sS', '-X', 'GET', f'https://api.geminigen.ai/uapi/v1/history/{uuid_value}',
        '-H', f'x-api-key: {api_key}',
    ]
    raw = subprocess.check_output(cmd, text=True)
    return json.loads(raw)


def download_file(url, out_format):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ext = '.jpg' if out_format.lower() in ('jpeg', 'jpg') else f'.{out_format.lower()}'
    out = OUT_DIR / f'geminigen-{uuid.uuid4().hex}{ext}'
    subprocess.check_call(['curl', '-L', '-sS', url, '-o', str(out)])
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--prompt', required=True)
    p.add_argument('--model', default='nano-banana-pro')
    p.add_argument('--aspect-ratio', default='16:9')
    p.add_argument('--style', default='Photorealistic')
    p.add_argument('--file-urls')
    p.add_argument('--output-format', default='jpeg')
    p.add_argument('--resolution', default='2K')
    p.add_argument('--wait', action='store_true')
    p.add_argument('--poll-interval', type=int, default=5)
    p.add_argument('--max-wait', type=int, default=180)
    args = p.parse_args()

    env = load_env()
    api_key = env['GEMINIGEN_API_KEY']

    cmd = [
        'curl', '-sS', '-X', 'POST', API_URL,
        '-H', f'x-api-key: {api_key}',
        '-F', f'prompt={args.prompt}',
        '-F', f'model={args.model}',
        '-F', f'aspect_ratio={args.aspect_ratio}',
        '-F', f'style={args.style}',
        '-F', f'output_format={args.output_format}',
        '-F', f'resolution={args.resolution}',
    ]
    if args.file_urls:
        cmd += ['-F', f'file_urls={args.file_urls}']

    raw = subprocess.check_output(cmd, text=True)
    data = json.loads(raw)
    if not args.wait:
        print(json.dumps(data, ensure_ascii=False))
        return

    uuid_value = data.get('uuid')
    if not uuid_value:
        print(json.dumps(data, ensure_ascii=False))
        return

    deadline = time.time() + args.max_wait
    last = data
    while time.time() < deadline:
        time.sleep(args.poll_interval)
        found = fetch_history(api_key, uuid_value)
        last = found
        status = str(found.get('status'))
        generated = found.get('generated_image') or []
        result = None
        if isinstance(generated, list) and generated:
            first = generated[0] or {}
            result = first.get('image_url') or first.get('file_download_url') or first.get('url')
        if status == '2':
            if result:
                out = download_file(result, args.output_format)
                print(json.dumps({'saved': str(out), 'history': found}, ensure_ascii=False))
                return
            continue
        if status == '3':
            print(json.dumps(found, ensure_ascii=False))
            return
    print(json.dumps(last, ensure_ascii=False))


if __name__ == '__main__':
    main()
