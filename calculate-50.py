#!/usr/bin/env python3

import json
import re
import sys

import type_ratio

CLASS_SPEECH = {
    "Letters, private": "S",
    "Diary, private": "S",
    "Trial proceedings": "S",
    "Witness depositions": "S",
    "Drama comedy": "S",
    "Sermon": "S",
    "Bible": "W",
    "Educational treatise": "W",
    "(Auto)biography": "W",
    "Travelogue": "W",
    "History": "W",
    "Law": "W",
    "Law reports": "W",
    "Medicine": "W",
    "Philosophy": "W",
    "Letters, non-private": "W",
    "Science, other": "W",
}

metadata = type_ratio.Metadata()
metadata.datasets = ["ity", "ness"]
metadata.dataset_labels = [f"-{x}" for x in metadata.datasets]
metadata.title = "PPCEME (1500–1710) and CED (1560–1760)"
metadata.xlabel = r"-$\it{" + metadata.datasets[
    0] + r"}$ and -$\it{" + metadata.datasets[1] + r"}$ types"
metadata.ylabel = r"Proportion of -$\it{" + metadata.datasets[0] + r"}$ types"
metadata.timeseries_xlabel = "Time period"
metadata.coll_labels = {
    "S": "Speech-related",
    "W": "Writing-based and writing-purposed",
}
metadata.coll_colors = {
    "S": "#f26924",
    "W": "#0088cc",
}
metadata.periods = [(p, p + 50) for p in range(1550, 1676, 25)]
metadata.periods_highlight = []
metadata.tick_hook = lambda x: x[0] % 50 == 0
metadata.shading_fraction = [0.1, 0.025]  # 80%, 95%
metadata.yrange = [35, 53]
metadata.trend_step = [100]
metadata.pdf = True
metadata.png = None
# metadata.png=400


def get_years(x):
    m = re.fullmatch(r"c?(1[5-7][0-9][0-9])", x)
    if m:
        return int(m.group(1)), None
    m = re.fullmatch(r"c?(1[5-7])([0-9][0-9])-c?([0-9][0-9])", x)
    if m:
        return int(m.group(1) + m.group(2)), int(m.group(1) + m.group(3))
    m = re.fullmatch(r"c?(1[5-7][0-9][0-9])-c?(1[5-7][0-9][0-9])", x)
    if m:
        return int(m.group(1)), int(m.group(2))
    assert False, x


def parse_year(x):
    if x == "a1671":
        # PENN / tillots
        x = "1661-1670"
    a, b = get_years(x)
    if b is None:
        assert 1500 <= a < 1800, x
        return float(a)
    else:
        assert 1500 <= a < b < 1800, x
        return (a + b) / 2


def get_periods(year):
    return [(a, b) for (a, b) in metadata.periods if a <= year < b]


class Sample(type_ratio.Sample):
    def __init__(self, d):
        self.corpus = d["corpus"]
        self.sample = d["sample"]
        self.genre = d["genre"]
        self.year = parse_year(d["year"])
        label = f"{self.corpus} {self.sample}"
        periods = get_periods(self.year)
        colls = [CLASS_SPEECH[self.genre]]
        super().__init__(label, periods, colls)

    def relevant(self):
        if self.corpus not in ["CED", "PENN"]:
            return False
        return True


class Data:
    def __init__(self, driver):
        self.driver = driver
        self.relevant = []
        self.samplemap = {}

    def read(self):
        dataset_index = {ds: i for i, ds in enumerate(metadata.datasets)}
        filename = "suffix-competition/data.json"
        print(filename)
        with open(filename) as f:
            input_data = json.load(f)
        for d in input_data["samples"]:
            s = Sample(d)
            assert s.label not in self.samplemap
            self.samplemap[s.label] = s
            if s.relevant():
                self.relevant.append(s)
        self.relevant.sort(key=lambda s: s.label)
        for token in input_data["tokens"]:
            corpus, sample, dataset, token, before, word, after = token
            label = f"{corpus} {sample}"
            s = self.samplemap[label]
            s.feed(dataset_index[dataset], token)

    def build(self):
        colls = type_ratio.list_colls(self.relevant)
        ts = type_ratio.TimeSeries(metadata, colls, self.relevant)
        self.driver.add_timeseries(ts)


def main():
    if len(sys.argv) <= 1:
        iter = 1_000_000
    else:
        iter = int(sys.argv[1])
    driver = type_ratio.Driver("50")
    data = Data(driver)
    data.read()
    data.build()
    driver.calc(iter)


main()
