# Taken from
# https://github.com/django/django/blob/master/django/core/management/commands/makemessages.py

from __future__ import unicode_literals

import fnmatch
import glob
import io
import os
import re
import sys
from functools import total_ordering
from itertools import dropwhile
from tempfile import NamedTemporaryFile

from python_bot import settings
from python_bot.common.localization.base import has_bom
from python_bot.common.utils.path import find_command, is_writable
from python_bot.common.utils.subprocess import popen_wrapper

plural_forms_re = re.compile(r'^(?P<value>"Plural-Forms.+?\\n")\s*$', re.MULTILINE | re.DOTALL)
STATUS_OK = 0
NO_LOCALE_DIR = object()


def check_programs(*programs):
    for program in programs:
        if find_command(program) is None:
            raise ValueError(
                "Can't find %s. Make sure you have GNU gettext tools 0.15 or "
                "newer installed." % program
            )


@total_ordering
class TranslatableFile(object):
    def __init__(self, dirpath, file_name, locale_dir):
        self.file = file_name
        self.dirpath = dirpath
        self.locale_dir = locale_dir

    def __repr__(self):
        return "<TranslatableFile: %s>" % os.sep.join([self.dirpath, self.file])

    def __eq__(self, other):
        return self.path == other.path

    def __lt__(self, other):
        return self.path < other.path

    @property
    def path(self):
        return os.path.join(self.dirpath, self.file)


class BuildFile(object):
    """
    Represents the state of a translatable file during the build process.
    """

    def __init__(self, command, domain, translatable):
        self.command = command
        self.domain = domain
        self.translatable = translatable

    @property
    def path(self):
        return self.translatable.path

    @property
    def work_path(self):
        return self.path


def normalize_eols(raw_contents):
    """
    Take a block of raw text that will be passed through str.splitlines() to
    get universal newlines treatment.
    Return the resulting block of text with normalized `\n` EOL sequences ready
    to be written to disk using current platform's native EOLs.
    """
    lines_list = raw_contents.splitlines()
    # Ensure last line has its EOL
    if lines_list and lines_list[-1]:
        lines_list.append('')
    return '\n'.join(lines_list)


def write_pot_file(potfile, msgs):
    """
    Write the :param potfile: POT file with the :param msgs: contents,
    previously making sure its format is valid.
    """
    pot_lines = msgs.splitlines()
    if os.path.exists(potfile):
        # Strip the header
        lines = dropwhile(len, pot_lines)
    else:
        lines = []
        found, header_read = False, False
        for line in pot_lines:
            if not found and not header_read:
                found = True
                line = line.replace('charset=CHARSET', 'charset=UTF-8')
            if not line and not found:
                header_read = True
            lines.append(line)
    msgs = '\n'.join(lines)
    with io.open(potfile, 'a', encoding='utf-8') as fp:
        fp.write(msgs)


