import os

base_directory = os.path.dirname(os.path.realpath(__file__))
snapshots_directory = os.path.join(base_directory, 'snapshots')


def get_snapshot_result_path(parser, canteen):
    return os.path.join(snapshots_directory, parser, canteen, 'snapshot-result.xml')
