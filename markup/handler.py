import os
import pandas as pd
import statistics
from time import time
from dataclasses import dataclass 
import PyQt5.QtWidgets as qtwidgets


@dataclass 
class Sentence:
    original: str 
    rewritten: str = '' 
    time: int = 0
    unable_to_paraphrase: bool = False
    is_already_formal: bool = False
    has_artefacts: bool = False


class Handler:
    def __init__(self, result, index, path):
        self.result = result
        self.file = path
        self.index = index
        self.timecheck = False
        self.timesave = time()

    def open(self):
        filename = qtwidgets.QFileDialog.getOpenFileName()
        filepath = filename[0]
        if filepath:
            if not filepath.endswith('txt'):
                return 'not txt'
            try:
                with open(filepath, 'r', encoding='utf8') as file:
                    self.result = [Sentence(line.rstrip()) for line in file.readlines()]
                    self.index = 0
                    self.file = filepath
                    return self.result[0].original
            except UnicodeDecodeError:
                return 

    def save(self):
        df = pd.DataFrame(
            [
                {
                    'original': sent.original,
                    'rewritten': sent.rewritten,
                    'time': sent.time,
                    'unable_to_paraphrase': sent.unable_to_paraphrase,
                    'is_already_formal': sent.is_already_formal,
                    'has_artefacts': sent.has_artefacts
                } for sent in self.result
            ]
        )
        df.to_csv(f'{os.path.splitext(self.file)[0]}.csv', index=False)

    def roll(self, res, unable_to_paraphrase, is_already_formal, has_artefacts, roll_next=True):
        if self.timecheck:
            self.result[self.index].time += time() - self.timesave
            self.timesave = time()

        if roll_next:
            cond = self.index >= len(self.result) - 1
        else:
            cond = self.index == 0
        if cond:
            return

        self.result[self.index].rewritten = res
        self.result[self.index].unable_to_paraphrase = unable_to_paraphrase
        self.result[self.index].is_already_formal = is_already_formal
        self.result[self.index].has_artefacts = has_artefacts

        if roll_next:
            self.index += 1
        else:
            self.index -= 1
        return self.result[self.index]

    def statscount(self):
        timescale = [sent.time for sent in self.result if sent.rewritten]
        if len(timescale) > 2:
            return [round(statistics.mean(timescale), 2), round(statistics.median(timescale), 2), round(statistics.stdev(timescale), 2), len(timescale)]
        return