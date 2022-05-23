from lsst.pipe.tasks.diff_matched_tract_catalog import (
    Median, Statistic, SigmaMAD,
    MatchType, MeasurementType, SourceType,
)

from collections import Counter
from dataclasses import dataclass
from typing import Callable, Tuple


def get_action_default(columns: Tuple[str]):
    if len(columns) != 1:
        raise ValueError('Default action must have exactly one column')
    return tuple((f"      action.column: '{columns[0]}'",))


@dataclass(frozen=True)
class MetricType:
    prefix: str
    tag: str
    unit: str


@dataclass(frozen=True)
class Metric:
    doc: str
    measure: str
    metric_type: MetricType
    action: Callable = get_action_default
    columns: Tuple = None
    supports_diff: bool = True
    supports_chi: bool = True


def get_action_true_positive(columns: Tuple[str]):
    return (
        f"      action: DivideColumns",
        f"      action.colA: SumColumns",
        f"      action.colA.colA.column: '{columns[0]}'",
        f"      action.colA.colB.column: '{columns[1]}'",
        f"      action.colB.column: '{columns[2]}'",
        f"      python: |",
        f"        from lsst.pipe.tasks.dataFrameActions import SumColumns, DivideColumns",
    )


def get_action_true_positive_all(columns: Tuple[str]):
    return (
        f"      action: DivideColumns",
        f"      action.colA: SumColumns",
        f"      action.colA.colA: SumColumns",
        f"      action.colA.colA.colA.column: '{columns[0]}'",
        f"      action.colA.colA.colB.column: '{columns[1]}'",
        f"      action.colA.colB: SumColumns",
        f"      action.colA.colB.colA.column: '{columns[2]}'",
        f"      action.colA.colB.colB.column: '{columns[3]}'",
        f"      action.colB: SumColumns",
        f"      action.colB.colA.column: '{columns[4]}'",
        f"      action.colB.colB.column: '{columns[5]}'",
        f"      python: |",
        f"        from lsst.pipe.tasks.dataFrameActions import SumColumns, DivideColumns",
    )


def get_pipeline_yaml(name_metric: str, columns: Tuple, row: int, unit: str, action: Callable):
    lines = [
        f"  {name_metric}:",
        f"    class: lsst.faro.measurement.TractTableValueMeasurementTask",
        f"    config:",
        f"      connections.metric: '{name_metric}'",
        f"      connections.package: 'validate_drp'",
        f"      connections.name_table: 'diff_matched_truth_summary_objectTable_tract'",
        f"      row: {row}",
        f"      unit: '{unit}'",
    ]
    lines.extend(action(columns))
    return lines


def get_yaml(metric: Metric, row: int, mag: str, stat: Statistic, doc: str, url: str,
             type_obj: str, type_obj_short: str, type_source: str):
    columns_single = metric.columns is None
    prefix_column = f'{metric.measure}'
    suffix_column = '' if stat is None else f'_{stat.name_short()}'
    suffix_metric = f'{type_obj_short}_mag{mag}'
    measurementTypes_metric = []
    if metric.supports_diff:
        measurementTypes_metric.append(MeasurementType.DIFF)
    if metric.supports_chi:
        measurementTypes_metric.append(MeasurementType.CHI)
    # Cheesy way to specify a column/metric that isn't a difference, e.g. number counts
    if not measurementTypes_metric:
        measurementTypes_metric.append(None)
    metric_yaml, pipeline_yaml, columns_all = [], [], []
    for measurementType in measurementTypes_metric:
        type_diff = '' if measurementType is None else f'_{measurementType.value.name}'
        # It seems to make more sense for table column names to have the source type first.
        # Users probably want multiple columns for a given category of sources.
        columns = ([f'{type_source}_{prefix_column}{type_diff}{suffix_column}'] if columns_single
                   else metric.columns)
        # However, for metrics, users seem more likely to care about the type of metric.
        # (Consider that metric names are prefixed by the statistic category e.g. astrom/photom)
        name_metric = (f'{metric.metric_type.prefix}_{prefix_column}_{type_source}{type_diff}'
                       f'{suffix_column}_{suffix_metric}')
        doc_metric = metric.doc
        if measurementType is not None:
            doc_metric = doc_metric.format(doc=measurementType.value.doc)

        desc = f'{f"{stat.doc()} " if stat is not None else ""}{doc_metric}'
        metric_yaml.extend((
            f'{name_metric}:',
            f'  description: >',
            f'    {desc} for {mag}-{mag + 1} {type_obj} mag',
            f"  unit: '{metric.metric_type.unit}'",
            f'  reference:',
            f'    doc: {doc}',
            f'    url: {url}',
            f'  tags: {metric.metric_type.tag}',
            f'',
        ))
        columns = tuple(column.format(type_obj_short=type_obj_short) for column in columns)
        pipeline_yaml.extend(get_pipeline_yaml(
            name_metric=name_metric,
            columns=columns,
            unit=metric.metric_type.unit,
            row=row,
            action=metric.action,
        ))
        columns_all.extend(columns)
    return metric_yaml, pipeline_yaml, columns_all


