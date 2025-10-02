# Copyright 2021 Ruffin White
# Licensed under the Apache License, Version 2.0

from pathlib import Path
from typing import List

from colcon_clean.base_handler import BaseHandlerExtensionPoint
from colcon_core.logging import colcon_logger
from colcon_core.package_descriptor import PackageDescriptor
from colcon_core.plugin_system import satisfies_version

logger = colcon_logger.getChild(__name__)

BASE_PATH = 'install'


class InstallBaseHandler(BaseHandlerExtensionPoint):
    """Determine how install paths for the workspace should be cleaned."""

    def __init__(self):  # noqa: D107
        super().__init__(BASE_PATH)
        satisfies_version(
            BaseHandlerExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')

    def add_arguments(self, *, parser):  # noqa: D102
        parser.add_argument(
            '--install-base',
            default=self.base_path,
            help='The base path for all install directories '
                 f'(default: {self.base_path})')

    def get_workspace_paths(self, *, args) -> List[Path]:  # noqa: D102
        return [Path(args.install_base)]

    def get_package_paths(  # noqa: D102
        self, *, args, pkg: PackageDescriptor
    ) -> List[Path]:
        paths: List[Path] = [
            Path(args.install_base) / pkg.name,
            Path(args.install_base) / 'share' / pkg.name,
        ]
        if hasattr(args, 'build_base'):
            manifest_path = (
                Path(args.build_base) / pkg.name / 'install_manifest.txt'
            )
            if not manifest_path.is_file():
                logger.debug(
                    f'No {manifest_path.name} found for {pkg.name} at '
                    f"'{manifest_path}'"
                )
                return paths
            with manifest_path.open() as f:
                for line in f:
                    paths.append(Path(line.strip()))
        else:
            logger.warning(
                "'build_base' argument not found, "
                "skipping 'install_manifest.txt' parsing"
            )
        return paths
