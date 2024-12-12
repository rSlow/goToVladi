import logging
import os.path

from sass import CompileError
from sassutils.wsgi import SassMiddleware as BaseSassMiddleware

__all__ = 'SassMiddleware',

logger = logging.getLogger(__name__ + '.SassMiddleware')


class SassMiddleware(BaseSassMiddleware):
    def __init__(
            self, *args,
            source_map: bool = True, output_style: str = "nested",
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.source_map = source_map
        self.output_style = output_style

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", '/')
        if path.endswith(".css"):
            for prefix, package_dir, manifest in self.paths:
                if not path.startswith(prefix):
                    continue
                css_filename = path[len(prefix):]
                sass_filename = manifest.unresolve_filename(package_dir, css_filename)
                try:
                    result = manifest.build_one(
                        package_dir,
                        sass_filename,
                        source_map=self.source_map,
                        output_style=self.output_style
                    )
                except OSError:
                    break
                except CompileError as e:
                    logger.error(str(e))
                    start_response(
                        self.error_status,
                        [('Content-Type', 'text/css; charset=utf-8')],
                    )
                    return [
                        b'/*\n', str(e).encode('utf-8'), b'\n*/\n\n',
                        b'body:before { content: ',
                        self.quote_css_string(str(e)).encode('utf-8'),
                        b'; color: maroon; background-color: white',
                        b'; white-space: pre-wrap; display: block',
                        b'; font-family: "Courier New", monospace'
                        b'; user-select: text; }',
                    ]

                def read_file(_path):
                    with open(_path, 'rb') as in_:
                        while 1:
                            chunk = in_.read(4096)
                            if chunk:
                                yield chunk
                            else:
                                break

                start_response('200 OK', [('Content-Type', 'text/css')])
                return read_file(os.path.join(package_dir, result))
        return self.app(environ, start_response)
