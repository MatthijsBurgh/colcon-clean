# Copyright 2021 Ruffin White
# Licensed under the Apache License, Version 2.0

from pathlib import Path

from colcon_clean.base_handler import BaseHandlerExtensionPoint
from colcon_core.package_descriptor import PackageDescriptor
from colcon_core.plugin_system import satisfies_version

BASE_PATH = 'build'


class BuildBaseHandler(BaseHandlerExtensionPoint):
    """Determine how build paths for the workspace should be cleaned."""

    def __init__(self):  # noqa: D107
        super().__init__(BASE_PATH)
        satisfies_version(
            BaseHandlerExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')

    def add_arguments(self, *, parser):  # noqa: D102
        parser.add_argument(
            '--build-base',
            default=self.base_path,
            help='The base path for all build directories '
                 f'(default: {self.base_path})')

    def get_workspace_paths(self, *, args):  # noqa: D102
        return [args.build_base]

    def get_package_paths(self, *, args, pkg: PackageDescriptor):  # noqa: D102
        return [Path(args.build_base) / pkg.name]
