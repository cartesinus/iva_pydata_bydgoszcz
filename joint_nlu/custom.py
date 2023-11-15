# coding=utf-8

"""Leyzer"""

import json
import datasets
import pandas as pd
from sklearn.model_selection import train_test_split


_DESCRIPTION = """\
        Leyzer is a multilingual text corpus designed to study multilingual and cross-lingual natural language
        understanding (NLU) models and the strategies of localization of virtual assistants. It consists of 20
        domains across three languages: English, Spanish and Polish, with 186 intents and a wide range of
        samples, ranging from 1 to 672 sentences per intent.
"""

_LICENSE = """\

"""

_URL = "iva_calendar-corpora-en_US-0.1.0-20231112.tsv"

_LANGUAGES = ['en-US']

_DOMAINS = ['Calendar']

_INTENTS = [
                "AddEventOnDateWithName",
                "AddEventWithName",
                "CheckCalendarEventName",
                "CheckCalendarOnDate",
                "NotifyOnEventInLocation",
                "NotifyOnEventStart",
                "NotifyWhenEventNameStart",
                "NotNotifyOnEventInLocation",
                "NotNotifyOnEventStart",
                "OpenCalendar"
            ]

_LEVELS = ['L0TC', 'L1TC', 'L2TC', 'REPHRASE']

_VPS = ['verb_pattern_01', 'verb_pattern_02', 'verb_pattern_03', 'verb_pattern_04',
        'verb_pattern_05', 'verb_pattern_06']


class LeyzerConfig(datasets.BuilderConfig):
    """BuilderConfig for Leyzer."""

    def __init__(self, dataset_version=None, *args, **kwargs):
        """BuilderConfig for Leyzer.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(LeyzerConfig, self).__init__(*args, **kwargs)
        self.dataset_version = dataset_version if dataset_version else "1.0"
        self.data_url = _URL


class Leyzer(datasets.GeneratorBasedBuilder):
    """Leyzer"""

    # All individual locale datasets are served from the latest version.
    BUILDER_CONFIGS = [
        LeyzerConfig(
            name = name,
            dataset_version = '0.2.0',
            version = datasets.Version("0.2.0"),
            description = f"The Leyzer v0.2.0 corpora for {name}",
        ) for name in _LANGUAGES
        ]
    # Version 1.0
    BUILDER_CONFIGS.append(LeyzerConfig(
            name = "all",
            dataset_version = '0.2.0',
            version = datasets.Version("0.2.0"),
            description = f"The Leyzer v0.2.0 corpora for entire corpus",
        )
    )

    DEFAULT_CONFIG_NAME = "all"

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "domain": datasets.features.ClassLabel(names=_DOMAINS),
                    "intent": datasets.features.ClassLabel(names=_INTENTS),
                    "levels": datasets.features.ClassLabel(names=_LEVELS),
                    "vps": datasets.features.ClassLabel(names=_VPS),
                    "utterance": datasets.Value("string"),
                    "bio": datasets.Value("string"),
                },
            ),
            supervised_keys=None,
            homepage="https://github.com/cartesinus/leyzer/",
            license=_LICENSE,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        file_path = self.config.data_url

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": file_path, "split": "train"}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": file_path, "split": "validation"}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": file_path, "split": "test"}
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples as (key, example) tuples for the specified split."""
        # Open and read the file
        with open(filepath, encoding="utf-8") as f:
            lines = f.read().split("\n")
            df = pd.DataFrame([line.split('\t') for line in lines if line],
                              columns=['domain', 'intent', 'levels', 'vps', 'utterance', 'bio'])

        # Split the data into train, validate, and test
        train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
        validate_df, test_df = train_test_split(test_df, test_size=0.5, random_state=42)

        # Select the appropriate dataframe based on the split
        if split == "train":
            data_df = train_df
        elif split == "validation":
            data_df = validate_df
        elif split == "test":
            data_df = test_df
        else:
            raise ValueError(f"Unknown split: {split}")

        # Yield examples from the selected dataframe
        for i, row in data_df.iterrows():
            yield i, row.to_dict()