def generate_yamls(mags=set(range(15, 28))):
    ticket = 'DM-33892'
    str_doc = ticket
    str_url = f'https://jira.lsstcorp.org/browse/{ticket}'

    types_metric = {
        'flux_cModelFlux': MetricType(prefix='photom', tag='photometry', unit='nJy'),
        'mag_cModelFlux': MetricType(prefix='photom', tag='photometry', unit='mag'),
        'color_cModelFlux': MetricType(prefix='photom', tag='photometry', unit='mag'),
        'x': MetricType(prefix='astrom', tag='astrometry', unit='pix'),
    }
    types_metric['color_cModelFlux'] = types_metric['mag_cModelFlux']
    types_metric['y'] = types_metric['x']
    types_metric['distance'] = types_metric['x']

    prefix_description = 'of the {doc} between measured and reference matched source'
    suffixes_description = {
        'x': ' position',
        'y': ' position',
        'distance': '',
    }

    measures = {
        'x': (True, True),
        'y': (True, True),
        'distance': (True, True),
        'flux_cModelFlux': (True, False),
        'mag_cModelFlux': (False, True),
        'color_cModelFlux': (True, True),
    }

    metrics = tuple(
        Metric(
            doc=f'{prefix_description}{suffixes_description.get(measure, "")}',
            measure=measure,
            metric_type=types_metric[measure],
            supports_chi=supports_chi,
            supports_diff=supports_diff,
        )
        for measure, (supports_chi, supports_diff) in measures.items()
    )

    str_objtype = '{type_obj_short}'

    metrictype_count = MetricType(prefix='detect', tag='photometry', unit='')

    metrics_counts = {
        sourcetype: (
            Metric(
                doc='True positive fraction', measure='truepositive',
                metric_type=metrictype_count, supports_chi=False, supports_diff=False,
                columns=(
                    f"{SourceType.RESOLVED.value.label}_n_{str_objtype}"
                    f"_{MatchType.MATCH_RIGHT.value}",
                    f"{SourceType.UNRESOLVED.value.label}_n_{str_objtype}"
                    f"_{MatchType.MATCH_RIGHT.value}",
                    f"{SourceType.RESOLVED.value.label}_n_{str_objtype}"
                    f"_{MatchType.MATCH_WRONG.value}",
                    f"{SourceType.UNRESOLVED.value.label}_n_{str_objtype}"
                    f"_{MatchType.MATCH_WRONG.value}",
                    f"{SourceType.RESOLVED.value.label}_n_{str_objtype}_{MatchType.ALL.value}",
                    f"{SourceType.UNRESOLVED.value.label}_n_{str_objtype}_{MatchType.ALL.value}",
                ) if sourcetype == SourceType.ALL else (
                    f"{sourcetype.value.label}_n_{str_objtype}_{MatchType.MATCH_RIGHT.value}",
                    f"{sourcetype.value.label}_n_{str_objtype}_{MatchType.MATCH_WRONG.value}",
                    f"{sourcetype.value.label}_n_{str_objtype}_{MatchType.ALL.value}",
                ),
                action=(get_action_true_positive_all
                        if (sourcetype == SourceType.ALL)
                        else get_action_true_positive),
            ),
        )
        for sourcetype in SourceType
    }

    newline = '\n'
    metric_str = ''
    pipeline_str = ''

    # TODO: Enable measured
    objtypes = {
        'ref': 'reference',
        'target': 'target',
    }

    stats = (Median(), SigmaMAD())

    columns = []

    for objtype_short, objtype in objtypes.items():
        for sourcetype in SourceType:
            label = sourcetype.value.label
            for row, mag in enumerate(mags):
                for metric in metrics_counts[sourcetype]:
                    metric_yaml, pipeline_yaml, columnlist = get_yaml(
                        metric=metric, row=row, mag=mag, stat=None,
                        doc=str_doc, url=str_url,
                        type_obj=objtype, type_obj_short=objtype_short,
                        type_source=label,
                    )
                    metric_str = f'{metric_str}{newline.join(metric_yaml)}\n'
                    pipeline_str = f'{pipeline_str}{newline.join(pipeline_yaml)}\n'
                    columns.extend(columnlist)

                if objtype_short == 'ref':
                    for metric in metrics:
                        for stat in stats:
                            metric_yaml, pipeline_yaml, columnlist = get_yaml(
                                metric=metric, row=row, mag=mag, stat=stat,
                                doc=str_doc, url=str_url,
                                type_obj=objtype, type_obj_short=objtype_short,
                                type_source=label,
                            )
                            metric_str = f'{metric_str}{newline.join(metric_yaml)}\n'
                            pipeline_str = f'{pipeline_str}{newline.join(pipeline_yaml)}\n'
                            columns.extend(columnlist)

    return metric_str, pipeline_str, columns


def main():
    metric_str, pipeline_str, columns = generate_yamls()
    print(Counter(columns))
    for filename, text in (('metrics.yaml', metric_str), ('pipeline.yaml', pipeline_str)):
        with open(filename, 'w') as file:
            file.writelines(text)


if __name__ == "__main__":
    main()
