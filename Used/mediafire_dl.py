import os
import os.path as osp
import re
import shutil
import sys
import tempfile
import requests
import six
import tqdm

CHUNK_SIZE = 1569


def extract_download_link(contents: str) -> str:
    """Takes a media fire shared link and then extracts the actual download link from it"""
    for line in contents.splitlines():
        m = re.search(r'href="((http|https)://download[^"]+)', line)
        if m:
            return m.groups()[0]


def download(url: str, output: str, quiet: bool) -> None:
    """Takes the file from a given url."""
    url_origin = url
    sess = requests.session()

    while True:
        res = sess.get(url, stream=True)
        if 'Content-Disposition' in res.headers:
            # This is the file
            break

        # Need to redirect with confirmation
        url = extract_download_link(res.text)

        if url is None:
            print(' Permission denied: %s' % url_origin, file=sys.stderr)
            print(
                " Maybe you need to change the permissions to allow "
                " Anyone with the link to download?",
                file=sys.stderr,
            )

    if output is None:
        m = re.search(
            'filename="(.*)"', res.headers['Content-Disposition']
        )
        output = m.groups()[0]
        # output = osp.basename(url)

    output_is_path = isinstance(output, six.string_types)

    if not quiet:
        print('Downloading...', file=sys.stderr)
        print('From:', url_origin, file=sys.stderr)
        print(
            'To:',
            osp.abspath(output) if output_is_path else output,
            file=sys.stderr,
        )

    if output_is_path:
        tmp_file = tempfile.mktemp(
            suffix=tempfile.template,
            prefix=osp.basename(output),
            dir=osp.dirname(output),
        )
        f = open(tmp_file, 'wb')
    else:
        tmp_file = None
        f = output

    try:
        total = res.headers.get('Content-Length')
        if total is not None:
            total = int(total)
        if not quiet:
            pbar = tqdm.tqdm(total=total, unit='B', unit_scale=True)
        for chunk in res.iter_content(chunk_size=CHUNK_SIZE):
            f.write(chunk)
            if not quiet:
                pbar.update(len(chunk))
        if not quiet:
            pbar.close()
        if tmp_file:
            f.close()
            shutil.move(tmp_file, output)
    except IOError as e:
        print(e, file=sys.stderr)
        return
    finally:
        try:
            if tmp_file:
                os.remove(tmp_file)
        except OSError:
            pass
    return output


if __name__ == "__main__":
    for url in sys.argv[1:]:
        download(url, output=None, quiet=False)

# Add try except, refactor and rename code