class LocaleMessages:
    options = {
        "use_default_ignore_patterns": True,
        "keep_pot": False,
        "no_obsolete": False,
        "no_location": False,
        "no_wrap": False,
        "ignore_patterns": [],
        "symlinks": False,
        "extensions": [],
        "exclude": [],
        "locale": [],
        "locale_paths": [],
        "all": False,
        "domain": "python_bot",
        'verbosity': 0
    }

    compile_program = 'msgfmt'
    compile_program_options = ['--check-format']

    def __init__(self, **options):
        self.options.update(options)
        self.domain = self.options["domain"]
        self.verbosity = self.options['verbosity']
        self.symlinks = self.options['symlinks']
        locale = self.options['locale']
        exclude = self.options['exclude']
        process_all = self.options['all']
        extensions = self.options['extensions']

        ignore_patterns = self.options['ignore_patterns']
        if self.options['use_default_ignore_patterns']:
            ignore_patterns += ['CVS', '.*', '*~', '*.pyc']
        self.ignore_patterns = list(set(ignore_patterns))

        # Avoid messing with mutable class variables
        if self.options['no_wrap']:
            self.msgmerge_options = self.msgmerge_options[:] + ['--no-wrap']
            self.msguniq_options = self.msguniq_options[:] + ['--no-wrap']
            self.msgattrib_options = self.msgattrib_options[:] + ['--no-wrap']
            self.xgettext_options = self.xgettext_options[:] + ['--no-wrap']
        if self.options['no_location']:
            self.msgmerge_options = self.msgmerge_options[:] + ['--no-location']
            self.msguniq_options = self.msguniq_options[:] + ['--no-location']
            self.msgattrib_options = self.msgattrib_options[:] + ['--no-location']
            self.xgettext_options = self.xgettext_options[:] + ['--no-location']

        self.no_obsolete = self.options['no_obsolete']
        self.keep_pot = self.options['keep_pot']

        self.extensions = extensions if extensions else ['.html', '.txt', '.py']

        if locale is None and not exclude and not process_all:
            raise ValueError(
                "Type '%s help %s' for usage information."
                % (os.path.basename(sys.argv[0]), sys.argv[1])
            )

        self.locale_paths = self.options['locale_paths']
        self.default_locale_path = None

        # self.locale_paths.extend([settings.LOCALE_DIR])
        # Allow to run makemessages inside an app dir
        if os.path.isdir('locale'):
            self.locale_paths.append(os.path.abspath('locale'))

        if self.locale_paths:
            self.locale_paths = list(set(self.locale_paths))
            self.default_locale_path = self.locale_paths[0]
            if not os.path.exists(self.default_locale_path):
                os.makedirs(self.default_locale_path)

        # Build locale list
        locale_dirs = filter(os.path.isdir, glob.glob('%s/*' % self.default_locale_path))
        all_locales = map(os.path.basename, locale_dirs)

        # Account for excluded locales
        if process_all:
            locales = all_locales
        else:
            locales = locale or all_locales
            locales = set(locales) - set(exclude)

        if locales:
            check_programs('msguniq', 'msgmerge', 'msgattrib', self.compile_program)

        check_programs('xgettext')
        self.locales = locales

    translatable_file_class = TranslatableFile
    build_file_class = BuildFile

    requires_system_checks = False
    leave_locale_alone = True

    msgmerge_options = ['-q', '--previous']
    msguniq_options = ['--to-code=utf-8']
    msgattrib_options = ['--no-obsolete']
    xgettext_options = ['--from-code=UTF-8', '--add-comments=Translators']

    def make_messages(self):
        try:
            potfiles = self.build_potfiles()

            # Build po files for each selected locale
            for locale in self.locales:
                for potfile in potfiles:
                    self.write_po_file(potfile, locale)
        finally:
            if not self.keep_pot:
                self.remove_potfiles()

    def compile_messages(self):
        if self.locales:
            dirs = [os.path.join(d, l, 'LC_MESSAGES') for l in self.locales for d in self.locale_paths]
        else:
            dirs = self.locale_paths

        locations = []
        for ldir in dirs:
            for dirpath, dirnames, filenames in os.walk(ldir):
                locations.extend((dirpath, f) for f in filenames if f.endswith('.po'))

        if not locations:
            return

        for i, (dirpath, f) in enumerate(locations):
            if self.verbosity > 0:
                print('processing file %s in %s\n' % (f, dirpath))
            po_path = os.path.join(dirpath, f)
            if has_bom(po_path):
                raise ValueError("The %s file has a BOM (Byte Order Mark). "
                                 "Django only supports .po files encoded in "
                                 "UTF-8 and without any BOM." % po_path)
            base_path = os.path.splitext(po_path)[0]

            # Check writability on first location
            if i == 0 and not is_writable(base_path + '.mo'):
                print("The po files under %s are in a seemingly not writable location. "
                      "mo files will not be updated/created." % dirpath)
                return

            args = [self.compile_program] + self.compile_program_options + [
                '-o', base_path + '.mo', base_path + '.po'
            ]
            output, errors, status = popen_wrapper(args)
            if status:
                if errors:
                    msg = "Execution of %s failed: %s" % (self.compile_program, errors)
                else:
                    msg = "Execution of %s failed" % self.compile_program
                raise ValueError(msg)

    @property
    def gettext_version(self):
        # Gettext tools will output system-encoded bytestrings instead of UTF-8,
        # when looking up the version. It's especially a problem on Windows.
        out, err, status = popen_wrapper(
            ['xgettext', '--version']
        )
        m = re.search(r'(\d+)\.(\d+)\.?(\d+)?', out)
        if m:
            return tuple(int(d) for d in m.groups() if d is not None)
        else:
            raise ValueError("Unable to get gettext version. Is it installed?")

    def build_potfiles(self):
        """
        Build pot files and apply msguniq to them.
        """
        file_list = self.find_files(".")
        self.remove_potfiles()
        self.process_files(file_list)
        potfiles = []
        for path in self.locale_paths:
            potfile = os.path.join(path, '%s.pot' % str(self.domain))
            if not os.path.exists(potfile):
                continue
            args = ['msguniq'] + self.msguniq_options + [potfile]
            msgs, errors, status = popen_wrapper(args)
            if errors:
                if status != STATUS_OK:
                    raise ValueError(
                        "errors happened while running msguniq\n%s" % errors)
                elif self.verbosity > 0:
                    print(errors)
            msgs = normalize_eols(msgs)
            with io.open(potfile, 'w', encoding='utf-8') as fp:
                fp.write(msgs)
            potfiles.append(potfile)
        return potfiles

    def remove_potfiles(self):
        for path in self.locale_paths:
            pot_path = os.path.join(path, '%s.pot' % str(self.domain))
            if os.path.exists(pot_path):
                os.unlink(pot_path)

    def find_files(self, root):
        """
        Helper method to get all files in the given root. Also check that there
        is a matching locale dir for each file.
        """

        def is_ignored(path, ignore_patterns):
            """
            Check if the given path should be ignored or not.
            """
            filename = os.path.basename(path)

            def ignore(pattern):
                return fnmatch.fnmatchcase(filename, pattern) or fnmatch.fnmatchcase(path, pattern)

            return any(ignore(pattern) for pattern in ignore_patterns)

        ignore_patterns = [os.path.normcase(p) for p in self.ignore_patterns]
        dir_suffixes = {'%s*' % path_sep for path_sep in {'/', os.sep}}
        norm_patterns = []
        for p in ignore_patterns:
            for dir_suffix in dir_suffixes:
                if p.endswith(dir_suffix):
                    norm_patterns.append(p[:-len(dir_suffix)])
                    break
            else:
                norm_patterns.append(p)

        all_files = []
        ignored_roots = []
        for dirpath, dirnames, filenames in os.walk(root, topdown=True, followlinks=self.symlinks):
            for dirname in dirnames[:]:
                if (is_ignored(os.path.normpath(os.path.join(dirpath, dirname)), norm_patterns) or
                            os.path.join(os.path.abspath(dirpath), dirname) in ignored_roots):
                    dirnames.remove(dirname)
                    if self.verbosity > 1:
                        print('ignoring directory %s\n' % dirname)
                elif dirname == 'locale':
                    dirnames.remove(dirname)
                    self.locale_paths.insert(0, os.path.join(os.path.abspath(dirpath), dirname))
            for filename in filenames:
                file_path = os.path.normpath(os.path.join(dirpath, filename))
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in self.extensions or is_ignored(file_path, self.ignore_patterns):
                    if self.verbosity > 1:
                        print('ignoring file %s in %s\n' % (filename, dirpath))
                else:
                    locale_dir = None
                    for path in self.locale_paths:
                        if os.path.abspath(dirpath).startswith(os.path.dirname(path)):
                            locale_dir = path
                            break
                    if not locale_dir:
                        locale_dir = self.default_locale_path
                    if not locale_dir:
                        locale_dir = NO_LOCALE_DIR
                    all_files.append(self.translatable_file_class(dirpath, filename, locale_dir))
        return sorted(all_files)

    def process_files(self, file_list):
        """
        Group translatable files by locale directory and run pot file build
        process for each group.
        """
        file_groups = {}
        for translatable in file_list:
            file_group = file_groups.setdefault(translatable.locale_dir, [])
            file_group.append(translatable)
        for locale_dir, files in file_groups.items():
            self.process_locale_dir(locale_dir, files)

    def process_locale_dir(self, locale_dir, files):
        """
        Extract translatable literals from the specified files, creating or
        updating the POT file for a given locale directory.
        Uses the xgettext GNU gettext utility.
        """
        build_files = []
        for translatable in files:
            if self.verbosity > 1:
                print('processing file %s in %s\n' % (
                    translatable.file, translatable.dirpath
                ))

            build_file = self.build_file_class(self, self.domain, translatable)
            build_files.append(build_file)

        args = [
            'xgettext',
            '-d', self.domain,
            '--language=Python',
            '--keyword=gettext_noop',
            '--keyword=gettext_lazy',
            '--keyword=localize_message',
            '--keyword=ngettext_lazy:1,2',
            '--keyword=ugettext_noop',
            '--keyword=ugettext_lazy',
            '--keyword=ungettext_lazy:1,2',
            '--keyword=pgettext:1c,2',
            '--keyword=npgettext:1c,2,3',
            '--keyword=pgettext_lazy:1c,2',
            '--keyword=npgettext_lazy:1c,2,3',
            '--output=-',
        ]

        input_files = [bf.work_path for bf in build_files]
        with NamedTemporaryFile(mode='w+') as input_files_list:
            input_files_list.write('\n'.join(input_files))
            input_files_list.flush()
            args.extend(['--files-from', input_files_list.name])
            args.extend(self.xgettext_options)
            msgs, errors, status = popen_wrapper(args)

        if errors:
            if status != STATUS_OK:
                raise ValueError(
                    'errors happened while running xgettext on %s\n%s' %
                    ('\n'.join(input_files), errors)
                )
            elif self.verbosity > 0:
                # Print warnings
                print(errors)

        if msgs:
            if locale_dir is NO_LOCALE_DIR:
                file_path = os.path.normpath(build_files[0].path)
                raise ValueError(
                    'Unable to find a locale path to store translations for '
                    'file %s' % file_path
                )
            potfile = os.path.join(locale_dir, '%s.pot' % str(self.domain))
            write_pot_file(potfile, msgs)

    def write_po_file(self, potfile, locale):
        """
        Creates or updates the PO file for self.domain and :param locale:.
        Uses contents of the existing :param potfile:.
        Uses msgmerge, and msgattrib GNU gettext utilities.
        """
        basedir = os.path.join(os.path.dirname(potfile), locale, 'LC_MESSAGES')
        if not os.path.isdir(basedir):
            os.makedirs(basedir)
        pofile = os.path.join(basedir, '%s.po' % str(self.domain))

        if os.path.exists(pofile):
            args = ['msgmerge'] + self.msgmerge_options + [pofile, potfile]
            msgs, errors, status = popen_wrapper(args)
            if errors:
                if status != STATUS_OK:
                    raise ValueError(
                        "errors happened while running msgmerge\n%s" % errors)
                elif self.verbosity > 0:
                    print(errors)
        else:
            with io.open(potfile, 'r', encoding='utf-8') as fp:
                msgs = fp.read()

        msgs = normalize_eols(msgs)
        msgs = msgs.replace(
            "#. #-#-#-#-#  %s.pot (PACKAGE VERSION)  #-#-#-#-#\n" % self.domain, "")
        with io.open(pofile, 'w', encoding='utf-8') as fp:
            fp.write(msgs)

        if self.no_obsolete:
            args = ['msgattrib'] + self.msgattrib_options + ['-o', pofile, pofile]
            msgs, errors, status = popen_wrapper(args)
            if errors:
                if status != STATUS_OK:
                    raise ValueError(
                        "errors happened while running msgattrib\n%s" % errors)
                elif self.verbosity > 0:
                    print(errors)
