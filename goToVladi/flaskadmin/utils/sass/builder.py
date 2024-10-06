import os.path

from sass import compile
from sassutils.builder import Manifest as BaseManifest


class Manifest(BaseManifest):
    def build_one(
            self, package_dir, filename,
            source_map=False, output_style="nested"
    ):
        """Builds one Sass/SCSS file.

        :param package_dir: the path of package directory
        :type package_dir: :class:`str`, :class:`basestring`
        :param filename: the filename of Sass/SCSS source to compile
        :type filename: :class:`str`, :class:`basestring`
        :param source_map: whether to use source maps.  if :const:`True`
                           it also write a source map to a ``filename``
                           followed by :file:`.map` suffix.
                           default is :const:`False`
        :type source_map: :class:`bool`
        :param output_style: an optional coding style of the compiled result.
                             choose one of: 'nested' (default), 'expanded',
                             'compact', 'compressed'.
        :type output_style: :class:`str`
        :returns: the filename of compiled CSS
        :rtype: :class:`str`, :class:`basestring`

        .. versionadded:: 0.4.0
           Added optional ``source_map`` parameter.

        """
        sass_filename, css_filename = self.resolve_filename(
            package_dir, filename,
        )
        root_path = os.path.join(package_dir, self.sass_path)
        css_path = os.path.join(package_dir, self.css_path, css_filename)
        if source_map:
            source_map_path = css_filename + '.map'
            css, source_map = compile(
                filename=sass_filename,
                include_paths=[root_path],
                source_map_filename=source_map_path,
                output_filename_hint=css_path,
                output_style=output_style,
            )
        else:
            css = compile(
                filename=sass_filename,
                include_paths=[root_path],
                output_style=output_style,
            )
            source_map_path = None
            source_map = None
        css_folder = os.path.dirname(css_path)
        if not os.path.exists(css_folder):
            os.makedirs(css_folder)
        with open(css_path, 'w', encoding='utf-8', newline='') as f:
            f.write(css)
        if source_map:
            # Source maps are JSON, and JSON has to be UTF-8 encoded
            with open(
                    source_map_path, 'w', encoding='utf-8', newline='',
            ) as f:
                f.write(source_map)
        return css_filename
